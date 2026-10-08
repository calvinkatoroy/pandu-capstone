// Tes mandiri GPS NEO-6M (ESP32 DevKit saja). Pin dan parser SAMA dengan vest_node.
// Wiring: GPS VCC -> 3V3, GND -> GND, GPS TX -> IO16, GPS RX -> IO17. Antena keramik menghadap langit.
// Tiap 2 detik cetak tabel per satelit (dari kalimat $GPGSV dan $GPGSA) + status fix. Ketik r di monitor = tampilkan NMEA mentah.
#include <Arduino.h>
#include <TinyGPSPlus.h>

constexpr int PIN_GPS_RX = 16, PIN_GPS_TX = 17;
TinyGPSPlus gps;
HardwareSerial gpsSerial(2);
bool raw = false;

struct Sat { int prn, elev, az, snr; };  // -1 = kosong
Sat sats[24]; int nSats = 0;
int usedPrn[12], nUsed = 0, fixMode = 1;  // 1 = tanpa fix, 2 = 2D, 3 = 3D
char line[120]; int len = 0;

int fld(const char *s) { return *s ? atoi(s) : -1; }

bool checksumOk(const char *l) {  // XOR karakter antara $ dan * harus sama dengan 2 digit hex setelah *
  if (*l != '$') return false;
  uint8_t x = 0; const char *p = l + 1;
  while (*p && *p != '*') x ^= (uint8_t)*p++;
  return *p == '*' && strtol(p + 1, nullptr, 16) == x;
}

void parseLine(char *l) {
  if (!checksumOk(l)) return;                             // abaikan kalimat rusak
  char *f[24]; int n = 0; f[n++] = l;
  for (char *p = l; *p && n < 24; p++) if (*p == ',') { *p = 0; f[n++] = p + 1; }
  for (char *p = f[n - 1]; *p; p++) if (*p == '*') { *p = 0; break; }
  if (!strcmp(f[0], "$GPGSV") && n >= 4) {
    if (atoi(f[2]) == 1) nSats = 0;                       // pesan pertama = daftar baru
    for (int i = 4; i + 3 < n && nSats < 24; i += 4)
      if (*f[i]) sats[nSats++] = {atoi(f[i]), fld(f[i + 1]), fld(f[i + 2]), fld(f[i + 3])};
  } else if (!strcmp(f[0], "$GPGSA") && n >= 15) {
    fixMode = atoi(f[2]); nUsed = 0;
    for (int i = 3; i < 15; i++) if (*f[i]) usedPrn[nUsed++] = atoi(f[i]);
  }
}

bool isUsed(int prn) { for (int i = 0; i < nUsed; i++) if (usedPrn[i] == prn) return true; return false; }

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, PIN_GPS_RX, PIN_GPS_TX);
  Serial.println("Siap. Bawa GPS ke luar ruangan, tunggu fix. Ketik r = NMEA mentah.");
}

void loop() {
  static uint32_t lastPrint = 0;
  while (Serial.available()) if (Serial.read() == 'r') raw = !raw;
  while (gpsSerial.available()) {
    char c = gpsSerial.read(); gps.encode(c);
    if (raw) Serial.write(c);
    if (c == '\n') { line[len] = 0; parseLine(line); len = 0; }
    else if (c != '\r' && len < (int)sizeof line - 1) line[len++] = c;
  }
  uint32_t now = millis();
  if (raw || now - lastPrint < 2000) return;
  lastPrint = now;

  if (gps.charsProcessed() < 10) { Serial.println("TIDAK ADA DATA dari GPS: cek wiring (GPS TX -> IO16, GPS RX -> IO17, VCC 3V3, GND)"); return; }
  bool fix = gps.location.isValid() && gps.location.age() < 3000;
  Serial.printf("\n[%lus] fix=%s (mode %s)  terlihat=%d  dipakai=%d  hdop=%.1f  checksum gagal=%lu\n", (unsigned long)(now / 1000),
                fix ? "YA" : "tidak", fixMode == 3 ? "3D" : fixMode == 2 ? "2D" : "tanpa fix", nSats, nUsed, gps.hdop.hdop(), (unsigned long)gps.failedChecksum());
  if (fix) Serial.printf("  lat=%.6f lon=%.6f\n", gps.location.lat(), gps.location.lng());
  for (int i = 0; i < nSats; i++) {
    Sat &s = sats[i];
    char e[8], a[8], bar[16] = "";
    if (s.elev < 0) strcpy(e, " --"); else snprintf(e, sizeof e, "%3d", s.elev);
    if (s.az < 0) strcpy(a, " --"); else snprintf(a, sizeof a, "%3d", s.az);
    for (int k = 0; k < s.snr / 5 && k < 12; k++) strcat(bar, "#");
    if (s.snr < 0) Serial.printf("  PRN %2d  elev %s  az %s  SNR  -- (tidak terdengar)\n", s.prn, e, a);
    else Serial.printf("  PRN %2d  elev %s  az %s  SNR %2d dB-Hz %-12s %s\n", s.prn, e, a, s.snr, bar, isUsed(s.prn) ? "<- DIPAKAI" : "");
  }
}
