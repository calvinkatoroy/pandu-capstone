// PANDU Edge Gateway: ESP32-DevKitC V4. Terima paket LoRa dari Vest, bunyikan sirine, log ke SD, keluarkan JSON ke serial,
// dan unggah ke dashboard (HTTPS POST ke Edge Function ingest) dengan antrean microSD (store-and-forward).
// Pin (PCB3 v3): LORA_CS=IO5, LORA_RST=IO14, LORA_DIO0=IO26, SPI LoRa=IO23/19/18, SD: SCK=IO25 MISO=IO35 MOSI=IO32 CS=IO33, SIREN_DRV=IO4 (HIGH = sirine ON via IRLZ44N).
// Paket Vest v2: PANDU,V2,<vest_id>,<seq>,<jenis>,<lat>,<lon>,<mV>,<helm>,<usia posisi detik>   (v1 tanpa vest_id/seq tetap diterima)
//   jenis: HB|SOS|FALL|MOB|OFF   helm: 1 dipakai, 0 tidak, 2 tidak terjangkau.   Kontrak: pandu-dashboard/docs/DATA_CONTRACT.md
// Arsitektur: loop() hanya LoRa + sirine (tidak boleh terblok). Task netTask() satu-satunya pengguna SD dan jaringan.
#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>
#include <SD.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <time.h>
#include <deque>
#if __has_include("config.h")
#include "config.h"
#endif

constexpr int PIN_LORA_CS = 5, PIN_LORA_RST = 14, PIN_LORA_DIO0 = 26, PIN_SIREN = 4;
constexpr int PIN_SD_CS = 33, PIN_SD_SCK = 25, PIN_SD_MISO = 35, PIN_SD_MOSI = 32;   // SD di bus SPI sendiri (PCB3 v3), terpisah dari LoRa
SPIClass sdSpi(HSPI);
constexpr long LORA_FREQ = 433E6;                 // Ra-02 SX1278, harus sama dengan Vest
constexpr uint32_t SIREN_MAX_MS   = 60000;        // sirine otomatis berhenti jika tidak ada alert baru selama ini (KALIBRASI)
constexpr uint32_t VEST_LOST_MS   = 90000;        // tidak ada paket sama sekali selama ini = peringatan "VEST LOST" (serial saja)
constexpr bool     SIREN_ON_LOST  = false;        // false: jangan bunyikan sirine hanya karena sinyal hilang (rawan alarm palsu)
constexpr uint32_t DUP_WINDOW_MS  = 60000;        // paket ulang (vest_id, seq) sama dalam jendela ini = duplikat radio, tidak diunggah ulang
constexpr int      UPLOAD_BATCH   = 20;           // maks event per POST (server menerima <= 100)
constexpr uint32_t RETRY_MS       = 30000;        // jeda setelah unggah gagal
constexpr size_t   RAM_QUEUE_MAX  = 64;           // antrean cadangan di RAM bila SD tidak ada (hilang saat mati)
const char *QFILE = "/queue.jsonl", *QOFF = "/queue.off", *CSVFILE = "/pandu_v2.csv";

#ifdef WIFI_SSID
constexpr bool NET_ENABLED = true;
#else
constexpr bool NET_ENABLED = false;
#define WIFI_SSID ""
#define WIFI_PASS ""
#define GATEWAY_ID "GW1"
#define INGEST_URL ""
#define DEVICE_KEY ""
#endif

bool loraOk = false, sdOk = false, sirenOn = false;
uint32_t lastAlertAt = 0, lastRxAt = 0, sirenPhaseAt = 0, rxCount = 0;
bool lostReported = false;
uint32_t bootId;                                   // membedakan millis() antar boot pada antrean SD
int v1Seq = 0;                                     // seq buatan untuk paket v1

struct Pkt { uint8_t vest; int seq; char type[8]; char lat[16]; char lon[16]; int mv, helm, age, rssi; float snr; };
struct Ev { Pkt p; time_t epoch; uint32_t ms; };  // epoch = 0 bila jam belum tersinkron saat paket diterima
QueueHandle_t evQ;                                 // loop() -> netTask()

bool validType(const char *t) { return !strcmp(t, "HB") || !strcmp(t, "SOS") || !strcmp(t, "FALL") || !strcmp(t, "MOB") || !strcmp(t, "OFF"); }
bool isAlert(const char *t) { return !strcmp(t, "SOS") || !strcmp(t, "MOB") || !strcmp(t, "FALL"); }

bool parse(const String &s, Pkt &p) {
  char buf[160];
  s.toCharArray(buf, sizeof buf);
  char *tok[12]; int n = 0;
  for (char *t = strtok(buf, ","); t && n < 12; t = strtok(nullptr, ",")) tok[n++] = t;
  if (n < 7 || strcmp(tok[0], "PANDU")) return false;   // abaikan paket asing
  int i;
  if (!strcmp(tok[1], "V2")) { p.vest = atoi(tok[2]); p.seq = atoi(tok[3]); i = 4; }
  else if (!strcmp(tok[1], "V1")) { p.vest = 1; p.seq = -1; i = 2; }
  else return false;
  if (n < i + 5 || p.vest < 1 || p.vest > 8 || !validType(tok[i])) return false;
  strlcpy(p.type, tok[i], sizeof p.type);
  strlcpy(p.lat, tok[i + 1], sizeof p.lat);
  strlcpy(p.lon, tok[i + 2], sizeof p.lon);
  p.mv = atoi(tok[i + 3]);
  p.helm = atoi(tok[i + 4]);
  p.age = n > i + 5 ? atoi(tok[i + 5]) : 0;       // usia posisi (detik); 0 = baru atau tidak ada
  return true;
}

// ---- Sirine ----
// Pola: SOS/MOB = 500 ms ON/500 ms OFF terus; FALL = 200 ms ON/200 ms OFF lebih cepat.
void sirenTick(const char *kind) {
  uint32_t period = !strcmp(kind, "FALL") ? 200 : 500;
  if (millis() - sirenPhaseAt >= period) { sirenPhaseAt = millis(); sirenOn = !sirenOn; digitalWrite(PIN_SIREN, sirenOn); }
}
void sirenOff() { sirenOn = false; digitalWrite(PIN_SIREN, LOW); }
char activeKind[8] = "";

// ---- Waktu ----
bool timeSynced() { return time(nullptr) > 1700000000; }
void iso(time_t t, char *out, size_t n) { struct tm g; gmtime_r(&t, &g); strftime(out, n, "%Y-%m-%dT%H:%M:%SZ", &g); }

// ---- Antrean store-and-forward (hanya dipakai netTask) ----
// Satu baris per event: "<tersinkron 0/1>,<epoch atau millis>,<bootId>,{json tanpa received_at dan tanpa kurung penutup}"
// received_at ditempel saat unggah. Bila jam belum tersinkron saat diterima, waktu dihitung dari millis() (boot yang sama) atau waktu unggah.
std::deque<String> ramQ;
uint32_t qOff = 0;   // offset byte baca di QFILE (diserialkan di QOFF)

String latJson(const char *s) { char *e; double v = strtod(s, &e); return (e != s && *e == 0) ? String(v, 6) : String("null"); }

String makeLine(const Ev &e) {
  char b[260];
  snprintf(b, sizeof b, "%d,%lu,%lu,{\"vest_id\":%d,\"seq\":%d,\"type\":\"%s\",\"lat\":%s,\"lon\":%s,\"pos_age_s\":%d,\"bat_mv\":%d,\"helm\":%d,\"rssi\":%d,\"snr\":%.1f",
           e.epoch ? 1 : 0, (unsigned long)(e.epoch ? (unsigned long)e.epoch : e.ms), (unsigned long)bootId, e.p.vest, e.p.seq, e.p.type,
           latJson(e.p.lat).c_str(), latJson(e.p.lon).c_str(), e.p.age, e.p.mv, e.p.helm, e.p.rssi, e.p.snr);
  return String(b);
}

void qPush(const String &line) {
  if (sdOk) { File f = SD.open(QFILE, FILE_APPEND); if (f) { f.println(line); f.close(); return; } }
  ramQ.push_back(line);
  if (ramQ.size() > RAM_QUEUE_MAX) ramQ.pop_front();
}

bool qPending() {
  if (!sdOk) return !ramQ.empty();
  File f = SD.open(QFILE, FILE_READ);
  if (!f) return false;
  bool p = f.size() > qOff;
  f.close();
  return p;
}

int qRead(String *out, uint32_t *endOff, int max) {
  int n = 0;
  if (!sdOk) { for (auto &l : ramQ) { if (n >= max) break; out[n] = l; endOff[n++] = 0; } return n; }
  File f = SD.open(QFILE, FILE_READ);
  if (!f) return 0;
  f.seek(qOff);
  while (n < max && f.available()) {
    String l = f.readStringUntil('\n');
    uint32_t pos = f.position();
    l.trim();
    if (l.length()) { out[n] = l; endOff[n++] = pos; }
  }
  f.close();
  return n;
}

void qAck(int n, const uint32_t *endOff) {
  if (!sdOk) { while (n-- > 0 && !ramQ.empty()) ramQ.pop_front(); return; }
  qOff = endOff[n - 1];
  File f = SD.open(QFILE, FILE_READ);
  bool empty = !f || qOff >= f.size();
  if (f) f.close();
  if (empty) { SD.remove(QFILE); qOff = 0; }
  File o = SD.open(QOFF, FILE_WRITE);   // FILE_WRITE memotong file
  if (o) { o.print(qOff); o.close(); }
}

// ---- Unggah ----
bool upload() {
  String lines[UPLOAD_BATCH]; uint32_t endOff[UPLOAD_BATCH];
  int n = qRead(lines, endOff, UPLOAD_BATCH);
  if (!n) return true;
  time_t now = time(nullptr);
  char ts[24]; iso(now, ts, sizeof ts);
  String body = String("{\"gateway_id\":\"") + GATEWAY_ID + "\",\"sent_at\":\"" + ts + "\",\"events\":[";
  int good = 0;
  for (int i = 0; i < n; i++) {
    int syn = 0, off = 0; unsigned long tv = 0, bid = 0;
    if (sscanf(lines[i].c_str(), "%d,%lu,%lu,%n", &syn, &tv, &bid, &off) < 3 || off == 0) { Serial.println("{\"queue\":\"bad_line_dropped\"}"); continue; }
    time_t t = syn ? (time_t)tv : (bid == bootId ? now - (time_t)((millis() - tv) / 1000) : now);
    char rt[24]; iso(t, rt, sizeof rt);
    if (body[body.length() - 1] != '[') body += ",";
    body += String(lines[i].c_str() + off) + ",\"received_at\":\"" + rt + "\"}";
    good++;
  }
  if (!good) { qAck(n, endOff); return true; }   // semua baris rusak: buang, jangan macetkan antrean
  body += "]}";
  // ponytail: setInsecure() tidak memverifikasi sertifikat server. Untuk produksi: pasang CA root (setCACert) agar device key tidak bisa disadap MITM.
  WiFiClientSecure client; client.setInsecure();
  HTTPClient http; http.setTimeout(8000);
  if (!http.begin(client, INGEST_URL)) return false;
  http.addHeader("Content-Type", "application/json");
  http.addHeader("x-device-key", DEVICE_KEY);
  int code = http.POST(body);
  String resp = code > 0 ? http.getString() : String();
  http.end();
  Serial.printf("{\"upload\":{\"events\":%d,\"http\":%d,\"resp\":%s}}\n", n, code, resp.length() ? resp.c_str() : "null");
  if (code != 200) return false;   // 401/422/429/5xx atau tanpa jaringan: antrean tetap, coba lagi nanti
  qAck(n, endOff);                 // per-event yang ditolak validasi (rejected) tetap dihapus agar antrean tidak macet
  return true;
}

void logCsv(const Ev &e) {
  if (!sdOk) return;
  File f = SD.open(CSVFILE, FILE_APPEND);
  if (!f) return;
  char ts[24] = "";
  if (e.epoch) iso(e.epoch, ts, sizeof ts);
  f.printf("%lu,%s,%d,%d,%s,%s,%s,%d,%d,%d,%d,%.1f\n", (unsigned long)e.ms, ts, e.p.vest, e.p.seq, e.p.type, e.p.lat, e.p.lon, e.p.mv, e.p.helm, e.p.age, e.p.rssi, e.p.snr);
  f.close();
}

void netTask(void *) {
  uint32_t nextTry = 0, lastWifi = 0;
  for (;;) {
    Ev e;
    while (xQueueReceive(evQ, &e, pdMS_TO_TICKS(500)) == pdTRUE) { logCsv(e); qPush(makeLine(e)); nextTry = 0; }
    if (!NET_ENABLED) continue;
    uint32_t now = millis();
    if (WiFi.status() != WL_CONNECTED) {
      if (now - lastWifi > 15000) { lastWifi = now; WiFi.disconnect(); WiFi.begin(WIFI_SSID, WIFI_PASS); }
      continue;
    }
    if (now >= nextTry && qPending() && timeSynced()) {
      while (qPending()) { if (!upload()) { nextTry = millis() + RETRY_MS; break; } }
    }
  }
}

void setup() {
  Serial.begin(115200);
  bootId = esp_random();
  pinMode(PIN_SIREN, OUTPUT);
  digitalWrite(PIN_SIREN, LOW);                   // pull-down R3 menjaga LOW saat boot
  pinMode(PIN_LORA_CS, OUTPUT); digitalWrite(PIN_LORA_CS, HIGH);
  pinMode(PIN_SD_CS, OUTPUT);   digitalWrite(PIN_SD_CS, HIGH);

  LoRa.setPins(PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  loraOk = LoRa.begin(LORA_FREQ);
  sdSpi.begin(PIN_SD_SCK, PIN_SD_MISO, PIN_SD_MOSI, PIN_SD_CS);
  sdOk = SD.begin(PIN_SD_CS, sdSpi);
  if (sdOk) {
    File f = SD.open(CSVFILE, FILE_APPEND);
    if (f) { if (f.size() == 0) f.println("ms,utc,vest,seq,type,lat,lon,bat_mv,helm,pos_age_s,rssi,snr"); f.close(); }
    File o = SD.open(QOFF, FILE_READ);
    if (o) { qOff = o.parseInt(); o.close(); }
  }
  if (NET_ENABLED) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    configTime(0, 0, "pool.ntp.org", "time.google.com");   // UTC
  }
  evQ = xQueueCreate(32, sizeof(Ev));
  xTaskCreatePinnedToCore(netTask, "net", 12288, nullptr, 1, nullptr, 0);   // loop() jalan di core 1, tidak terblok jaringan/SD
  Serial.printf("{\"boot\":true,\"lora\":%d,\"sd\":%d,\"net\":%d}\n", loraOk, sdOk, NET_ENABLED);
  lastRxAt = millis();
}

void loop() {
  uint32_t now = millis();
  static int lastSeq[9]; static uint32_t lastSeqAt[9]; static bool seen[9];

  if (loraOk && LoRa.parsePacket()) {
    String s;
    while (LoRa.available()) s += (char)LoRa.read();
    Pkt p; p.rssi = LoRa.packetRssi(); p.snr = LoRa.packetSnr();
    if (parse(s, p)) {
      rxCount++; lastRxAt = now; lostReported = false;
      if (p.seq < 0) p.seq = (v1Seq++) & 0xFFFF;                      // v1: seq dibuat Gateway
      bool dup = seen[p.vest] && lastSeq[p.vest] == p.seq && now - lastSeqAt[p.vest] < DUP_WINDOW_MS;
      Serial.printf("{\"vest_id\":%d,\"seq\":%d,\"type\":\"%s\",\"lat\":\"%s\",\"lon\":\"%s\",\"bat_mv\":%d,\"helm\":%d,\"pos_age_s\":%d,\"rssi\":%d,\"snr\":%.1f%s}\n",
                    p.vest, p.seq, p.type, p.lat, p.lon, p.mv, p.helm, p.age, p.rssi, p.snr, dup ? ",\"dup\":true" : "");
      if (!dup) {
        seen[p.vest] = true; lastSeq[p.vest] = p.seq; lastSeqAt[p.vest] = now;
        Ev e = { p, timeSynced() ? time(nullptr) : 0, now };
        if (xQueueSend(evQ, &e, 0) != pdTRUE) Serial.println("{\"warning\":\"queue_full_event_dropped\"}");
      }
      if (isAlert(p.type)) { lastAlertAt = now; strlcpy(activeKind, p.type, sizeof activeKind); }
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
