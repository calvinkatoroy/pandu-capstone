// Tes LoRa (ESP32 DevKit + Ra-02 + ANTENA). Pin = vest_node. Satu modul: wiring/SPI saja (LoRa.begin OK, TX selesai).
// Dua modul (flash sketch ini ke kedua ESP32): baris "RX ..." dengan RSSI/SNR membuktikan paket sampai ke modul lain.
// Wiring: SCK IO18, MISO IO19, MOSI IO23, NSS IO5, RESET IO25, DIO0 IO26, 3.3V, GND. PASANG ANTENA SEBELUM NYALA.
#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>

constexpr int PIN_CS = 5, PIN_RST = 25, PIN_DIO0 = 26;
constexpr long LORA_FREQ = 433E6;   // Ra-02 SX1278 433 MHz

void setup() {
  Serial.begin(115200);
  delay(300);
  LoRa.setPins(PIN_CS, PIN_RST, PIN_DIO0);
  if (!LoRa.begin(LORA_FREQ)) {
    Serial.println("LoRa.begin GAGAL: cek 3.3V, GND, SCK/MISO/MOSI/NSS/RESET, dan label pin modul (bukan RA-02?)");
    while (true) delay(1000);
  }
  Serial.println("LoRa.begin OK (modul terdeteksi, SPI benar)");
}

void loop() {
  // Dua modul: flash sketch yang sama ke kedua ESP32. Tiap node kirim PING berjeda acak dan mendengar di sela-selanya,
  // sehingga "RX dari ..." di serial salah satu node membuktikan paket benar-benar sampai ke modul lain (RSSI/SNR nyata).
  static uint32_t n = 0;
  static const uint32_t id = (uint32_t)(ESP.getEfuseMac() & 0xFFFF);
  LoRa.receive();
  uint32_t until = millis() + 1500 + (esp_random() % 1000);
  while (millis() < until) {
    int len = LoRa.parsePacket();
    if (len > 0) {
      String msg;
      while (LoRa.available()) msg += (char)LoRa.read();
      Serial.printf("RX \"%s\"  rssi=%d dBm  snr=%.1f dB\n", msg.c_str(), LoRa.packetRssi(), LoRa.packetSnr());
    }
    delay(5);
  }
  LoRa.beginPacket(); LoRa.printf("PING %04X #%lu", (unsigned)id, (unsigned long)n);
  uint32_t t0 = millis();
  int ok = LoRa.endPacket();                  // tunggu TxDone
  Serial.printf("TX #%lu kirim=%s (%lu ms)\n", (unsigned long)n++, ok ? "OK" : "GAGAL", (unsigned long)(millis() - t0));
}
