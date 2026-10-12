# Ringkasan alat PANDU (sesuai definisi proyek yang disepakati)

Per 10 Okt 2026. Catatan status menunjukkan mana yang sudah jalan di breadboard dan mana yang masih rencana.

## 1. Helmet Node

**Tidak ada sensor.** Deteksi "helm dipakai" memakai sinyal BLE dan ambang RSSI, bukan sensor sentuh.

| Komponen | Fungsi |
|---|---|
| ESP32-C3 SuperMini | Pengendali dan radio BLE (beacon) |
| Tact switch ON/OFF (GPIO4) | Menyalakan atau mematikan beacon |
| LiPo 3,7 V + modul TP4056 USB-C berproteksi | Daya dan pengisian; B- dipisah dari GND agar proteksi aktif |
| Header jumper (J1), resistor pull-up 100 kΩ, kapasitor 10 µF dan 100 µF | Pemutus jalur baterai, pull-up tombol, penyaring daya |

**Cara kerja**
- ON: helm menyiarkan beacon BLE; Vest mengukur RSSI. Kuat = dekat (dipakai), lemah = jauh, tidak terdengar = OFF atau terlalu jauh.
- Firmware produk memakai deep sleep berkala: bangun tiap 8 detik, siaran 0,4 detik.
- Status: beacon dan tombol jalan di breadboard; ambang RSSI (-85 dBm) belum dikalibrasi.

## 2. Vest Node

| Sensor/Komponen | Fungsi |
|---|---|
| MPU-6050 (GY-521) | Deteksi jatuh dari akselerometer (free-fall lalu benturan) |
| Sensor air non-kontak XKC-Y25 | Mendeteksi air di balik casing (prototipe sekarang masih sensor analog kontak) |
| GPS NEO-6M | Koordinat; dinyalakan hanya saat perlu lewat MOSFET untuk hemat daya |
| Modul LoRa SX1276 (915/920 MHz) | Mengirim paket ke Gateway |
| ESP32 DevKit (WROOM-32) | Pengendali; BLE scanner membaca beacon Helmet |
| 2 tact switch | Power/tidur (IO13) dan SOS manual (IO27) |
| Baterai Doublepow 18650 1200 mAh + TP4056 USB-C + boost 5 V | Daya dan pengisian lewat USB-C |
| Pembagi tegangan (IO35) | Memantau tegangan baterai |

**Logika**
- **FALL:** free-fall <0,6 g selama ≥120 ms, lalu benturan >2,5 g dalam 1 detik. Jatuh saja sudah dianggap bahaya.
- **MOB:** FALL **dan** basah ≥3 detik dalam 60 detik.
- **SOS:** tombol ditahan 2 detik; tombol ini juga membangunkan alat dari tidur.
- **Status helm:** dekat, jauh, atau tidak terdengar (batas 30 detik).
- **Heartbeat:** paket berkala 30 detik berisi posisi terakhir (beserta usianya), tegangan baterai, dan status helm. Bila heartbeat berhenti, Gateway menandai Vest "tidak terjangkau/inaktif" (warning).
- Status: logika diuji di breadboard lewat serial; pengiriman lewat LoRa belum diuji.

## 3. Edge Gateway (di dermaga)

**Tidak ada sensor.** Fungsinya penerima, pencatat, dan pemberi alarm.

| Komponen | Fungsi |
|---|---|
| ESP32 DevKit | Pengendali dan WiFi ke cloud |
| Modul LoRa SX1276 | Menerima paket dari sampai 8 Vest |
| Modul microSD (bus SPI terpisah) | Log insiden dan buffer saat internet putus (store-and-forward) |
| MOSFET IRLZ44N + buzzer/sirine | Alarm lokal di Gateway |
| Adaptor 5 V | Daya |
| Tombol mute | Belum ada di PCB (rencana) |

**Fungsi**
- Memetakan setiap paket ke **stage 1 (aman), 2 (warning), atau 3 (danger)**.
- Buzzer berpola: SOS dan MOB 500 ms, FALL 200 ms.
- Alarm padam otomatis saat kondisi normal; operator dapat mute atau dismiss.
- Mengirim data ke cloud lewat WiFi (cap waktu dari NTP) dan menyimpan ke microSD saat internet putus.
- Status: firmware baru ter-compile, belum diuji di papan; WiFi, cloud, dan ACK untuk SOS belum dibuat.

## 4. Dashboard

**Tech stack:** keputusan belum final (K6: Supabase atau Firebase). Laporan Pekan 7 menyebut **Supabase (BaaS)**, dibangun Rafif, dengan target real-time dan cepat. Isi "Mosquitto, InfluxDB, FastAPI" di dek proposal belum sesuai dan perlu diselaraskan.

**Yang ditampilkan** (hanya data yang benar-benar dikirim hardware):
- Daftar sampai 8 Vest dengan warna stage (1 hijau, 2 warning, 3 danger).
- Peta posisi live (lat/lon beserta usia posisi).
- Jenis kejadian: SOS, FALL, atau MOB.
- Baterai Vest.
- Status helm (dipakai, tidak dipakai, tidak terdengar).
- Kekuatan sinyal LoRa (RSSI/SNR).
- Waktu terakhir terdengar dan status "tidak terjangkau/inaktif".
- Log insiden.
- Kontrol operator: mute dan dismiss alarm.

**Tidak perlu ditampilkan** (hardware tidak mengirim): baterai helm, jumlah satelit, arah, kecepatan. Tombol "I'm safe" dan "Hold to send SOS" di aplikasi juga tidak diperlukan, karena SOS hanya dari tombol di Vest.

Mockup `APP/index.html` yang sekarang belum sesuai (satu pandu, 3 state statis, data hardcode).
