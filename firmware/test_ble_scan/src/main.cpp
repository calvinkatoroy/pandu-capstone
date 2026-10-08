// Tes mandiri scanner BLE (ESP32 DevKit saja): cari beacon Helmet "PANDU-HELM", cetak worn, counter, RSSI. Logika callback SAMA dengan vest_node.
// Paket: manufacturer data {FF FF 'P' 'H' worn counter}. Helmet mode tes (supermini_test) menyiarkan terus; mode normal hanya 400 ms tiap 8 s.
// Tiap paket yang cocok dicetak; tiap 2 detik ringkasan status helm (1 dipakai, 0 tidak, 2 tidak terjangkau > HELM_TIMEOUT_MS).
#include <Arduino.h>
#include <NimBLEDevice.h>

constexpr uint32_t HELM_TIMEOUT_MS = 30000;
constexpr int HELM_RSSI_MIN = -85;   // KALIBRASI: lebih lemah dari ini = helm jauh = tidak dipakai (sama dengan vest_node)
volatile float rssiAvg = -127;
volatile uint32_t seenAt = 0; volatile uint8_t worn = 0, counter = 0; volatile int rssi = 0; volatile uint32_t pktCount = 0;
volatile bool newPkt = false;

class Cb : public NimBLEAdvertisedDeviceCallbacks {
  void onResult(NimBLEAdvertisedDevice *d) override {
    if (!d->haveManufacturerData()) return;
    std::string m = d->getManufacturerData();
    if (m.size() >= 6 && (uint8_t)m[0] == 0xFF && (uint8_t)m[1] == 0xFF && m[2] == 'P' && m[3] == 'H') {
      worn = (uint8_t)m[4] ? 1 : 0; counter = (uint8_t)m[5]; rssi = d->getRSSI();
      rssiAvg = seenAt ? rssiAvg * 0.8f + rssi * 0.2f : rssi;
      seenAt = millis() ? millis() : 1; pktCount++; newPkt = true;
    }
  }
};
Cb cb;

void setup() {
  Serial.begin(115200);
  NimBLEDevice::init("");
  NimBLEScan *scan = NimBLEDevice::getScan();
  scan->setAdvertisedDeviceCallbacks(&cb, true);
  scan->setActiveScan(false);
  scan->setInterval(100); scan->setWindow(99);   // hampir selalu mendengar, untuk tes
  scan->setDuplicateFilter(false);
  scan->start(0, nullptr, false);
  Serial.println("Scan BLE jalan. Mencari PANDU-HELM (FF FF 50 48 worn counter)...");
}

void loop() {
  static uint32_t lastPrint = 0, lastPkt = 0;
  if (newPkt) {  // cetak paket baru, tapi paling cepat 4x per detik supaya tidak banjir
    newPkt = false;
    if (millis() - lastPkt >= 250) { lastPkt = millis(); Serial.printf("  paket: worn=%d counter=%3d rssi=%d dBm\n", worn, counter, rssi); }
  }
  if (millis() - lastPrint >= 2000) {
    lastPrint = millis();
    uint32_t age = seenAt ? millis() - seenAt : 0;
    int st = (!seenAt || age > HELM_TIMEOUT_MS) ? 2 : (worn && rssiAvg >= HELM_RSSI_MIN);
    Serial.printf("[%lus] rssi_avg=%d dBm  helm=%d (%s)  terakhir terdengar %s%lu s lalu  total paket=%lu\n", (unsigned long)(millis() / 1000), (int)rssiAvg, st,
                  st == 1 ? "DIPAKAI" : st == 0 ? (worn ? "worn=1 tapi JAUH -> tidak dipakai" : "tidak dipakai") : "tidak terjangkau", seenAt ? "" : "(belum pernah) ", (unsigned long)(age / 1000), (unsigned long)pktCount);
  }
  delay(20);
}
