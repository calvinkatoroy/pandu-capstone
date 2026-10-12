# Audit progresi PANDU, Pekan 2-7 (10 Okt 2026)

Tujuan: mencocokkan klaim tiap pekan dengan bukti (repo, hasil uji, audit v2) dan jadwal Gantt proposal. Sumber: laporan kelompok dan individu Pekan 2-7 (`weekly/`), `Riwayat_Progres_Pekan2-5.md`, `docs/AUDIT_V2.md`, `docs/BOM_V2.md`, riwayat git, dek proposal (Canva).

Penilaian: **Terbukti** = ada artefak atau hasil uji. **Dilebih-lebihkan** = klaim lebih besar daripada bukti atau terbantah audit. **Tidak terverifikasi** = tidak ada bukti di repo (bisa benar, tapi belum ada artefaknya).

## 1. Bukti objektif yang tersedia

- Repo `pandu-capstone` baru dibuat 2 Okt (Pekan 6). Commit: 2 Okt (5), 3 Okt (7), 6 Okt (15), 8 Okt (4) = 31 commit. Tidak ada commit pada 5, 7, 9 Okt, dan tidak ada sebelum 2 Okt.
- Artefak Pekan 2-5 hanya ada sebagai laporan (`WEEK_2`-`WEEK_5`); tidak ada file desain di repo untuk periode itu.
- Hasil uji nyata baru ada di Pekan 7: log serial FALL/MOB/SOS/air/GPS/BLE, tanpa LoRa.

## 2. Klaim per pekan vs bukti

| Pekan | Klaim | Bukti / temuan | Penilaian |
|---|---|---|---|
| 2 | On-site visit SPJM, BME680 dipangkas, draft BoM, skenario jadi Proof of Concept. Progres 16,25% | Tidak ada artefak di repo selain laporan; konsisten dengan keputusan scope berikutnya | Tidak terverifikasi (masuk akal) |
| 3 | Skematik 3 unit selesai (EasyEDA). Draft casing 55x65x18 mm. Wireframe Figma. 24,25% | Audit Pekan 6 dan v2 menemukan kesalahan di skematik "selesai": AMS1117 tak dapat 3,3 V dari Li-ion, dua sumber 3V3 paralel, pin 1 RA-02 salah, rangkaian EN Gateway hilang | Dilebih-lebihkan |
| 4 | PCB Vest dan Helmet "selesai", Gateway kendala routing. Casing direvisi 18 ke 23 mm tebal, 65 ke 70 mm tinggi. 27,25% | Pekan 6 merouting ulang PCB1 dan menyebut klaim itu belum final; Gerber 3 dan 6 Okt tidak berlaku (SAW1, proteksi TP4056, footprint LoRa). Laporan menyebut ESP32-C3/DevKitM-1, proposal ESP32-WROOM-32 | Dilebih-lebihkan |
| 5 | Dashboard marine pilot dan supervisor (wireframe HTML/CSS/JS). Menunggu endpoint ESP32 | Repo `pandu-dashboard` tidak diperiksa; `APP/index.html` adalah mockup statis (satu pandu, data hardcode). Endpoint belum ada sampai Pekan 7 | Terbukti sebagai mockup; blokir 3 pekan |
| 6 | Audit 3 board, DRC 0 error, Gerber 3 board, casing v5 114x101x36,6 mm, cross-check BOM. 29% | Artefak ada (Gerber, casing, BOM). Tapi audit v2 menemukan 9 temuan kritis, jadi desain tidak boleh dipesan. Riwayat menulis casing tinggi 30,6 mm, laporan individu 36,6 mm | Terbukti sebagai artefak; "siap fabrikasi" dilebih-lebihkan |
| 7 (kelompok) | Skematik/PCB final, DRC 0, Gerber diekspor; semua komponen tiba; sensor air non-kontak di prototipe; FALL/MOB/SOS "paketnya terkirim"; 52,25% | Gerber lama dibatalkan (`_obsolete`); BOM v2: LoRa kedua, boost, MOSFET, sirine, LiPo belum ada; prototipe memakai sensor air analog (kontak); paket hanya tercetak di serial (`LoRa=0`) | Dilebih-lebihkan (lihat tab Pekan 7 Revisi) |
| 7 (individu Calvin) | Prototipe, firmware, uji fitur, audit 9 kritis, revisi PCB2/PCB3 (DRC 0), BOM v2, tutorial | Commit fd760d8, c07ba35, cde3e0a, 9ba8900, firmware/, hardware/netlist/, docs/ | Terbukti |

## 3. Pola yang berulang

1. **"PCB selesai/final" dinyatakan tiga kali (Pekan 4, 6, 7)**, dan ketiganya terbantah audit v2. Penyebab: desain dibuat dari library, bukan dari modul fisik, dan belum diuji di breadboard.
2. **Dimensi casing tidak konsisten sejak Pekan 4:** 55x65x18, 55x65x23, tinggi 70 mm, 114x101x30,6, 114x101x36,6. Blueprint 55x65 mm tidak mungkin memuat DevKit + 18650 + LoRa + GPS.
3. **Perubahan scope tidak ikut ke dokumen lain:** VL53L0X (anti-crush), BME680, TTP223, CR2032 dihapus dari desain, tapi masih ada di dek proposal (slide 4, 5, 9, indikator 10) dan sebagian dokumen.
4. **Tech stack tidak konsisten:** proposal (Mosquitto, InfluxDB, FastAPI, React, Mapbox, AES) vs laporan (Supabase BaaS) vs kenyataan (Gateway belum punya WiFi atau cloud).
5. **Spesifikasi LoRa tidak konsisten:** proposal 50-330 m dan 920 MHz (AS923-2); slide 5 menulis 915 MHz; definisi proyek ~5 km; modul fisik pita belum terverifikasi; library masih SF7.
6. **Angka "akurasi sensor 96,2%"** muncul di laporan kelompok tanpa data uji.
7. **Logbook individu Pekan 6** meninggalkan Senin-Rabu `[ISI]` dan total jam `[ISI]`; Pekan 7 juga masih menyisakan hari tanpa isi (perlu diisi sebelum dikumpulkan).
8. **Ketergantungan dashboard ke hardware** (endpoint ESP32) tidak pernah dipecahkan; dashboard belum punya skema data.
9. **Ejaan nama:** "Avincena" (dek proposal) vs "Avicena" (laporan).

## 4. Progres vs jadwal (Gantt proposal, 17 minggu)

| Fase | Jadwal | Kondisi Pekan 7 | Selisih |
|---|---|---|---|
| F1 Procurement & Setup | Mgg 1-2 | Sebagian besar; komponen untuk Gateway/PCB final belum lengkap | Terlambat sebagian |
| F2 Implementasi Hardware | Mgg 2-6 | Prototipe breadboard baru Pekan 7; PCB belum dipesan | Terlambat ~1 minggu |
| F3 Implementasi Software | Mgg 3-7 | Firmware 3 node ada; Gateway cloud, dashboard, paket v2 belum (software 10-15%) | Terlambat |
| F4 Integrasi Subsistem | Mgg 7-10 | Baru Helmet ke Vest via BLE; LoRa dan Gateway belum | Baru mulai |
| F5 Testing & Validation | Mgg 10-14 | Uji fitur awal (serial); belum LoRa, RSSI, baterai, IP67 | Awal lebih cepat dari jadwal |

Pekan 8 = presentasi UTS; sisa 10 pekan untuk integrasi, uji lapangan, dan penyempurnaan.

## 5. Progres total: klaim vs usulan berbasis bukti

| Komponen | Bobot | Pekan 6 | Pekan 7 (klaim) | Usulan berbasis bukti |
|---|---|---|---|---|
| Perancangan | 25 | 80 | 80 | 75 |
| Implementasi Hardware | 20 | 25 | 50 | 45 |
| Implementasi Software | 20 | 10 | 10 | 15 |
| Integrasi Sistem | 15 | 0 | 50 | 30 |
| Pengujian | 15 | 5 | 70 | 45 |
| Dokumentasi | 5 | 25 | 45 | 45 |
| **Total** | 100 | **29%** | **52,25%** | **44,25%** |

Lompatan klaim Pekan 6 ke 7 (+23,25 poin) sebagian besar dari Integrasi (0 ke 50) dan Pengujian (5 ke 70). Bukti mendukung kenaikan, tapi tidak sebesar itu: integrasi baru Helmet-Vest lewat BLE, dan semua uji lewat serial tanpa LoRa.

## 6. Tindakan

1. Pakai tab "Pekan 7 (Revisi)" untuk laporan kelompok; ubah angka progres sesuai keputusan tim.
2. Satukan dimensi casing (satu angka final) dengan Yoga; perbarui blueprint 2D.
3. Perbarui dek proposal/progress UTS: hapus VL53L0X, BME680, TTP223, CR2032; samakan tier (3 stage), stack cloud, dan frekuensi LoRa; hapus slide template IoT tersembunyi (20-32); perbaiki ejaan nama.
4. Isi logbook hari yang masih kosong dan total jam sebelum dikumpulkan.
5. Cantumkan di Pekan 8: hasil uji LoRa, kalibrasi RSSI, revisi PCB1, dan keputusan tech stack backend.
6. Jangan klaim "final" untuk PCB sampai ada uji LoRa dan Gerber baru; gunakan gerbang di `PLAN_REVISI.md`.
