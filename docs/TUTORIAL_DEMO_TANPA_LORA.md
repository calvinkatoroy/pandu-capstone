# Tutorial demo: Helmet Node dan Vest Node (tanpa LoRa)

Tujuan: demo bahwa fungsi inti Vest dan Helmet berjalan. Daya dari USB laptop, dua laptop dengan serial monitor (Laptop A = Vest, Laptop B = Helmet). Tanpa LoRa, Gateway, dashboard, dan baterai.

Yang didemokan:
- Helm: beacon BLE dengan tombol ON/OFF.
- Vest: deteksi helm dari RSSI (dekat, jauh, tidak terdengar), jatuh (FALL), MOB (jatuh DAN air dalam 60 detik), SOS manual (tahan 2 detik), tombol power (tidur dan bangun), GPS (opsional, perlu di luar ruangan).
- Paket yang akan dikirim lewat LoRa tetap dicetak ke serial (`PANDU,V1,...`), jadi isi paket bisa ditunjukkan.

Tidak didemokan: pengiriman LoRa, Gateway, dashboard, baterai dan charging.

## 0. Persiapan
- Dua kabel micro-USB **data** (bukan charge-only) dan USB-C/micro sesuai board. Pakai kabel pendek dan tebal (BLE bisa memicu brownout kalau kabel buruk).
- PlatformIO terpasang (`python -m platformio --version`), repo `pandu-capstone` di laptop yang dipakai untuk upload.
- **Tip:** upload kedua firmware dari satu laptop dulu. Setelah itu board cukup dicolok ke laptop masing-masing untuk daya dan serial.
- Cari port tiap board: `python -m platformio device list`. DevKit biasanya CP210x, SuperMini biasanya `303A:1001`. Ganti `COMx` di perintah di bawah.

## 1. Helmet Node (SuperMini ESP32-C3), Laptop B

### Bahan
ESP32-C3 SuperMini, 1 tact switch, 2 kabel jumper, kabel USB. (Tanpa TTP223, tanpa baterai.)

### Wiring
```
SuperMini pin GPIO4 ---- [tact switch] ---- SuperMini pin GND
```
Pull-up sudah internal. Daya dan serial lewat kabel USB ke laptop.

### Upload (mode demo: siaran terus, serial tetap hidup)
```bash
cd pandu-capstone/firmware/helmet_node
python -m platformio run -e supermini_test -t upload --upload-port COMx
python -m platformio device monitor --port COMx
```
Kalau upload macet: tahan **BOOT**, tekan **RESET**, lepas BOOT, ulangi. Setelah upload tekan RESET sekali.

### Yang muncul di serial
```
HELMET demo: beacon ON. Tekan tombol (GPIO4) untuk ON/OFF.
siaran counter=1
siaran counter=2
```
Tekan tombol: `BEACON OFF`, tekan lagi: `BEACON ON`. Counter naik tiap detik selama ON.

Catatan: mode ini bukan firmware produk (produk memakai deep sleep, `-e supermini`). Deep sleep memutus serial USB tiap 8 detik, jadi tidak cocok untuk demo dengan serial monitor.

## 2. Vest Node (ESP32 DevKit), Laptop A

### Bahan
ESP32-DevKitC, GY-521 (MPU6050), GPS NEO-6M, sensor air (sensor murah S/+/- atau XKC-Y25), 2 tact switch, 1 resistor 10 kΩ, kapasitor 100 µF (disarankan), breadboard, jumper, kabel micro-USB.

### Wiring lengkap
```
                           ESP32 DevKit (daya: micro-USB dari laptop)
                       +----------------------------------+
 GY-521 (MPU6050)      |                                  |
   VCC ----------------| 3V3                              |
   GND ----------------| GND                              |
   SDA ----------------| IO21                             |
   SCL ----------------| IO22                             |
                       |                                  |
 GPS NEO-6M            |                                  |
   VCC ----------------| 3V3                              |
   GND ----------------| GND                              |
   TX  ----------------| IO16   (TX GPS ke RX ESP)        |
   RX  ----------------| IO17                             |
                       |                                  |
 Sensor air            |                                  |
   (lihat 2.2)         | IO34                             |
                       |                                  |
 Tombol SOS            |                                  |
   kaki A -------------| 3V3                              |
   kaki B ---+---------| IO27                             |
             |         |                                  |
          [10 kOhm]    |                                  |
             |         |                                  |
            GND        |                                  |
                       |                                  |
 Tombol power          |                                  |
   kaki A -------------| IO13                             |
   kaki B -------------| GND                              |
                       |                                  |
 Kapasitor 100 uF: antara pin 3V3 dan GND (kaki panjang ke 3V3)
                       +----------------------------------+
```
Dibiarkan kosong: IO4, IO32, IO35 (tidak dipakai di demo). Angka mV baterai di paket tidak berarti.
Semua GND disatukan di satu rel breadboard.

### 2.1 Upload
```bash
cd pandu-capstone/firmware/vest_node
python -m platformio run -t upload --upload-port COMx
python -m platformio device monitor --port COMx
```
Serial awal: `Boot: MPU=1 LoRa=0 wake=other`. `LoRa=0` **normal** (LoRa tidak dipasang), program tetap jalan dan mencetak paket ke serial.

### 2.2 Sensor air (pilih satu)
**Sensor murah (S, +, -):**
```
Sensor +  ---- 3V3   (jangan 5 V)
Sensor -  ---- GND
Sensor S  ---- IO34   (tanpa resistor)
```
Kering terbaca sekitar 150-250 mV, basah sekitar 1700-2000 mV. Ambang di firmware 1000 mV (`WATER_WET_MV`).

**XKC-Y25 (kalau sudah ada):**
```
XKC VCC (coklat) ---- pin VIN/5V DevKit   (5 V dari USB)
XKC GND (biru)   ---- GND
XKC OUT (kuning) ---- [10 kOhm] ---- IO34 ---- [20 kOhm] ---- GND
```
Ukur output dulu dengan multimeter (kering dan basah). Tanpa pembagi, output 5 V merusak IO34. Firmware menganggap **tegangan tinggi = ada air**; kalau XKC kamu kebalikannya, kabari supaya logika dibalik. Sensitivitas diatur di potensiometer sensor.

### 2.3 Tahap perakitan (cek tiap tahap sebelum lanjut)
| Tahap | Tambahkan | Yang harus muncul di serial |
|---|---|---|
| 1 | Hanya DevKit | `Boot: MPU=0 LoRa=0 ...` |
| 2 | + GY-521 | `MPU=1`, `g=` sekitar 1.00-1.20 di baris `[status]` |
| 3 | + tombol power dan SOS | Tahan SOS 2 detik: paket `PANDU,V1,SOS,...`. Tekan power: `Sleep...` |
| 4 | + sensor air | `air=kering (xxx mV)`, celup: `air=ADA AIR` |
| 5 | + GPS | `gps=NOFIX` (dalam ruangan), `FIX` di luar ruangan |
| 6 | Helmet menyala | `helm=1` setelah beberapa detik |

### 2.4 Baris serial Vest
Tiap 2 detik:
```
[status] helm=1 rssi=-62 dBm | air=kering (180 mV) | jendela MOB=0s | gps=NOFIX sat=0 | g=1.02
```
| Bagian | Arti |
|---|---|
| `helm=1` | Beacon helm terdengar dan dekat (RSSI di atas ambang) |
| `helm=0` | Terdengar tapi jauh (RSSI lemah) |
| `helm=2` | Tidak terdengar lebih dari 30 detik (helm OFF atau terlalu jauh) |
| `air` | `kering` atau `ADA AIR` plus tegangan sensor |
| `jendela MOB=Ns` | Sisa jendela 60 detik setelah FALL (0 = tidak aktif) |
| `g` | Besar percepatan (1.0 = diam) |

Paket yang terkirim (untuk LoRa nanti), contoh:
```
PANDU,V1,HB,NOFIX,NOFIX,<mV>,1,0      heartbeat tiap 30 detik
PANDU,V1,SOS,NOFIX,NOFIX,<mV>,1,0     SOS (ulang tiap 5 detik, 3 kali)
PANDU,V1,FALL,...                     jatuh
PANDU,V1,MOB,...                      jatuh + air
```
Kolom ke-7 = status helm (1/0/2), kolom ke-8 = usia posisi GPS (detik).

## 3. Skenario demo (urut)
Taruh Helmet sekitar 0,3-0,5 m dari Vest.

1. **Boot**: Vest `MPU=1 LoRa=0`, Helmet `beacon ON`.
2. **Helm dekat**: `helm=1` di status Vest dalam beberapa detik.
3. **Helm dimatikan**: tekan tombol Helmet (`BEACON OFF`). Setelah 30 detik status Vest jadi `helm=2` (tidak terjangkau). Tekan lagi, kembali `helm=1`.
4. **Helm dijauhkan** (beberapa meter atau di balik dinding): `helm=0` saat RSSI di bawah ambang -85 dBm (`HELM_RSSI_MIN`, perlu kalibrasi, lihat bawah).
5. **SOS manual**: tahan tombol SOS 2 detik, paket `SOS` muncul (diulang 3 kali).
6. **FALL**: jatuhkan Vest dari sekitar 0,5-1 m ke bantal tebal. Paket `FALL` muncul dan `jendela MOB` mulai 60 detik.
7. **MOB**: setelah FALL (dalam 60 detik), celupkan sensor air selama 3 detik atau lebih. Paket `MOB` muncul.
8. **Basah saja**: celup sensor air tanpa jatuh dulu, **tidak ada** alarm (hanya `air=ADA AIR` di status).
9. **Power**: tekan tombol power (`Sleep...`), lalu SOS saat tidur membangunkan dan langsung mengirim paket SOS. Tombol power juga membangunkan.
10. **GPS** (opsional): bawa ke luar ruangan dan tunggu fix. Kolom lat/lon terisi.

## 4. Kalibrasi singkat sebelum demo
- **RSSI helm**: letakkan Helmet pada jarak "dipakai" (sekitar 0,3-0,5 m dari Vest) dan lihat `rssi=` di status. Lalu pada jarak "tidak dipakai" (2-3 m). Pilih `HELM_RSSI_MIN` di tengahnya, ubah di `firmware/vest_node/src/main.cpp`, lalu upload ulang. Default -85 dBm.
- **Jatuh**: kalau FALL tidak terpicu di bantal, turunkan `IMPACT_G` (2,5 g); kalau terlalu sensitif, naikkan `FREEFALL_MS`.
- **Air**: kalau air tidak terbaca, cek mV saat basah dan sesuaikan `WATER_WET_MV`.

## 5. Masalah umum
| Gejala | Cek |
|---|---|
| Board reset terus dengan "Brownout detector was triggered" | Ganti kabel USB (pendek, tebal), tambah 100 µF di 3V3, lepas modul yang tidak dipakai, coba port USB lain |
| Port tidak terdeteksi | Kabel data, driver, tahan BOOT saat colok (SuperMini) |
| Serial kosong di SuperMini | Tekan RESET sekali, pastikan hanya satu monitor membuka port |
| `MPU=0` | SDA/SCL tertukar, VCC, GND |
| `helm=2` terus | Helmet belum menyala atau terlalu jauh, cek serial Helmet, dekatkan |
| FALL tidak terpicu | Jatuhkan lebih tinggi (>=0,5 m), cek `g=` turun di bawah 0,6 saat jatuh |
| MOB tidak terpicu | MOB hanya setelah FALL dan dalam 60 detik; air harus aktif 3 detik |
| SOS terpicu sendiri | Resistor 10 kΩ IO27 ke GND belum terpasang |

## 6. Batasan demo
- LoRa tidak dites; pengiriman ke Gateway dan dashboard belum ada.
- Daya dari USB, bukan baterai; umur baterai belum terbukti.
- Ambang jatuh, air, dan RSSI belum divalidasi di kondisi nyata (badan, kapal, hujan).
- GPS di dalam ruangan tidak akan fix.
