// PANDU Helmet Node: ESP32-C3 SuperMini. Kirim status "helm dipakai" lewat BLE advertising.
// Pin (PCB2 v2): TOUCH_SIG=GPIO2 (modul TTP223, HIGH = tersentuh/dipakai), PWR_BTN=GPIO4 (tact ke GND, pull-up R1).
// Format advertising: nama "PANDU-HELM", manufacturer data = {0xFF,0xFF,'P','H', worn(0/1), counter}
//
// HEMAT DAYA: library Arduino-ESP32 bawaan dikompilasi tanpa CONFIG_PM_ENABLE, jadi light sleep otomatis
// (dengan BLE) tidak tersedia. Pengganti: duty-cycle deep sleep. Tiap WAKE_PERIOD_S detik bangun,
// baca sensor, siaran BLE singkat (ADV_BURST_MS), lalu deep sleep lagi. State disimpan di memori RTC.
// Tombol (GPIO4) = toggle ON/OFF: bangun dari tidur kapan saja; OFF = tidur tanpa timer.
#include <Arduino.h>
#include <NimBLEDevice.h>
#include "esp_sleep.h"

constexpr int PIN_TOUCH = 2;
constexpr int PIN_PWR   = 4;                       // GPIO0-5 bisa wake deep sleep di C3
constexpr uint32_t WAKE_PERIOD_S = 8;              // KALIBRASI: makin kecil makin responsif, makin boros
constexpr uint32_t ADV_BURST_MS  = 400;            // lama siaran per bangun
constexpr uint8_t  CONFIRM_ON    = 2;              // sentuhan harus terbaca 2x berturut-turut = dipakai
constexpr uint8_t  CONFIRM_OFF   = 3;              // lepas 3x berturut-turut = tidak dipakai (anti-kedip)

RTC_DATA_ATTR bool powered = true;                 // toggle tombol
RTC_DATA_ATTR bool worn = false;
RTC_DATA_ATTR uint8_t streak = 0;                  // jumlah pembacaan berturut-turut yang berbeda dari 'worn'
RTC_DATA_ATTR uint8_t counter = 0;

void sleepNow(bool withTimer) {
  while (digitalRead(PIN_PWR) == LOW) delay(10);   // tunggu tombol dilepas agar tidak langsung bangun
  delay(50);
  esp_deep_sleep_enable_gpio_wakeup(1ULL << PIN_PWR, ESP_GPIO_WAKEUP_GPIO_LOW);
  if (withTimer) esp_sleep_enable_timer_wakeup((uint64_t)WAKE_PERIOD_S * 1000000ULL);
  esp_deep_sleep_start();
}

void advertiseBurst() {
  NimBLEDevice::init("PANDU-HELM");
  NimBLEDevice::setPower(ESP_PWR_LVL_N0);          // 0 dBm cukup untuk jarak helm ke vest
  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();
  adv->setMinInterval(32);                         // 20 ms (satuan 0,625 ms) -> ~20 paket per burst
  adv->setMaxInterval(48);
  uint8_t d[6] = {0xFF, 0xFF, 'P', 'H', (uint8_t)worn, counter++};
  NimBLEAdvertisementData ad, sr;
  ad.setFlags(BLE_HS_ADV_F_DISC_GEN | BLE_HS_ADV_F_BREDR_UNSUP);
  ad.setManufacturerData(std::string((char *)d, sizeof d));
  sr.setName("PANDU-HELM");
  adv->setAdvertisementData(ad);
  adv->setScanResponseData(sr);
  adv->start();
  delay(ADV_BURST_MS);
  adv->stop();
  NimBLEDevice::deinit(true);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PWR, INPUT_PULLUP);
  pinMode(PIN_TOUCH, INPUT);

  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_GPIO) {   // tombol ditekan: toggle ON/OFF
    powered = !powered;
    streak = 0;
    Serial.printf("Tombol: %s\n", powered ? "ON" : "OFF");
  }
  if (!powered) sleepNow(false);                   // OFF: hanya tombol yang membangunkan

  bool touch = digitalRead(PIN_TOUCH);
  if (touch == worn) streak = 0;
  else if (++streak >= (touch ? CONFIRM_ON : CONFIRM_OFF)) { worn = touch; streak = 0; }

  Serial.printf("helm dipakai=%d (streak %d)\n", worn, streak);
  advertiseBurst();
  sleepNow(true);
}

void loop() {}  // tidak pernah tercapai: setup() selalu berakhir di deep sleep
