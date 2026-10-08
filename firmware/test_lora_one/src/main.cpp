// Tes LoRa dengan SATU modul (ESP32 DevKit + modul LoRa + ANTENA). Pin = vest_node.
// Yang dibuktikan: SPI/wiring benar (LoRa.begin lolos = register versi 0x12 terbaca), pemancar menyelesaikan kirim (endPacket=1),
// penerima hidup (RSSI derau latar berubah). Yang TIDAK terbukti: paket benar-benar sampai ke modul lain (butuh modul kedua).
// Wiring: SCK IO18, MISO IO19, MOSI IO23, NSS IO5, RESET IO25, DIO0 IO26, 3.3V, GND. PASANG ANTENA SEBELUM NYALA.
#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>

constexpr int PIN_CS = 5, PIN_RST = 25, PIN_DIO0 = 26;
constexpr long LORA_FREQ = 915E6;

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
  static uint32_t n = 0;
  LoRa.receive();
  delay(100);
  int rx = LoRa.rssi();                       // derau latar saat mendengar
  LoRa.beginPacket(); LoRa.printf("PING %lu", (unsigned long)n);
  uint32_t t0 = millis();
  int ok = LoRa.endPacket();                  // tunggu TxDone
  Serial.printf("#%lu kirim=%s (%lu ms)  derau latar=%d dBm\n", (unsigned long)n++, ok ? "OK" : "GAGAL", (unsigned long)(millis() - t0), rx);
  delay(1900);
}
