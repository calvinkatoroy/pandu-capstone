# Verifikasi skematik PCB1 (Vest Node Master)

Sumber: netlist hasil export EasyEDA (`Netlist_PCB1_2026-10-01.tel`). Dibandingkan dengan
pinout datasheet dari ingatan, BUKAN dari datasheet yang dibuka langsung -> yang bertanda
"VERIFIKASI" harus dicek ke datasheet/modul fisik.

## Temuan serius (perlu diperbaiki sebelum order)

1. **AMS1117-3.3 (U3) tidak bisa menghasilkan 3.3 V dari baterai Li-ion.**
   Dropout ~1.1 V -> butuh Vin >= 4.4 V, padahal baterai 3.0-4.2 V (VBAT_RAW ke U3.3).
   Saat baterai < ~4.4 V, 3V3_SYS turun ikut baterai. Ganti ke LDO low-dropout
   (mis. AP2112K-3.3, HT7333, XC6220) atau suplai dari boost 5 V.
2. **Dua sumber 3.3 V diparalel.** 3V3_SYS (output U3) tersambung ke U1.2 (pin 3V3 DevKit),
   sementara U1.16 (VBAT_RAW) masuk ke pin daya DevKit yang punya LDO sendiri. Dua output
   regulator di satu net -> arus balik/berebut. Pilih satu: suplai DevKit lewat pin 5V
   dan jangan sambung 3V3_SYS ke pin 3V3 DevKit, atau sebaliknya.
3. **SW1 adalah tact switch SMD (SW-SMD L3.9 W3.0) dipakai sebagai saklar daya.**
   Momentary (tidak mengunci) dan rating ~50 mA, sedangkan jalur ini membawa seluruh
   arus beban. Ganti ke slide switch / saklar latching berarus >= 1 A.
4. **RA-02 (U6): hanya pin 1 yang ke GND.** Modul punya beberapa pad GND (VERIFIKASI
   pin 2/9/16 di datasheet). GND yang tidak tersambung merusak ground RF dan jangkauan.

## Perlu diverifikasi

5. U1 (ESP32-DevKitM-1): footprint bernama `34P-L43.8` sedangkan DevKitM-1 asli ~54 mm
   dengan 30 pin. VERIFIKASI footprint dan tabel pin sebelum percaya nomor pin di bawah.
6. GPS_RX/GPS_TX: modul GPS RX (U9.2) ke U1.11, TX (U9.3) ke U1.12. Cek di firmware
   bahwa pin 11/12 bukan pin flash/strapping dan UART di-map: RX modul <- TX ESP.
7. C1 100 uF dan C2 10 uF memakai footprint 0603. 100 uF di 0603 jarang/mahal dan
   kapasitansinya turun banyak saat dibias. AMS1117 juga minta kapasitor output >= 22 uF
   ber-ESR (tantalum), bukan keramik murni -> bisa osilasi.
8. TP4056 modul (U7): VBUS_5V hanya terhubung ke U7.5 (tidak dipakai di tempat lain),
   tidak berbahaya. VERIFIKASI urutan pin 1-6 modul fisik (OUT+, B+, GND...).
   Pastikan modul punya proteksi DW01 (over-discharge); tanpa itu sel Li-ion bisa rusak.

## Yang sudah sesuai

| Blok | Net | Hasil |
|---|---|---|
| LoRa SPI | SCK/MISO/MOSI/CS -> U6.12/13/14/15 | cocok dengan pinout Ra-02 (SCK, MISO, MOSI, NSS) |
| LoRa kontrol | RST U6.4, DIO0 U6.5, 3V3 U6.3 | cocok |
| I2C MPU6050 | SCL U8.6, SDA U8.5, VCC U8.8, GND U8.7 | konsisten; GY-521 sudah punya pull-up |
| Sensor air | VCC VBOOST_5V (U10.2), OUT -> R1 pull-up 10k ke 3V3 -> U1.8 | sesuai rencana (varian NPN) |
| Tombol SOS | SW2 -> 3V3, R2 10k pulldown, BTN_SOS -> U1.14 | benar, aktif-tinggi |
| Boost | U2.1 VBAT_RAW, U2.2/3 GND, U2.4 VBOOST_5V | konsisten dengan rencana |
| Baterai | BT1.1 VBAT_POS -> U7.2, BT1.2 GND | benar |

Semua net lain punya >= 2 simpul, tidak ada net yatim kecuali VBUS_5V (1 simpul).
