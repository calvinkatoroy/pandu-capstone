// PANDU Helmet Node: ESP32-C3 SuperMini. Beacon BLE: tombol ON = helm menyiarkan sinyal, Vest menilai "dekat" dari RSSI.
// Tidak ada sensor sentuh. Pin: PWR_BTN=GPIO4 (tact ke GND, pull-up R1).
// Format advertising: nama "PANDU-HELM", manufacturer data = {0xFF,0xFF,'P','H', 1, counter}  (byte ke-5 selalu 1 = helm menyala; dipertahankan agar cocok dengan Vest)
//
// HEMAT DAYA: library Arduino-ESP32 bawaan dikompilasi tanpa CONFIG_PM_ENABLE, jadi light sleep otomatis
// (dengan BLE) tidak tersedia. Pengganti: duty-cycle deep sleep. Tiap WAKE_PERIOD_S detik bangun,
// siaran BLE singkat (ADV_BURST_MS), lalu deep sleep lagi. State ON/OFF disimpan di memori RTC.
// Tombol (GPIO4) = toggle ON/OFF: bangun dari tidur kapan saja; OFF = tidur tanpa timer (tidak menyiarkan = Vest menilai "tidak terjangkau").
// #define TEST_BEACON
#include <Arduino.h>
#include <NimBLEDevice.h>
#include "esp_sleep.h"
#include "driver/gpio.h"  // <--- TAMBAHKAN INI UNTUK MENGONTROL PIN

constexpr int PIN_PWR   = 4;                       // GPIO0-5 bisa wake deep sleep di C3
constexpr uint32_t WAKE_PERIOD_S = 8;              // KALIBRASI: makin kecil makin responsif, makin boros
constexpr uint32_t ADV_BURST_MS  = 400;            // lama siaran per bangun

RTC_DATA_ATTR bool powered = true;                 // toggle tombol
RTC_DATA_ATTR uint8_t counter = 0;

void setAd(uint8_t c) {
  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();
  uint8_t d[6] = {0xFF, 0xFF, 'P', 'H', 1, c};
  NimBLEAdvertisementData ad, sr;
  ad.setFlags(BLE_HS_ADV_F_DISC_GEN | BLE_HS_ADV_F_BREDR_UNSUP);
  ad.setManufacturerData(std::string((char *)d, sizeof d));
  sr.setName("PANDU-HELM");
  adv->setAdvertisementData(ad);
  adv->setScanResponseData(sr);
}

#ifdef TEST_BEACON
// Mode demo (env supermini_test): siaran BLE TERUS-MENERUS, tanpa deep sleep, serial tetap hidup. Counter naik tiap 1 detik.
// Tombol GPIO4 = toggle ON/OFF siaran (seperti tombol di produk), status dicetak ke serial.
bool beaconOn = true;
void setup() {
  Serial.begin(115200);
  pinMode(PIN_PWR, INPUT_PULLUP);
  NimBLEDevice::init("PANDU-HELM");
  NimBLEDevice::setPower(ESP_PWR_LVL_N0);
  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();
  adv->setMinInterval(160); adv->setMaxInterval(240);   // 100-150 ms
  setAd(0);
  adv->start();
  Serial.println("HELMET demo: beacon ON. Tekan tombol (GPIO4) untuk ON/OFF.");
}
void loop() {
  static uint32_t last = 0; static uint8_t cnt = 0;
  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();
  if (digitalRead(PIN_PWR) == LOW) {
    delay(30);
    if (digitalRead(PIN_PWR) == LOW) {
      beaconOn = !beaconOn;
      if (beaconOn) { setAd(cnt); adv->start(); } else adv->stop();
      Serial.printf("BEACON %s\n", beaconOn ? "ON" : "OFF");
      while (digitalRead(PIN_PWR) == LOW) delay(10);
    }
  }
  if (beaconOn && millis() - last >= 1000) {
    last = millis(); cnt++;
    adv->stop(); setAd(cnt); adv->start();
    Serial.printf("siaran counter=%d\n", cnt);
  }
  delay(20);
}

#else
void sleepNow(bool withTimer) {
  while (digitalRead(PIN_PWR) == LOW) delay(10);   // tunggu tombol dilepas agar tidak langsung bangun
  delay(50);
  
  // KUNCI PERBAIKAN: Paksa internal pull-up tetap menyala & ditahan selama tidur
  gpio_pullup_en((gpio_num_t)PIN_PWR);
  gpio_hold_en((gpio_num_t)PIN_PWR);
  gpio_deep_sleep_hold_en();

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
  setAd(counter++);
  adv->start();
  delay(ADV_BURST_MS);
  adv->stop();
  NimBLEDevice::deinit(true);
}

void setup() {
  Serial.begin(115200);
  
  // Lepas status "hold" (tahan) saat bangun agar pin bisa dibaca normal oleh sistem
  gpio_hold_dis((gpio_num_t)PIN_PWR); 
  pinMode(PIN_PWR, INPUT_PULLUP);

  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_GPIO) {   // tombol ditekan: toggle ON/OFF
    powered = !powered;
    Serial.printf("Tombol: %s\n", powered ? "ON" : "OFF");
  }
  if (!powered) sleepNow(false);                   // OFF: hanya tombol yang membangunkan

  Serial.println("siaran beacon");
  advertiseBurst();
  sleepNow(true);
}

void loop() {}  // tidak pernah tercapai: setup() selalu berakhir di deep sleep
#endif
