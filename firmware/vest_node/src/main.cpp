// PANDU Vest Node: firmware dasar (ESP32-DevKitC V4, Arduino core)
// Pin mengikuti HANDOVER.md. Nilai ber-tanda "KALIBRASI" perlu di-tune di perangkat nyata.
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <TinyGPSPlus.h>
#include "driver/rtc_io.h"
#include <NimBLEDevice.h>
#include <time.h>
#if __has_include("config.h")
#include "config.h"
#endif
#include "pandu_mac.h"   // ../common: HMAC paket + sync word (audit K2)
#ifdef DEMO_NO_BROWNOUT
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#endif

// ---- Pin ----
constexpr int PIN_PWR_BTN  = 13;  // tact (ke GND), RTC: toggle deep sleep
constexpr int PIN_SOS      = 27;  // tact ke 3V3, pull-down R2 10k di PCB (aktif HIGH), tahan SOS_HOLD_MS
constexpr int PIN_BAT      = 35;  // BAT_SENSE: pembagi 100k/100k dari VBAT_RAW (ADC1_CH7, input-only)
constexpr int PIN_WATER    = 34;  // output XKC-Y25 (input-only, tanpa pull internal)
constexpr int PIN_GPS_EN   = 4;   // gate P-MOSFET Q1: LOW=ON, hi-Z=OFF (JANGAN drive HIGH)
constexpr int PIN_XKC_EN   = 32;  // via Q5: HIGH=ON, LOW/hi-Z=OFF
constexpr int PIN_GPS_RX   = 16;  // ESP RX <- GPS TX (asumsi, cek skematik)
constexpr int PIN_GPS_TX   = 17;
constexpr int PIN_SDA = 21, PIN_SCL = 22;
constexpr int PIN_LORA_CS = 5, PIN_LORA_RST = 25, PIN_LORA_DIO0 = 26;

// ---- Identitas paket (DATA_CONTRACT v2) ----
#ifndef VEST_ID
#define VEST_ID 1                         // 1-8, set per perangkat: build_flags = -DVEST_ID=2
#endif
RTC_DATA_ATTR uint16_t seqCounter = 0;    // nomor urut kejadian; bertahan lewat deep sleep, acak saat cold boot (lihat setup)
uint16_t nextSeq() { return seqCounter++; }

// ---- Parameter (KALIBRASI) ----
constexpr long LORA_FREQ       = 433E6;   // Ra-02 SX1278 (410-525 MHz): TIDAK bisa 915/920. Harus sama dengan Gateway
constexpr float FREEFALL_G     = 0.6f;    // |a| di bawah ini = jatuh bebas (tes nyata: terbaca 0,3-0,5 g karena offset sensor)
constexpr uint32_t FREEFALL_MS = 120;
constexpr float IMPACT_G       = 2.5f;    // benturan setelah jatuh bebas
constexpr uint32_t IMPACT_WIN  = 1000;    // jendela benturan setelah free-fall
constexpr uint32_t MOB_WINDOW_MS = 60000;   // MOB = jatuh DAN basah dalam jendela ini setelah jatuh
constexpr uint32_t WATER_MS    = 3000;    // sensor air harus aktif sebanyak ini = MOB
constexpr int WATER_WET_MV     = 1000;    // KALIBRASI: sensor murah analog, kering 140-230 mV, basah 1700-2070 mV
constexpr uint32_t SOS_HOLD_MS = 2000;
constexpr uint32_t HEARTBEAT_MS = 30000;   // + jitter acak +-HEARTBEAT_JITTER_MS agar beberapa Vest tidak bertabrakan
constexpr uint32_t HEARTBEAT_JITTER_MS = 5000;
constexpr uint32_t ALERT_REPEAT_MS = 5000;
constexpr float BAT_DIV = 2.0f;     // KALIBRASI: faktor pembagi (cek dengan multimeter)
constexpr uint8_t MPU = 0x68;

TinyGPSPlus gps;
HardwareSerial gpsSerial(2);
bool loraOk = false, mpuOk = false;

// ---- Posisi terakhir di memori RTC (audit K3): bertahan lewat deep sleep, jadi SOS dari bangun tidur tetap membawa posisi ----
// Umur posisi dihitung dari jam sistem (time(nullptr)); jam ini ditopang RTC dan DIHARAPKAN jalan terus selama deep sleep. [DUGAAN: belum diuji di perangkat]
constexpr uint32_t POS_AGE_UNKNOWN_S = 86400;   // jam tampak mundur (reset di luar deep sleep): posisi tetap dikirim, ditandai sangat tua
RTC_DATA_ATTR bool    rtcHasFix  = false;
RTC_DATA_ATTR double  rtcLat = 0, rtcLon = 0;
RTC_DATA_ATTR int64_t rtcFixAtS  = 0;
void updateFix() {
  if (gps.location.isValid() && gps.location.age() < 3000) { rtcLat = gps.location.lat(); rtcLon = gps.location.lng(); rtcFixAtS = time(nullptr); rtcHasFix = true; }
}
uint32_t posAgeS() {
  int64_t now = time(nullptr);
  return now >= rtcFixAtS ? (uint32_t)(now - rtcFixAtS) : POS_AGE_UNKNOWN_S;
}

void helmScanStop();  // didefinisikan di bagian Helm
void sendPkt(const char *type, uint16_t seq);   // didefinisikan di bagian LoRa

// ---- Power gating ----
void gpsPower(bool on) {
  if (on) { pinMode(PIN_GPS_EN, OUTPUT); digitalWrite(PIN_GPS_EN, LOW); }
  else    { pinMode(PIN_GPS_EN, INPUT); }  // hi-Z: pull-up R3 100k ke 3V3_SYS mematikan Q1
}
void xkcPower(bool on) { pinMode(PIN_XKC_EN, OUTPUT); digitalWrite(PIN_XKC_EN, on); }

// ---- Deep sleep ----
void goToSleep() {
  Serial.println("Sleep...");
  sendPkt("OFF", nextSeq());   // dimatikan sengaja: Gateway/dashboard menandai Nonaktif, bukan "tidak terjangkau"
  gpsPower(false); xkcPower(false);
  NimBLEDevice::getScan()->stop();   // tanpa deinit: deinit(true) crash (PC=0) di NimBLE 1.4.3, deep sleep me-reset radio sendiri
  if (loraOk) LoRa.sleep();
  while (digitalRead(PIN_PWR_BTN) == LOW || digitalRead(PIN_SOS) == HIGH) delay(10);   // tunggu lepas agar tidak langsung bangun
  delay(50);
  rtc_gpio_pullup_en((gpio_num_t)PIN_PWR_BTN);
  rtc_gpio_pulldown_dis((gpio_num_t)PIN_PWR_BTN);
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_PWR_BTN, 0);          // tombol power: aktif-LOW
  rtc_gpio_pulldown_en((gpio_num_t)PIN_SOS);                         // SOS: aktif-HIGH (R2 10k juga menahan LOW)
  rtc_gpio_pullup_dis((gpio_num_t)PIN_SOS);
  esp_sleep_enable_ext1_wakeup(1ULL << PIN_SOS, ESP_EXT1_WAKEUP_ANY_HIGH);  // SOS membangunkan alat saat sleep
  esp_deep_sleep_start();
}

// ---- MPU6050 (register mentah, +-8 g) ----
// Audit K4: tiap tulis/baca diperiksa, WHO_AM_I dan register range dibaca balik, gagal baca TIDAK lagi dianggap "diam" (1 g),
// sensor di-init ulang otomatis, dan kesehatannya dilaporkan lewat field `sens` di paket. Skala 1 g dikalibrasi saat boot (diam).
constexpr float    MPU_LSB_PER_G   = 4096.0f;   // +-8 g
constexpr uint8_t  MPU_FAIL_REINIT = 5;         // gagal berturut-turut sebelum Wire + sensor di-init ulang
constexpr uint8_t  MPU_FAIL_LIMIT  = 15;        // gagal berturut-turut sebelum sensor dinyatakan mati (mpuOk=false)
constexpr uint32_t MPU_RETRY_MS    = 1000;      // jeda percobaan ulang saat sensor mati (jangan memblok loop SOS)
RTC_DATA_ATTR float gScale = 1.0f;              // pengali hasil kalibrasi 1 g
RTC_DATA_ATTR bool  gScaleSet = false;
uint8_t  mpuFails = 0;
uint32_t mpuNextTry = 0;

bool mpuWrite(uint8_t r, uint8_t v) { Wire.beginTransmission(MPU); Wire.write(r); Wire.write(v); return Wire.endTransmission() == 0; }
bool mpuRead(uint8_t r, uint8_t *buf, size_t n) {
  Wire.beginTransmission(MPU); Wire.write(r);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom((int)MPU, (int)n) != (int)n) return false;
  for (size_t i = 0; i < n; i++) buf[i] = Wire.read();
  return true;
}
bool mpuInit() {
  uint8_t who = 0, rng = 0;
  if (!mpuRead(0x75, &who, 1)) return false;                 // WHO_AM_I
  if (who == 0x00 || who == 0xFF) return false;              // bus mengambang / tidak ada perangkat
  if (who != 0x68) Serial.printf("PERINGATAN: WHO_AM_I=0x%02X (MPU6050 asli 0x68), kemungkinan klon\n", who);
  if (!mpuWrite(0x6B, 0x00)) return false;                   // wake
  delay(50);
  if (!mpuWrite(0x1C, 0x10)) return false;                   // +-8 g -> 4096 LSB/g
  if (!mpuRead(0x1C, &rng, 1) || rng != 0x10) { Serial.printf("MPU range tidak terterap (baca 0x%02X, harus 0x10)\n", rng); return false; }
  return true;
}
// Besar percepatan (g, sudah dikali gScale) atau -1 bila gagal/tidak sah. Tidak pernah mengembalikan 1,0 palsu.
float accelG() {
  uint8_t b[6];
  if (!mpuRead(0x3B, b, 6)) return -1.0f;
  int16_t x = (int16_t)(b[0] << 8 | b[1]), y = (int16_t)(b[2] << 8 | b[3]), z = (int16_t)(b[4] << 8 | b[5]);
  if (x == 0 && y == 0 && z == 0) return -1.0f;              // semua nol = bacaan mati, bukan jatuh bebas
  float ax = x / MPU_LSB_PER_G, ay = y / MPU_LSB_PER_G, az = z / MPU_LSB_PER_G;
  return sqrtf(ax * ax + ay * ay + az * az) * gScale;
}
// Pembaca dengan pemulihan: dipakai loop deteksi. Mengembalikan -1 bila tidak ada data sah saat ini.
float accelSafe() {
  uint32_t now = millis();
  if (!mpuOk && now < mpuNextTry) return -1.0f;
  float g = accelG();
  if (g >= 0) { mpuFails = 0; if (!mpuOk) { mpuOk = true; Serial.println("MPU pulih"); } return g; }
  if (mpuFails < 255) mpuFails++;
  if (mpuFails == MPU_FAIL_REINIT || (mpuFails > MPU_FAIL_REINIT && mpuFails % 10 == 0) || (!mpuOk && now >= mpuNextTry)) {
    Wire.end(); Wire.begin(PIN_SDA, PIN_SCL); Wire.setTimeOut(20);
    if (mpuInit()) { mpuFails = 0; mpuOk = true; Serial.println("MPU di-init ulang"); }
    mpuNextTry = now + MPU_RETRY_MS;
  }
  if (mpuFails >= MPU_FAIL_LIMIT && mpuOk) { mpuOk = false; mpuNextTry = now + MPU_RETRY_MS; Serial.println("MPU MATI: deteksi jatuh tidak aktif"); }
  return -1.0f;
}
// Kalibrasi 1 g: rata-rata 32 sampel saat diam. Dibatalkan bila bergerak (simpangan > 0,05 g) atau skala tidak masuk akal;
// kalibrasi lama (RTC) dipertahankan. Menangani skala keliru, mis. g=4,8 saat diam (audit K4; penyebab asli masih DUGAAN).
bool mpuCalibrate() {
  float s = 0, s2 = 0; int n = 0;
  const float oldScale = gScale;
  gScale = 1.0f;                                              // ukur mentah, tanpa skala lama
  for (int i = 0; i < 32; i++) { float g = accelG(); if (g >= 0) { s += g; s2 += g * g; n++; } delay(10); }
  if (n < 24) { gScale = oldScale; Serial.println("Kalibrasi g dibatalkan: terlalu banyak bacaan gagal"); return false; }
  float mean = s / n, var = s2 / n - mean * mean;
  if (var > 0.0025f) { gScale = oldScale; Serial.printf("Kalibrasi g dibatalkan: alat bergerak (var=%.4f)\n", var); return false; }
  float scale = 1.0f / mean;
  if (scale < 0.2f || scale > 2.0f) { gScale = oldScale; Serial.printf("Kalibrasi g ditolak: rata-rata diam %.2f g tidak masuk akal\n", mean); return false; }
  gScale = scale; gScaleSet = true;
  Serial.printf("Kalibrasi g: diam terbaca %.2f g, skala %.3f\n", mean, scale);
  return true;
}

// ---- Helm (BLE scanner) ----
// Helmet menyiarkan manufacturer data {FF FF 'P' 'H' worn counter} tiap ~8 s (burst 400 ms).
constexpr uint32_t HELM_TIMEOUT_MS = 30000;   // tidak terdengar > 30 s = helm tidak terjangkau (KALIBRASI)
volatile uint32_t helmSeenAt = 0;             // millis() terakhir paket valid; 0 = belum pernah
volatile uint8_t helmWorn = 0;
constexpr int HELM_RSSI_MIN = -85;            // KALIBRASI: RSSI (dBm, dirata-rata) minimum agar worn=1 dihitung "dipakai"; lebih lemah = helm jauh = tidak dipakai
volatile float helmRssi = -127;               // rata-rata bergerak RSSI paket helm (EMA)

class HelmCb : public NimBLEAdvertisedDeviceCallbacks {
  void onResult(NimBLEAdvertisedDevice *d) override {
    if (!d->haveManufacturerData()) return;
    std::string m = d->getManufacturerData();
    if (m.size() >= 5 && (uint8_t)m[0] == 0xFF && (uint8_t)m[1] == 0xFF && m[2] == 'P' && m[3] == 'H') {
      helmWorn = (uint8_t)m[4] ? 1 : 0;
      helmRssi = helmSeenAt ? helmRssi * 0.8f + d->getRSSI() * 0.2f : d->getRSSI();   // RSSI BLE naik-turun +-10 dB: dirata-ratakan
      helmSeenAt = millis() ? millis() : 1;
    }
  }
};
HelmCb helmCb;

void helmScanStart() {
  NimBLEDevice::init("");
  NimBLEScan *scan = NimBLEDevice::getScan();
  scan->setAdvertisedDeviceCallbacks(&helmCb, true);
  scan->setActiveScan(false);                  // pasif: hemat daya, manufacturer data ada di paket iklan
  scan->setInterval(100);                      // satuan 0,625 ms -> 62,5 ms
  scan->setWindow(50);                         // ~50% radio aktif (KALIBRASI: turunkan jika boros, helm hanya 400 ms/8 s)
  scan->setDuplicateFilter(false);
  scan->start(0, nullptr, false);              // scan terus-menerus
}
void helmScanStop() { NimBLEDevice::getScan()->stop(); NimBLEDevice::deinit(true); }

// 1 = dipakai, 0 = terdengar tapi tidak dipakai, 2 = tidak terjangkau
int helmState() {
  if (!helmSeenAt || millis() - helmSeenAt > HELM_TIMEOUT_MS) return 2;
  return helmWorn && helmRssi >= HELM_RSSI_MIN;   // dipakai = sentuh terdeteksi DAN dekat
}

// ---- Baterai ----
int batMilliVolts() {  // rata-rata 8 sampel, analogReadMilliVolts memakai kalibrasi eFuse ESP32
  uint32_t sum = 0;
  for (int i = 0; i < 8; i++) sum += analogReadMilliVolts(PIN_BAT);
  return (int)(sum / 8 * BAT_DIV);
}

// ---- LoRa ----
// Field sens (bitmask): 1 = MPU mati/tidak terbaca (deteksi jatuh tidak aktif), 2 = skala 1 g belum terkalibrasi.
uint8_t sensFlags() { return (mpuOk ? 0 : 1) | (gScaleSet ? 0 : 2); }

void sendPkt(const char *type, uint16_t seq) {
  while (gpsSerial.available()) gps.encode(gpsSerial.read());
  updateFix();
  char buf[184];
  int bat = batMilliVolts();
  // format v2: PANDU,V2,<vest_id>,<seq>,<jenis>,<lat>,<lon>,<mV>,<helm 0/1/2>,<usia posisi detik>,<sens>*<hmac 8 hex>
  // lat/lon dari memori RTC (bertahan deep sleep, K3); NOFIX hanya bila belum pernah ada fix sejak cold boot.
  int n;
  if (rtcHasFix)
    n = snprintf(buf, sizeof buf, "PANDU,V2,%d,%u,%s,%.6f,%.6f,%d,%d,%lu,%u", VEST_ID, (unsigned)seq, type, rtcLat, rtcLon, bat, helmState(), (unsigned long)posAgeS(), (unsigned)sensFlags());
  else
    n = snprintf(buf, sizeof buf, "PANDU,V2,%d,%u,%s,NOFIX,NOFIX,%d,%d,0,%u", VEST_ID, (unsigned)seq, type, bat, helmState(), (unsigned)sensFlags());
  char mac[PANDU_MAC_HEX + 1];
  panduMac(buf, n, mac);
  snprintf(buf + n, sizeof buf - n, "*%s", mac);
  Serial.println(buf);
  if (!loraOk) return;
  LoRa.beginPacket(); LoRa.print(buf); LoRa.endPacket();
}

// ---- Deteksi ----
enum Alert { NONE, FALL, MOB, SOS };
const char *alertName[] = {"", "FALL", "MOB", "SOS"};
Alert active = NONE;
bool sosWake = false;
int repeatsLeft = 0;  // SOS dikirim ulang min. 3x (LoRa tanpa ACK)
uint32_t lastSend = 0, lastBeat = 0, beatInterval = HEARTBEAT_MS;
uint16_t alertSeq = 0;   // seq alert aktif: kirim ulang SOS memakai seq yang sama (Gateway membuang duplikat)

Alert detectFall() {  // free-fall >= FREEFALL_MS lalu benturan dalam IMPACT_WIN
  static uint32_t ffStart = 0, ffEnd = 0;
  float g = accelSafe(); uint32_t now = millis();
  if (g < 0) return NONE;   // tidak ada data sah (K4): jangan diartikan jatuh maupun diam
  if (g < FREEFALL_G) { if (!ffStart) ffStart = now; if (now - ffStart >= FREEFALL_MS) ffEnd = now; }
  else ffStart = 0;
  if (ffEnd && g > IMPACT_G && now - ffEnd < IMPACT_WIN) { ffEnd = 0; return FALL; }
  if (ffEnd && now - ffEnd >= IMPACT_WIN) ffEnd = 0;
  return NONE;
}
bool waterWet() { return analogReadMilliVolts(PIN_WATER) > WATER_WET_MV; }
uint32_t fallAt = 0;  // millis() jatuh terakhir; 0 = belum pernah
Alert detectMob() {  // MOB = jatuh DAN sensor air aktif kontinu WATER_MS dalam MOB_WINDOW_MS setelah jatuh (basah saja tanpa jatuh = bukan alarm)
  static uint32_t since = 0;
  if (!fallAt || millis() - fallAt > MOB_WINDOW_MS) { since = 0; return NONE; }
  if (waterWet()) { if (!since) since = millis(); return millis() - since >= WATER_MS ? MOB : NONE; }
  since = 0; return NONE;
}
Alert detectSos() {
  static uint32_t since = 0;
  if (digitalRead(PIN_SOS) == HIGH) { if (!since) since = millis(); return millis() - since >= SOS_HOLD_MS ? SOS : NONE; }
  since = 0; return NONE;
}

void setup() {
  Serial.begin(115200);
#ifdef DEMO_NO_BROWNOUT
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);   // HANYA demo di USB tanpa kapasitor: mematikan detektor brownout (jangan dipakai di produk)
#endif
  rtc_gpio_deinit((gpio_num_t)PIN_PWR_BTN);
  rtc_gpio_deinit((gpio_num_t)PIN_SOS);
  pinMode(PIN_PWR_BTN, INPUT_PULLUP);
  pinMode(PIN_SOS, INPUT);  // pull-down eksternal R2
  pinMode(PIN_WATER, INPUT);
  analogSetPinAttenuation(PIN_WATER, ADC_11db);
  analogSetPinAttenuation(PIN_BAT, ADC_11db);  // 0-3,1 V; baterai 4,2 V / 2 = 2,1 V
  while (digitalRead(PIN_PWR_BTN) == LOW) delay(10);   // abaikan tekanan yang membangunkan
  if (esp_reset_reason() != ESP_RST_DEEPSLEEP) seqCounter = (uint16_t)esp_random();   // cold boot: mulai acak supaya tidak menabrak seq lama
  Serial.println("[1] gpio ok");
  gpsPower(true); xkcPower(true);
  Serial.println("[2] gps+xkc power on");
  gpsSerial.begin(9600, SERIAL_8N1, PIN_GPS_RX, PIN_GPS_TX);
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setTimeOut(20);   // ms; bus macet tidak boleh membekukan loop SOS
  Serial.println("[3] i2c");
  mpuOk = mpuInit();
  // Kalibrasi butuh ~0,4 s dan alat diam. Bangun karena SOS: lewati (jangan tunda alarm), pakai skala terakhir dari RTC bila ada.
  if (mpuOk && !(gScaleSet && esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT1)) mpuCalibrate();
  Serial.println("[4] mpu done");
  LoRa.setPins(PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  loraOk = LoRa.begin(LORA_FREQ);
  if (loraOk) { LoRa.enableCrc(); LoRa.setSyncWord(PANDU_SYNC_WORD); }   // K2: CRC + sync word unik, harus sama dengan Gateway
  if (PANDU_KEY_IS_DEFAULT) Serial.println("PERINGATAN: PANDU_KEY bawaan (dev). Buat include/config.h agar paket terautentikasi.");
  Serial.println("[5] lora done");
  helmScanStart();
  Serial.println("[6] ble scan on");
  sosWake = esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT1;
  Serial.printf("Boot: MPU=%d LoRa=%d wake=%s\n", mpuOk, loraOk, sosWake ? "SOS" : "other");
}

void loop() {
  while (gpsSerial.available()) gps.encode(gpsSerial.read());
  updateFix();   // simpan posisi ke RTC begitu ada fix, supaya SOS dari bangun tidur membawa posisi (K3)

  // tombol power: tekan sebentar = tidur
  if (digitalRead(PIN_PWR_BTN) == LOW) { delay(30); if (digitalRead(PIN_PWR_BTN) == LOW) goToSleep(); }

  if (sosWake) { active = SOS; alertSeq = nextSeq(); repeatsLeft = 3; lastSend = millis() - ALERT_REPEAT_MS; sosWake = false; }  // bangun karena SOS = langsung kirim, tanpa tahan 2 detik
  Alert a = detectSos();
  if (a == NONE) a = detectMob();
  if (a == NONE) a = detectFall();   // selalu dipanggil: accelSafe() menangani sensor mati/pulih (K4)
  if (a == FALL) fallAt = millis() ? millis() : 1;
  if (a != NONE) { if (a != active) { alertSeq = nextSeq(); repeatsLeft = (a == SOS ? 3 : 2); lastSend = millis() - ALERT_REPEAT_MS; } active = a; }  // alert baru: kirim segera

  uint32_t now = millis();
  if (active != NONE && now - lastSend >= ALERT_REPEAT_MS) {
    sendPkt(alertName[active], alertSeq); lastSend = now;
    if (repeatsLeft > 0) repeatsLeft--;
    bool still = (active == SOS && digitalRead(PIN_SOS) == HIGH) || (active == MOB && waterWet());
    if (repeatsLeft == 0 && !still) active = NONE;  // berhenti setelah kirim ulang & kondisi berakhir
  }
  static uint32_t lastStat = 0;   // ringkasan status untuk demo/serial monitor
  if (now - lastStat >= 2000) {
    lastStat = now;
    uint32_t left = (fallAt && now - fallAt <= MOB_WINDOW_MS) ? (MOB_WINDOW_MS - (now - fallAt)) / 1000 : 0;
    Serial.printf("[status] helm=%d rssi=%d dBm | air=%s (%d mV) | jendela MOB=%lus | gps=%s sat=%d | g=%.2f\n", helmState(), (int)helmRssi,
                  waterWet() ? "ADA AIR" : "kering", analogReadMilliVolts(PIN_WATER), (unsigned long)left,
                  gps.location.isValid() ? "FIX" : "NOFIX", gps.satellites.isValid() ? (int)gps.satellites.value() : 0, mpuOk ? accelG() : -1.0f);
  }
  if (now - lastBeat >= beatInterval) {
    sendPkt("HB", nextSeq()); lastBeat = now;
    beatInterval = HEARTBEAT_MS - HEARTBEAT_JITTER_MS + esp_random() % (2 * HEARTBEAT_JITTER_MS + 1);
  }
  delay(10);
}
