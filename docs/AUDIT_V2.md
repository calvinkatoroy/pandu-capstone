# Audit PANDU v2 vs definisi proyek (8 Okt 2026)

Definisi acuan (dari Calvin): Vest = MOB (jatuh AND ada air di balik casing, non-contact) + deteksi helm via RSSI BLE + LoRa 915 ke Gateway + GPS + USB-C + 18650 1200 mAh + 2 tact (SOS, power). Helmet = beacon BLE, tact on/off, baterai kecil. Gateway = LoRa, microSD, dashboard 3 tahap (1 aman, 2 warning APD tidak lengkap, 3 danger SOS/FALL/MOB), peta real-time, buzzer lokal, WiFi di dermaga, sampai 8 Vest.

Yang diperiksa: netlist `PCB1/2/3.tel`, skematik EasyEDA (Vest, Helmet, Gateway, dibuka langsung), PCB1 (cek sebagian), firmware di `firmware/`, dashboard `APP/index.html`, BOM sheet, dokumen repo.
Tingkat: **KRITIS** = alat tidak jalan/berbahaya, **SEDANG** = tidak sesuai definisi atau berisiko, **MINOR** = rapikan.

## A. Skematik dan PCB (EasyEDA)

| # | Tingkat | Board | Temuan | Perbaikan |
|---|---|---|---|---|
| A1 | KRITIS | PCB2 | `SAW1` = filter SMD SAPPLAND SPST40SU03C (footprint FILTER-SMD 1,1x0,9 mm), bukan saklar. Jalur baterai Helmet lewat komponen ini | Ganti saklar geser sungguhan atau header 2 pin + jumper |
| A2 | KRITIS | PCB1, PCB2 | TP4056: pin `B-` dan `OUT-` sama-sama GND, negatif baterai ke GND. Proteksi DW01 terlewati (over-discharge, over-current, korslet) | Negatif baterai hanya ke `B-`; `OUT-` ke GND sistem |
| A3 | KRITIS | PCB1, PCB3 | Footprint LoRa `RA-02` (pin 1 ANT, 3 3,3V, 4 RST, 5 DIO0, 12-15 SCK/MISO/MOSI/NSS). Modul fisik XL1276-P01 berpinout RFM95 (kiri atas-bawah DIO2, DIO1, DIO0, VCC, DIO4, DIO3, GND, ANT; kanan GND, MISO, MOSI, SCK, NSS, REST, DIO5, GND) | Ganti footprint ke RFM95, cek jarak deret pad, route ulang |
| A4 | KRITIS | PCB1 | XKC-Y25 (5 V) ke IO34 tanpa pembagi/pelindung. Beberapa varian outputnya naik ke tegangan suplai (5 V), batas IO34 sekitar 3,6 V. Pull-up R1 ke 3V3 hanya cocok untuk varian open-collector | Ukur output saat modul datang; tambah pembagi 10k/20k atau pakai pull-up saja sesuai varian; cek polaritas |
| A5 | SEDANG | PCB2 | TTP223 (`H1`), net `TOUCH_SIG` masih ada, padahal deteksi helm via tombol + BLE + RSSI | Hapus H1 dan TOUCH_SIG; GPIO2 bebas |
| A6 | SEDANG | PCB2 | Definisi: CR2032. EasyEDA: LiPo + TP4056 (CR2032 tidak kuat untuk lonjakan BLE dan tidak bisa diisi ulang). Pin 5V SuperMini harus lewat regulator (belum diverifikasi), dan USB SuperMini + baterai bersamaan belum diuji | Perbarui definisi ke LiPo. Cek pin 5V di board fisik |
| A7 | SEDANG | PCB1 | TP4056 HW-373 mengisi default sekitar 1 A (R-prog 1,2k). Baterai 1200 mAh: 0,83C, di atas 0,5C yang umum disarankan | Cek datasheet sel; ganti R-prog sekitar 2k (sekitar 580 mA) |
| A8 | SEDANG | PCB3 | microSD satu bus SPI dengan LoRa (IO18/19/23). Penulisan SD memblokir sampai ratusan ms, paket LoRa bisa hilang | Pisahkan SD ke bus SPI kedua |
| A9 | SEDANG | PCB3 | Tidak ada tombol mute atau LED di Gateway; mute hanya lewat serial `M`. Definisi: operator bisa mematikan alarm | Tombol mute fisik, dan/atau mute dari dashboard (perlu downlink MQTT) |
| A10 | SEDANG | PCB3 | Tidak ada cadangan daya. Mati listrik di dermaga = sistem keselamatan mati | Catat sebagai risiko, atau tambah UPS/powerbank |
| A11 | SEDANG | PCB1 | Tidak ada indikator di Vest (LED/haptic) untuk memberi tahu "SOS terkirim/diterima". HANDOVER: tanpa buzzer di Vest, tapi BOM berisi "LED indikator, buzzer/haptic" | Putuskan: LED/haptic atau hapus dari BOM |
| A12 | MINOR | PCB1 | Urutan pad footprint GY-521 (simbol memberi nomor 8..1, VCC = 8), TP4056, DevKit (jarak baris), SuperMini belum dicocokkan ke modul fisik | Cek satu per satu dengan modul |
| A13 | MINOR | PCB1 | `VBAT_RAW` dan `VBOOST_5V` masih 10 mil untuk arus beberapa ratus mA | Lebarkan 20-30 mil |
| A14 | MINOR | PCB1 | Jalur UART TX ESP ke GPS (IO17) tidak dipakai firmware; saat GPS dimatikan, TX bisa memberi daya lewat dioda proteksi | Boleh tidak disambung |
| A15 | MINOR | PCB3 | Sirine lewat IRLZ44N tanpa dioda flyback (aman untuk buzzer elektronik, tidak untuk beban berkoil) | Pastikan jenis buzzer |

Yang sudah sesuai: 2 tact di Vest (power IO13 RTC, SOS IO27 RTC aktif-HIGH), 18650 + TP4056 USB-C, GPS gating Q1, MPU6050 I2C, pembagi baterai IO35, pin map firmware vs netlist (script OK untuk PCB1 dan PCB3), IRLZ44N logic-level di Gateway, tact on/off + pull-up di Helmet.

## B. Firmware vs definisi

| # | Tingkat | Temuan | Perbaikan |
|---|---|---|---|
| B1 | KRITIS | MOB: firmware memicu `FALL` dan `MOB` sebagai alarm terpisah (OR). Definisi: jatuh AND basah | FALL langsung danger; naik ke MOB jika basah (>=3 s) dalam 60 s setelah jatuh |
| B2 | KRITIS | Paket `PANDU,V1,...` tanpa ID Vest dan nomor urut. Tidak bisa banyak Vest, tidak bisa membuang duplikat SOS | Format biner v2: ID, seq, jenis, lat, lon, baterai, helm, usia posisi |
| B3 | KRITIS | LoRa memakai default library (SF7). Anggaran link sekitar 142 dB; jarak 5 km di atas air perlu SF10-12 | Atur SF, BW, daya lewat konstanta di kedua sisi |
| B4 | KRITIS | Gateway tidak ada WiFi/cloud/pemetaan tahap. Hanya JSON ke serial dan CSV dengan `millis()` | WiFi, NTP, kirim ke server, antrean SD, tahap 1/2/3 |
| B5 | SEDANG | Deteksi jatuh memakai akselerometer saja; definisi menyebut gyroscope. Ambang 0,6 g / 2,5 g belum divalidasi (hanya jatuh ke kasur) | Pertimbangkan laju rotasi; kalibrasi dengan data nyata |
| B6 | SEDANG | SOS dikirim 3x tanpa ACK, heartbeat tetap 30 s tanpa jitter, tidak ada paket OFF (inaktif vs tidak terjangkau tidak bisa dibedakan) | ACK untuk SOS, jitter, paket OFF |
| B7 | SEDANG | Beacon helm tanpa ID: Vest bisa menangkap helm orang lain. Ambang RSSI -85 dBm tebakan | Pairing ID, kalibrasi |
| B8 | SEDANG | Tidak ada downlink Gateway ke Vest (untuk mute/"aku selamat") | Putuskan perlu atau tidak |
| B9 | MINOR | Firmware hanya mengirim posisi terakhir + usia; sat, HDOP, kecepatan, arah tidak dikirim | Tambah jika dashboard menampilkannya |

Sudah sesuai: Helmet beacon + tombol (tanpa sentuh), Vest membaca RSSI, posisi terakhir dengan usia, paket baterai, SOS wake dari tidur, buzzer lokal di Gateway (pola SOS/MOB 500 ms, FALL 200 ms).

## C. Dashboard (`APP/index.html`)

File ini mockup statis (satu pandu, tombol "Mockup state" Safe/Offline/SOS, data hardcode).

| # | Tingkat | Temuan |
|---|---|---|
| C1 | KRITIS | Tidak ada sumber data (tanpa backend/WebSocket), semua teks hardcode |
| C2 | SEDANG | Hanya 3 state: ON STATION / SIGNAL LOST / SOS SENT. Definisi: aman / warning (APD tidak lengkap) / danger. Warning tidak ada; FALL vs MOB tidak dibedakan |
| C3 | SEDANG | Satu pandu ("Capt. A. Ridwan"). Definisi: overseer memantau sampai 8 pandu; perlu daftar dan ringkasan |
| C4 | SEDANG | Peta = SVG statis Tg. Priok, bukan peta live (perlu Leaflet/OpenStreetMap atau peta laut) |
| C5 | SEDANG | Menampilkan baterai helm (%), jumlah satelit, akurasi (m), heading dan kecepatan (kt). Hardware tidak mengirim baterai helm, sat, HDOP, arah, kecepatan |
| C6 | SEDANG | Tombol "I'm safe" dan "Hold to send SOS" di app. Definisi: SOS hanya dari tact Vest. App menyiratkan uplink dan peran pandu sebagai pengguna app, bukan overseer |
| C7 | MINOR | Tidak ada kontrol operator: mute, hapus alarm, log kejadian ("Log ›" belum ada isinya) |
| C8 | MINOR | Label campur Inggris dan Indonesia |

Sudah sesuai: dua indikator yang tersedia (sinyal LoRa dalam dBm, baterai Vest) dan tata letak mobile, peta di tengah, log kejadian terakhir.

## D. Dokumen, BOM, repo

| # | Tingkat | Temuan |
|---|---|---|
| D1 | SEDANG | Folder `hardware/gerber/` memuat versi lama (10-03, 10-06) yang sudah tidak valid, dan semua versi memuat A1-A3. Jangan dipesan |
| D2 | SEDANG | BOM sheet (6 Okt) masih memuat VL53L0X, BME680, AMS1117, CR2032; belum ada boost, MOSFET, LiPo, TP4056 kedua, XKC, saklar |
| D3 | MINOR | `HANDOVER.md` bagian awal usang (mis. "XKC_EN=IO2" vs IO32 di bagian bawah; PCB2 "belum diubah"). `hardware/README.md` menyebut Gerber 3 Okt sebagai terbaru |
| D4 | MINOR | Checklist dan tutorial breadboard masih menyebut TTP223 dan umur CR2032 |
| D5 | MINOR | Laporan kelompok memuat "akurasi sensor 96,2%" tanpa data uji (catatan lama di HANDOVER) |
| D6 | MINOR | Klaim "tahan percikan" belum ada uji |

## E. Belum diperiksa
Footprint dan posisi pad fisik di PCB (GY-521, TP4056, SuperMini, DevKit), hasil DRC terbaru (terakhir 0 error), lebar trek, casing SCAD, dan skematik PCB2 untuk pin map SuperMini terhadap modul fisik.

## F. Ringkasan
- KRITIS: A1, A2, A3, A4, B1, B2, B3, B4, C1 (9 item)
- SEDANG: A5-A11, B5-B8, C2-C6, D1-D2 (21 item)
- MINOR: sisanya
- Yang sudah benar: pin map firmware, 2 tombol, daya Vest, USB-C, gating GPS, beacon + RSSI, logika posisi terakhir.
