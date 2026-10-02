# HANDOVER: PANDU hardware (per 2 Okt 2026)

Penerima: sesi baru (cloud atau lokal). Baca ini dulu, lalu `weekly/WEEK_6/Audit_Skematik_Status.md`.

## Konteks singkat
- Proyek: P.A.N.D.U (Perangkat Alarm Nirkabel Deteksi Urgensi), wearable keselamatan pandu laut. Kelompok 13, user: Calvin (bahasa Indonesia santai).
- Proposal: `weekly/WEEK_2/Proposal Bab 6 ... .pdf`. Riwayat Pekan 2-5: `weekly/WEEK_6/Riwayat_Progres_Pekan2-5.md`. Jangan ulang konten itu di laporan Pekan 6.
- 3 board di EasyEDA Pro project **Pandu-Capstone**: Board1/PCB1 Vest Node Master, Board2/PCB2 Helmet Node, Board3/PCB3 Edge Gateway.
- Sumber kebenaran skematik/PCB = EasyEDA (akun calvinwkatoroy). Repo ini hanya salinan.

## Keputusan yang sudah final
- Sensor Vest: MPU6050, XKC-Y25 (air, non-kontak, VCC 5 V), GPS NEO-6M, LoRa. **Tanpa VL53L0X dan BME680** (false positive anti-crush). Tanpa buzzer di Vest.
- Board ESP32 Vest: **ESP32-DevKitC V4 WROOM-32D (klasik, Micro USB)**, bukan DevKitM-1/C3. Nama part di EasyEDA "ESP32-DEVKITM-1" menyesatkan.
- Daya Vest: 18650 > TP4056 > `VBAT_RAW` (tanpa saklar seri). Boost 5 V selalu aktif memberi pin 5V ESP32 dan `VBOOST_5V`. AMS1117, C1, C2 dihapus.
- SW1 (tact + rubber boot) = input GPIO RTC (IO13), toggle deep sleep di firmware. SOS (SW2) di IO27 (RTC).
- Gating hemat daya: GPS lewat P-MOSFET Q1 (`GPS_EN`=IO4); XKC-Y25 lewat Q2 + level shifter Q5 (`XKC_EN`=IO2). Default OFF saat sleep.
- Casing: PETG, plug silikon bertali untuk USB, SMA bulkhead, boot karet di tombol, gasket di sambungan. Klaim jujur "tahan percikan" kecuali ada uji rendam.

## Status per board
**PCB1 (Vest)**: skematik sudah diperbaiki (RA-02 pin 1 = ANT bukan GND, GND pin 2/9/16, GPS_EN tersambung, gating MOSFET). PCB di-update, auto-route, DRC 0 error, 0 ratline.
**PCB2 (Helmet)**: belum diubah. Risiko brownout CR2032 (tambah 100-220 uF low-ESR di 3V0).
**PCB3 (Gateway)**: EN pull-up + 100 nF, header program J1 1x6, ANT RA-02 diperbaiki, EP ke GND, pull-down gate sirine R3. DRC 0 error. Masih ESP32 **modul polos** WROOM-32.

## BLOCKER (urut prioritas)
1. **Footprint ESP32 di PCB1 salah.** Sekarang 17 pin/sisi, jarak baris 0,9". Board yang dibeli (DevKitC V4) 2x19 pin, jarak baris resmi 25,4 mm (klon kadang 22,86 mm). Tidak ada part siap pakai di library EasyEDA, harus dibuat sendiri (simbol 38 pin + footprint 2x19 THT). **Minta Calvin ukur board fisik** (jarak tengah lubang kiri-kanan, jumlah pin) sebelum membuat.
2. **PCB3**: BOM beli DevKit tapi PCB3 didesain untuk modul polos. Rekomendasi: ganti ke footprint DevKitC V4 yang sama, hapus U4/C1/C2/J1/R2/C3 (DevKit sudah punya regulator dan USB).
3. **Modul LoRa yang dibeli bukan Ra-02**: listing "Wifi LoRa XL1276/SX1276 915MHz" (akhishop, Rp95k, datang dengan antena pegas, 1,8-3,7 V, SPI, foto mirip RFM95). Simbol/footprint RA-02 di PCB1/PCB3 mungkin tidak cocok. Minta foto sisi pin atau datasheet modul, cek urutan pin.
4. Setelah 1-3: lebarkan trek daya (VBAT_RAW, VBAT_POS 20 mil; auto-route menimpa ke 10 mil), DRC, ekspor Gerber PCB1/2/3 baru ke `hardware/`.

## Item terbuka lain
- Gateway: Q1 IRFZ44N bukan logic-level, ganti IRLZ44N (footprint sama). USB-C tanpa resistor CC 5,1k (pakai kabel A-ke-C). Dioda flyback hanya jika beban induktif.
- Pin TP4056 dan boost: urutan harus dicek ke modul fisik.
- Casing SCAD (`weekly/WEEK_6/PANDU_VestNode_Casing.scad`) belum diupdate: TP4056 di sisi Bottom (bukaan USB), posisi boost (kiri), XKC-Y25, plug USB, alur gasket.
- Gerber lama (`weekly/WEEK_6/Gerber`) **jangan dipesan**.
- Laporan Pekan 6 belum ditulis. Catat sebagai perubahan scope: tanpa ToF/BME680, PCB1 di-routing ulang setelah audit, casing dibuat ulang mengikuti PCB.
- BOM sheet (Google Sheets "Bills of Materials") belum di-update oleh tim; Rafif bilang semua sudah dibeli kecuali baris kuning dan PCB. ESP32 Vest dan LoRa Gateway tercentang FALSE padahal link sama (kemungkinan sudah dibeli 2). Harga ESP32 di listing Rp128k vs BOM Rp80k. VL53L0X/BME680 masih di BOM (hapus, hemat Rp250k). Belum ada di BOM: boost 5 V, XKC-Y25, antena+SMA untuk Vest, komponen SMD (AO3401A, 2N7002, resistor), IRLZ44N. Total BOM Rp2,495 jt vs dana Rp2 jt.
- RA-02/LoRa: proposal 915 MHz, modul dibeli 915 MHz (OK). Regulasi Indonesia 920-923 MHz, sebut di laporan.
- Angka "akurasi sensor 96,2%" di laporan kelompok tidak punya data pengujian; cek atau hapus.

## Catatan teknis EasyEDA (penting, UI-nya rapuh)
- Dikendalikan lewat ekstensi Claude-in-Chrome (klik koordinat). **Cloud session tidak bisa menjangkau Chrome lokal Calvin**, jadi pekerjaan EasyEDA harus dilakukan di sesi lokal. Cloud cocok untuk dokumen, laporan, riset, BOM, SCAD.
- Kabel yang digambar dengan klik sering meleset beberapa piksel dari ujung pin dan pin tetap mengambang. Taruh **net label tepat di titik ujung pin**, lalu verifikasi dengan DRC skematik ("Pins floating", baca via get_page_text).
- Jangan `ctrl+a` kecuali fokus pasti di kolom input; di kanvas PCB ia memilih semua objek. Mengetik teks saat fokus di kanvas memicu hotkey. Selalu klik kolom input dulu.
- Edit X/Y komponen lewat panel properti kadang tidak tersimpan; verifikasi dengan zoom ke panel. Drag di kanvas lebih andal.
- Alur PCB: Design > Update PCB from Schematic (Apply Changes), Route > Unroute > All, Route > Auto Routing (Run), Tools > Copper Manager Rebuild All, Ctrl+S, Check DRC.
- Setiap tool hotkey/aksi destruktif: cek tab tidak berasterisk (*) bila tidak ingin perubahan.

## File penting
- `weekly/WEEK_6/PANDU_VestNode_Casing.scad` (+ png render), `PCB1_Verifikasi_Skematik.md` (versi lama), `Audit_Skematik_Status.md` (status terbaru), `Riwayat_Progres_Pekan2-5.md`.
- `weekly/WEEK_6/Gerber/` (LAMA, jangan dipesan).
- `APP/` (di luar repo ini) = dashboard wireframe, repo `pandu-dashboard`.
