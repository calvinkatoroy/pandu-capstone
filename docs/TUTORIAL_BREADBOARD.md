# Tutorial Rakit Breadboard PANDU (tanpa PCB)

Tujuan: membuktikan rangkaian dan firmware v2 bekerja sebelum PCB dipesan. Semua sambungan diambil dari netlist (`hardware/netlist/PCB1.tel`, `PCB2.tel`, `PCB3.tel`).
Pakai bersama [CHECKLIST_UJI_RAKIT.md](CHECKLIST_UJI_RAKIT.md). Setiap tahap punya "Lulus jika ...": jangan lanjut kalau gagal.

> **Penting.** Nomor pin modul di bawah memakai **label yang tercetak di modul**, bukan nomor pin footprint EasyEDA. Selalu baca label di modul fisik kamu. Kalau tidak cocok dengan tabel, **berhenti dan catat**: itu temuan yang harus diperbaiki di PCB.

## Jalur cepat: prototipe hanya dengan bahan BOM (tanpa boost, MOSFET, LiPo)
Untuk bukti konsep sebelum belanja tambahan. Firmware tidak diubah. Lewati bagian yang disebut "lewati".
Butuh tambahan murah: 2 resistor 10 k (SOS), beberapa jumper, 1 LED + resistor 330 Ω.

**Vest**: daya dari **power bank lewat micro-USB DevKit** (lewati 2.1, 2.2, 2.3, 2.9; tanpa baterai, boost, SS14, TP4056).
- MPU6050 (2.5), GPS langsung ke 3V3 (2.6), LoRa Ra-02 433 MHz + antena pegas U.fl (2.7), tombol power IO13 dan SOS IO27 (2.8) tetap sama.
- IO4 dan IO32 dibiarkan kosong (firmware tetap jalan, GPS selalu hidup).
- **Sensor air**: untuk uji MOB tanpa sensor, sambungkan IO34 ke 3V3 pakai jumper selama 3 detik (= basah), lepas (= kering); tambah resistor 10 k IO34 ke GND supaya tidak mengambang. XKC-Y25-V (digital, 5 V): ukur OUT dulu dan pakai pembagi 10 k/20 k (bagian 2.8), jangan langsung ke IO34.
- Angka baterai (mV) di paket tidak berarti tanpa baterai/pembagi; abaikan.

**Gateway**: daya dari adaptor 5 V lewat micro-USB DevKit. Pin LoRa dan SD sesuai tabel di bagian 3.
- Lewati IRLZ44N dan sirine. Pengganti: **IO4 → LED + 330 Ω → GND** (LED nyala = sirine ON). Jangan sambungkan sirine 85 dB langsung ke pin.

**Helmet**: daya dari **USB SuperMini** (lewati LiPo, TP4056, saklar). Tanpa sensor sentuh. Tombol GPIO4 ke GND (pull-up internal sudah ada); untuk demo pakai env `supermini_test` (beacon terus-menerus, serial hidup).
- Pada C3 dengan USB, serial putus-sambung tiap siklus deep sleep (8 s). Normal; buka ulang monitor atau baca lewat paket Vest.

**Urutan uji**: Gateway sendiri (`lora":1,"sd":1`) → Vest sendiri (`MPU=1 LoRa=1`) → heartbeat Vest ke Gateway → SOS (LED Gateway menyala) → jatuh dan MOB → Helmet (`helm` di paket berubah `2 → 1` saat beacon ON dan helm didekatkan).
Yang **belum** terbukti dengan jalur ini: daya baterai Vest, gating GPS/XKC, siren daya penuh, helm dengan baterai.

## 0. Keselamatan dan aturan
1. Baterai 18650 **harus berproteksi** (ada PCB proteksi) atau lewat TP4056 modul berproteksi (DW01). Jangan pernah korsleting baterai. Pasang sekring/polyfuse kalau ada.
2. **Jangan transmit LoRa tanpa antena** (merusak chip RF). Pasang antena sebelum upload firmware yang memanggil `LoRa.begin`.
3. Setel **boost ke 5,0 V dengan multimeter sebelum** disambung ke ESP32 atau sensor (lihat 2.1).
4. **Satu sumber 5 V pada satu waktu** untuk ESP32: jika USB dicolok untuk upload, lepas sumber 5 V dari boost ke pin 5V (atau pakai dioda SS14 seperti di PCB).
5. Semua GPIO ESP32 hanya 3,3 V. Pin 5 V tidak boleh masuk ke GPIO.
6. Tiap kali ganti kabel, matikan daya dulu.

## 1. Daftar bahan
**Vest**
- ESP32-DevKitC V4, breadboard besar, kabel jumper M-M / M-F
- Baterai 18650 + holder, modul TP4056 (USB-C, berproteksi), modul boost MT3608
- Dioda SS14 (atau 1N5819), kapasitor 100 µF tantalum/elko, 100 nF
- GY-521 (MPU6050), GPS NEO-6M, modul LoRa Ra-02 SX1278 433 MHz (breakout 2,54 mm) + antena pegas 433 MHz U.fl
- XKC-Y25-V (air, kabel XH 4 pin), tact switch 2 buah (power dan SOS), resistor 10 k (2 buah: 1 pembagi XKC, 1 pull SOS), 20 k (pembagi XKC), 100 k (2 buah untuk pembagi baterai + 1 pull)
- Opsional untuk uji gating: MOSFET P-channel logic-level (mis. AO3401A di adapter SOT-23) dan 2N7000

**Helmet**
- ESP32-C3 SuperMini, LiPo 3,7 V berproteksi (±400-500 mAh) + modul TP4056 USB-C, saklar geser, tact switch, resistor 100 k, 10 µF dan 100 µF (tanpa sensor sentuh TTP223: sudah dibuang dari desain)

**Gateway**
- ESP32-DevKitC V4, modul LoRa Ra-02 SX1278 433 MHz + antena pegas 433 MHz, modul microSD (SPI), kartu microSD (FAT32)
- IRLZ44N, resistor 220 Ω dan 100 k, sirine 5 V (atau LED + resistor 330 Ω untuk uji), kabel

**Alat**: multimeter, kabel micro-USB data (bukan kabel charge-only), laptop dengan PlatformIO.

## 2. Vest: tahap per tahap

### 2.1 Daya (belum ada ESP32)
Sambungan:

| Dari | Ke | Catatan |
|---|---|---|
| Baterai + | TP4056 `B+` | |
| Baterai - | TP4056 `B-` | |
| TP4056 `OUT+` | Boost `IN+` | net `VBAT_RAW` |
| TP4056 `OUT-` | Boost `IN-` dan GND bersama | |
| Boost `OUT-` | GND bersama | |
| Boost `OUT+` | rel 5 V (net `VBOOST_5V`) | |

Langkah:
1. Colok USB-C ke TP4056 (tanpa baterai dulu), ukur `OUT+`: harus kira-kira 4,2 V atau tegangan USB. Lalu pasang baterai.
2. **Setel trimmer boost** sampai `OUT+` = **5,0 V** (± 0,1).
3. Ukur `VBAT_RAW` (di `OUT+` TP4056): 3,0–4,2 V.

Lulus jika: boost 5,0 V stabil, TP4056 LED charging menyala saat USB dicolok.

### 2.2 Pembagi baterai (BAT_SENSE)
- `VBAT_RAW` → R 100 k → titik tengah → R 100 k → GND.
- Titik tengah → **IO35** dan C 100 nF ke GND.
- Ukur titik tengah = separuh `VBAT_RAW` (4,0 V → 2,0 V).

### 2.3 ESP32 dan sumber 5 V
- Rel 5 V boost → anoda SS14; **katoda** SS14 → pin **5V** DevKit (net `5V_DK`).
- GND bersama → pin GND DevKit.
- 100 µF antara 3V3 dan GND DevKit (net `3V3_SYS`).
- **Jangan** colok USB DevKit saat boost menyuplai 5V tanpa dioda SS14 terpasang.

Upload (USB dicolok, bisa bersamaan dengan SS14):
```
cd firmware/vest_node
python -m platformio run -t upload
python -m platformio device monitor
```
Lulus jika: serial tercetak `Boot: ...`. (MPU/LoRa=0 normal pada tahap ini karena belum disambung.)

### 2.4 Peta pin ESP32 Vest

| Fungsi | Pin DevKit | Ke modul / komponen |
|---|---|---|
| Tombol power | **IO13** | tact → GND (pull-up internal) |
| Tombol SOS | **IO27** | tact → **3V3**, resistor 10 k dari IO27 ke GND (aktif-HIGH) |
| Sensor air `WATER_SIG` | **IO34** | output XKC-Y25 (lihat catatan tipe output) |
| Enable GPS | **IO4** | gate P-MOSFET (lihat 2.9); sementara kosongkan |
| Enable XKC | **IO32** | gate N-MOSFET (lihat 2.9); sementara kosongkan |
| Baterai | **IO35** | titik tengah pembagi (2.2) |
| I2C SDA / SCL | **IO21 / IO22** | GY-521 SDA / SCL |
| GPS RX (ESP) / TX (ESP) | **IO16 / IO17** | **TX modul GPS → IO16**, RX modul GPS ← IO17 |
| SPI SCK / MISO / MOSI | **IO18 / IO19 / IO23** | LoRa SCK / MISO / MOSI |
| LoRa NSS (CS) | **IO5** | |
| LoRa RESET | **IO25** | |
| LoRa DIO0 | **IO26** | pin `DIO0` breakout; DIO1-5 tidak dipakai |

### 2.5 MPU6050 (GY-521)
- VCC → 3V3, GND → GND, SCL → IO22, SDA → IO21.
- Lulus jika serial: `Boot: MPU=1 ...`.
- **Catatan PCB:** urutan pin footprint GY-521 di PCB tampak terbalik dari urutan header modul (VCC, GND, SCL, SDA, XDA, XCL, AD0, INT). Cek apakah footprint cocok dengan modul fisik, atau modul harus dipasang terbalik. Catat hasilnya (temuan PCB).

### 2.6 GPS NEO-6M
- VCC → 3V3 (sementara langsung, tanpa gating), GND → GND.
- Pin **TX modul** → **IO16**, pin **RX modul** → **IO17**.
- Lulus jika: di luar ruangan, setelah beberapa menit paket berisi lat/lon (bukan `NOFIX`).

### 2.7 LoRa (pasang antena dulu)
Modul: **Ra-02 SX1278 433 MHz (breakout 2,54 mm)**, antena pegas 433 MHz di konektor U.fl. Pinout dan pemetaan lengkap: [LORA_RA02_BREAKOUT.md](LORA_RA02_BREAKOUT.md).
Label pin breakout → pin DevKit: `3.3V` → 3V3, `GND` → GND (cukup satu atau dua dari empat pin GND, semua boleh), `SCK` → IO18, `MISO` → IO19, `MOSI` → IO23, `NSS` → IO5, `RST` → IO25, `DIO0` → IO26. DIO1-5 tidak dipakai. **Antena lewat U.fl, bukan pin header.** Jangan ke 5 V.
- Lulus jika: `Boot: MPU=1 LoRa=1 ...`. Jika `LoRa=0`: cek kabel, GND, 3V3, dan urutan label pin breakout (atas: GND NSS MOSI MISO SCK DIO5 DIO4 GND; bawah: GND GND 3.3V RST DIO0 DIO1 DIO2 DIO3).
- Tes tautan dua modul: flash `firmware/test_lora_one` ke kedua ESP32; baris `RX ... rssi snr` membuktikan paket sampai.
- Daya: arus pulsa transmit ±120 mA. Sertakan 100 µF dekat modul.

### 2.8 Sensor air XKC-Y25 dan tombol
- **XKC-Y25-V** (spesifikasi: halaman produk xkc-sensor.com/detail/1432.html): digital high/low, 5-24 V, 5 mA, riak catu ≤ 200 mV, respons 500 ms, tebal dinding ≤ 20 mm, kabel XH2.54-4P. Kawat: cokelat = `VCC`, kuning = `OUT`, biru = `GND`, hitam = "signal option" (polaritas, belum diketahui; tes terbuka vs ke GND).
- Sambungan: `VCC` → 5 V (rel `VBOOST_5V` atau VIN USB), `GND` → GND, `OUT` → **pembagi 10 k (seri) lalu 20 k ke GND, titik tengah ke IO34** (5 V → 3,3 V). **Tanpa pull-up ke 3V3.** Jangan sambung OUT langsung ke IO34.
- **Ukur dulu dengan multimeter** sebelum ke ESP32: tegangan OUT kering dan basah, dengan kawat hitam terbuka lalu ke GND. Catat state mana yang berarti ada cairan.
- Sensor harus menempel di dinding (non-logam, ≤ 20 mm) dengan cairan di sisi seberang; uji juga dengan casing asli.
- Tombol power: antara IO13 dan GND. Tombol SOS: antara IO27 dan 3V3, plus 10 k dari IO27 ke GND.
- Lulus jika: celup sensor 3 detik → serial/LoRa `MOB`. Tahan tombol SOS 2 detik → `SOS`. Tekan tombol power → `Sleep...`, lalu SOS membangunkan alat dan langsung mengirim.

### 2.9 (Opsional) Gating GPS / XKC
Di PCB, GPS lewat P-MOSFET (Q1), XKC lewat P-MOSFET + N-MOSFET (Q2/Q5). Di breadboard, SOT-23 sulit. Uji gating terpisah dengan adapter SOT-23:
- GPS: source P-MOSFET → 3V3, drain → VCC GPS, gate → IO4 dan pull-up 100 k ke 3V3. IO4 LOW = ON, hi-Z (INPUT) = OFF.
- XKC: source P-MOSFET → 5 V, drain → VCC XKC, gate → pull-up 100 k ke 5 V; N-MOSFET: gate ← IO32 (pull-down 100 k ke GND), source → GND, drain → gate P-MOSFET. IO32 HIGH = ON.
- Lulus jika: ukur VCC modul ON ≈ 3,3 V / 5 V dan OFF ≈ 0 V.

### 2.10 Tes sistem Vest
Lihat tahap 2 pada [CHECKLIST_UJI_RAKIT.md](CHECKLIST_UJI_RAKIT.md): jatuh, MOB, SOS, baterai (kalibrasi `BAT_DIV`), tidur/bangun.

## 3. Gateway

| Fungsi | Pin DevKit | Ke |
|---|---|---|
| LoRa SCK / MISO / MOSI | **IO18 / IO19 / IO23** | pin `SCK` / `MISO` / `MOSI` breakout Ra-02 |
| LoRa NSS | **IO5** | pin `NSS` breakout |
| LoRa RST | **IO14** | pin `RST` breakout (beda dengan Vest = IO25!) |
| LoRa DIO0 | **IO26** | pin `DIO0` breakout; DIO1-5 tidak dipakai |
| SD SCK / MISO / MOSI | **IO25 / IO35 / IO32** | bus SPI **terpisah** dari LoRa (PCB3 v3; MISO di IO35 input-only) |
| SD CS | **IO33** | + pull-up 10 k ke 3V3 |
| Sirine drive | **IO4** | → 220 Ω → gate IRLZ44N; gate → 100 k → GND |
| 3V3 / GND | 3V3, GND | LoRa, SD |

- IRLZ44N: source → GND, drain → sirine `−`; sirine `+` → pin 5V DevKit. Untuk uji awal pakai **LED + resistor 330 Ω** sebagai pengganti sirine.
- Modul microSD butuh 5 V atau 3,3 V sesuai modulnya: cek label (kebanyakan modul punya regulator dan menerima 5 V, tetapi level SPI harus 3,3 V).
- **Hanya satu port USB**. Gateway diprogram lewat micro-USB DevKit; sirine disuplai dari pin 5V DevKit (arus sirine mengalir lewat jalur USB).
- Upload dan monitor:
```
cd firmware/gateway
python -m platformio run -t upload
python -m platformio device monitor
```
- **Unggah ke dashboard (opsional):** salin `firmware/gateway/include/config.example.h` menjadi `config.h` (di-gitignore), isi WiFi, `GATEWAY_ID`, `INGEST_URL`, `DEVICE_KEY`. Tanpa `config.h` Gateway jalan offline (serial, SD, sirine). Paket yang belum terunggah antre di `/queue.jsonl` di microSD dan dikirim otomatis saat WiFi dan NTP siap. Serial menampilkan `{"upload":{"events":N,"http":200,...}}`.
- Paket Vest sekarang v2 (`PANDU,V2,<vest_id>,<seq>,<jenis>,...`); `VEST_ID` diatur lewat `-DVEST_ID=n` (default 1). Vest mengirim paket `OFF` saat tombol power ditekan (tidur).
- Antena U.fl terpasang sebelum menyala; 3V3 saja, jangan 5 V; 100 µF dekat modul LoRa. Frekuensi firmware 433E6 (sama dengan Vest).
- Lulus jika: `{"boot":true,"lora":1,"sd":1}`. Kirim `M` di serial untuk mute.

## 4. Helmet

| Fungsi | Pin SuperMini | Ke |
|---|---|---|
| Tombol on/off | **GPIO4** | tact → GND, pull-up 100 k ke 3V3 |
| Daya masuk | pin **5V** | LiPo `+` > TP4056 `B+`; TP4056 `OUT+` > saklar geser > pin 5V SuperMini (net `VBAT_SW`). Jangan ke pin 3V3 (4,2 V terlalu tinggi) |
| 3V3 | pin 3V3 (output) | 10 µF + 100 µF ke GND |
| GND | GND | `−` baterai (via TP4056 `OUT−`) |

- **Daya:** baterai masuk lewat pin 5V (bukan 3V3). Cek di board fisik bahwa pin 5V melewati regulator 3,3 V dan ada dioda ke VBUS; ukur 3V3 = 3,3 V dengan baterai 3,3-4,2 V. Isi baterai lewat USB-C TP4056, bukan lewat USB SuperMini.
- Upload lewat USB SuperMini (saklar geser OFF supaya aman):
```
cd firmware/helmet_node
python -m platformio run -t upload
python -m platformio device monitor
```
- Tidak ada sensor sentuh. Helm menyiarkan beacon BLE selama ON; Vest menilai dekat/jauh dari RSSI (`helm` = 1 dekat, 0 jauh, 2 tidak terdengar).
- Mode produk (default): deep sleep, bangun tiap 8 s dan siaran 400 ms. Mode demo: aktifkan env `supermini_test` (`TEST_BEACON`): siaran terus-menerus, serial hidup, tombol GPIO4 = ON/OFF.
- Lulus jika: beacon ON dan helm di dekat Vest → serial Vest `helm=1`; jauhkan helm → `0`; tombol OFF atau matikan → `2` setelah 30 s. RSSI ambang -85 dBm belum dikalibrasi: catat nilai RSSI pada jarak dekat/jauh.
- Ukur arus rata-rata dengan multimeter ampere seri dengan baterai.

## 5. Tautan Vest ↔ Gateway ↔ Helmet
1. Nyalakan Gateway (serial terbuka). Nyalakan Vest. Tunggu `HB` (heartbeat 30 s) muncul di Gateway: `{"type":"HB",...,"rssi":-xx}`.
2. Tekan SOS di Vest → sirine/LED Gateway menyala dalam < 2 detik, baris baru di `/pandu.csv`.
3. Nyalakan Helmet (beacon ON) dan dekatkan ke Vest: field `helm` berubah `2 → 1` (atau `0` bila terlalu jauh). Tombol OFF → `2` setelah 30 s.
4. LoRa 433 MHz, antena terpasang di kedua sisi; catat `rssi` dan `snr` di JSON Gateway.

## 6. Troubleshooting singkat

| Gejala | Cek |
|---|---|
| ESP32 tidak terdeteksi USB | kabel data, driver CP210x/CH340, tahan BOOT saat upload |
| `LoRa=0` | antena, 3V3, GND, label pin modul, NSS/RST/DIO0 benar |
| `MPU=0` | SDA/SCL tertukar, VCC, alamat 0x68 (AD0 ke GND) |
| GPS selalu `NOFIX` | di luar ruangan, TX/RX tertukar, tunggu cold start |
| Reset acak | catu 3V3/5V jatuh (kapasitor 100 µF, kabel panjang), arus sirine |
| Boost keluar bukan 5 V | setel trimmer sebelum disambung |
| Tidak bangun dari sleep | tombol ke pin RTC yang benar (IO13, IO27), wiring tombol |

## 7. Catat temuan untuk revisi PCB
Setiap kali pinout/ukuran modul tidak cocok dengan skematik, tulis di sini lalu laporkan:

| Modul | Temuan | Dampak PCB |
|---|---|---|
| ~~LoRa XL1276-P01 (chip SX1276)~~ (USANG 13 Okt: modul diganti Ra-02 SX1278 433 MHz, lihat LORA_RA02_BREAKOUT.md) | Dari foto sisi pad: kolom kiri atas ke bawah `DIO2, DIO1, DIO0, VCC, DIO4, DIO3, GND, ANT`; kolom kanan `GND, MISO, MOSI, SCK, NSS, REST, DIO5, GND`. Urutan ini = pinout **RFM95**, bukan RA-02 (RA-02: 1 ANT, 2 GND, 3 3,3V, 4 RST, 5 DIO0, ... 15 NSS). | Footprint `WIRELM-SMD_RA-02-BL` di PCB1/PCB3 **tidak cocok** dengan modul ini. Ganti footprint ke RFM95 (atau beli Ra-01H) sebelum order PCB. Cek juga jarak antar deret pad. |
| ~~LoRa XL1276-P01~~ (usang) | Di foto sisi pad, kotak pita frekuensi (915M/868M/433M/315M/169M) yang terisi/ditandai hitam adalah **868M**. Belum dicek di modul fisik. | Kalau modul fisik juga 868M, matching RF-nya untuk 868 MHz, bukan 915/920 MHz. Cek modul dan listing. |

> **Update 13 Okt 2026:** baris XL1276 di atas usang. Modul sekarang Ra-02 SX1278 433 MHz (breakout); pinout dan wiring di [LORA_RA02_BREAKOUT.md](LORA_RA02_BREAKOUT.md). Frekuensi firmware 433E6.
