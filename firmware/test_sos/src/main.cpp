// Tes mandiri tombol SOS dan tombol power (ESP32 DevKit saja, tanpa LoRa/GPS/MPU).
// Wiring: SOS = tact antara IO27 dan 3V3, resistor 10k dari IO27 ke GND (aktif-HIGH).
//         Power = tact antara IO13 dan GND.  LED = LED onboard IO2.
// Logika dan ambang SAMA dengan vest_node (SOS_HOLD_MS, urutan sleep/wake).
// Uji: (1) tahan SOS 2 s -> "SOS TERPICU"; (2) tekan singkat -> diabaikan;
//      (3) tekan power -> "Sleep..."; (4) tekan SOS saat tidur -> bangun dan langsung "SOS TERPICU"; (5) tekan power saat tidur -> bangun biasa.
#include <Arduino.h>
#include "driver/rtc_io.h"

constexpr int PIN_PWR_BTN = 13, PIN_SOS = 27, PIN_LED = 2;
constexpr uint32_t SOS_HOLD_MS = 2000;

void goToSleep() {
  Serial.println("Sleep... (tekan SOS atau power untuk bangun)");
  Serial.flush();
  while (digitalRead(PIN_PWR_BTN) == LOW || digitalRead(PIN_SOS) == HIGH) delay(10);
  delay(50);
  rtc_gpio_pullup_en((gpio_num_t)PIN_PWR_BTN);
  rtc_gpio_pulldown_dis((gpio_num_t)PIN_PWR_BTN);
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_PWR_BTN, 0);
  rtc_gpio_pulldown_en((gpio_num_t)PIN_SOS);
  rtc_gpio_pullup_dis((gpio_num_t)PIN_SOS);
  esp_sleep_enable_ext1_wakeup(1ULL << PIN_SOS, ESP_EXT1_WAKEUP_ANY_HIGH);
  esp_deep_sleep_start();
}

void sosFired(const char *why) {
  Serial.printf("\n*** SOS TERPICU (%s) ***  paket akan dikirim 3x\n\n", why);
  digitalWrite(PIN_LED, HIGH); delay(2000); digitalWrite(PIN_LED, LOW);
}

void setup() {
  Serial.begin(115200);
  delay(300);
  rtc_gpio_deinit((gpio_num_t)PIN_PWR_BTN);
  rtc_gpio_deinit((gpio_num_t)PIN_SOS);
  pinMode(PIN_PWR_BTN, INPUT_PULLUP);
  pinMode(PIN_SOS, INPUT);
  pinMode(PIN_LED, OUTPUT);
  esp_sleep_wakeup_cause_t w = esp_sleep_get_wakeup_cause();
  Serial.printf("Boot: bangun karena %s\n", w == ESP_SLEEP_WAKEUP_EXT1 ? "SOS" : w == ESP_SLEEP_WAKEUP_EXT0 ? "tombol power" : "power-on/reset");
  while (digitalRead(PIN_PWR_BTN) == LOW) delay(10);
  if (w == ESP_SLEEP_WAKEUP_EXT1) sosFired("bangun dari tidur, langsung kirim");
  Serial.println("Siap. Tahan SOS 2 detik, atau tekan power untuk tidur.");
}

void loop() {
  if (digitalRead(PIN_PWR_BTN) == LOW) { delay(30); if (digitalRead(PIN_PWR_BTN) == LOW) goToSleep(); }

  if (digitalRead(PIN_SOS) == HIGH) {
    uint32_t t0 = millis(), lastPrint = 0;
    bool fired = false;
    while (digitalRead(PIN_SOS) == HIGH) {
      uint32_t held = millis() - t0;
      if (!fired && held - lastPrint >= 500) { lastPrint = held; Serial.printf("SOS ditahan %.1f / %.1f s\n", held / 1000.0, SOS_HOLD_MS / 1000.0); }
      if (!fired && held >= SOS_HOLD_MS) { fired = true; sosFired("ditahan 2 detik"); }
      delay(10);
    }
    if (!fired) Serial.printf("tekan singkat (%lu ms): diabaikan\n", (unsigned long)(millis() - t0));
  }
  delay(10);
}
