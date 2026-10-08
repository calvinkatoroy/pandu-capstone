// Tes mandiri deteksi jatuh: hanya ESP32 + GY-521 (SDA IO21, SCL IO22, VCC 3V3, GND). Tanpa LoRa/GPS.
// Logika dan ambang SAMA dengan vest_node (salin; kalau ambang diubah di sini, ubah juga di sana).
// Serial 115200: tiap 20 ms cetak "g" (buka Serial Plotter), saat jatuh cetak "FALL" dan LED onboard (IO2) menyala 2 s.
#include <Arduino.h>
#include <Wire.h>
#include <math.h>

constexpr float FREEFALL_G = 0.6f;  // KALIBRASI: tes nyata, jatuh bebas terbaca 0,3-0,5 g (offset sensor ±0,2 g)
constexpr uint32_t FREEFALL_MS = 120;
constexpr float IMPACT_G = 2.5f;
constexpr uint32_t IMPACT_WIN = 1000;
constexpr uint8_t MPU = 0x68;
constexpr int PIN_LED = 2;

void mpuWrite(uint8_t r, uint8_t v) { Wire.beginTransmission(MPU); Wire.write(r); Wire.write(v); Wire.endTransmission(); }
bool mpuInit() {
  Wire.beginTransmission(MPU);
  if (Wire.endTransmission() != 0) return false;
  mpuWrite(0x6B, 0x00);
  mpuWrite(0x1C, 0x10);  // +-8 g
  return true;
}
float accelG() {
  Wire.beginTransmission(MPU); Wire.write(0x3B); Wire.endTransmission(false);
  if (Wire.requestFrom((int)MPU, 6) != 6) return 1.0f;
  float ax = (int16_t)(Wire.read() << 8 | Wire.read()) / 4096.0f;
  float ay = (int16_t)(Wire.read() << 8 | Wire.read()) / 4096.0f;
  float az = (int16_t)(Wire.read() << 8 | Wire.read()) / 4096.0f;
  return sqrtf(ax * ax + ay * ay + az * az);
}

bool detectFall(float g) {
  static uint32_t ffStart = 0, ffEnd = 0;
  uint32_t now = millis();
  if (g < FREEFALL_G) { if (!ffStart) ffStart = now; if (now - ffStart >= FREEFALL_MS) ffEnd = now; }
  else ffStart = 0;
  if (ffEnd && g > IMPACT_G && now - ffEnd < IMPACT_WIN) { ffEnd = 0; return true; }
  if (ffEnd && now - ffEnd >= IMPACT_WIN) ffEnd = 0;
  return false;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  Wire.begin(21, 22);
  Serial.println(mpuInit() ? "MPU=1" : "MPU=0 (cek SDA IO21, SCL IO22, VCC 3V3, GND)");
}

void loop() {
  static uint32_t ledOff = 0;
  float g = accelG();
  Serial.println(g, 2);
  if (detectFall(g)) { Serial.println("FALL"); digitalWrite(PIN_LED, HIGH); ledOff = millis() + 2000; }
  if (ledOff && millis() > ledOff) { digitalWrite(PIN_LED, LOW); ledOff = 0; }
  delay(20);
}
