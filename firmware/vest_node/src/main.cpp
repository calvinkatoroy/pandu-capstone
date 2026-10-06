// PANDU Vest Node: firmware dasar (ESP32-DevKitC V4, Arduino core)
// Pin mengikuti HANDOVER.md. Nilai ber-tanda "KALIBRASI" perlu di-tune di perangkat nyata.
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <TinyGPSPlus.h>
#include "driver/rtc_io.h"

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

// ---- Parameter (KALIBRASI) ----
constexpr long LORA_FREQ       = 915E6;   // modul dibeli 915 MHz (regulasi ID 920-923 MHz)
constexpr float FREEFALL_G     = 0.4f;    // |a| di bawah ini = jatuh bebas
constexpr uint32_t FREEFALL_MS = 120;
constexpr float IMPACT_G       = 2.5f;    // benturan setelah jatuh bebas
constexpr uint32_t IMPACT_WIN  = 1000;    // jendela benturan setelah free-fall
constexpr uint32_t WATER_MS    = 3000;    // sensor air harus aktif sebanyak ini = MOB
constexpr uint32_t SOS_HOLD_MS = 2000;
constexpr uint32_t HEARTBEAT_MS = 30000;
constexpr uint32_t ALERT_REPEAT_MS = 5000;
constexpr float BAT_DIV = 2.0f;     // KALIBRASI: faktor pembagi (cek dengan multimeter)
constexpr uint8_t MPU = 0x68;

TinyGPSPlus gps;
HardwareSerial gpsSerial(2);
bool loraOk = false, mpuOk = false;

// ---- Power gating ----
void gpsPower(bool on) {
  if (on) { pinMode(PIN_GPS_EN, OUTPUT); digitalWrite(PIN_GPS_EN, LOW); }
  else    { pinMode(PIN_GPS_EN, INPUT); }  // hi-Z: pull-up R3 100k ke 3V3_SYS mematikan Q1
}
void xkcPower(bool on) { pinMode(PIN_XKC_EN, OUTPUT); digitalWrite(PIN_XKC_EN, on); }

// ---- Deep sleep ----
void goToSleep() {
  Serial.println("Sleep...");
  gpsPower(false); xkcPower(false);
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
void mpuWrite(uint8_t r, uint8_t v) { Wire.beginTransmission(MPU); Wire.write(r); Wire.write(v); Wire.endTransmission(); }
bool mpuInit() {
  Wire.beginTransmission(MPU);
  if (Wire.endTransmission() != 0) return false;
  mpuWrite(0x6B, 0x00);  // wake
  mpuWrite(0x1C, 0x10);  // +-8 g -> 4096 LSB/g
  return true;
}
float accelG() {
  Wire.beginTransmission(MPU); Wire.write(0x3B); Wire.endTransmission(false);
  if (Wire.requestFrom((int)MPU, 6) != 6) return 1.0f;  // gagal baca = anggap diam
  float ax = (int16_t)(Wire.read() << 8 | Wire.read()) / 4096.0f;
  float ay = (int16_t)(Wire.read() << 8 | Wire.read()) / 4096.0f;
  float az = (int16_t)(Wire.read() << 8 | Wire.read()) / 4096.0f;
  return sqrtf(ax * ax + ay * ay + az * az);
}

// ---- Baterai ----
int batMilliVolts() {  // rata-rata 8 sampel, analogReadMilliVolts memakai kalibrasi eFuse ESP32
  uint32_t sum = 0;
  for (int i = 0; i < 8; i++) sum += analogReadMilliVolts(PIN_BAT);
  return (int)(sum / 8 * BAT_DIV);
}

// ---- LoRa ----
void sendPkt(const char *type) {
  while (gpsSerial.available()) gps.encode(gpsSerial.read());
  char buf[112];
  int bat = batMilliVolts();  // format: PANDU,V1,<jenis>,<lat>,<lon>,<mV baterai>
  if (gps.location.isValid())
    snprintf(buf, sizeof buf, "PANDU,V1,%s,%.6f,%.6f,%d", type, gps.location.lat(), gps.location.lng(), bat);
  else
    snprintf(buf, sizeof buf, "PANDU,V1,%s,NOFIX,NOFIX,%d", type, bat);
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
uint32_t lastSend = 0, lastBeat = 0;

Alert detectFall() {  // free-fall >= FREEFALL_MS lalu benturan dalam IMPACT_WIN
  static uint32_t ffStart = 0, ffEnd = 0;
  float g = accelG(); uint32_t now = millis();
  if (g < FREEFALL_G) { if (!ffStart) ffStart = now; if (now - ffStart >= FREEFALL_MS) ffEnd = now; }
  else ffStart = 0;
  if (ffEnd && g > IMPACT_G && now - ffEnd < IMPACT_WIN) { ffEnd = 0; return FALL; }
  if (ffEnd && now - ffEnd >= IMPACT_WIN) ffEnd = 0;
  return NONE;
}
Alert detectMob() {  // sensor air aktif kontinu WATER_MS (anti-percikan)
  static uint32_t since = 0;
  if (digitalRead(PIN_WATER)) { if (!since) since = millis(); return millis() - since >= WATER_MS ? MOB : NONE; }
  since = 0; return NONE;
}
Alert detectSos() {
  static uint32_t since = 0;
  if (digitalRead(PIN_SOS) == HIGH) { if (!since) since = millis(); return millis() - since >= SOS_HOLD_MS ? SOS : NONE; }
  since = 0; return NONE;
}

void setup() {
  Serial.begin(115200);
  rtc_gpio_deinit((gpio_num_t)PIN_PWR_BTN);
  rtc_gpio_deinit((gpio_num_t)PIN_SOS);
  pinMode(PIN_PWR_BTN, INPUT_PULLUP);
  pinMode(PIN_SOS, INPUT);  // pull-down eksternal R2
  pinMode(PIN_WATER, INPUT);
  analogSetPinAttenuation(PIN_BAT, ADC_11db);  // 0-3,1 V; baterai 4,2 V / 2 = 2,1 V
  while (digitalRead(PIN_PWR_BTN) == LOW) delay(10);   // abaikan tekanan yang membangunkan
  gpsPower(true); xkcPower(true);
  gpsSerial.begin(9600, SERIAL_8N1, PIN_GPS_RX, PIN_GPS_TX);
  Wire.begin(PIN_SDA, PIN_SCL);
  mpuOk = mpuInit();
  LoRa.setPins(PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  loraOk = LoRa.begin(LORA_FREQ);
  sosWake = esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT1;
  Serial.printf("Boot: MPU=%d LoRa=%d wake=%s\n", mpuOk, loraOk, sosWake ? "SOS" : "other");
}

void loop() {
  while (gpsSerial.available()) gps.encode(gpsSerial.read());

  // tombol power: tekan sebentar = tidur
  if (digitalRead(PIN_PWR_BTN) == LOW) { delay(30); if (digitalRead(PIN_PWR_BTN) == LOW) goToSleep(); }

  if (sosWake) { active = SOS; repeatsLeft = 3; lastSend = millis() - ALERT_REPEAT_MS; sosWake = false; }  // bangun karena SOS = langsung kirim, tanpa tahan 2 detik
  Alert a = detectSos();
  if (a == NONE) a = detectMob();
  if (a == NONE && mpuOk) a = detectFall();
  if (a != NONE) { if (a != active) { repeatsLeft = (a == SOS ? 3 : 2); lastSend = millis() - ALERT_REPEAT_MS; } active = a; }  // alert baru: kirim segera

  uint32_t now = millis();
  if (active != NONE && now - lastSend >= ALERT_REPEAT_MS) {
    sendPkt(alertName[active]); lastSend = now;
    if (repeatsLeft > 0) repeatsLeft--;
    bool still = (active == SOS && digitalRead(PIN_SOS) == HIGH) || (active == MOB && digitalRead(PIN_WATER));
    if (repeatsLeft == 0 && !still) active = NONE;  // berhenti setelah kirim ulang & kondisi berakhir
  }
  if (now - lastBeat >= HEARTBEAT_MS) { sendPkt("HB"); lastBeat = now; }
  delay(10);
}
