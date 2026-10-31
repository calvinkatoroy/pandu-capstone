// LoRa probe: "multimeter" untuk Ra-02. SPI bit-bang tanpa library, jadi pin SCK/MOSI/MISO bisa ditukar bebas.
// ESP32 tidak bisa merasakan kabel ke pin pasif; bukti sambungan = modul MEMBALAS RegVersion (0x42) = 0x12.
// Tiap tes dibaca 2x (MISO pull-up lalu pull-down): hasil sama = MISO dikendalikan modul, beda = mengambang.
// Mode SCAN: coba semua 6 susunan SCK/MOSI/MISO di atas IO18/IO19/IO23, lalu lapor susunan yang membuat modul menjawab.
#include <Arduino.h>
constexpr int CS = 5, RST = 25, DIO0 = 26;
constexpr int P[3] = {18, 19, 23};          // kandidat pin SPI (kabel SCK, MOSI, MISO modul ada di salah satunya)

uint8_t rd(uint8_t addr, int sck, int mosi, int miso, int bias) {
  pinMode(CS, OUTPUT); pinMode(sck, OUTPUT); pinMode(mosi, OUTPUT); pinMode(miso, bias);
  digitalWrite(sck, LOW); digitalWrite(CS, LOW); delayMicroseconds(5);
  for (int i = 7; i >= 0; i--) {                      // fase alamat (bit7=0 -> baca)
    digitalWrite(mosi, (addr >> i) & 1); delayMicroseconds(2);
    digitalWrite(sck, HIGH); delayMicroseconds(2); digitalWrite(sck, LOW);
  }
  pinMode(mosi, INPUT);                               // lepas MOSI: hindari tabrakan kalau kabel tertukar
  uint8_t v = 0;
  for (int i = 0; i < 8; i++) {                       // fase data
    delayMicroseconds(2); digitalWrite(sck, HIGH); delayMicroseconds(2);
    v = (v << 1) | digitalRead(miso);
    digitalWrite(sck, LOW);
  }
  digitalWrite(CS, HIGH); pinMode(sck, INPUT); delayMicroseconds(5);
  return v;
}

void setup() {
  Serial.begin(115200); delay(500);
  pinMode(CS, OUTPUT); digitalWrite(CS, HIGH);
  pinMode(RST, OUTPUT);
  Serial.println("\n=== LoRa probe ===  NSS=IO5 RST=IO25 DIO0=IO26, SPI di IO18/19/23");
}

void loop() {
  digitalWrite(RST, LOW); delay(10); digitalWrite(RST, HIGH); delay(20);   // reset modul
  Serial.println("\n--- tes ---");
  pinMode(DIO0, INPUT_PULLUP); delay(2); int d0 = digitalRead(DIO0);
  pinMode(DIO0, INPUT_PULLDOWN); delay(2); int d1 = digitalRead(DIO0);
  Serial.printf("  DIO0 (IO26): pull-up=%d pull-down=%d -> %s\n", d0, d1,
                d0 == d1 ? "dikendalikan modul (ada daya)" : "mengambang (kabel putus / modul mati)");
  int found = 0;
  for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) for (int c = 0; c < 3; c++) {
    if (a == b || b == c || a == c) continue;
    int sck = P[a], mosi = P[b], miso = P[c];
    uint8_t up = rd(0x42, sck, mosi, miso, INPUT_PULLUP), dn = rd(0x42, sck, mosi, miso, INPUT_PULLDOWN);
    Serial.printf("  SCK=IO%d MOSI=IO%d MISO=IO%d: pull-up=0x%02X pull-down=0x%02X%s\n", sck, mosi, miso, up, dn,
                  (up == 0x12 && dn == 0x12) ? "   <<< MODUL MENJAWAB" : "");
    if (up == 0x12 && dn == 0x12) found++;
  }
  Serial.println(found ? "  => Ada susunan yang bekerja. Pasang kabel SESUAI baris <<< itu, atau ubah pin di firmware."
                       : "  => TIDAK ADA susunan yang bekerja: salah satu kabel SCK/MOSI/MISO tidak sampai ke modul (putus / bukan di IO18/19/23).");
  delay(3000);
}
