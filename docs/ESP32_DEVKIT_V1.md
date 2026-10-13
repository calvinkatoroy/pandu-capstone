# ESP32 DevKit V1 (30 pin) yang dipakai tim

Konfirmasi Calvin 13 Okt 2026: papan yang dipegang = **ESP32 DevKit V1 (30 pin)**. BOM awal dan netlist PCB1/PCB3 dibuat untuk **ESP32-DevKitC V4 (38 pin)**. Breadboard tidak terpengaruh; PCB terpengaruh (lihat bawah).

## Pinout DevKit V1 30 pin (antena di atas, USB di bawah; verifikasi dengan papan)
| Kiri (atas ke bawah) | Kanan (atas ke bawah) |
|---|---|
| EN | D23 |
| VP (IO36) | D22 |
| VN (IO39) | TX0 (IO1) |
| D34 | RX0 (IO3) |
| D35 | D21 |
| D32 | D19 |
| D33 | D18 |
| D25 | D5 |
| D26 | TX2 (IO17) |
| D27 | RX2 (IO16) |
| D14 | D4 |
| D12 | D2 |
| D13 | D15 |
| GND | GND |
| **VIN (5 V)** | **3V3** |

Urutan dari pengetahuan umum papan DOIT V1; clone bisa berbeda. Cocokkan dengan silkscreen papan sebelum menyolder atau membuat footprint.

## Pin PANDU di DevKit V1
| Fungsi | GPIO | Label di V1 |
|---|---|---|
| Vest: tombol power / SOS | 13 / 27 | D13 / D27 |
| Vest: baterai / air | 35 / 34 | D35 / D34 |
| Vest: GPS_EN / XKC_EN | 4 / 32 | D4 / D32 |
| Vest: GPS RX (ESP) / TX | 16 / 17 | RX2 / TX2 |
| Vest: I2C SDA / SCL | 21 / 22 | D21 / D22 |
| LoRa NSS / SCK / MISO / MOSI | 5 / 18 / 19 / 23 | D5 / D18 / D19 / D23 |
| LoRa RST: Vest / Gateway | 25 / 14 | D25 / D14 |
| LoRa DIO0 | 26 | D26 |
| Gateway: SD SCK / MISO / MOSI / CS | 25 / 35 / 32 / 33 | D25 / D35 / D32 / D33 |
| Gateway: sirine | 4 | D4 |

Semua GPIO ada di V1 dan tidak ada yang bentrok dengan pin flash (6-11). IO34/IO35 input-only (sesuai pemakaian). IO5 strapping tetapi idle HIGH (NSS).

## Dampak
- **Breadboard:** aman, firmware tidak berubah (`board = esp32dev`). Pin catu 5 V di V1 bernama **VIN**. Banyak clone V1 butuh tombol **BOOT** ditahan saat upload.
- **PCB1 (`U3`) dan PCB3 (`U5`):** footprint dan nomor pin di netlist = DevKitC V4 (`U3.J2-5` = IO34, `J2-19` = 5V). V1 punya jumlah pin (15 per sisi, bukan 19), urutan, dan mungkin jarak deret yang berbeda. **Footprint dan koneksi harus dibuat ulang** bila PCB memakai V1.

## Keputusan yang dibutuhkan
Pakai V1 di PCB (memakai papan yang sudah ada; footprint = dua female header 1x15 2,54 mm, jarak deret **ukur**), atau beli DevKitC V4 sesuai BOM (netlist lama tetap berlaku). Rekomendasi: pakai V1 yang sudah ada, tapi hanya setelah jarak deret dan urutan pin diverifikasi di papan fisik.

## Update 13 Okt: DevKit V1 = untuk Edge Gateway (PCB3)
PCB3 `U5` sekarang footprint `ESP32-DEVKITC-32D` (V4, 38 pin). Untuk V1 buat footprint dua female header 1x15 (jarak deret: ukur) dan sambungkan ulang. Penomoran di bawah: `L1..L15` = kolom kiri atas ke bawah, `R1..R15` = kolom kanan atas ke bawah (urutan tabel di atas, **verifikasi di papan**).

| Net PCB3 | GPIO | Pin V1 (baru) | Pin lama (V4) |
|---|---|---|---|
| 5V_SYS | VIN | L15 | J2-19 |
| 3V3 | 3V3 | R15 | J2-1 |
| GND | GND | L14 (dan R14) | J2-14, J3-1, J3-7 |
| LORA_CS | IO5 | R8 | J3-10 |
| LORA_RST | IO14 | L11 | J2-12 |
| LORA_DIO0 | IO26 | L9 | J2-10 |
| SPI_SCK | IO18 | R7 | J3-9 |
| SPI_MISO | IO19 | R6 | J3-8 |
| SPI_MOSI | IO23 | R1 | J3-2 |
| SD_SCK | IO25 | L8 | J2-9 |
| SD_MISO | IO35 | L5 | J2-6 |
| SD_MOSI | IO32 | L6 | J2-7 |
| SD_CS | IO33 | L7 | J2-8 |
| SIREN_DRV | IO4 | R11 | J3-13 |

Setelah footprint diganti: ekspor ulang `PCB3.tel` dan jalankan `hardware/netlist/check_netlist.py`. Vest (PCB1) tetap memakai papan yang akan dipilih terpisah (V1 atau DevKitC V4).
