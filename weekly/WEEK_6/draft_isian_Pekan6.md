# Draft isian: LAPORAN KEMAJUAN Pekan 6 Group 13

Periode: 28 Sep - 3 Okt 2026. Hanya hal BARU di Pekan 6 (Pekan 2-5 lihat `Riwayat_Progres_Pekan2-5.md`).
Bagian bertanda `[ISI]` perlu diputuskan tim. Angka dan temuan di bawah sudah diverifikasi lewat EasyEDA (DRC 0 error) dan OpenSCAD.

## Ringkasan
Pekan ini fokus mematangkan desain hardware setelah audit skematik. Routing PCB Vest Node diulang, daya diubah (AMS1117 dihapus, boost 5 V, gating GPS dan sensor air lewat MOSFET), board ESP32 disamakan dengan komponen yang dibeli (ESP32-DevKitC V4), dan casing Vest Node dibuat ulang mengikuti PCB. Ketiga PCB sudah memiliki Gerber baru dengan DRC 0 error.

## Perubahan scope (catat di laporan)
- Sensor VL53L0X (anti-crush) dihapus: berisiko banyak false positive saat pandu menempel dinding kapal tanpa terjepit. Deteksi difokuskan ke jatuh (MPU-6050) dan Man Overboard (sensor air). BME680 sudah dihapus sejak Pekan 2.
- Buzzer di Vest Node dihapus. Alarm bunyi ada di Edge Gateway.
- Sensor air diganti ke XKC-Y25 (non-kontak) untuk ketahanan korosi air laut; membutuhkan 5 V sehingga ditambah modul boost.

## Realisasi kegiatan (tabel Pekan 6)
| Kegiatan | Hasil |
|---|---|
| Audit skematik 3 PCB | Ditemukan: AMS1117 tidak dapat 3,3 V dari Li-ion (dropout), dua sumber 3V3 paralel, tombol sesaat dipakai sebagai saklar daya, pin 1 RA-02 salah dihubungkan ke GND (itu pin antena), GND tambahan RA-02 belum tersambung, ESP32 Gateway tanpa rangkaian program/EN, gate MOSFET sirine tanpa pull-down. Dokumen: `Audit_Skematik_Status.md`. |
| Perbaikan PCB1 (Vest) | Daya: U3/C1/C2 dihapus, TP4056 ke VBAT_RAW, boost 5 V untuk ESP32 dan XKC-Y25. Tombol power jadi input GPIO (deep sleep di firmware). Gating GPS dan XKC-Y25 via MOSFET (standby hemat). RA-02 diperbaiki. Footprint ESP32 diganti ke DevKitC V4. TP4056 di sisi bawah dan diputar agar USB-C menghadap dinding. Trek VBAT_POS 20 mil. DRC 0 error. |
| Perbaikan PCB3 (Gateway) | ESP32 diganti ke DevKitC V4, regulator dan header program dihapus (sudah ada di DevKit), RA-02 diperbaiki, pull-down gate sirine, SD_CS dipindah dari pin strapping. DRC 0 error. |
| Perbaikan PCB2 (Helmet) | Ditambah C2 100 uF tantalum 6,3 V di rel CR2032 untuk menahan lonjakan arus BLE. Outline diperpanjang. DRC 0 error. |
| Gerber ketiga board | `hardware/gerber/` (3 Okt 2026). Belum dipesan. |
| Casing Vest Node v5 | Dibuat ulang mengikuti PCB1: 114 x 101 x 36,6 mm (PETG). Bukaan: USB-C charging (dinding kiri), ekstensi micro-USB DevKit dan SMA (dinding bawah), plunger tombol power/SOS di tutup, boost digantung di tutup. Validasi dimensi otomatis lulus. |
| Cross-check BOM | Ditemukan selisih BOM vs desain (lihat bawah). |

## Selisih BOM vs desain (butuh tindak lanjut Rafif/Gibran)
- Hapus: VL53L0X x2 (Rp80k) dan BME680 (Rp170k) -> hemat Rp250k.
- Tambah: XKC-Y25, modul boost 5 V, antena + SMA bulkhead untuk Vest, MOSFET (AO3401A, 2N7002), resistor/kapasitor, IRLZ44N (Gateway), kapasitor tantalum 100 uF (Helmet), kabel ekstensi panel-mount micro-USB.
- ESP32 DevKit dan LoRa Vest/Gateway: BOM menandai FALSE padahal link sama dengan yang TRUE; konfirmasi jumlah.
- Modul LoRa yang dibeli (SX1276 915 MHz, bentuk RFM95/XL1276) BUKAN Ra-02; footprint PCB memakai Ra-02. Dinilai: beli Ra-02 atau sesuaikan footprint.
- Harga ESP32 di listing Rp128k vs BOM Rp80k. Total BOM Rp2,495 jt vs dana Rp2 jt.

## Kendala dan solusi
| Kendala | Solusi |
|---|---|
| Desain awal tidak cocok dengan komponen yang dibeli (ESP32 dan LoRa) | Desain disesuaikan: footprint DevKitC V4; LoRa menunggu konfirmasi |
| Port USB beberapa modul menghadap ke dalam papan, tidak terjangkau dari dinding | TP4056 diputar 180 derajat; DevKit memakai kabel ekstensi panel-mount |
| Auto-router menimpa lebar trek daya | Dilebarkan manual per net; VBOOST_5V dan VBAT_RAW tetap 10 mil karena clearance |

## Belum selesai / rencana Pekan 7
1. Ukur board ESP32 fisik (jarak baris pin) dan cek urutan pin LoRa, TP4056, boost sebelum order PCB.
2. Pesan modul yang kurang; update BOM dan kolom harga final.
3. Uji rakit di breadboard/perfboard sebelum fabrikasi.
4. Firmware: deep sleep + wake RTC, kontrol GPS_EN/XKC_EN, deteksi jatuh.
5. Casing Helmet Node dan Gateway disesuaikan ke PCB baru.
6. Persentase progres: `[ISI]` (PCB 3 unit desain selesai, belum fabrikasi).

## Dokumentasi (gambar)
- `PANDU_VestNode_Casing.png`, `_exploded.png`, `_top.png` (render OpenSCAD v5).
- Screenshot EasyEDA PCB1/PCB2/PCB3 (ambil ulang dari editor; folder screenshots sengaja tidak di repo).

## Catatan sebelum disubmit
- Angka "akurasi sensor 96,2%" di laporan kelompok lama tidak punya data pengujian; hapus atau lengkapi datanya.
- Samakan penyebutan ESP32 (proposal WROOM-32; laporan lama C3/DevKitM-1; desain final DevKitC V4 WROOM-32D).
- Gerber lama di `weekly/WEEK_6/Gerber` jangan dipesan.
