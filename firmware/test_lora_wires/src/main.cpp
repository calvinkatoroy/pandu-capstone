// Uji kabel LoRa TANPA multimeter: ESP32 mengedipkan SATU pin terus-menerus sampai kamu memilih pin lain lewat serial monitor.
// LED + resistor 330 ohm di ujung modul menunjukkan apakah kabel itu benar-benar sampai ke pin modul.
// Cara: LED kaki panjang (+) -> resistor 330 ohm -> pin breakout yang diuji; kaki pendek (-) -> GND breakout.
// Pilih pin: ketik angka 1-7 di serial monitor lalu Enter. 0 = berhenti. Sketsa ini tidak memancar (pasang antena tetap disarankan).
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
int sel = 1;   // pin yang sedang berkedip (1-based), 0 = diam

void menu() {
  Serial.println("\nKetik angka lalu Enter untuk memilih pin yang berkedip:");
  for (int i = 0; i < N; i++) Serial.printf("  %d = %s  -> LED di pin modul '%s'\n", i + 1, PINS[i].name, PINS[i].modulePin);
  Serial.println("  0 = berhenti\n");
}

void select(int s) {
  for (int j = 0; j < N; j++) pinMode(PINS[j].gpio, INPUT);   // semua pin dilepas
  pinMode(5, OUTPUT); digitalWrite(5, HIGH);                  // NSS dijaga HIGH agar modul tidak menggerakkan MISO
  sel = s;
  if (s >= 1 && s <= N) { pinMode(PINS[s - 1].gpio, OUTPUT); Serial.printf("BERKEDIP: %s -> pasang LED di pin modul '%s'\n", PINS[s - 1].name, PINS[s - 1].modulePin); }
  else Serial.println("Berhenti.");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== Uji kabel LoRa (LED) ===");
  Serial.println("LED(+) -> 330 ohm -> pin modul; LED(-) -> GND modul. LED harus berkedip. Tidak berkedip = kabel itu tidak sampai.");
  menu();
  select(1);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c >= '0' && c <= '0' + N) select(c - '0');
  }
  if (sel >= 1 && sel <= N) {
    static uint32_t t = 0; static bool lvl = false;
    if (millis() - t >= 400) { t = millis(); lvl = !lvl; digitalWrite(PINS[sel - 1].gpio, lvl); }
  }
}
