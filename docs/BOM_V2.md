# BOM PANDU (desain v2, per 8 Okt 2026; Gateway diperbarui 11 Nov 2026)

**11 Nov 2026: Edge Gateway = pure gateway, tanpa sirine/buzzer.** Dihapus dari PCB3 dan BOM: Q1 (IRLZ44N, lalu 2N7002), R1 220 ohm, R3 100 k, terminal sirine U2, sirine/strobo, H2. Firmware Gateway tanpa kode sirine.

Sumber: netlist `hardware/netlist/PCB1.tel`, `PCB2.tel`, `PCB3.tel`, firmware, dan hasil tes sesi ini. Tanpa harga (harga final ikut invoice di sheet "Bills of Materials").
Kolom **Status** diambil dari checklist sheet BOM (6 Okt) dan percakapan; belum tentu terkini, cek ulang dengan Rafif/Gibran.
Tanda **PERLU DIPERBAIKI** = item di desain/EasyEDA yang salah atau belum cocok dengan komponen fisik (lihat HANDOVER.md).

## 1. Vest Node Master (PCB1)
| Ref | Komponen | Jml | Status / catatan |
|---|---|---|---|
| U3 | ESP32-DevKitC V4 (WROOM-32) | 1 | Ada. Cek jarak baris pin (25,4 vs 22,86 mm) |
| U8 | GY-521 (MPU6050) | 1 | Ada, tes jatuh jalan. Urutan footprint belum dicek |
| U9 | GPS NEO-6M + antena keramik | 1 | Ada, dapat fix (sinyal lemah). Antena aktif eksternal disarankan |
| U6 | Modul LoRa Ra-02 SX1278 433 MHz (breakout 28x20 mm, header 2,54 mm) | 1 | **Sudah dibeli (sepasang, 13 Okt).** Footprint PCB diganti female header 2x8 (lihat LORA_RA02_BREAKOUT.md). XL1276 915 MHz lama tidak dipakai |
| U10 | Sensor air non-kontak XKC-Y25-V (digital high/low, 5-24 V, kabel XH2.54-4P) | 1 | **Sudah dibeli (13 Okt).** PCB: header XH 4 pin, pembagi R8 10 k / R9 20 k ke IO34, hapus R1, kapasitor di VBOOST_5V (riak ≤ 200 mV). Sensor air analog murah = cadangan tes |
| BT1 | Holder 18650 | 1 | Ada |
| - | Baterai 18650 1200 mAh | 1 | Ada |
| U7 | Modul TP4056 USB-C berproteksi (HW-373 V1.2.1) | 1 | **Ada 1 (28 Okt); modul kedua masih dicari (satu untuk Vest, satu untuk Helmet).** **PERLU DIPERBAIKI:** B- dan OUT- sama-sama GND (proteksi terlewati). Pin bukan pitch breadboard (lihat bagian 7) |
| U2 | Modul boost MT3608 (set 5,0 V), header 1x4 | 1 | Belum ada |
| D1 | Dioda SS14 (SMA) | 1 | Belum ada |
| Q1, Q2 | MOSFET P-channel AO3401A (SOT-23) | 2 | Belum ada. Q2 mungkin tidak perlu lagi jika XKC dibuang |
| Q5 | MOSFET N-channel 2N7002 (SOT-23) | 1 | Belum ada. Sama, mungkin tidak perlu |
| R1, R2 | Resistor 10 k (0603) | 2 | R1 dihapus untuk sensor analog. R2 = pull-down SOS |
| R3, R4, R5, R6, R7 | Resistor 100 k (0603) | 5 | R6/R7 = pembagi baterai |
| C1 | Kapasitor 100 uF (case B 3528) | 1 | |
| C2 | Kapasitor 100 nF (0603) | 1 | |
| SW1, SW2 | Tact switch SMD (TS-1088-AR02016) | 2 | Power dan SOS |
| H1 | Header 2 pin 2,54 mm | 1 | Untuk pigtail antena LoRa |
| - | Antena pegas 433 MHz U.fl 3 dBi (kabel ±15 cm) | 1 | **Sudah dibeli.** Konektor U.fl langsung ke breakout |

## 2. Helmet Node (PCB2)
| Ref | Komponen | Jml | Status / catatan |
|---|---|---|---|
| U1 | ESP32-C3 SuperMini | 1 | Ada, BLE beacon jalan. Pastikan pin 5V lewat regulator |
| H1 | Header 3 pin + modul TTP223 | 0 | **TIDAK DIPAKAI**: deteksi helm lewat tombol on/off + BLE + RSSI (tanpa sensor sentuh). Hapus H1, net `TOUCH_SIG` (GPIO2) dari PCB2 |
| H2 | Header 2 pin (LiPo) | 1 | |
| - | Baterai 18650 1200 mAh + holder (sama dengan Vest) | 1 | **Sudah ada (28 Okt, total 2 sel + 2 holder).** LiPo pipih dibatalkan; ganti hanya jika casing Helmet harus tipis |
| U7 | Modul TP4056 USB-C berproteksi (HW-373) | 1 | Ada 1 modul tim, tapi dipakai Vest; yang untuk Helmet masih dicari |
| SAW1 | Saklar geser (jalur baterai ke pin 5V) | 1 | **PERLU DIPERBAIKI:** di EasyEDA berisi filter SMD SAPPLAND SPST40SU03C, bukan saklar. Ganti saklar geser sungguhan |
| SW1 | Tact switch SMD (TS-1088-AR02016) | 1 | On/off |
| R1 | Resistor 100 k (0603) | 1 | Pull-up tombol |
| C1 | Kapasitor 10 uF (0603) | 1 | |
| C2 | Kapasitor 100 uF (case B 3528) | 1 | |
| - | CR2032 + holder | 0 | Dihapus di v2.1, tidak dipakai lagi |

## 3. Edge Gateway (PCB3)
| Ref | Komponen | Jml | Status / catatan |
|---|---|---|---|
| U5 | ESP32-DevKitC V4 (WROOM-32) | 1 | Ada |
| U1 | Modul LoRa Ra-02 SX1278 433 MHz (breakout) | 1 | **Sudah dibeli (modul kedua dari sepasang).** Footprint: female header 2x8 |
| H1 | Header 1x6 + modul microSD (SPI) | 1 | Ada. Urutan pin dan level logika perlu dicek |
| - | Kartu microSD 16/32 GB (FAT32) | 1 | Ada |
| R2 | Resistor 10 k (0603) | 1 | Pull-up CS SD |
| - | Antena pegas 433 MHz U.fl 3 dBi | 1 | **Sudah dibeli** |
| - | Adaptor 5 V 2 A + kabel | 1 | Ada |
| - | Box enclosure gateway | 1 | Belum ada |

## 4. Fabrikasi dan bahan pendukung
| Item | Status |
|---|---|
| PCB 2 layer: PCB1, PCB2, PCB3 | Belum dipesan. Jangan pesan sebelum revisi footprint dan proteksi |
| Casing 3D print PETG (Vest, Helmet, Gateway) | Vest v5 ada (belum update parts baru). Helmet dan Gateway belum |
| Konektor IP67, cable gland, seal | Belum |
| Kabel, header, JST, spacer, screw, heat shrink | Belum |
| Solder, flux, conformal coating, silikon | Belum |
| Perfboard/breadboard dan jumper | Ada (breadboard) |
| Resistor/kapasitor assortment untuk prototipe breadboard | Cek stok (10 k, 100 k, 330 ohm, 100 uF) |

## 5. Dihapus dari BOM lama (tidak dipakai di desain)
VL53L0X x2 (Rp80 rb), BME680 (Rp170 rb), AMS1117/step-down, CR2032 + holder, XKC-Y25 (sudah dibeli 13 Okt).

## 6. Minimum untuk prototipe breadboard (tanpa PCB, power bank/USB)
Vest: ESP32 DevKit, GY-521, GPS NEO-6M, sensor air, 2 tact, 1 resistor 10 k, kabel jumper, LoRa (setelah disolder + antena).
Helmet: SuperMini, 1 tact (opsional), kabel USB (LiPo + TP4056 + saklar nanti).
Gateway: ESP32 DevKit, LoRa + antena, modul microSD + kartu, kabel USB (LED + 330 ohm opsional sebagai indikator uji).

## 7. Ukuran komponen (diukur tim, 28 Okt 2026; p x l, tinggi belum diukur)
| Komponen | Ukuran (cm) | Catatan |
|---|---|---|
| ESP32-C3 SuperMini | 2,24 x 1,38 | 8 pin per sisi |
| GPS NEO-6M (GY-GPS6MV2) | 3,5 x 2,65 | 4 pin satu sisi, pitch breadboard |
| LoRa Ra-02 SX1278 433 MHz | 2,8 x 2,05 | 2x8 pin 2,54 mm |
| GY-521 (MPU6050) | 2,0 x 1,6 | 8 pin satu sisi, pitch breadboard |
| ESP32 DevKit V1 Type-C | 5,15 x 2,85 | 15 pin per sisi (30 pin) |
| ESP32 "U" (U.FL) | 4,8 x 2,8 | Belum ada di BOM; diasumsikan DevKit kedua (Vest/Gateway). Cek jarak baris pin |
| Holder 18650 (1 sel) | 7,65 x 2,05 | Tinggi holder + sel sekitar 2,1 (diukur) |
| TP4056 HW-373 V1.2.1 USB-C | 2,75 x 1,7 | **Pad BUKAN pitch breadboard** (pad besar di 4 sudut; IN+/IN- di kiri, OUT+/B+/B-/OUT- di kanan). Sumber online berbeda 22-29 x 17 mm; ukuran pad harus diukur dari modul asli sebelum footprint dibuat |
| Modul microSD | 2,9 x 4,15 | |
| MT3608 (belum dibeli) | ±3,7 x 1,7, tinggi 0,7-0,8 | Dari listing toko; varian bisa beda, ukur saat datang |
| Tact switch 2 pin | 0,6 x 0,6 | Jumlah 3: SOS, on/off Vest, on/off Helmet. BOM lama memakai SMD TS-1088 (bukan ini); sesuaikan footprint |
| XKC-Y25-V | belum ada | Kabel 50 cm; warna: coklat VCC, kuning sinyal, biru GND, hitam opsi |
| Antena pegas U.FL 433 MHz | sudah dibeli (2) | |

Belum ada: MOSFET, dioda, resistor, kapasitor. Tinggi komponen (untuk casing) belum diukur.

## 8. Daftar beli MOSFET, dioda, resistor (diperbaiki 28 Okt 2026)
Sumber jumlah: netlist PCB1-3 (bisa tertinggal dari EasyEDA) dan TUTORIAL_BREADBOARD (jalur cepat tanpa boost/MOSFET). Nilai MOSFET/dioda = nilai tipikal datasheet, cek di listing.

### A. Beli SEKARANG (prototipe breadboard, semua THT)
| Item | Spesifikasi | Jumlah beli | Untuk |
|---|---|---|---|
| Resistor 10 k | 1/4 W, 5%, THT | 5 | SOS pull-down, pembagi XKC (seri), CS microSD |
| Resistor 20 k | 1/4 W, 5%, THT | 3 | Pembagi XKC ke IO34 |
| Resistor 100 k | 1/4 W, 5%, THT | 5 | Pembagi baterai (2) + cadangan |
| Resistor 330 ohm | 1/4 W, 5%, THT | 5 | LED indikator uji, uji kabel LoRa |
| LED 5 mm | merah/hijau | 5 | LED uji |
Tanpa MOSFET dan tanpa dioda di breadboard (daya lewat USB/power bank). Opsi praktis: satu paket assorted resistor 1/4 W.

### B. Beli NANTI (saat PCB dipesan, SMD)
| Item | Spesifikasi | Perlu | Beli |
|---|---|---|---|
| MOSFET P-ch AO3401A, SOT-23 | -30 V, -4 A | 2 (PCB1 Q1, Q2) | 4 |
| MOSFET N-ch 2N7002, SOT-23 | 60 V, 115 mA | 1 (PCB1 Q5) | 3 |
| Dioda Schottky SS14, SMA | 40 V, 1 A | 1 (PCB1 D1) | 3 |
| Resistor 100 k, 0603, 1% | | 6 | 14 |
| Resistor 10 k, 0603, 1% | | 3 | 8 |
| Resistor 20 k, 0603, 1% | | 1 | 4 |
Keputusan: IRLZ44N dan MOSFET sirine tidak dibeli (Gateway tanpa sirine, 11 Nov). Hapus R1 10 k PCB1 (XKC digital). Tambah R8 10 k dan R9 20 k di PCB1.
