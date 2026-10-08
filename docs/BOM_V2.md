# BOM PANDU (desain v2, per 8 Okt 2026)

Sumber: netlist `hardware/netlist/PCB1.tel`, `PCB2.tel`, `PCB3.tel`, firmware, dan hasil tes sesi ini. Tanpa harga (harga final ikut invoice di sheet "Bills of Materials").
Kolom **Status** diambil dari checklist sheet BOM (6 Okt) dan percakapan; belum tentu terkini, cek ulang dengan Rafif/Gibran.
Tanda **PERLU DIPERBAIKI** = item di desain/EasyEDA yang salah atau belum cocok dengan komponen fisik (lihat HANDOVER.md).

## 1. Vest Node Master (PCB1)
| Ref | Komponen | Jml | Status / catatan |
|---|---|---|---|
| U3 | ESP32-DevKitC V4 (WROOM-32) | 1 | Ada. Cek jarak baris pin (25,4 vs 22,86 mm) |
| U8 | GY-521 (MPU6050) | 1 | Ada, tes jatuh jalan. Urutan footprint belum dicek |
| U9 | GPS NEO-6M + antena keramik | 1 | Ada, dapat fix (sinyal lemah). Antena aktif eksternal disarankan |
| U6 | Modul LoRa SX1276 (XL1276-P01, 915 MHz) + antena pegas | 1 | Ada 1. **PERLU DIPERBAIKI:** pinout RFM95, footprint PCB = RA-02. Belum disolder. Cek pita 868M vs 915M |
| U10 | Sensor air analog (S, +, -) | 1 | Ada, ambang 1000 mV. **PERLU DIPERBAIKI:** VCC ke 3V3, hapus R1. (XKC-Y25 tidak dipakai/belum dibeli) |
| BT1 | Holder 18650 | 1 | Ada |
| - | Baterai 18650 1200 mAh | 1 | Ada |
| U7 | Modul TP4056 USB-C berproteksi (HW-373) | 1 | Ada. **PERLU DIPERBAIKI:** B- dan OUT- sama-sama GND (proteksi terlewati) |
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
| - | Antena LoRa 915 MHz + pigtail (SMA) | 1 | Untuk Vest belum ada di BOM; antena pegas bawaan modul bisa dipakai tes |

## 2. Helmet Node (PCB2)
| Ref | Komponen | Jml | Status / catatan |
|---|---|---|---|
| U1 | ESP32-C3 SuperMini | 1 | Ada, BLE beacon jalan. Pastikan pin 5V lewat regulator |
| H1 | Header 3 pin + modul TTP223 | 0 | **TIDAK DIPAKAI**: deteksi helm lewat tombol on/off + BLE + RSSI (tanpa sensor sentuh). Hapus H1, net `TOUCH_SIG` (GPIO2) dari PCB2 |
| H2 | Header 2 pin (LiPo) | 1 | |
| - | Baterai LiPo 3,7 V ~400-500 mAh berproteksi | 1 | Belum ada |
| U7 | Modul TP4056 USB-C berproteksi | 1 | Perlu yang kedua (sheet hanya 1) |
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
| U1 | Modul LoRa SX1276 915 MHz | 1 | **Belum dibeli (baru 1 modul)**. Footprint RA-02 sama masalahnya |
| H1 | Header 1x6 + modul microSD (SPI) | 1 | Ada. Urutan pin dan level logika perlu dicek |
| - | Kartu microSD 16/32 GB (FAT32) | 1 | Ada |
| Q1 | MOSFET IRLZ44N (TO-220) | 1 | Belum ada |
| R1 | Resistor 220 ohm (0603) | 1 | |
| R2 | Resistor 10 k (0603) | 1 | Pull-up CS SD |
| R3 | Resistor 100 k (0603) | 1 | Pull-down gate |
| U2 | Terminal block 2 pin 3,81 mm | 1 | Untuk sirine |
| - | Sirine/strobo 5 V (>= 85 dB) | 1 | Belum ada. Perlu dioda flyback jika sirine berkoil/motor |
| H2 | Header 2 pin | 1 | Pigtail antena |
| - | Antena LoRa 915 MHz + pigtail SMA | 1 | Ada |
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
VL53L0X x2 (Rp80 rb), BME680 (Rp170 rb), AMS1117/step-down, CR2032 + holder, XKC-Y25 (belum dibeli; sensor air analog dipakai).

## 6. Minimum untuk prototipe breadboard (tanpa PCB, power bank/USB)
Vest: ESP32 DevKit, GY-521, GPS NEO-6M, sensor air, 2 tact, 1 resistor 10 k, kabel jumper, LoRa (setelah disolder + antena).
Helmet: SuperMini, 1 tact (opsional), kabel USB (LiPo + TP4056 + saklar nanti).
Gateway: ESP32 DevKit, LoRa + antena, modul microSD + kartu, LED + 330 ohm (pengganti sirine), kabel USB.
