// Tes mandiri sensor air / MOB (ESP32 DevKit saja). Sinyal di IO34 (input-only, tanpa pull internal).
// Logika SAMA dengan vest_node: sinyal HIGH terus-menerus >= WATER_MS (3 s) = MOB; lebih singkat = percikan, diabaikan.
// Wiring uji TANPA sensor: jumper IO34 -> 3V3 (= basah), lepas (= kering), resistor 10k IO34 -> GND.
// Wiring sensor murah: VCC -> 3V3 (JANGAN 5 V), GND -> GND, S/OUT -> IO34 (+ 10k ke GND).
// Sambil jalan, cetak tegangan analog (mV) supaya kelihatan apakah sensor memberi HIGH/LOW bersih atau analog.
#include <Arduino.h>

constexpr int PIN_WATER = 34, PIN_LED = 2;
constexpr uint32_t WATER_MS = 3000;
constexpr int WATER_WET_MV = 1000;  // KALIBRASI: kering 140-230 mV, basah 1700-2070 mV (sensor murah, analog)

void setup() {
  Serial.begin(115200);
  pinMode(PIN_WATER, INPUT);
  pinMode(PIN_LED, OUTPUT);
  analogSetPinAttenuation(PIN_WATER, ADC_11db);
  Serial.println("Siap. Basahi sensor (atau jumper IO34 ke 3V3) selama 3 detik.");
}

void loop() {
  static uint32_t since = 0, lastPrint = 0;
  static bool fired = false;
  bool wet = analogReadMilliVolts(PIN_WATER) > WATER_WET_MV;
  uint32_t now = millis();

  if (wet && !since) { since = now; lastPrint = now; Serial.printf("BASAH mulai (%d mV)\n", analogReadMilliVolts(PIN_WATER)); }
  if (wet) {
    uint32_t t = now - since;
    if (!fired && now - lastPrint >= 500) { lastPrint = now; Serial.printf("basah %.1f / %.1f s (%d mV)\n", t / 1000.0, WATER_MS / 1000.0, analogReadMilliVolts(PIN_WATER)); }
    if (!fired && t >= WATER_MS) { fired = true; Serial.println("\n*** MOB TERPICU (basah 3 detik) ***  paket akan dikirim\n"); digitalWrite(PIN_LED, HIGH); }
  } else {
    if (since) {
      if (!fired) Serial.printf("percikan %lu ms: diabaikan\n", (unsigned long)(now - since));
      else Serial.println("kering lagi, MOB selesai");
      since = 0; fired = false; digitalWrite(PIN_LED, LOW);
    }
    if (now - lastPrint >= 2000) { lastPrint = now; Serial.printf("kering (%d mV)\n", analogReadMilliVolts(PIN_WATER)); }
  }
  delay(20);
}
