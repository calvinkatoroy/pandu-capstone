# Audit skematik PANDU: temuan dan status (Pekan 6)

Menggantikan status di `PCB1_Verifikasi_Skematik.md`. Tanggal: 2 Okt 2026.

## Keputusan desain Pekan 6
- Sensor Vest: MPU6050 (jatuh), XKC-Y25 (air/MOB), GPS, LoRa. **Tanpa VL53L0X dan BME680** (ToF rawan false positive saat crew menempel dinding).
- Board ESP32 Vest: **ESP32-WROOM-32 DevKit klasik** (nama part di EasyEDA "DEVKITM-1" menyesatkan).
- Daya: baterai 18650 > TP4056 > `VBAT_RAW` (tanpa saklar seri). Boost 5 V selalu aktif, menyuplai pin 5V ESP32. AMS1117 dan C1/C2 dihapus.
- Tombol power SW1 (tact + rubber boot): input GPIO RTC (IO13), toggle deep sleep di firmware.
- Gating daya (arus standby rendah): GPS lewat P-MOSFET Q1 (`GPS_EN`=IO4), XKC-Y25 lewat Q2 + level shifter Q5 (`XKC_EN`=IO2).
- `BTN_SOS` di IO27 (RTC) agar SOS bisa membangunkan rompi.

## PCB1 (Vest Node Master)
| Temuan | Status |
|---|---|
| AMS1117 tidak cukup dropout dari Li-ion | Beres (dihapus) |
| Dua sumber 3V3 paralel | Beres |
| Tact switch sebagai saklar daya | Beres (jadi input GPIO) |
| RA-02: pin 1 itu ANT, GND = pin 2/9/16 | Beres (`LORA_ANT`, GND tersambung) |
| `GPS_EN` dan GND RA-02 sempat tidak tersambung (kabel meleset) | Beres, diverifikasi DRC "Pins floating" |
| Footprint ESP32 (17 pin/sisi, 0,9") tidak cocok DevKit klasik 30/38 pin | **Terbuka**: butuh nama/foto board |
| Urutan pin TP4056 dan boost | **Terbuka**: cek modul fisik |
| Trek daya kembali 10 mil setelah auto-route | **Terbuka** |
| Gerber PCB1 | **Perlu ekspor ulang** |

## PCB3 (Edge Gateway)
| Temuan | Status |
|---|---|
| ESP32 tanpa pull-up EN, tanpa BOOT, tanpa header program | Beres (R2 10k, C3 100 nF, J1 1x6) |
| Pin 1 RA-02 ke GND | Beres (`LORA_ANT`) |
| Gate MOSFET tanpa pull-down | Beres (R3 100k) |
| EP ESP32 tidak ke GND | Beres |
| IRFZ44N bukan logic-level | **Terbuka**: beli IRLZ44N (footprint sama) |
| USB-C tanpa resistor CC 5,1k | **Terbuka** (pakai kabel A-ke-C untuk PoC) |
| Dioda flyback (jika beban induktif) | Terbuka, bergantung beban |
| Gerber PCB3 | **Perlu ekspor ulang** |

## PCB2 (Helmet Node)
- CR2032 menyuplai ESP32-C3 lewat dioda: lonjakan arus BLE berisiko brownout. Tambah kapasitor 100-220 uF low-ESR di jalur 3V0 atau pakai LiPo kecil. **Terbuka.**

## Lintas board
- RA-02 = SX1278 **433 MHz**, proposal menyebut **915 MHz** (Indonesia: 920-923 MHz). Perlu dicek modul yang dipesan.
- Gerber lama di `WEEK_6\Gerber` **jangan dipesan**.
