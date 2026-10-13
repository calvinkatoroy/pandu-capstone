# Revisi dan tambahan presentasi PANDU untuk UTS (Minggu 8, 17 Okt 2026)

Dasar: dek Canva "Proposal_Group13_PANDU" (32 slide) dibaca penuh pada 10 Okt, dicocokkan dengan hasil audit (`AUDIT_V2.md`), BOM v2, hasil uji prototipe, dan Laporan Pekan 7 (tab Revisi).
Tujuan presentasi UTS (dari rencana Pekan 7): arsitektur, progres terhadap timeline, hasil pengujian awal, status pengadaan, dan demo prototipe breadboard.
Dek saat ini adalah **proposal**. Untuk UTS ia harus berubah menjadi **laporan progres**: sebagian besar slide lama dipertahankan sebagai konteks (maksimal 5-6 slide), sisanya diganti dengan slide status, hasil uji, audit, dan demo.

Tanda: **[UBAH]** revisi slide yang ada, **[HAPUS]**, **[BARU]** tambahan, **[ISI]** perlu diisi anggota yang bersangkutan.

---

## 1. Struktur dek yang disarankan (±16 slide utama + lampiran)

| No | Slide | Status | Sumber |
|---|---|---|---|
| 1 | Cover | [UBAH] ejaan nama, tambah "Laporan Progres UTS" | slide 1 |
| 2 | Ringkasan proyek dan klien (gabung profil + problem) | [UBAH] | slide 2, 3 |
| 3 | Solusi dan scope | [UBAH] | slide 4 |
| 4 | Perubahan desain sejak proposal | [BARU] | audit, laporan |
| 5 | Arsitektur terkini | [UBAH] ganti gambar | slide 5, 7 |
| 6 | Prototipe breadboard | [BARU] | foto prototipe |
| 7 | Stage alarm dan logika deteksi | [UBAH] | slide 9 |
| 8 | Gateway dan backend | [UBAH] | slide 8 |
| 9 | Hasil pengujian awal | [BARU] | log serial |
| 10 | Indikator keberhasilan: target vs status | [UBAH] | slide 12-14 |
| 11 | Audit desain: 9 temuan kritis dan perbaikan | [BARU] | AUDIT_V2 |
| 12 | Status PCB dan pengadaan | [BARU] + [UBAH] | slide 15, BOM v2 |
| 13 | Progres terhadap Gantt | [UBAH] | slide 16 |
| 14 | Kendala dan risiko | [BARU] | laporan |
| 15 | Rencana Pekan 8-10 | [BARU] | PLAN_REVISI |
| 16 | Demo | [BARU] | tutorial demo |
| 17 | Penutup | [UBAH] | slide 17 |
| L1-L4 | Lampiran: pin map, format paket, SOP-AI (rencana), anggaran | [BARU]/[UBAH] | slide 10, 11, 15 |

Slide SOP-AI (10) dan skenario T+10 detik (11) dipindah ke lampiran dan diberi label "rencana/target". Slide 19-32 (template IoT tersembunyi) dihapus.

---

## 2. Revisi per slide yang sudah ada

### Slide 1 Cover [UBAH]
- Ejaan: "M Gibran Arya **Avincena**" menjadi "**Avicena**" (laporan memakai "Avicena").
- Tambah subjudul "Laporan Progres UTS, Pekan 7" dan tanggal.
- Logo, foto kapal, dan susunan anggota dipertahankan.

### Slide 2 Profil klien dan Slide 3 Problem [UBAH]
- Gabung menjadi satu slide agar muat: kiri klien (Pelindo Jasa Maritim, pilotage/towage/fleet management), kanan tiga masalah (pilot ladder 56% non-compliance menurut IMPA, MOB, APD lemah).
- Pertahankan referensi (IMPA Safety Campaign 2025). Gambar ilustrasi yang buram diganti versi resolusi lebih tinggi.

### Slide 4 Core idea [UBAH]
- Ganti kutipan: "Wearable Safety Multi-Modul untuk pandu kapal dengan Deteksi **Fall + Man Overboard (MOB)** + **APD compliance**, dengan Emergency Beacon LoRa + GPS untuk rescue dispatch dalam detik."
- **Hapus "Anti-Crush"** dan **"Bridge environmental (BME680) sebagai bonus telemetry"** (keduanya sudah dibuang).
- Scope v1 baru: "Fase boarding dan navigasi pandu. Cellular, TinyML, dan SOP-AI adalah pengembangan lanjutan."

### Slide 5 Arsitektur dan Slide 7 Komponen sistem [UBAH, gambar dibuat ulang]
Gambar lama masih menampilkan komponen yang sudah dibuang. Buat ulang dengan isi berikut:

| Blok | Isi yang benar sekarang |
|---|---|
| Helmet Node | ESP32-C3 SuperMini, tombol ON/OFF (GPIO4), beacon BLE, LiPo + TP4056 (**bukan** TTP223 dan CR2032) |
| Vest Node Master | ESP32 DevKit (WROOM-32), MPU-6050, GPS NEO-6M, sensor air (analog di prototipe, XKC-Y25 non-kontak direncanakan), LoRa Ra-02 SX1278 433 MHz, tombol SOS dan power, 18650 + TP4056 + boost 5 V (**bukan** VL53L0X dan BME680) |
| Edge Gateway | ESP32 + LoRa, microSD (bus SPI terpisah), buzzer lewat MOSFET, WiFi |
| Cloud/Dashboard | [ISI Rafif] sesuai keputusan stack (lihat slide 8) |
| Tautan | Helmet ke Vest: BLE (RSSI); Vest ke Gateway: LoRa 433 MHz; Gateway ke cloud: WiFi |

Slide 7 (diagram blur) cukup dihapus jika slide 5 sudah jelas.

### Slide 6 Gambar perangkat [UBAH]
Render AI perangkat (ada kamera dan layar yang tidak ada di desain) tidak sesuai. Ganti dengan **render casing v5 (OpenSCAD)** dan **foto prototipe breadboard**. Tulis dimensi casing yang disepakati dengan Yoga (lihat bagian 6, item 1).

### Slide 8 Edge Gateway dan Cloud backend [UBAH]
Ganti isi kolom dengan yang akurat:

- **Gateway:** ESP32 + LoRa Ra-02 SX1278 433 MHz sebagai penerima; microSD sebagai buffer store-and-forward dan log insiden; buzzer lokal; WiFi di dermaga; NTP untuk waktu.
- **Backend:** [ISI Rafif] Supabase (real-time) atau Firebase, sesuai keputusan tim. Hapus "Mosquitto, InfluxDB, FastAPI" kalau stack berubah.
- **Keamanan:** tulis "AES pada payload LoRa: direncanakan" (belum diimplementasi).
- **Status:** "Firmware Gateway ter-compile; WiFi, cloud, dan uji di papan belum."
- Hapus "sirine/strobo" kalau hanya buzzer.

### Slide 9 Tier [UBAH menjadi stage]
Definisi proyek memakai **3 stage**, bukan 4 tier. Ganti isi:

| Stage | Kondisi | Respons |
|---|---|---|
| 1 Aman | Semua normal, helm terdeteksi | Heartbeat berkala, tampil hijau di dashboard |
| 2 Warning | APD tidak lengkap (helm tidak terdeteksi/jauh) atau Vest tidak mengirim (tidak terjangkau/inaktif) | Notifikasi ke dashboard |
| 3 Danger | SOS manual (tombol), FALL, atau MOB (jatuh lalu basah dalam 60 detik) | Beacon LoRa + koordinat GPS, buzzer Gateway, eskalasi tim rescue |

Catatan di slide: alarm padam otomatis saat kondisi normal; operator dapat mute/dismiss. Hapus "haptic di rompi" dan "anti-crush".

### Slide 10 SOP-AI (RAG + LLM) [UBAH, pindah ke lampiran]
Beri label besar "**Rencana pengembangan lanjutan, belum diimplementasikan**". Hapus klaim apa pun yang menyiratkan sudah berjalan.

### Slide 11 Skenario T+0 s sampai T+10 s [UBAH, lampiran]
Tulis "target skenario" dan "belum diukur". Latensi nyata tergantung SF LoRa (waktu udara SF12 ±2 detik untuk satu paket) ditambah jitter heartbeat.

### Slide 12-14 Indikator keberhasilan [UBAH menjadi tabel target vs status]
Gabung menjadi 1-2 slide dengan kolom baru **Status Pekan 7**. Isi usulan:

| No | Parameter | Target (revisi) | Status Pekan 7 | Rencana uji |
|---|---|---|---|---|
| 1 | Durasi operasi | ≥8-12 jam, baterai **18650 1200 mAh** (bukan 1500) | Belum diukur | Uji discharge |
| 2 | BLE helm-Vest | 1-5 m, ambang RSSI ≈ -85 dBm | Sebagian: status dekat/jauh/tidak terdengar bekerja; ambang belum dikalibrasi | Kalibrasi jarak |
| 3 | Jarak LoRa | [ISI: samakan 50-330 m vs ~5 km] pada pita 433 MHz | Belum diuji (modul sudah dua, uji tautan berikutnya) | Uji lapangan |
| 4 | PDR dan latensi | PDR ≥95%, latensi ≤30 s | Belum diuji | Uji LoRa |
| 5 | GPS | 5-10 m | Sebagian: dapat satelit, fix lemah di dalam ruangan | Uji luar ruangan |
| 6 | Suara alarm | ≥85 dB | Belum (sirine belum dibeli) | Sound level meter |
| 7 | Log luring | ≥100 log di microSD | Firmware ada, belum diuji di papan | Uji SD |
| 8 | Deteksi jatuh | Free-fall <0,6 g ≥120 ms lalu benturan >2,5 g dalam 1 s | Sebagian: terdeteksi di kasur; belum drop test | Uji jatuh terkontrol |
| 9 | Deteksi MOB | Jatuh **AND** basah ≥3 s dalam 60 s | Sebagian: logika berjalan; sensor analog, XKC belum | Uji perendaman |
| 10 | ~~Anti-crush~~ | Dihapus dari scope | - | - |
| 11 | Kepatuhan APD | Helm tidak terdengar >30 s memicu Stage 2 | Sebagian: status helm bekerja | Uji fungsi |
| 12 | Klasifikasi urgensi | **3 stage** (aman, warning, danger) | Logika di firmware; Gateway belum | Uji state machine |
| 13 | Ketahanan fisik | PETG, IP67 (uji rendam 1 m, 30 menit) | Belum | Uji rendam. Jangan tulis "tersertifikasi" |
| 14 | Biaya | BOM ≤ Rp2.000.000 per unit | Perlu dihitung ulang (slide 15) | Audit BOM |
| 15 | Dashboard | Peta live, status APD, update real-time | Mockup statis; backend belum | Rafif |

### Slide 15 Anggaran [UBAH]
Tabel lama: pengeluaran Rp2.495.000 vs pemasukan Rp2.000.000 (defisit Rp495.000). Perbarui:
- Komponen dibuang: VL53L0X ×2 dan BME680 (hemat sekitar Rp250.000 menurut perhitungan Pekan 6).
- Komponen ditambah: XKC-Y25, boost 5 V, MOSFET, modul LoRa kedua, TP4056 kedua, LiPo, sirine, antena/pigtail.
- [ISI Rafif/Gibran] angka final dari sheet BOM. Tampilkan juga selisih terhadap dana Rp2.000.000 dan rencana menutupnya.

### Slide 16 Gantt [UBAH menjadi Gantt rencana vs aktual]
Tambah baris bayangan "aktual" dan garis "Pekan 7 (sekarang)". Isi:

| Fase | Rencana | Aktual Pekan 7 |
|---|---|---|
| F1 Procurement | Mgg 1-2 | Sebagian besar; modul Gateway/PCB final belum lengkap |
| F2 Hardware | Mgg 2-6 | Prototipe breadboard Pekan 7; PCB belum dipesan |
| F3 Software | Mgg 3-7 | Firmware 3 node ada; Gateway cloud, dashboard belum |
| F4 Integrasi | Mgg 7-10 | Baru Helmet-Vest (BLE) |
| F5 Testing | Mgg 10-14 | Uji fitur awal lewat serial |

Tambahkan milestone "Order PCB" setelah uji LoRa lolos.

### Slide 17 Penutup [UBAH]
Ganti klaim menjadi pencapaian terukur ("prototipe Vest dan Helmet berjalan, audit menangkap 9 temuan kritis sebelum fabrikasi"), bukan hanya slogan.

### Slide 18 Terima kasih [pertahankan]; Slide 19-32 [HAPUS]
Template IoT tersembunyi (19-32) dihapus agar tidak ikut terekspor atau terbuka saat presentasi.

---

## 3. Slide baru yang perlu ditambahkan

### B1. Perubahan desain sejak proposal
Tabel: item, proposal, sekarang, alasan.

| Item | Proposal | Sekarang | Alasan |
|---|---|---|---|
| Anti-crush | 2× VL53L0X | Dihapus | Mengurangi false positive dan biaya |
| Lingkungan | BME680 | Dihapus | Tidak relevan untuk keselamatan |
| Deteksi helm | TTP223 sentuh | Tombol ON/OFF + beacon BLE + RSSI | Lebih andal, tanpa sensor kontak |
| Baterai Helmet | CR2032 | LiPo + TP4056 | CR2032 tidak kuat untuk lonjakan BLE dan tidak bisa diisi ulang |
| Daya Vest | AMS1117 | Boost 5 V | Li-ion tidak memberi 3,3 V stabil lewat AMS1117 |
| Sensor air | Kontak | Non-kontak (XKC-Y25, direncanakan) | Menghindari celah kebocoran casing |
| Alarm | 4 tier | 3 stage | Disederhanakan sesuai operasi lapangan |
| MOB | Air + orientasi + GPS | Jatuh DAN basah dalam 60 s | Lebih sederhana dan dapat diuji |
| Backend | Mosquitto/InfluxDB/FastAPI | [ISI Rafif] (Supabase) | Cepat dibangun dan real-time |

### B2. Prototipe breadboard
Foto Vest dan Helmet (sudah ada di laporan), diagram sambungan sederhana, dan satu baris per modul. Sertakan foto baterai 18650 dan TP4056 HW-373.

### B3. Hasil pengujian awal (jujur)
Slide tabel dengan angka nyata:

| Fitur | Hasil | Catatan |
|---|---|---|
| FALL | Terdeteksi (free-fall <0,6 g ≥120 ms, benturan >2,5 g) | Uji di kasur; belum drop test |
| SOS | Tahan 2 detik memicu paket SOS, diulang 3×; tombol membangunkan dari deep sleep | Lulus |
| Sensor air | Kering ±150-250 mV, basah ±1700-2000 mV; ambang 1000 mV | Sensor analog (kontak) |
| MOB | Jatuh lalu basah ≥3 s dalam 60 s memicu MOB; basah saja tidak | Logika di firmware |
| Helm via BLE | Status dekat/jauh/tidak terdengar; ambang -85 dBm | Belum dikalibrasi |
| GPS | Dapat satelit; fix lemah di dalam ruangan | NEO-6M GPS-only |
| Paket | `PANDU,V1,...` tercetak di serial | **Belum dikirim lewat LoRa** |

Tempel screenshot log serial (log helmet dan log Vest dari laporan Pekan 7) sebagai bukti.

### B4. Audit desain: 9 temuan kritis
Tabel ringkas (dari AUDIT_V2): SAW1 salah komponen, proteksi TP4056 terlewati, footprint LoRa tidak cocok, XKC ke IO34 tanpa pembagi, logika MOB, paket tanpa ID/seq, LoRa default SF7, Gateway tanpa WiFi/cloud, dashboard statis. Kolom "Perbaikan" dan "Status" (PCB2 dan PCB3 selesai, PCB1 menunggu). Pesan: **audit sebelum fabrikasi menyelamatkan biaya PCB yang salah**.

### B5. Status PCB dan pengadaan

| Board | Status |
|---|---|
| PCB1 Vest | Menunggu revisi (BAT_NEG, footprint LoRa, sensor air, lebar trek) |
| PCB2 Helmet | Direvisi, DRC 0 |
| PCB3 Gateway | Direvisi (SD di SPI terpisah), DRC 0; footprint LoRa menunggu |
| Gerber | Versi lama dibatalkan; Gerber baru setelah uji LoRa lolos |

Pengadaan: modul LoRa kedua (sepasang identik), boost, MOSFET, sirine, LiPo masih dipesan [ISI Rafif].

### B6. Kendala dan risiko
Footprint dan pita LoRa; brownout dan GPS lambat; jadwal software tertinggal; ketergantungan dashboard ke endpoint. Kolom mitigasi dan PIC.

### B7. Rencana Pekan 8-10
Uji LoRa Vest ke Gateway (SF, daya, jarak); revisi PCB1 dan footprint LoRa; kalibrasi RSSI dan ambang jatuh; GPS luar ruangan; paket biner v2 (ID Vest, seq); Gateway WiFi + cloud; dashboard multi-vest; order PCB setelah gerbang lolos.

### B8. Demo
Urutan 3-4 menit (lihat bagian 5). Satu slide berisi urutan dan gambar setup dua laptop.

### Lampiran L1-L3
Pin map Vest/Gateway/Helmet; format paket `PANDU,V1,<tipe>,<lat>,<lon>,<mV>,<helm>,<usia>`; rumus airtime LoRa (SF7 vs SF12) dan alasan target 5 km perlu SF10-12.

---

## 4. Fakta yang harus konsisten di semua slide

| Hal | Nilai yang dipakai |
|---|---|
| Nama anggota | M Gibran Arya **Avicena** |
| MCU Vest/Gateway | ESP32 DevKit (WROOM-32) |
| MCU Helmet | ESP32-C3 SuperMini |
| IMU | **MPU-6050** (bukan 6059) |
| LoRa | SX1278 (Ra-02), LoRa **point-to-point** (bukan LoRaWAN); pita 433 MHz (keputusan final: modul SX1278 tidak bisa 915/920) |
| Baterai Vest | Doublepow 18650 **1200 mAh** |
| Alarm | 3 stage |
| Deteksi helm | BLE RSSI (bukan sensor sentuh) |
| Casing | [ISI: satu dimensi final dengan Yoga] |

Klaim yang jangan dipakai: "paket terkirim lewat LoRa", "PCB final/selesai", "akurasi 96,2%", "IP67 tersertifikasi", "AES terimplementasi", "SOP-AI berjalan".

---

## 5. Skrip demo (3-4 menit) dan cadangan

1. **Boot:** Vest `Boot: MPU=1 LoRa=0`, Helmet `beacon ON`.
2. **Helm terdeteksi:** `helm=1` di status Vest; tekan tombol Helmet lalu `helm=2` setelah 30 detik (tidak terjangkau).
3. **SOS:** tahan tombol SOS 2 detik; paket `PANDU,V1,SOS` muncul.
4. **FALL lalu MOB:** jatuhkan Vest ke bantal; `jendela MOB` jalan; celupkan sensor air ≥3 detik; paket MOB muncul. Lalu tunjukkan basah saja tidak memicu alarm.
5. Tutup dengan tabel "yang belum" (LoRa, Gateway, dashboard).

Cadangan: rekam video demo yang sama; siapkan screenshot log; bawa kabel USB pendek dan kapasitor 100 µF; build `demo_usb` bila terjadi reset. GPS tidak perlu fix di dalam ruangan (`NOFIX` normal).

---

## 6. Keputusan dan data yang perlu dilengkapi

1. Dimensi casing final (55×65 vs 114×101×36,6): Calvin dan Yoga.
2. Jarak target LoRa (pita sudah 433 MHz; 330 m vs ~5 km) dan regulasi 433 MHz: seluruh tim.
3. Stack backend dan dashboard (Supabase vs MQTT): Rafif.
4. Angka anggaran terbaru: Rafif dan Gibran.
5. Foto prototipe dan screenshot log yang lebih lengkap: Rifat dan Gibran.

---

## 7. Antisipasi pertanyaan dosen

| Pertanyaan | Jawaban jujur |
|---|---|
| Kenapa PCB belum dipesan? | Audit menemukan kesalahan kritis (saklar, proteksi baterai, footprint LoRa); dipesan setelah revisi dan uji LoRa. |
| Berapa jangkauan LoRa? | Belum diuji. Budget link menunjukkan SF10-12 diperlukan untuk target jauh; uji lapangan dijadwalkan. |
| Bagaimana mencegah false positive MOB? | MOB butuh jatuh **dan** basah ≥3 s dalam 60 s; basah saja atau jatuh saja tidak memicu MOB (jatuh tetap Stage 3). |
| Berapa akurasi deteksi? | Belum ada data kuantitatif; baru uji fungsional. Drop test terkontrol direncanakan. |
| Baterai berapa jam? | Belum diukur; target 8-12 jam; uji discharge direncanakan. |
| Kenapa BLE bukan sensor sentuh? | Lebih andal untuk status "dipakai" lewat RSSI dan tombol ON/OFF; ambang dikalibrasi. |
| Kenapa tanpa anti-crush? | Mengurangi false positive dan biaya; bisa ditambahkan nanti. |
| Bagaimana IP67? | Rencana uji rendam 1 m, 30 menit pada casing PETG; belum dilakukan. |
| SOP-AI sudah ada? | Belum; ini pengembangan lanjutan. |
| Apa yang terjadi jika Vest hilang sinyal? | Gateway menandai "tidak terjangkau/inaktif" (Stage 2) bila heartbeat berhenti. |
