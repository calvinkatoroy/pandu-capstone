# Revisi Laporan Pekan 7 (tanpa redundansi dengan Pekan 6)

Prinsip: Pekan 7 hanya memuat yang BARU sejak Pekan 6. Hal yang sudah dilaporkan di Pekan 6 cukup dirujuk ("lihat Laporan Pekan 6"). Tanda `[ISI: ...]` = diisi anggota yang bersangkutan, aku tidak punya datanya.

## 1. Redundansi yang ditemukan (P6 vs P7)

| Bagian | Di P7 | Tindakan |
|---|---|---|
| 1 Ringkasan Project | Sama persis dengan P6 (termasuk salah ketik "MPU-6059") | Persingkat 2-3 kalimat atau "Sama dengan Pekan 6". Perbaiki: MPU-6050, "LoRa point-to-point" (bukan LoRaWAN) |
| 2 Ringkasan | Mengulang P6 (revisi skematik, casing alternatif, wireframe dashboard, komponen datang) | Ganti ringkasan baru di bawah |
| 4 Baris 1 | "Schematic final setelah revisi" = isi baris "Order PCB" P6 (false positive, sensor air non-kontak) | Hapus atau ganti ke revisi hasil audit |
| 5 Calvin | Teks tugas SAMA PERSIS dengan P6 (audit, AMS1117, re-route DRC 0, casing OpenSCAD, cross-check BOM) | Ganti teks baru di bawah |
| 5 Yoga | Teks tugas SAMA PERSIS dengan P6 | `[ISI Yoga: simulasi assembly 3D, hasil kecocokan lubang baut. Target P6 10 Okt]` |
| 5 Gibran, Rifat | Mengulang "revisi skematik Vest Node untuk false positive" dari P6 | Isi kerja Pekan 7 saja (rakit prototipe, tes) |
| 6 Software | Wireframe dashboard + repo, sama dengan P6 | Tulis "Wireframe: lihat P6", hanya laporkan yang baru |
| 6 Mekanik | Sama persis (Fusion 360, blueprint 55×65×23) | Hapus, rujuk P6 |
| 7 Dokumentasi | Gambar 3D, blueprint, PCB, foto paket, foto tim, screenshot dashboard SAMA dengan P6 | Hapus; sisakan foto prototipe, log tes, screenshot PCB/skema terbaru |
| 8 Tabel dan analisis casing | Baris "kesesuaian dimensi casing" dan analisisnya sudah ada di P6 | Hapus dari P7 |
| 9 Kendala | Kendala "ganti sensor air non-kontak" sudah dibahas di P6 | Ganti kendala baru (bagian 9 di bawah) |
| 10 Deviasi | Tabel Minggu 1-5 diulang semua; analisis mengulang P6 (IP67, false positive) | Sisakan baris Minggu 6-8, ringkas |
| 11 Rencana | "Simulasi assembly" dan "design dashboard" dari P6 tidak dilaporkan hasilnya | Laporkan hasilnya atau jelaskan kenapa pindah |
| 13 Kesimpulan | Kosong | Isi (di bawah) |

Catatan: dimensi casing bertentangan sejak P6 (55×65×23, gambar 55×65×18, tinggi 65→70, Calvin 114×101×36,6). Samakan dulu dengan Yoga sebelum dikumpulkan.

## 2. Teks siap tempel

### 2. Ringkasan Kemajuan Pekanan
Pekan ini kegiatan bergeser dari perancangan ke implementasi. Vest Node dan Helmet Node dirakit di atas breadboard, firmware ketiga node dibuat, dan logic Vest Node (FALL, MOB, SOS) serta deteksi helm lewat BLE RSSI diuji dan berjalan. Audit ulang desain terhadap definisi proyek menemukan beberapa kesalahan skematik yang kemudian direvisi pada PCB Helmet dan Gateway. Integrasi LoRa Vest ke Gateway dan pemesanan PCB belum dilakukan dan dilanjutkan pekan depan.

### 3. Target Pekan Ini (saran penamaan agar tidak duplikat P6)
1. Perakitan prototipe breadboard Vest Node dan Helmet Node: Tercapai
2. Pembuatan firmware Vest, Helmet, Gateway: Tercapai (Gateway baru ter-compile, belum diuji di papan)
3. Pengujian logic fitur satu per satu: Tercapai sebagian (FALL, SOS, air, helm BLE; belum: LoRa, GPS di luar ruangan, baterai)
4. Revisi skematik/PCB hasil audit: Sebagian (PCB Helmet dan Gateway; Vest belum)

### 4. Realisasi Kegiatan (baris baru)
| Kegiatan | Hasil |
|---|---|
| Prototipe breadboard | Vest (ESP32, MPU6050, GPS NEO-6M, sensor air, tombol SOS dan power) dan Helmet (SuperMini + tombol, beacon BLE) dirakit. |
| Firmware dan pengujian logic | Vest: FALL (free-fall lalu benturan), MOB (jatuh lalu basah dalam 60 detik), SOS (tahan 2 detik), status helm dari RSSI. Paket `PANDU,V1,...` tercetak di serial. Helmet: beacon BLE, tombol ON/OFF. Gateway: ter-compile. |
| Audit dan revisi desain | Audit terhadap definisi proyek: 9 temuan kritis (lihat `docs/AUDIT_V2.md`). PCB Helmet dan Gateway direvisi, DRC 0. |
| Pengadaan | `[ISI Rafif: status modul yang masih dipesan: LoRa kedua, boost, MOSFET, sirine, LiPo]` |

### 5. Calvin Wirathama Katoroy (tugas baru Pekan 7)
- Merakit prototipe Vest Node di breadboard dan menguji fitur satu per satu: FALL, SOS, sensor air, GPS (first fix), beacon BLE Helmet dengan RSSI.
- Memperbarui firmware Vest: MOB = jatuh lalu basah dalam 60 detik, status helm dari ambang RSSI, status serial berkala, firmware Helmet baru (beacon + tombol, tanpa sensor sentuh).
- Mengaudit desain terhadap definisi proyek (`AUDIT_V2.md`, 9 temuan kritis) dan merevisi PCB Helmet (BAT_NEG agar proteksi TP4056 aktif, tanpa TTP223, saklar diganti header) serta PCB Gateway (microSD di bus SPI terpisah), DRC 0.
- Menyusun BOM v2 dan tutorial demo tanpa LoRa.

### 6. Hasil Implementasi
Hardware: prototipe Vest dan Helmet di breadboard terintegrasi lewat BLE; PCB belum difabrikasi (dalam revisi); LoRa belum diuji.
Software: firmware tiga node ada; dashboard tidak berubah dari P6 `[ISI Rafif: tech stack Supabase + rencana skema data]`.
Mekanik: tidak ada perubahan, lihat P6 `[ISI Yoga jika ada]`.

### 7. Dokumentasi: hanya foto prototipe, screenshot log tes, skematik/PCB hasil revisi.

### 8. Pengujian (jujur terhadap bukti)
| Parameter | Target | Hasil | Status |
|---|---|---|---|
| Deteksi FALL, MOB, SOS di breadboard | Terdeteksi, paket tercetak | Paket `PANDU,V1,...` muncul di serial (belum dikirim lewat LoRa). FALL diuji di kasur, ambang perlu validasi lapangan. | Lulus (serial) |
| Deteksi helm via BLE RSSI | helm=1 dekat, 2 tidak terdengar | Status berubah sesuai kondisi helm. Ambang -85 dBm belum dikalibrasi. | Lulus |
| LoRa Vest ke Gateway | Paket sampai | Belum diuji | Belum |
| GPS | Fix posisi | Dapat satelit tapi lemah di dalam ruangan | Sebagian |

Hapus baris casing (sudah di P6). Hapus kata "paketnya terkirim", ganti "tercetak di serial".

### 9. Kendala (baru, nyata)
| Kendala | Dampak | Solusi |
|---|---|---|
| Footprint LoRa (RA-02) tidak cocok dengan modul fisik (pinout RFM95, pitch lebih kecil dari 2,54 mm) | PCB belum bisa dipesan | Modul diganti Ra-02 SX1278 433 MHz (breakout 2,54 mm); footprint diganti female header 2x8 setelah modul diukur |
| Proteksi TP4056 terlewati karena negatif baterai ke GND | Risiko over-discharge/korslet | Pisahkan BAT_NEG (sudah di PCB Helmet, PCB Vest belum) |
| GPS NEO-6M cold start lama dengan antena keramik | Fix lambat | Uji di luar ruangan, antena aktif/modul multi-konstelasi |
| ESP32 brownout/reset saat BLE menyala dengan daya USB | Demo tidak stabil | Kabel pendek-tebal, kapasitor 100 µF, firmware demo tanpa deteksi brownout |
| microSD berbagi bus SPI dengan LoRa | Paket LoRa bisa hilang | SD dipindah ke bus SPI sendiri (PCB Gateway) |

### 10. Deviasi: sisakan baris Minggu 6, 7, 8; hapus Minggu 1-5.
Analisis: PCB belum dipesan karena audit menemukan kesalahan yang harus diperbaiki dulu; pemesanan menunggu uji tautan LoRa.

### 11. Rencana Pekan Berikutnya (saran)
1. Uji tautan LoRa Vest ke Gateway (jarak dan SF) - PIC `[ISI]`
2. Revisi PCB Vest (BAT_NEG, footprint LoRa, sensor air) lalu DRC - Calvin
3. Pesan PCB hanya setelah tes LoRa lolos dan modul dicek fisik - Gibran, Rifat
4. Gateway: WiFi, penyimpanan SD, tahap 1/2/3 - `[ISI]`
5. Dashboard: skema data multi-vest (sampai 8), peta live - Rafif
6. Simulasi assembly dan finalisasi casing - Yoga

### 12. Progress (opsional, lebih jujur)
Angka P7 sekarang: 80/50/10/50/70/45 = 52,25%. Karena LoRa, Gateway, dan GPS luar ruangan belum teruji serta ada 9 temuan kritis, usulan: Perancangan 75, Hardware 45, Software 15, Integrasi 30, Pengujian 45, Dokumentasi 45 = 44,25%. Keputusan tim.

### 13. Kesimpulan
Pekan ini tim berhasil merakit dan menguji prototipe Vest dan Helmet di breadboard: deteksi FALL, MOB, SOS, dan status helm via BLE RSSI berjalan. Audit desain menemukan kesalahan pada skematik dan footprint yang sedang diperbaiki, sehingga PCB belum dipesan. Prioritas pekan depan: uji tautan LoRa ke Gateway, revisi PCB Vest, dan pengembangan Gateway serta dashboard.
