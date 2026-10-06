// PANDU Helmet Node: ESP32-C3 SuperMini. Hanya kirim status "helm dipakai" lewat BLE advertising.
// Pin (PCB2 v2): TOUCH_SIG=GPIO2 (modul TTP223, HIGH = tersentuh/dipakai), PWR_BTN=GPIO4 (tact ke GND, pull-up R1).
// Format advertising: nama "PANDU-HELM", manufacturer data = {0xFF,0xFF, 'P','H', worn(0/1), counter}
#include <Arduino.h>
#include <NimBLEDevice.h>
#include "esp_sleep.h"

constexpr int PIN_TOUCH = 2;
constexpr int PIN_PWR   = 4;                 // GPIO0-5 bisa wake deep sleep di C3
constexpr uint32_t WORN_ON_MS  = 1000;       // sentuhan harus stabil 1 s = dipakai (KALIBRASI)
constexpr uint32_t WORN_OFF_MS = 5000;       // lepas 5 s = tidak dipakai (anti-kedip saat bergerak)
constexpr uint16_t ADV_MIN = 1600, ADV_MAX = 1600;  // satuan 0,625 ms -> 1 detik (hemat CR2032)

NimBLEAdvertising *adv;
bool worn = false;
uint8_t counter = 0;

void publish() {
  uint8_t d[6] = {0xFF, 0xFF, 'P', 'H', (uint8_t)worn, counter++};
  NimBLEAdvertisementData ad, sr;
  ad.setFlags(BLE_HS_ADV_F_DISC_GEN | BLE_HS_ADV_F_BREDR_UNSUP);
  ad.setManufacturerData(std::string((char *)d, sizeof d));
  sr.setName("PANDU-HELM");
  adv->setAdvertisementData(ad);
  adv->setScanResponseData(sr);
  adv->start();
  Serial.printf("helm dipakai=%d\n", worn);
}

void goToSleep() {
  Serial.println("Sleep...");
  adv->stop();
  while (digitalRead(PIN_PWR) == LOW) delay(10);   // tunggu tombol dilepas
  delay(50);
  esp_deep_sleep_enable_gpio_wakeup(1ULL << PIN_PWR, ESP_GPIO_WAKEUP_GPIO_LOW);
  esp_deep_sleep_start();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PWR, INPUT_PULLUP);
  pinMode(PIN_TOUCH, INPUT);
  while (digitalRead(PIN_PWR) == LOW) delay(10);   // abaikan tekanan yang membangunkan
  NimBLEDevice::init("PANDU-HELM");
  NimBLEDevice::setPower(ESP_PWR_LVL_N0);          // 0 dBm cukup untuk jarak helm ke vest
  adv = NimBLEDevice::getAdvertising();
  adv->setMinInterval(ADV_MIN);
  adv->setMaxInterval(ADV_MAX);
  worn = digitalRead(PIN_TOUCH);
  publish();
}

void loop() {
  static uint32_t changeSince = 0, lastPub = 0;
  if (digitalRead(PIN_PWR) == LOW) { delay(30); if (digitalRead(PIN_PWR) == LOW) goToSleep(); }

  bool touch = digitalRead(PIN_TOUCH);
  uint32_t now = millis();
  if (touch != worn) {                              // debounce berbeda untuk pasang vs lepas
    if (!changeSince) changeSince = now;
    if (now - changeSince >= (touch ? WORN_ON_MS : WORN_OFF_MS)) { worn = touch; changeSince = 0; publish(); lastPub = now; }
  } else changeSince = 0;

  if (now - lastPub >= 10000) { publish(); lastPub = now; }  // refresh counter agar Vest tahu helm masih hidup
  delay(20);
}
