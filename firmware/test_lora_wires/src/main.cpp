// Uji kabel LoRa TANPA multimeter: ESP32 mengedipkan satu pin pada satu waktu; LED + resistor 330 ohm di ujung modul
// menunjukkan apakah kabel itu benar-benar sampai ke pin modul.
// Cara: LED kaki panjang (+) -> resistor 330 ohm -> pin breakout yang sedang diuji; kaki pendek (-) -> GND breakout.
// Pasang antena. Sketsa ini tidak memancar. Pin yang diuji berganti tiap 6 detik; lihat nama di serial monitor.
#include <Arduino.h>

struct P { int gpio; const char *name; const char *modulePin; };
const P PINS[] = {
  {5,  "IO5  (NSS)",  "NSS"},
  {18, "IO18 (SCK)",  "SCK"},
  {23, "IO23 (MOSI)", "MOSI"},
  {19, "IO19 (MISO)", "MISO"},
  {14, "IO14 (RST Gateway)", "RST"},
  {25, "IO25 (RST Vest)",    "RST"},
  {26, "IO26 (DIO0)", "DIO0"},
};
constexpr int N = sizeof(PINS) / sizeof(PINS[0]);

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== Uji kabel LoRa (LED) ===");
  Serial.println("LED(+) -> 330 ohm -> pin modul yang disebut; LED(-) -> GND modul. LED harus berkedip.");
  Serial.println("Tidak berkedip = kabel dari pin ESP itu tidak sampai ke pin modul (atau salah pin/baris).\n");
}

void loop() {
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) pinMode(PINS[j].gpio, INPUT);   // pin lain dilepas
    pinMode(5, OUTPUT); digitalWrite(5, HIGH);                  // NSS dijaga HIGH agar modul tidak menggerakkan MISO
    Serial.printf("SEKARANG: %s -> pasang LED di pin modul '%s'\n", PINS[i].name, PINS[i].modulePin);
    pinMode(PINS[i].gpio, OUTPUT);
    for (int k = 0; k < 12; k++) { digitalWrite(PINS[i].gpio, k & 1); delay(250); }   // kedip 2 Hz selama 3 detik, lalu jeda
    digitalWrite(PINS[i].gpio, LOW);
    delay(3000);
  }
  Serial.println("--- ulang dari awal ---\n");
}
