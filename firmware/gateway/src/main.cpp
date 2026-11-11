// PANDU Edge Gateway: ESP32-DevKitC V4. Terima paket LoRa dari Vest (pure gateway, tanpa sirine), log ke SD, keluarkan JSON ke serial,
// dan unggah ke dashboard (HTTPS POST ke Edge Function ingest) dengan antrean microSD (store-and-forward).
// Pin (PCB3 v3): LORA_CS=IO5, LORA_RST=IO14, LORA_DIO0=IO26, SPI LoRa=IO23/19/18, SD: SCK=IO25 MISO=IO35 MOSI=IO32 CS=IO33.
// Paket Vest v2: PANDU,V2,<vest_id>,<seq>,<jenis>,<lat>,<lon>,<mV>,<helm>,<usia posisi detik>[,<sens>]*<hmac 8 hex>
//   Paket tanpa HMAC sah dibuang (bad_mac). Paket v1 (tanpa vest_id/seq) masih bisa di-parse tetapi tidak punya HMAC, jadi praktis tidak diterima lagi.
//   sens = bitmask kesehatan sensor Vest (1 = MPU mati, 2 = g belum terkalibrasi); hanya dicetak di serial, belum ada di kontrak ingest.
//   jenis: HB|SOS|FALL|MOB|OFF   helm: 1 dipakai, 0 tidak, 2 tidak terjangkau.   Kontrak: pandu-dashboard/docs/DATA_CONTRACT.md
// Arsitektur: loop() hanya LoRa (tidak boleh terblok). Task netTask() satu-satunya pengguna SD dan jaringan.
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
#include "pandu_mac.h"   // ../common: HMAC paket + sync word (audit K2)

constexpr int PIN_LORA_CS = 5, PIN_LORA_RST = 14, PIN_LORA_DIO0 = 26;
constexpr int PIN_SD_CS = 33, PIN_SD_SCK = 25, PIN_SD_MISO = 35, PIN_SD_MOSI = 32;   // SD di bus SPI sendiri (PCB3 v3), terpisah dari LoRa
SPIClass sdSpi(HSPI);
constexpr long LORA_FREQ = 433E6;                 // Ra-02 SX1278, harus sama dengan Vest
constexpr uint32_t VEST_LOST_MS   = 90000;        // tidak ada paket sama sekali selama ini = peringatan "VEST LOST" (serial saja)
constexpr uint32_t DUP_WINDOW_MS  = 60000;        // paket ulang (vest_id, seq) sama dalam jendela ini = duplikat radio, tidak diunggah ulang
constexpr int      UPLOAD_BATCH   = 20;           // maks event per POST (server menerima <= 100)
constexpr uint32_t RETRY_MS       = 30000;        // jeda setelah unggah gagal
constexpr size_t   RAM_QUEUE_MAX  = 64;           // antrean cadangan di RAM bila SD tidak ada (hilang saat mati)
const char *QFILE = "/queue.jsonl", *QOFF = "/queue.off", *CSVFILE = "/pandu_v2.csv", *DEADFILE = "/deadletter.jsonl";
constexpr size_t   RAM_DEAD_MAX   = 16;           // dead-letter di RAM bila SD tidak ada

// Batas yang sama dengan validateEvent di server (supabase/functions/_shared/stage.ts). Untuk event ALARM, nilai di luar batas
// diperbaiki sebelum unggah supaya alarm tidak ditolak (K1); data mentah tetap utuh di CSV.
constexpr int BAT_MV_MIN = 2500, BAT_MV_MAX = 4500;

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

bool loraOk = false, sdOk = false;
uint32_t lastRxAt = 0, rxCount = 0;
bool lostReported = false;
uint32_t bootId;                                   // membedakan millis() antar boot pada antrean SD
int v1Seq = 0;                                     // seq buatan untuk paket v1

struct Pkt { uint8_t vest; int seq; char type[8]; char lat[16]; char lon[16]; int mv, helm, age, rssi; float snr; int sens; };
struct Ev { Pkt p; time_t epoch; uint32_t ms; };  // epoch = 0 bila jam belum tersinkron saat paket diterima
QueueHandle_t evQ;                                 // loop() -> netTask()

bool validType(const char *t) { return !strcmp(t, "HB") || !strcmp(t, "SOS") || !strcmp(t, "FALL") || !strcmp(t, "MOB") || !strcmp(t, "OFF"); }
bool isAlarm(const char *t) { return !strcmp(t, "SOS") || !strcmp(t, "FALL") || !strcmp(t, "MOB"); }

bool parse(const String &s, Pkt &p) {
  char buf[200];
  if (s.length() >= sizeof buf) return false;   // lebih panjang dari paket sah mana pun: jangan dipotong diam-diam
  s.toCharArray(buf, sizeof buf);
  char *tok[14]; int n = 0;
  for (char *t = strtok(buf, ","); t && n < 14; t = strtok(nullptr, ",")) tok[n++] = t;
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
  p.sens = n > i + 6 ? atoi(tok[i + 6]) : 0;      // kesehatan sensor Vest (bitmask)
  return true;
}

// ---- Waktu ----
bool timeSynced() { return time(nullptr) > 1700000000; }
void iso(time_t t, char *out, size_t n) { struct tm g; gmtime_r(&t, &g); strftime(out, n, "%Y-%m-%dT%H:%M:%SZ", &g); }

// ---- Antrean store-and-forward (hanya dipakai netTask) ----
// Satu baris per event: "<tersinkron 0/1>,<epoch atau millis>,<bootId>,{json tanpa received_at dan tanpa kurung penutup}"
// received_at ditempel saat unggah. Bila jam belum tersinkron saat diterima, waktu dihitung dari millis() (boot yang sama) atau waktu unggah.
std::deque<String> ramQ;
uint32_t qOff = 0;   // offset byte baca di QFILE (diserialkan di QOFF)

// Koordinat di luar rentang (atau bukan angka) -> null, supaya server tidak menolak seluruh event.
String latJson(const char *s, double lim) { char *e; double v = strtod(s, &e); return (e != s && *e == 0 && v >= -lim && v <= lim) ? String(v, 6) : String("null"); }

String makeLine(const Ev &e) {
  char b[260];
  int mv = e.p.mv;
  if (isAlarm(e.p.type) && (mv < BAT_MV_MIN || mv > BAT_MV_MAX)) {   // K1: alarm tidak boleh gugur karena angka baterai tidak masuk akal
    mv = mv < BAT_MV_MIN ? BAT_MV_MIN : BAT_MV_MAX;
    Serial.printf("{\"warning\":\"alarm_bat_mv_clamped\",\"vest_id\":%d,\"seq\":%d,\"raw_mv\":%d,\"sent_mv\":%d}\n", e.p.vest, e.p.seq, e.p.mv, mv);
  }
  snprintf(b, sizeof b, "%d,%lu,%lu,{\"vest_id\":%d,\"seq\":%d,\"type\":\"%s\",\"lat\":%s,\"lon\":%s,\"pos_age_s\":%d,\"bat_mv\":%d,\"helm\":%d,\"rssi\":%d,\"snr\":%.1f",
           e.epoch ? 1 : 0, (unsigned long)(e.epoch ? (unsigned long)e.epoch : e.ms), (unsigned long)bootId, e.p.vest, e.p.seq, e.p.type,
           latJson(e.p.lat, 90).c_str(), latJson(e.p.lon, 180).c_str(), e.p.age, mv, e.p.helm, e.p.rssi, e.p.snr);
  return String(b);
}

// ---- Dead-letter (K1): event ALARM yang ditolak server tidak boleh hilang diam-diam ----
std::deque<String> ramDead;
void deadLetter(const String &line, const String &why) {
  String shown = line; shown.replace('"', '\'');   // supaya baris serial tetap JSON valid
  Serial.printf("{\"alarm_rejected\":{\"why\":\"%s\",\"line\":\"%s\"}}\n", why.c_str(), shown.c_str());   // selalu terlihat di serial
  String rec = line + "\t" + why;
  if (sdOk) { File f = SD.open(DEADFILE, FILE_APPEND); if (f) { f.println(rec); f.close(); return; } }
  ramDead.push_back(rec);
  if (ramDead.size() > RAM_DEAD_MAX) ramDead.pop_front();
}
// Ambil alasan penolakan untuk indeks idx dari respons {"rejected":[{"index":N,"reason":"..."}]}. Kosong bila tidak ketemu.
String rejectReason(const String &resp, int idx) {
  String key = String("\"index\":") + idx;
  int p = -1;
  for (int from = 0; (from = resp.indexOf(key, from)) >= 0; from += key.length()) {
    char next = from + key.length() < resp.length() ? resp[from + key.length()] : ',';
    if (next < '0' || next > '9') { p = from; break; }   // "index":1 tidak boleh cocok dengan "index":10
  }
  if (p < 0) return String();
  int r = resp.indexOf("\"reason\":\"", p);
  if (r < 0) return String("(tanpa alasan)");
  r += 10;
  int e = resp.indexOf('"', r);
  return e < 0 ? String() : resp.substring(r, e);
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
  int bodyLine[UPLOAD_BATCH];   // indeks event di body -> indeks baris antrean (baris rusak dilewati, jadi tidak selalu sama)
  for (int i = 0; i < n; i++) {
    int syn = 0, off = 0; unsigned long tv = 0, bid = 0;
    if (sscanf(lines[i].c_str(), "%d,%lu,%lu,%n", &syn, &tv, &bid, &off) < 3 || off == 0) { Serial.println("{\"queue\":\"bad_line_dropped\"}"); continue; }
    bodyLine[good] = i;
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
  WiFiClient plainClient;                                       // http:// hanya untuk uji LAN (Supabase lokal); produksi wajib https
  HTTPClient http; http.setTimeout(8000);
  bool plain = strncmp(INGEST_URL, "http://", 7) == 0;
  if (!(plain ? http.begin(plainClient, INGEST_URL) : http.begin(client, INGEST_URL))) return false;
  http.addHeader("Content-Type", "application/json");
  http.addHeader("x-device-key", DEVICE_KEY);
  int code = http.POST(body);
  String resp = code > 0 ? http.getString() : String();
  http.end();
  Serial.printf("{\"upload\":{\"events\":%d,\"http\":%d,\"resp\":%s}}\n", n, code, resp.length() ? resp.c_str() : "null");
  if (code != 200) return false;   // 401/422/429/5xx atau tanpa jaringan: antrean tetap, coba lagi nanti
  // Event yang ditolak validasi tetap dihapus dari antrean (agar tidak macet), TAPI yang bertipe alarm disimpan ke dead-letter dulu (K1).
  for (int bi = 0; bi < good; bi++) {
    String why = rejectReason(resp, bi);
    if (!why.length()) continue;
    const String &ln = lines[bodyLine[bi]];
    if (ln.indexOf("\"type\":\"SOS\"") >= 0 || ln.indexOf("\"type\":\"FALL\"") >= 0 || ln.indexOf("\"type\":\"MOB\"") >= 0) deadLetter(ln, why);
    else Serial.printf("{\"rejected\":{\"index\":%d,\"why\":\"%s\"}}\n", bi, why.c_str());
  }
  qAck(n, endOff);
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
  pinMode(PIN_LORA_CS, OUTPUT); digitalWrite(PIN_LORA_CS, HIGH);
  pinMode(PIN_SD_CS, OUTPUT);   digitalWrite(PIN_SD_CS, HIGH);

  LoRa.setPins(PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  loraOk = LoRa.begin(LORA_FREQ);
  if (loraOk) { LoRa.enableCrc(); LoRa.setSyncWord(PANDU_SYNC_WORD); LoRa.receive(); }   // K2: CRC + sync word unik (sama dengan Vest); receive() sekali (S5)
  if (PANDU_KEY_IS_DEFAULT) Serial.println("{\"warning\":\"PANDU_KEY bawaan (dev): paket tidak terautentikasi, buat include/config.h\"}");
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
    String body;
    if (!panduVerify(s, body)) {   // K2: HMAC salah/tidak ada = paket asing atau palsu
      Serial.printf("{\"ignored\":\"bad_mac\",\"rssi\":%d}\n", p.rssi);
    } else if (parse(body, p)) {
      rxCount++; lastRxAt = now; lostReported = false;
      if (p.seq < 0) p.seq = (v1Seq++) & 0xFFFF;                      // v1: seq dibuat Gateway
      bool dup = seen[p.vest] && lastSeq[p.vest] == p.seq && now - lastSeqAt[p.vest] < DUP_WINDOW_MS;
      Serial.printf("{\"vest_id\":%d,\"seq\":%d,\"type\":\"%s\",\"lat\":\"%s\",\"lon\":\"%s\",\"bat_mv\":%d,\"helm\":%d,\"pos_age_s\":%d,\"rssi\":%d,\"snr\":%.1f,\"sens\":%d%s}\n",
                    p.vest, p.seq, p.type, p.lat, p.lon, p.mv, p.helm, p.age, p.rssi, p.snr, p.sens, dup ? ",\"dup\":true" : "");
      if (!dup) {
        seen[p.vest] = true; lastSeq[p.vest] = p.seq; lastSeqAt[p.vest] = now;
        Ev e = { p, timeSynced() ? time(nullptr) : 0, now };
        if (xQueueSend(evQ, &e, 0) != pdTRUE) Serial.println("{\"warning\":\"queue_full_event_dropped\"}");
      }
    } else Serial.printf("{\"ignored\":\"bad_packet\",\"rssi\":%d}\n", p.rssi);
  }

  // Status berkala: bukti Gateway hidup walau belum ada paket
  static uint32_t lastStat = 0;
  if (now - lastStat >= 10000) {
    lastStat = now;
    Serial.printf("{\"status\":{\"lora\":%d,\"sd\":%d,\"rx\":%lu,\"last_rx_s\":%ld,\"wifi\":%d,\"time_synced\":%d}}\n",
                  loraOk, sdOk, (unsigned long)rxCount, rxCount ? (long)((now - lastRxAt) / 1000) : -1L, NET_ENABLED && WiFi.status() == WL_CONNECTED, timeSynced());
  }

  // Vest hilang sinyal
  if (!lostReported && now - lastRxAt > VEST_LOST_MS) {
    lostReported = true;
    Serial.println("{\"warning\":\"vest_lost\"}");
  }
  delay(5);
}
