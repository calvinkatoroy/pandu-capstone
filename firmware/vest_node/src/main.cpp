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
constexpr int PIN_SOS      = 27;  // tact (ke GND), tahan SOS_HOLD_MS
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
constexpr uint8_t MPU = 0x68;

TinyGPSPlus gps;
HardwareSerial gpsSerial(2);
bool loraOk = false, mpuOk = false;

// ---- Power gating ----
void gpsPower(bool on) {
  if (on) { pinMode(PIN_GPS_EN, OUTPUT); digitalWrite(PIN_GPS_EN, LOW); }
  else    { pinMode(PIN_GPS_EN, INPUT); }  // hi-Z: pull-up 100k mematikan Q1 (HIGH 3,3 V bocor di VBAT 4,2 V)
}
void xkcPower(bool on) { pinMode(PIN_XKC_EN, OUTPUT); digitalWrite(PIN_XKC_EN, on); }

// ---- Deep sleep ----
void goToSleep() {
  Serial.println("Sleep...");
  gpsPower(false); xkcPower(false);
  if (loraOk) LoRa.sleep();
  while (digitalRead(PIN_PWR_BTN) == LOW) delay(10);   // tunggu lepas agar tidak langsung bangun
  delay(50);
  rtc_gpio_pullup_en((gpio_num_t)PIN_PWR_BTN);
  rtc_gpio_pulldown_dis((gpio_num_t)PIN_PWR_BTN);
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_PWR_BTN, 0);
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

// ---- LoRa ----
void sendPkt(const char *type) {
  while (gpsSerial.available()) gps.encode(gpsSerial.read());
  char buf[96];
  if (gps.location.isValid())
    snprintf(buf, sizeof buf, "PANDU,V1,%s,%.6f,%.6f", type, gps.location.lat(), gps.location.lng());
  else
    snprintf(buf, sizeof buf, "PANDU,V1,%s,NOFIX,NOFIX", type);
  Serial.println(buf);
  if (!loraOk) return;
  LoRa.beginPacket(); LoRa.print(buf); LoRa.endPacket();
}

// ---- Deteksi ----
enum Alert { NONE, FALL, MOB, SOS };
const char *alertName[] = {"", "FALL", "MOB", "SOS"};
Alert active = NONE;
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
  if (digitalRead(PIN_SOS) == LOW) { if (!since) since = millis(); return millis() - since >= SOS_HOLD_MS ? SOS : NONE; }
  since = 0; return NONE;
}

void setup() {
  Serial.begin(115200);
  rtc_gpio_deinit((gpio_num_t)PIN_PWR_BTN);
  pinMode(PIN_PWR_BTN, INPUT_PULLUP);
  pinMode(PIN_SOS, INPUT_PULLUP);
  pinMode(PIN_WATER, INPUT);
  while (digitalRead(PIN_PWR_BTN) == LOW) delay(10);   // abaikan tekanan yang membangunkan
  gpsPower(true); xkcPower(true);
  gpsSerial.begin(9600, SERIAL_8N1, PIN_GPS_RX, PIN_GPS_TX);
  Wire.begin(PIN_SDA, PIN_SCL);
  mpuOk = mpuInit();
  LoRa.setPins(PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  loraOk = LoRa.begin(LORA_FREQ);
  Serial.printf("Boot: MPU=%d LoRa=%d\n", mpuOk, loraOk);
}

void loop() {
  while (gpsSerial.available()) gps.encode(gpsSerial.read());

  // tombol power: tekan sebentar = tidur
  if (digitalRead(PIN_PWR_BTN) == LOW) { delay(30); if (digitalRead(PIN_PWR_BTN) == LOW) goToSleep(); }

  Alert a = detectSos();
  if (a == NONE) a = detectMob();
  if (a == NONE && mpuOk) a = detectFall();
  if (a != NONE) active = a;

  uint32_t now = millis();
  if (active != NONE && now - lastSend >= ALERT_REPEAT_MS) {
    sendPkt(alertName[active]); lastSend = now;
    if (digitalRead(PIN_SOS) == HIGH && !digitalRead(PIN_WATER) && active != FALL) active = NONE;  // alert hilang saat kondisi berakhir
    else if (active == FALL) active = NONE;  // FALL dikirim sekali per kejadian (ulang tiap deteksi baru)
  }
  if (now - lastBeat >= HEARTBEAT_MS) { sendPkt("HB"); lastBeat = now; }
  delay(10);
}
