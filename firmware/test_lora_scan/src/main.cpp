// Cari tukar-tempat kabel LoRa otomatis. SPI dibuat lewat kode (bit-bang) pada empat pin IO5, IO18, IO19, IO23,
// dan dicoba semua 24 kemungkinan peran (NSS, SCK, MOSI, MISO). Pin yang menghasilkan RegVersion = 0x12 memberi tahu
// kabel mana yang sebenarnya ke pin modul mana. RST: IO14 dan IO25 dipulsa bersamaan (yang tidak tersambung tidak berpengaruh).
// Wiring seperti biasa. Sketsa tidak memancar. Hasil ditulis ke serial tiap ~6 detik.
#include <Arduino.h>
#include <algorithm>

const int PINS4[4] = {5, 18, 19, 23};
const char *ROLE[4] = {"NSS", "SCK", "MOSI", "MISO"};
constexpr int RST_A = 14, RST_B = 25;

uint8_t xfer(int sck, int mosi, int miso, uint8_t out) {
  uint8_t in = 0;
  for (int b = 7; b >= 0; b--) {
    digitalWrite(mosi, (out >> b) & 1);
    delayMicroseconds(5);
    digitalWrite(sck, HIGH);
    delayMicroseconds(5);
    in = (in << 1) | digitalRead(miso);
    digitalWrite(sck, LOW);
  }
  return in;
}

uint8_t readReg(int nss, int sck, int mosi, int miso, uint8_t addr) {
  digitalWrite(nss, LOW); delayMicroseconds(5);
  xfer(sck, mosi, miso, addr & 0x7F);
  uint8_t v = xfer(sck, mosi, miso, 0x00);
  digitalWrite(nss, HIGH);
  return v;
}

void resetModule() {
  pinMode(RST_A, OUTPUT); pinMode(RST_B, OUTPUT);
  digitalWrite(RST_A, LOW); digitalWrite(RST_B, LOW); delay(10);
  digitalWrite(RST_A, HIGH); digitalWrite(RST_B, HIGH); delay(20);
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== Cari tukar-tempat kabel LoRa ===");
  Serial.println("Mencoba 24 kemungkinan peran untuk pin IO5, IO18, IO19, IO23...\n");
}

void loop() {
  int perm[4] = {0, 1, 2, 3};   // perm[i] = indeks peran untuk PINS4[i]
  int found = 0, interesting = 0;
  // generate semua permutasi lewat next_permutation sederhana (std::next_permutation tersedia di toolchain)
  do {
    int pinOf[4];   // pin untuk tiap peran
    for (int i = 0; i < 4; i++) pinOf[perm[i]] = PINS4[i];
    int nss = pinOf[0], sck = pinOf[1], mosi = pinOf[2], miso = pinOf[3];
    pinMode(nss, OUTPUT);  digitalWrite(nss, HIGH);
    pinMode(sck, OUTPUT);  digitalWrite(sck, LOW);
    pinMode(mosi, OUTPUT); digitalWrite(mosi, LOW);
    pinMode(miso, INPUT);
    resetModule();
    uint8_t v = readReg(nss, sck, mosi, miso, 0x42);
    if (v == 0x12) {
      found++;
      Serial.printf("*** COCOK: NSS=IO%d  SCK=IO%d  MOSI=IO%d  MISO=IO%d  (RegVersion=0x12)\n", nss, sck, mosi, miso);
    } else if (v != 0x00 && v != 0xFF) {
      interesting++;
      Serial.printf("  (aneh) NSS=IO%d SCK=IO%d MOSI=IO%d MISO=IO%d -> 0x%02X\n", nss, sck, mosi, miso, v);
    }
  } while (std::next_permutation(perm, perm + 4));

  if (!found) {
    Serial.println("Tidak ada kombinasi yang menghasilkan 0x12.");
    Serial.println("-> Bukan sekadar kabel tertukar. Penyebab tersisa: modul tidak dapat 3,3 V cukup, RST tertahan, kabel longgar, atau modul rusak.");
    Serial.println("-> Coba modul kedua. Kalau sama, kirim hasil ini.");
  } else {
    Serial.println("-> Pindahkan kabel di papan sesuai baris COCOK (atau ubah pin di firmware).");
  }
  Serial.println();
  delay(3000);
}
