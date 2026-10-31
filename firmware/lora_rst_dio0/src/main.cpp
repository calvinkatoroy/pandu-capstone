// Tes kabel RST (IO25) dan DIO0 (IO26) Ra-02. Syarat: SPI sudah benar (lora_probe: MODUL MENJAWAB).
// Wiring: SCK IO18, MOSI IO23, MISO IO19, NSS IO5, RST IO25, DIO0 IO26. Tanpa mengirim sinyal radio (pakai CAD).
#include <Arduino.h>
constexpr int CS = 5, SCK_ = 18, MOSI_ = 23, MISO_ = 19, RST = 25, DIO0 = 26;

uint8_t xfer(uint8_t addr, uint8_t val, bool w) {      // SPI mode 0 bit-bang pelan
  digitalWrite(SCK_, LOW); digitalWrite(CS, LOW); delayMicroseconds(5);
  uint8_t a = w ? (addr | 0x80) : (addr & 0x7F), v = 0;
  for (int i = 7; i >= 0; i--) {
    digitalWrite(MOSI_, (a >> i) & 1); delayMicroseconds(2);
    digitalWrite(SCK_, HIGH); delayMicroseconds(2); digitalWrite(SCK_, LOW);
  }
  for (int i = 7; i >= 0; i--) {
    if (w) digitalWrite(MOSI_, (val >> i) & 1);
    delayMicroseconds(2); digitalWrite(SCK_, HIGH); delayMicroseconds(2);
    v = (v << 1) | digitalRead(MISO_);
    digitalWrite(SCK_, LOW);
  }
  digitalWrite(CS, HIGH); delayMicroseconds(5);
  return v;
}
uint8_t rd(uint8_t a) { return xfer(a, 0, false); }
void wr(uint8_t a, uint8_t v) { xfer(a, v, true); }
void reset() { digitalWrite(RST, LOW); delay(10); digitalWrite(RST, HIGH); delay(20); }

void setup() {
  Serial.begin(115200); delay(500);
  pinMode(CS, OUTPUT); digitalWrite(CS, HIGH);
  pinMode(SCK_, OUTPUT); pinMode(MOSI_, OUTPUT); pinMode(MISO_, INPUT);
  pinMode(RST, OUTPUT); digitalWrite(RST, HIGH);
  pinMode(DIO0, INPUT_PULLDOWN);
  Serial.println("\n=== Tes RST + DIO0 ===");
}

void loop() {
  Serial.println("\n--- tes ---");
  reset();
  if (rd(0x42) != 0x12) { Serial.printf("  SPI belum jalan (versi=0x%02X). Jalankan lora_probe dulu.\n", rd(0x42)); delay(3000); return; }
  Serial.println("  SPI OK (versi 0x12)");

  // Tes RST: tulis RegFrfMsb (0x06, default 0x6C) = 0x70, lalu reset. Kalau kembali 0x6C, pin RST bekerja.
  wr(0x06, 0x70); uint8_t b4 = rd(0x06);
  digitalWrite(RST, LOW); delay(10); digitalWrite(RST, HIGH); delay(20);
  uint8_t af = rd(0x06);
  Serial.printf("  RST : tulis=0x70 baca=0x%02X, setelah reset=0x%02X -> %s\n", b4, af,
                b4 != 0x70 ? "register tidak bisa ditulis (cek MOSI/SCK)" :
                af == 0x6C ? "RST BEKERJA" : "RST TIDAK sampai ke modul (kabel IO25 putus / salah pin RST)");

  // Tes DIO0: mulai CAD (deteksi aktivitas kanal). Selesai -> flag CadDone (0x04) & DIO0 naik.
  wr(0x01, 0x80); wr(0x01, 0x81);                      // sleep LoRa -> standby LoRa
  wr(0x40, 0x80);                                      // DIO0 = CadDone
  wr(0x12, 0xFF);                                      // hapus flag
  int low0 = digitalRead(DIO0);
  wr(0x01, 0x87);                                      // CAD
  uint32_t t = millis(); while (!digitalRead(DIO0) && millis() - t < 500) delay(1);
  int hi = digitalRead(DIO0); uint8_t fl = rd(0x12);
  wr(0x12, 0xFF); delay(5); int low1 = digitalRead(DIO0);
  wr(0x01, 0x80);
  Serial.printf("  DIO0: sebelum=%d, setelah CAD=%d, flag=0x%02X, setelah hapus flag=%d -> %s\n", low0, hi, fl, low1,
                (hi && !low0 && !low1) ? "DIO0 BEKERJA" :
                (!hi && (fl & 0x04))   ? "modul selesai CAD tapi IO26 tetap LOW: kabel DIO0 tidak sampai / salah pin" :
                !(fl & 0x04)           ? "CAD tidak jalan (modul tidak masuk mode LoRa)" : "hasil tidak jelas");
  delay(3000);
}
