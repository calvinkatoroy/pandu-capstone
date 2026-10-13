# LoRa: Ra-02 SX1278 433 MHz (breakout 2,54 mm)

Keputusan 13 Okt 2026: modul LoRa untuk Vest dan Gateway = **sepasang Ra-02 SX1278 433 MHz** (breakout 28 x 20 mm). Antena = pegas 433 MHz U.fl 3 dBi (kabel sekitar 15 cm). Modul XL1276 (SX1276 868/915) yang lama **tidak dipakai** dan jangan dicampur: beda pita, tidak akan saling terima.

Catatan: SX1278 hanya 137-525 MHz. Tidak bisa diatur ke 915/920 MHz. Firmware: `LORA_FREQ = 433E6` di `vest_node`, `gateway`, dan `test_lora_one`.

## Pinout breakout (dari foto produk, VERIFIKASI di modul fisik)
Dua deret 8 pin, pitch 2,54 mm.

| Deret | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Atas | GND | NSS | MOSI | MISO | SCK | DIO5 | DIO4 | GND |
| Bawah | GND | GND | 3.3V | RST | DIO0 | DIO1 | DIO2 | DIO3 |

Konektor antena: U.fl (IPEX). Catu: 1,8-3,7 V (tipikal 3,3 V). **Jangan ke 5 V.** Arus kirim sekitar 120 mA pada +20 dBm.

## Pemetaan ke net PCB
Hanya posisi pin di footprint yang berubah; net logika tetap seperti firmware sekarang.

| Pin breakout | Net Vest (PCB1, `U6`) | Net Gateway (PCB3, `U1`) |
|---|---|---|
| 3.3V | 3V3 (+ kapasitor 100 uF dan 100 nF dekat pin) | 3V3 (+ 100 uF) |
| GND (x4) | GND | GND |
| NSS | IO5 | IO5 |
| SCK | IO18 | IO18 |
| MISO | IO19 | IO19 |
| MOSI | IO23 | IO23 |
| RST | IO25 | IO14 |
| DIO0 | IO26 | IO26 |
| DIO1-5 | tidak dipakai (NC) | tidak dipakai (NC) |

Cek pin SPI (18/19/23) terhadap netlist sebelum edit: `hardware/netlist/PCB1.tel` dan `PCB3.tel`, lalu `check_netlist.py`.

## Footprint di EasyEDA
- Ganti footprint `RA-02` (WIRELM-SMD_RA-02-BL, modul telanjang castellated 2 mm) dengan **dua female header 1x8 2,54 mm** (atau satu 2x8 kalau jarak deret pas).
- Jarak antar dua deret: **ukur di modul fisik** (tengah ke tengah). Belum ada angkanya; jangan menebak. Panjang x lebar papan: 28 x 20 mm menurut listing.
- Sisakan area bebas tembaga/komponen di bawah dan di sekitar papan, dan tempatkan modul di tepi PCB dengan konektor U.fl menghadap tepi supaya kabel antena tidak menekuk tajam.
- Header modul bisa disolder jantan di breakout (jantan di modul, betina di PCB), supaya modul bisa dilepas untuk tes.

## Yang harus dicek di modul fisik (Calvin)
- [ ] Label di modul: SX1278 / 433 MHz / ISM 410-525 MHz (foto produk sudah menunjukkan ini).
- [ ] Jarak tengah ke tengah antar dua deret header (mm).
- [ ] Header sudah tersolder atau lepasan; urutan pin sama dengan tabel di atas.
- [ ] Dua modul identik (pita dan label sama).
- [ ] Antena terpasang di U.fl **sebelum** firmware yang memanggil `LoRa.begin` / transmit diunggah.

## Uji tautan di breadboard (gerbang 4 PLAN_REVISI)
1. Dua ESP32 DevKit, masing-masing satu Ra-02 + antena. Kabel pendek; 100 uF di rel 3V3.
2. Pengirim: `firmware/test_lora_one` (433E6). Penerima: `firmware/gateway`, atau tes kedua `test_lora_one` sebagai penerima.
3. Hasil yang dicatat: `LoRa=1` saat boot, RSSI/SNR pada jarak 1 m, 10 m, jarak terjauh yang aman, dan apakah paket `PANDU,V1,HB,...` sampai di JSON Gateway.
4. Jangan simpulkan jarak 5-10 km dari listing; itu kondisi ideal. Tulis hasil nyata.

## Regulasi
Pemakaian pita 433 MHz di Indonesia perlu dicek dan disebut di laporan (belum diverifikasi). Untuk prototipe kampus bukan penghalang. Proposal dan definisi yang menyebut 915/920 MHz perlu dibuat konsisten dengan pita 433 MHz.
