// PANDU Edge Gateway: ESP32-DevKitC V4. Terima paket LoRa dari Vest, bunyikan sirine, log ke SD, keluarkan JSON ke serial.
// Pin (PCB3 v2): LORA_CS=IO5, LORA_RST=IO14, LORA_DIO0=IO26, SPI=IO23/19/18, SD_CS=IO13, SIREN_DRV=IO4 (HIGH = sirine ON via IRLZ44N).
// Paket Vest: PANDU,V1,<jenis>,<lat>,<lon>,<mV>,<helm>[,<usia posisi detik>]   jenis: SOS|MOB|FALL|HB   helm: 1 dipakai, 0 tidak, 2 tidak terjangkau
#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>
#include <SD.h>

constexpr int PIN_LORA_CS = 5, PIN_LORA_RST = 14, PIN_LORA_DIO0 = 26, PIN_SD_CS = 13, PIN_SIREN = 4;
constexpr long LORA_FREQ = 915E6;                 // harus sama dengan Vest
constexpr uint32_t SIREN_MAX_MS   = 60000;        // sirine otomatis berhenti jika tidak ada alert baru selama ini (KALIBRASI)
constexpr uint32_t VEST_LOST_MS   = 90000;        // tidak ada paket sama sekali selama ini = peringatan "VEST LOST" (serial saja)
constexpr bool     SIREN_ON_LOST  = false;        // false: jangan bunyikan sirine hanya karena sinyal hilang (rawan alarm palsu)

bool loraOk = false, sdOk = false, sirenOn = false;
uint32_t lastAlertAt = 0, lastRxAt = 0, sirenPhaseAt = 0;
uint32_t rxCount = 0;
bool lostReported = false;

struct Pkt { char type[8]; char lat[16]; char lon[16]; int mv; int helm; int age; int rssi; float snr; };

bool parse(const String &s, Pkt &p) {
  char buf[128];
  s.toCharArray(buf, sizeof buf);
  char *tok[8]; int n = 0;
  for (char *t = strtok(buf, ","); t && n < 8; t = strtok(nullptr, ",")) tok[n++] = t;
  if (n < 7 || strcmp(tok[0], "PANDU") || strcmp(tok[1], "V1")) return false;   // abaikan paket asing/format lain
  strlcpy(p.type, tok[2], sizeof p.type);
  strlcpy(p.lat, tok[3], sizeof p.lat);
  strlcpy(p.lon, tok[4], sizeof p.lon);
  p.mv = atoi(tok[5]);
  p.helm = atoi(tok[6]);
  p.age = n > 7 ? atoi(tok[7]) : 0;               // usia posisi (detik); 0 = baru atau tidak ada
  return true;
}

bool isAlert(const char *t) { return !strcmp(t, "SOS") || !strcmp(t, "MOB") || !strcmp(t, "FALL"); }

// Pola sirine: SOS/MOB = 500 ms ON/500 ms OFF terus; FALL = 200 ms ON/200 ms OFF lebih cepat.
void sirenTick(const char *kind) {
  uint32_t period = !strcmp(kind, "FALL") ? 200 : 500;
  if (millis() - sirenPhaseAt >= period) { sirenPhaseAt = millis(); sirenOn = !sirenOn; digitalWrite(PIN_SIREN, sirenOn); }
}
void sirenOff() { sirenOn = false; digitalWrite(PIN_SIREN, LOW); }

char activeKind[8] = "";

void logSd(const Pkt &p) {
  if (!sdOk) return;
  File f = SD.open("/pandu.csv", FILE_APPEND);
  if (!f) return;
  f.printf("%lu,%s,%s,%s,%d,%d,%d,%d,%.1f\n", millis(), p.type, p.lat, p.lon, p.mv, p.helm, p.age, p.rssi, p.snr);
  f.close();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_SIREN, OUTPUT);
  digitalWrite(PIN_SIREN, LOW);                   // pull-down R3 menjaga LOW saat boot
  // Kedua perangkat SPI memakai bus yang sama: pastikan CS dua-duanya HIGH sebelum init
  pinMode(PIN_LORA_CS, OUTPUT); digitalWrite(PIN_LORA_CS, HIGH);
  pinMode(PIN_SD_CS, OUTPUT);   digitalWrite(PIN_SD_CS, HIGH);

  LoRa.setPins(PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  loraOk = LoRa.begin(LORA_FREQ);
  sdOk = SD.begin(PIN_SD_CS);
  if (sdOk) { File f = SD.open("/pandu.csv", FILE_APPEND); if (f) { if (f.size() == 0) f.println("ms,type,lat,lon,bat_mv,helm,pos_age_s,rssi,snr"); f.close(); } }
  Serial.printf("{\"boot\":true,\"lora\":%d,\"sd\":%d}\n", loraOk, sdOk);
  lastRxAt = millis();
}

void loop() {
  uint32_t now = millis();

  if (loraOk && LoRa.parsePacket()) {
    String s;
    while (LoRa.available()) s += (char)LoRa.read();
    Pkt p; p.rssi = LoRa.packetRssi(); p.snr = LoRa.packetSnr();
    if (parse(s, p)) {
      rxCount++; lastRxAt = now; lostReported = false;
      Serial.printf("{\"type\":\"%s\",\"lat\":\"%s\",\"lon\":\"%s\",\"bat_mv\":%d,\"helm\":%d,\"pos_age_s\":%d,\"rssi\":%d,\"snr\":%.1f}\n",
                    p.type, p.lat, p.lon, p.mv, p.helm, p.age, p.rssi, p.snr);
      logSd(p);
      if (isAlert(p.type)) { lastAlertAt = now; strlcpy(activeKind, p.type, sizeof activeKind) ; }
    } else Serial.printf("{\"ignored\":\"bad_packet\",\"rssi\":%d}\n", p.rssi);
  }

  // Sirine: bunyi selama masih ada alert baru dalam SIREN_MAX_MS
  if (activeKind[0] && now - lastAlertAt < SIREN_MAX_MS) sirenTick(activeKind);
  else if (activeKind[0]) { sirenOff(); activeKind[0] = 0; Serial.println("{\"siren\":\"timeout\"}"); }

  // Perintah serial: 'M' = mute sirine sekarang
  if (Serial.available() && Serial.read() == 'M') { sirenOff(); activeKind[0] = 0; Serial.println("{\"siren\":\"muted\"}"); }

  // Vest hilang sinyal
  if (!lostReported && now - lastRxAt > VEST_LOST_MS) {
    lostReported = true;
    Serial.println("{\"warning\":\"vest_lost\"}");
    if (SIREN_ON_LOST) { strlcpy(activeKind, "SOS", sizeof activeKind); lastAlertAt = now; }
  }
  delay(5);
}
