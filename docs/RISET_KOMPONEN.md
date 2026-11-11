# Riset ukuran komponen dari web (11 Nov 2026)

Dibuat karena tim tidak punya jangka sorong. Semua angka di sini **D** (dugaan dari sumber web), kecuali ditandai lain. Sumber toko/komunitas bisa beda dari modul yang dibeli; penentu akhir tetap uji tusuk cetak 1:1 (lihat `PRE_ORDER_PCB.md` bagian 4 dan "Cara ukur tanpa jangka sorong" di bawah).

## Temuan penting
1. **Ra-02 breakout: jarak antar deret kemungkinan 25,4 mm (10 x 2,54), bukan 26,0 mm** (footprint sekarang 26,0). Dihitung dari foto mekanik di manual 7Semi (board 27,7 x 20,4 mm): jarak tengah lubang kiri-kanan = 777 px, pitch vertikal = 77,7 px, rasio 10,0 pitch = 25,4 mm. Ukuran penggaris Calvin (26 mm +-0,5) masih konsisten dengan 25,4. Selisih 0,6 mm cukup untuk membuat pin tidak masuk. Pin order di manual itu sama dengan tabel kita (`LORA_RA02_BREAKOUT.md`). Catatan: dari gambar produk 7Semi, bukan dari modul yang dibeli, dan bergantung pada foto tegak lurus. **Wajib diuji tusuk dengan kertas cetak 1:1 untuk kedua kemungkinan (25,4 dan 26,0) sebelum footprint dikunci.**
2. **Lubang 1,0 mm untuk pin header standar sudah umum**: pin header 2,54 mm berpenampang persegi 0,64 mm (diagonal sekitar 0,91 mm), contoh footprint header memakai lubang 1,0 mm dan pad 1,7 mm. Aturan "diagonal + 0,2-0,3 mm" yang tadi kusebut di checklist adalah usulanku, bukan standar; 1,0 mm sudah cukup untuk pin 0,64 mm. Risiko ada bila pin modul lebih tebal dari 0,64 mm (klon murah); uji tusuk menjawabnya.
3. **TP4056 Type-C: tiga angka berbeda**: 27,5 x 17 (pengukuran 28 Okt), 28,5 x 17 (5 Nov), 28 x 17 (toko), **29 x 17,3 x 4,3 mm (datasheet AZ-Delivery)**. Ukuran papan beragam antar penjual; yang menentukan footprint adalah jarak pad (tidak ada di sumber web), jadi tetap diukur/diuji tusuk. Letak pad: IN+/IN- di sisi USB (kiri), B+, B-, OUT+, OUT- di sisi kanan; pad besar di sudut, bukan pitch 2,54 mm.

## Hasil per komponen
| Komponen | Hasil riset | Status | Sumber |
|---|---|---|---|
| ESP32 DevKit V1 30 pin | papan 28,2 x 51,8 mm (pengukuran pembaca + gambar Fritzing berukuran asli). Jarak antar deret dan lubang **tidak ditemukan** di sumber web; angka 25,4 mm hanya dari pengukuran sendiri. Banyak klon, ukuran bervariasi | D | Mischianti |
| ESP32 DevKitC 38 pin (Gateway) | tidak diriset khusus; jarak deret resmi DevKitC 25,4 mm, klon kadang 22,86 mm (HANDOVER) | D | |
| ESP32-C3 SuperMini | 22,5 x 18 mm (x 4,5 mm tinggi); 16 pin = 2 x 8, pitch 2,54 mm; **jarak antar deret: 0,6" (15,24 mm) menurut satu toko, belum terkonfirmasi**; regulator 3,3 V onboard; pin 5V melewati dioda dari VBUS (sekitar 4,8 V); jangan colok USB-C dan 5V pin bersamaan | D | Mischianti, Protosupplies, Components101 |
| Ra-02 modul telanjang | 17 x 16 x 3,2 mm, SMD-16, pitch pad 2 mm, 2,5-3,7 V | T (datasheet Ai-Thinker) | Ai-Thinker Ra-02 V1.1 |
| Ra-02 breakout (7Semi, mirip punya kita) | 27,7 x 20,4 mm, 2 x 8 pin, pitch 2,54 mm, konektor U.fl, 1,8-3,3 V. Pin: kolom kiri GND, GND, 3V3, RST, DIO0, DIO1, DIO2, DIO3; kolom kanan GND, NSS, MOSI, MISO, SCK, DIO5, DIO4, GND (cocok dengan tabel kita). Jarak deret turunan gambar = 25,4 mm | D (turunan) | Manual 7Semi |
| TP4056 Type-C (dengan proteksi) | 29 x 17,3 x 4,3 mm (AZ-Delivery); 1 A; pad IN+/IN-, B+/B-, OUT+/OUT- | D | AZ-Delivery, Mischianti |
| GY-521 (MPU6050) | sekitar 21 x 16 mm (ada yang 20,5 x 15,5); header 8 pin pitch 2,54 mm; lubang baut M3 (sekitar 3,2 mm), jarak antar lubang tidak ditemukan. Urutan pin umum VCC, GND, SCL, SDA, XDA, XCL, AD0, INT (dari pengetahuan umum, belum dari sumber) | D | Flux Workshop, Zaitronics, OpenELab |
| GPS NEO-6M GY-GPS6MV2 | 36 x 25,8 x 4 mm (ada yang 35 x 25/26 mm); 4 pin pitch 2,54 mm (VCC, RX, TX, GND, urutan belum terkonfirmasi sumber); 4 lubang baut 3 mm, jarak tidak ditemukan | D | listing toko, Core Electronics |
| MT3608 boost | 36-37 x 17 mm, tinggi 6-14 mm; jarak pad tidak ditemukan; belum dibeli | D | listing toko, Components101 |
| Modul microSD SPI | 41 x 24 mm (datasheet), ada juga 45 x 28 dan 25 x 20 mm; header 6 pin GND, VCC, MISO, MOSI, SCK, CS pada sebagian besar, **urutan bervariasi antar penjual** (cek silkscreen) | D | datasheet modul, Circuit Digest |
| XKC-Y25-V | supply 5-24 V; **keluaran tidak seragam di listing** (digital NPN/level, ada yang menyebut RS485); ukuran 30 x 30 x 20 mm menurut satu toko; varian T12V (DFRobot) 28 x 28 mm; pinout -V tidak ditemukan (T12V: VCC, OUT, GND, ADJ) | D | Aryabot, DFRobot SEN0204, Robu |
| 2N7002 / AO3401A (SOT-23) | pin SOT-23 umum: 1 = Gate, 2 = Source, 3 = Drain (pengetahuan umum; **tidak terkonfirmasi** oleh hasil pencarian). Cek datasheet part LCSC sebelum memesan. (Gateway tidak memakai 2N7002 lagi; PCB1 memakai keduanya) | D | Components101 |
| Pin header 2,54 mm | pin 0,64 mm persegi; lubang footprint umum 1,0 mm, pad 1,7 mm | D | RS PRO, Flux.ai |
| Tact switch, holder 18650 | tidak diriset; ukuran sesuai pengukuran 28 Okt | B | |

## Cara ukur tanpa jangka sorong
1. **Uji tusuk kertas 1:1** (paling andal, tanpa alat ukur): cetak footprint 100%, lubangi kertas tepat di pad, tusukkan pin modul. Coba dua versi untuk Ra-02: deret 25,4 mm dan 26,0 mm; pilih yang pin-nya masuk tanpa dipaksa. Cek skala cetak dengan penggaris pada garis 50 mm.
2. **Scanner flatbed** (atau foto tegak lurus dengan penggaris di sebelah modul): scan modul bersama penggaris, ukur di komputer. Akurasi sekitar 0,1 mm jika skala dikalibrasi dari penggaris.
3. **Pinjam jangka sorong** (kampus lab, toko alat, bahkan kantor bengkel 10-20 ribu rupiah): paling cepat untuk jarak deret, diameter pin, dan jarak lubang baut.
4. **Hitung jumlah pitch**: jarak antar pin pada satu deret = n x 2,54 mm tepat (tidak perlu diukur); yang perlu diukur hanya jarak deret, yang biasanya kelipatan 2,54 mm (15,24; 17,78; 22,86; 25,4).

## Yang tidak ditemukan di web (harus fisik)
Jarak antar deret DevKit V1 dan 38 pin, SuperMini (hanya 15,24 mm dari satu toko), jarak lubang baut GY-521 dan GPS, jarak pad TP4056 dan MT3608, urutan pin microSD dan GPS pada modul kita, pinout XKC-Y25-V, ukuran tact switch dan holder.

## Sumber
- Mischianti: DOIT ESP32 DevKit V1 https://mischianti.org/doit-esp32-dev-kit-v1-high-resolution-pinout-and-specs ; ESP32-C3 SuperMini https://mischianti.org/esp32-c3-super-mini-high-resolution-pinout-datasheet-and-specs/ ; TP4056 https://mischianti.org/tp4056-lipo-battery-charger-high-resolution-pinout-datasheet-and-specs/
- Ai-Thinker Ra-02 V1.1 Specification (PDF, diunduh) https://aithinker-static.oss-cn-shenzhen.aliyuncs.com/docs/Public%20Document%20Center/LoRa/lora/Specification/Ra-02_V1.1%20Specification-20171219.pdf
- 7Semi SX1278 Ra-02 manual https://evelta.com/content/datasheets/004-7Semi-LoRa-ra-02.pdf
- AZ-Delivery TP4056 Type-C datasheet https://cdn.shopify.com/s/files/1/1509/1638/files/TP4056-TypeC_datasheet.pdf
- Protosupplies ESP32-C3 SuperMini https://protosupplies.com/product/esp32c3-supermini/ ; Components101 https://components101.com/development-boards/esp32c3-mini-development-board-datasheet-pinout
- Flux Workshop GY-521 https://fluxworkshop.com/collections/abd-sensors/products/bdaa100044-gy-521-mpu-6050 ; Core Electronics GPS https://core-electronics.com.au/u-blox-neo-6m-gps-module.html.plain.md
- Components101 MT3608 https://components101.com/modules/mt3608-2a-dc-dc-step-up-power-module ; Components101 2N7002 https://components101.com/mosfets/2n7002-datasheet-pinout-equivalent
- Aryabot XKC-Y25-V https://aryabot.in/?p=36025 ; DFRobot SEN0204 (datasheet.chipsmall.com/SEN0204/635212.pdf)
- RS PRO pin header https://uk.rs-online.com/web/p/pcb-headers/2518086 ; Flux.ai header footprint https://www.flux.ai/markwuflux/pin-header-01x01-2p54mm-vertical-circular-pad~vp
