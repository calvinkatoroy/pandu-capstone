// Diagnostik modul LoRa Ra-02 (SX1278) tanpa library: baca register chip lewat SPI dan jelaskan hasilnya.
// Wiring (sama dengan Gateway): NSS=IO5, SCK=IO18, MISO=IO19, MOSI=IO23, RST=IO14 (Vest: IO25), 3V3, GND. PASANG ANTENA (tidak ada transmit di sketsa ini).
// Lulus: RegVersion = 0x12. Sketsa mencoba RST IO14 dan IO25 bergantian supaya cocok untuk Gateway maupun Vest.
#include <Arduino.h>
#include <SPI.h>

constexpr int PIN_NSS = 5, PIN_SCK = 18, PIN_MISO = 19, PIN_MOSI = 23;
const int RST_CANDIDATES[] = {14, 25};

uint8_t readReg(uint8_t addr) {
  digitalWrite(PIN_NSS, LOW);
  SPI.transfer(addr & 0x7F);
  uint8_t v = SPI.transfer(0x00);
  digitalWrite(PIN_NSS, HIGH);
  return v;
}

// MISO saat NSS HIGH seharusnya hi-Z (mengambang): ikut pull-up/pull-down. Bila tetap, ada yang menahannya.
void misoFloatTest() {
  pinMode(PIN_MISO, INPUT_PULLUP);   delay(5); int up = digitalRead(PIN_MISO);
  pinMode(PIN_MISO, INPUT_PULLDOWN); delay(5); int down = digitalRead(PIN_MISO);
  pinMode(PIN_MISO, INPUT);
  Serial.printf("  MISO diam (NSS HIGH): pull-up->%d pull-down->%d  %s\n", up, down,
                (up == 1 && down == 0) ? "(mengambang: wajar bila modul hi-Z ATAU kabel MISO tidak tersambung)" : "(ditahan tetap: ada yang menggerakkan MISO)");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  pinMode(PIN_NSS, OUTPUT); digitalWrite(PIN_NSS, HIGH);
  SPI.begin(PIN_SCK, PIN_MISO, PIN_MOSI, PIN_NSS);
  SPI.setFrequency(1000000);   // lambat, toleran terhadap kabel jumper panjang
  Serial.println("\n=== Diagnostik LoRa Ra-02 ===");
}

void loop() {
  bool anyOk = false;
  for (int rst : RST_CANDIDATES) {
    pinMode(rst, OUTPUT);
    digitalWrite(rst, LOW);  delay(10);
    digitalWrite(rst, HIGH); delay(20);
    uint8_t ver = readReg(0x42), opmode = readReg(0x01), f0 = readReg(0x06), f1 = readReg(0x07), f2 = readReg(0x08);
    Serial.printf("RST=IO%d  RegVersion=0x%02X  OpMode=0x%02X  Frf=%02X%02X%02X\n", rst, ver, opmode, f0, f1, f2);
    if (ver == 0x12) { anyOk = true; Serial.println("  -> OK: SX127x terdeteksi. Setelah reset Frf normal = 6C8000 dan OpMode 09."); }
    else if (ver == 0xFF) Serial.println("  -> 0xFF: MISO terbaca HIGH terus. Modul tidak menjawab: 3V3/GND modul tidak ada, NSS salah, atau MISO tidak tersambung (mengambang ke HIGH).");
    else if (ver == 0x00) Serial.println("  -> 0x00: MISO terbaca LOW terus. SCK/MOSI tidak sampai, MISO tertahan ke GND, atau modul tidak diberi 3V3.");
    else Serial.println("  -> Nilai aneh: kabel longgar/berderau, atau ini bukan chip SX127x. Cek urutan pin breakout.");
    pinMode(rst, INPUT);   // lepaskan RST agar pin RST yang salah tidak menahan modul
  }
  misoFloatTest();
  if (!anyOk) Serial.println("  Cek: (1) 3V3 modul terukur ~3,3 V dengan multimeter, (2) NSS->IO5, SCK->IO18, MISO->IO19, MOSI->IO23, (3) MISO/MOSI tidak tertukar, (4) urutan pin breakout vs foto produk.");
  Serial.println();
  delay(3000);
}
