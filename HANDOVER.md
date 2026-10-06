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
**PCB3 (Gateway, sudah diganti ke DevKitC, lihat blocker 2)**: EN pull-up + 100 nF, header program J1 1x6, ANT RA-02 diperbaiki, EP ke GND, pull-down gate sirine R3. DRC 0 error. Masih ESP32 **modul polos** WROOM-32.

## BLOCKER (urut prioritas)
1. **[SELESAI di PCB1, 2 Okt malam]** Footprint ESP32 PCB1 sudah diganti ke DevKitC V4 (part LCSC C571181, designator U3, jarak baris resmi 1,0"). Skematik PCB1 tersimpan, PCB di-update, auto-route 0 ratline, DRC 0 error. Yang masih harus dicek: ukuran fisik board klon, dan USB micro DevKit sekarang menghadap ke dalam papan (perhatikan akses di casing). Teks lama:
   **Footprint ESP32 di PCB1 salah.** Sekarang 17 pin/sisi, jarak baris 0,9". Board yang dibeli (DevKitC V4) 2x19 pin, jarak baris resmi 25,4 mm (klon kadang 22,86 mm). **Part siap pakai ADA** di library EasyEDA (System): cari "DevKitC" di tab Device, baris ke-7 (LCSC C571181, nama ESP32-DEVKITC...). Simbol 38 pin (3V3, EN, VP, VN, IO34... GND, IO23, IO22, TX, RX, ... CLK) cocok dengan pinout DevKitC V4, footprint 2x19 THT dengan jarak baris sekitar 1,0" (estimasi dari preview, **ukur setelah ditempatkan**). Tidak perlu membuat dari nol. Tetap minta Calvin ukur board fisik (jarak tengah lubang kiri-kanan) sebelum order PCB.
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

## Pemetaan pin final
- Vest (U3 DevKitC): PWR_BTN=IO13, BTN_SOS=IO27, WATER_SIG=IO34, GPS_EN=IO4, **XKC_EN=IO32** (bukan IO2, strapping), SPI MOSI/MISO/SCK=IO23/19/18, LORA_CS=IO5, LORA_RST=IO25, LORA_DIO0=IO26, I2C SDA/SCL=IO21/22, GPS RX/TX=IO17/16.
- Gateway (U5 DevKitC): SPI IO23/19/18, LORA_CS=IO5, LORA_RST=IO14, LORA_DIO0=IO26, SD_CS=IO13, SIREN_DRV=IO4, 3V3 dan 5V_SYS dari/ke pin DevKit.
- Modul baru yang akan dibeli (kata Calvin): XKC-Y25, boost 5 V; sebaiknya LoRa tipe Ra-02 agar footprint cocok.

## Update 3 Okt 2026 (akhir sesi lokal)
- Gerber ketiga board baru ada di `hardware/gerber/` (DRC 0 error). PCB1: TP4056 diputar 180 (USB-C ke dinding kiri). PCB2: +C2 100 uF tantalum.
- Casing `weekly/WEEK_6/PANDU_VestNode_Casing.scad` v5 (standoff 9 mm, boost di atas DevKit, ekstensi micro-USB DevKit di dinding bawah). Asumsi yang perlu diverifikasi: tinggi modul TP4056 + header (~8,5 mm), tinggi holder baterai.
- Draft laporan Pekan 6: `weekly/WEEK_6/draft_isian_Pekan6.md` (butuh keputusan tim di bagian [ISI]).
- Sisa: cek fisik modul (LoRa bukan Ra-02, TP4056, boost), pesan modul kurang (XKC-Y25, boost), VBOOST_5V masih 10 mil, casing Helmet dan Gateway belum, firmware belum.

## Versi (6 Okt 2026)
- **v1** = kondisi sebelum perbaikan netlist: tag git `v1` (Gerber 3 Okt, netlist 6 Okt) dan version node EasyEDA `v1-sebelum-perbaikan` (File > Version Control > Version Management; buka node itu untuk revert).
- **v2** = branch git `v2` untuk perbaikan: konektor antena PCB1/PCB3, backfeed 5V, pull-up SD_CS, kapasitor bulk 3V3 PCB1. Di EasyEDA, v2 dikerjakan di `main` (revert lewat node v1).
- Temuan lengkap: `hardware/netlist/` (PCB1-3 .tel + check_netlist.py).

## v2 (6 Okt 2026): perbaikan dari cek netlist (branch `v2`, EasyEDA `main`)
Gerber v2: `hardware/gerber/Gerber_PCB1_2026-10-06.zip` dan `Gerber_PCB3_2026-10-06.zip` (DRC 0 error). PCB2 tidak berubah (pakai Gerber 3 Okt). Netlist terbaru: `hardware/netlist/` (cek: `python check_netlist.py`).
- PCB1: + header 2 pin H1 untuk antena (pigtail ke SMA, `LORA_ANT` sekarang terhubung ke RA-02 pin 1, `GND`); + C1 100 uF tantalum di 3V3_SYS; + D1 SS14 antara `VBOOST_5V` (anoda) dan pin 5V DevKit (`5V_DK`, katoda) agar USB DevKit tidak backfeed ke boost/baterai.
- PCB3: USB-C (USB1) dihapus, hanya micro-USB DevKit (satu port); + R2 10k pull-up SD_CS ke 3V3; + H2 header antena; Q1 IRFZ44N diganti IRLZ44N (logic-level, footprint TO-220 vertikal).
- Catatan: sirine di PCB3 sekarang disuplai lewat jalur 5V DevKit/USB (arus sirine lewat konektor micro-USB; cek rating adaptor dan jalur DevKit). Antena: sambung pigtail U.FL/SMA ke H1/H2 manual.
- Belum: modul fisik belum diverifikasi, PCB2 (dioda D1 + CR2032 vs ESP32), casing Helmet/Gateway, firmware Gateway.

- PCB2 (v2): dioda D1 1N5819 dihapus (drop 0,3-0,45 V membuat modul < 3,0 V dari CR2032); SAW1.OUTPUT langsung ke `3V0_HELMET`. DRC 0 error, Gerber `hardware/gerber/Gerber_PCB2_2026-10-06.zip`. Arus puncak BLE vs CR2032 tetap perlu uji nyata (cadangan: Li-ion kecil / 2xCR2032).

- PCB1 (v2, +pembagi baterai): R6/R7 100k + C2 100 nF, `VBAT_RAW` > `BAT_SENSE` > IO35 (ADC1_CH7). Firmware menambah kolom mV baterai di semua paket LoRa: `PANDU,V1,<jenis>,<lat>,<lon>,<mV>`. Drain pembagi ~21 uA. Kalibrasi `BAT_DIV` dengan multimeter. DRC 0 error; Gerber PCB1 tanggal 6 Okt diganti versi terbaru.

- PCB2 (v2, +tombol on/off): tact switch SW1 (tanpa saklar geser tambahan) antara `PWR_BTN` dan GND, pull-up R1 100k ke `3V0_HELMET`, `PWR_BTN` = GPIO4 SuperMini (pin RTC/deep sleep C3 = GPIO0-5). Firmware Helmet (belum ada) harus toggle deep sleep seperti Vest: tekan = tidur, tekan lagi = bangun (`esp_deep_sleep_enable_gpio_wakeup` aktif-LOW). SAW1 (saklar geser) tetap sebagai isolasi baterai penuh. DRC 0 error, Gerber `Gerber_PCB2_2026-10-06.zip` diganti, netlist `PCB2.tel` diperbarui.

## Status Vest Node (6 Okt 2026, v2)
Firmware: SOS bangun dari sleep dan langsung kirim (3x ulang), alert baru dikirim segera (tanpa tunggu 5 s), FALL/MOB 2x ulang, baterai mV di tiap paket. Casing v5 tidak perlu diubah untuk v2 (SMA bulkhead sudah ada; header antena/dioda/pembagi rendah). Belum: lebarkan trek VBAT_RAW (auto-router + clearance bentrok, 10 mil cukup untuk ~0,5 A rata-rata), uji perangkat nyata, kalibrasi ambang jatuh dan BAT_DIV.

## Firmware Helmet (6 Okt 2026)
`firmware/helmet_node/` (PlatformIO, ESP32-C3 SuperMini, NimBLE). Hanya BLE advertising 'PANDU-HELM', manufacturer data `FF FF 'P' 'H' worn counter`. Dipakai = TOUCH_SIG (GPIO2) stabil 1 s, lepas = 5 s. Tombol GPIO4 = toggle deep sleep (wake GPIO aktif-LOW). Advertising 1 s, 0 dBm, refresh tiap 10 s. Kompilasi OK, belum diuji perangkat. Belum ada: Vest men-scan BLE ini (field 'helm dipakai' di paket LoRa). Tidak ada sensor baterai di Helmet.

- Helmet firmware v2 (hemat daya): Arduino-ESP32 bawaan tanpa CONFIG_PM_ENABLE -> light sleep+BLE tidak tersedia, diganti duty-cycle deep sleep (bangun tiap 8 s, burst BLE 400 ms, state di RTC memory; tombol GPIO4 = toggle ON/OFF, OFF = tidur tanpa timer). Estimasi rata-rata ~1,5-2 mA (belum diukur), lebih baik dari ~15-20 mA sebelumnya. Latensi status helm ~8-24 s. Vest harus menyimpan status helm dengan timeout >= 30 s.

- Vest scanner BLE (6 Okt): NimBLE pasif, interval 62,5 ms/window 31 ms, scan terus-menerus; paket helm = manufacturer data FF FF 'P' 'H' worn counter. Paket LoRa sekarang: `PANDU,V1,<jenis>,<lat>,<lon>,<mV>,<helm>` dengan helm 1=dipakai, 0=terdengar tidak dipakai, 2=tidak terjangkau (timeout 30 s, juga 2 setelah bangun sampai paket pertama ~8 s). Konsekuensi: scan terus menambah arus Vest (perkiraan +10-15 mA, ukur) -> kalau boros, ganti ke scan berkala. Gateway/dashboard harus mem-parse field ke-7. Kompilasi OK (flash 48%), belum diuji.

## Firmware Gateway (6 Okt 2026)
`firmware/gateway/` (PlatformIO, DevKitC V4). Terima LoRa 915 MHz, parse `PANDU,V1,<jenis>,<lat>,<lon>,<mV>,<helm>`, keluarkan JSON per baris di serial 115200 (tambahan rssi/snr), log CSV ke SD (/pandu.csv), sirine (IO4 HIGH): SOS/MOB 500 ms, FALL 200 ms, otomatis berhenti 60 s tanpa alert baru, kirim 'M' di serial untuk mute. Peringatan `vest_lost` setelah 90 s tanpa paket (sirine mati secara default, `SIREN_ON_LOST`). Kompilasi OK (flash 26%), belum diuji. Belum: ACK ke Vest, enkripsi/otentikasi paket, tombol mute fisik (PCB3 tidak punya), jembatan serial -> dashboard.
