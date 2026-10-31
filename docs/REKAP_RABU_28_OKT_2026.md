# Rekap kerja minggu 26-31 Okt 2026 (fokus Rabu 28 Okt)

Sumber: riwayat sesi, jejak file (waktu ubah), log serial, DRC EasyEDA, dan hasil uji hari itu. Catatan jujur: **semua jejak file di minggu ini jatuh pada Rabu 28 Okt**. Senin-Selasa dan Kamis-Sabtu tidak ada perubahan file atau commit yang tercatat; kalau ada kerja di hari itu, tambahkan manual. **Belum ada commit apa pun di dua repo sejak 23 Okt** (semua di bawah masih berupa perubahan lokal).

Sebelum minggu ini (sudah ada di `CATATAN_PEKAN8.md` dan laporan kumulatif 23 Okt): modul LoRa 433 MHz dibeli, firmware paket v2, perbaikan keamanan dashboard, laporan individu kumulatif Pekan 2-7.

## A. Hardware dan BOM
1. **Konfirmasi daftar belanja terhadap BOM** dan ukuran modul (p x l, cm): SuperMini 2,24x1,38; GPS NEO-6M 3,5x2,65; Ra-02 2,8x2,05; GY-521 2,0x1,6; ESP32 "U" 4,8x2,8; DevKit V1 Type-C 5,15x2,85 (15 pin per sisi); holder 18650 7,65x2,05 (tinggi ±2,1); TP4056 HW-373 2,75x1,7 (pad bukan pitch breadboard); microSD 2,9x4,15; MT3608 ±3,7x1,7 (belum dibeli); tact 2 pin 0,6x0,6.
2. **Status pembelian dikoreksi:** XKC-Y25-V dan 2 antena sudah ada; TP4056 baru 1 (perlu 2); MT3608, MOSFET, dioda, resistor belum ada; saklar geser dan LiPo dibatalkan.
3. **Keputusan desain:** Helmet dan Vest sama-sama 18650 1200 mAh (tanpa LiPo); jumper pengganti saklar geser; buzzer sebagai sirine; IRLZ44N diganti 2N7002 (PCB3 Q1); PCB1 hapus R1 dan tambah R8 10 k / R9 20 k (pembagi XKC); pin 5 V DevKit V1 bernama **VIN**.
4. **Riset live:** halaman botland (charger) diblok Cloudflare 403; spesifikasi TP4056 dari Open Electronics (1 A, cutoff 2,4 V, OUT+/OUT- untuk beban); MT3608 ±37x17 mm; XKC (kabel 50 cm, coklat VCC, kuning sinyal, biru GND, hitam opsi); pin 5V SuperMini menerima 3,3-6 V.
5. **Dokumen:** `BOM_V2.md` bagian 7 (ukuran) dan bagian 8 (daftar beli MOSFET/dioda/resistor, breadboard vs PCB).

## B. EasyEDA dan PCB
1. Akses EasyEDA Pro lewat browser control; proyek tim `Pandu-Capstone` (Board1 Vest, Board2 Helmet, Board3 Gateway).
2. Temuan: semua jalur PCB1 10 mil (default 0,254 mm), clearance 0,2 mm, min 5 mil; board PCB1 107,95 x 95,25 mm, 2 layer, 28 net; DRC bersih (124 item).
3. **Uji pelebaran jalur permintaan dosen:** 253 jalur ke 16 mil, 128 jalur net daya ke 25 mil. Hasil DRC **188 pelanggaran clearance** (EasyEDA otomatis menyimpan). **Dibatalkan (undo), DRC ulang bersih**, filter seleksi di-reset. Kesimpulan: perlu rute ulang atau board lebih besar; pelebaran bertahap per net sambil cek DRC.
4. Belum: skematik dan netlist PCB2/PCB3, footprint DevKit V1 / Ra-02 / TP4056.

## C. Rakit dan uji hardware
1. Panduan rakit breadboard (daftar A) untuk Vest, Helmet, Gateway; Helmet dengan baterai 18650 + TP4056 (OUT+/OUT-); XKC lewat pembagi 10 k/20 k ke D34 dan daya dari VIN; tes buzzer aktif/pasif.
2. Perintah PowerShell untuk upload dan monitor (`;` bukan `&&`), cek port COM (Vest COM7, Gateway COM8).
3. **Vest:** `MPU=1 LoRa=1`; error I2C berulang (`Wire Error 263/-1`) lalu hilang setelah kontak diperbaiki; `g=4.8` saat diam (seharusnya ±1,0; kalibrasi belum); XKC kering terbaca 142 mV; helm RSSI -54 sampai -88 dBm; heartbeat terkirim.
4. **Gateway:** `lora:1`; **menerima paket asli Vest lewat LoRa** (RSSI -84 sampai -92 dBm, SNR ±9,8) = tautan LoRa Vest-Gateway terbukti; `sd:0` (`f_mount failed`, belum teratasi).
5. **WiFi:** "kalpinoo" ternyata hanya 5 GHz (ESP32 tidak bisa); setelah band 2,4 GHz diaktifkan Gateway `wifi:1`, NTP sinkron.
6. **Baterai Vest demo:** pin IO35 mengambang membuat `bat_mv` acak (284-1950) dan **ditolak server**; dipasang pembagi demo 2 x 100 k dari 3V3 (±3300 mV) lalu diterima.
7. **Terbukti ujung ke ujung dengan hardware asli:** Vest, LoRa, Gateway, WiFi, ingest, database, dashboard (Vest 01 tampil, WARNING baterai rendah).

## D. Backend dan dashboard (`pandu-dashboard`)
1. Cek repo: `master`/`pat` hanya merge PR Rifat (isi sama dengan commit `410fbaf`); dua commit redesign (`redesign-peta-melayang`) **belum di-push**; 23 tes lulus.
2. **Project Supabase lama tidak ada** (NXDOMAIN lewat 1.1.1.1 dan 8.8.8.8).
3. **Supabase lokal di Docker:** CLI lewat npx, `supabase init`, port bawaan 543xx bentrok dengan port yang dicadangkan Windows lalu dipindah ke 563xx; semua migrasi 0001-0005 + seed berhasil; fungsi `ingest` di-serve dengan device key acak (gitignored); dashboard diarahkan ke Supabase lokal via `.env.local`; akun uji admin lokal.
4. **Bug ditemukan dan diperbaiki:** signup gagal ("Database error saving new user") karena fungsi trigger tanpa skema `public`; perbaikan `0006_fix_signup_trigger.sql` (juga harus dijalankan di project hosted nanti).
5. Uji API: HB dan SOS simulasi, dashboard berubah **realtime ke BAHAYA**; catatan: `lat` harus `null` (bukan `"NOFIX"`).
6. Firmware Gateway: dukungan `http://` untuk uji LAN (`main.cpp`), `config.h` lokal (gitignored).
7. Dashboard dibuka dan diperiksa lewat browser control (login, halaman Peta, Log).

## E. Audit menyeluruh
`AUDIT_V3.md`: 4 kritis, 7 tinggi, 8 sedang, 3 proses. Inti: alarm bisa ditolak server karena `bat_mv` di luar rentang dan dibuang Gateway (terbukti hari ini); LoRa tanpa CRC/sync word/autentikasi; SOS dari bangun deep sleep tanpa posisi; deteksi jatuh gagal diam-diam; signup terbuka; tidak ada umpan balik SOS; sirine hanya bisa dimute lewat serial; SD belum jalan; timeout upload 8 s terlalu pendek.

## F. File yang berubah (belum di-commit)
- `pandu-capstone`: `docs/BOM_V2.md`, `docs/AUDIT_V3.md`, `docs/REKAP_RABU_28_OKT_2026.md`, `firmware/gateway/src/main.cpp`, `firmware/test_lora_one/src/main.cpp`, folder baru `firmware/lora_probe/` dan `firmware/lora_rst_dio0/` (dari sebelum 24 Okt), `weekly/LAPORAN_INDIVIDU_TERBARU/`.
- `pandu-dashboard`: `supabase/config.toml`, `supabase/.gitignore`, `supabase/migrations/0006_fix_signup_trigger.sql`; cabang `redesign-peta-melayang` belum di-push.

## G. Belum selesai
Kalibrasi MPU (`g=4.8`); SD Gateway; uji basah dan polaritas XKC; GPS fix di luar ruangan; SOS, jatuh, MOB dari hardware ke dashboard; MT3608 dan TP4056 kedua (daya baterai Vest); footprint PCB dan pelebaran jalur; perbaikan K1-K4 dari audit; project Supabase bersama; commit dan push.
