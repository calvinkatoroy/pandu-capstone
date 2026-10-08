# Checklist Uji Rakit PANDU (v2)

Urutan dari paling aman ke paling berisiko. Centang `[x]` hanya jika diukur sendiri. Jangan lanjut ke tahap berikutnya kalau tahap sebelumnya gagal.
Alat: multimeter, power supply 5 V terbatas arus (atau USB), kabel USB, kabel jumper, perfboard/breadboard, 1 antena LoRa (JANGAN transmit tanpa antena).

Firmware: `firmware/vest_node`, `firmware/helmet_node`, `firmware/gateway` (build: `python -m platformio run`, upload: `python -m platformio run -t upload`, monitor: `python -m platformio device monitor`).

## 0. Verifikasi modul fisik (sebelum order PCB)
- [ ] **ESP32 DevKit**: ukur jarak tengah lubang pin kiri-kanan. Resmi 25,4 mm. Hasil: ____ mm. Jika 22,86 mm, footprint PCB1/PCB3 harus diubah.
- [ ] **Modul LoRa**: foto sisi pin, cocokkan urutan dengan RA-02 (pin 1 ANT, 2 GND, 3 3,3V, 4 RESET, 5 DIO0 ... 12 SCK, 13 MISO, 14 MOSI, 15 NSS, 16 GND). Hasil: ____ (cocok / tidak cocok). Jika bukan RA-02, footprint harus diubah.
- [ ] **TP4056**: urutan pin/pad (IN+, IN-, OUT+, OUT-, B+, B-) dan posisi USB-C sesuai footprint.
- [ ] **Boost MT3608**: urutan IN+/IN-/OUT-/OUT+ sesuai header 4 pin (`IN+ IN- OUT- OUT+`).
- [ ] **SuperMini C3 (Helmet)**: urutan pin dan posisi pin 3V3/5V/GND/GPIO2/GPIO4 sesuai simbol.
- [ ] **XKC-Y25**: tipe output (NPN open-collector atau tegangan) dan tegangan kerja. Hasil: ____. Jika output 5 V, IO34 butuh pembagi/level shifter.
- [ ] **Modul sentuh TTP223**: mode (momentary/toggle), output aktif-HIGH atau LOW. Hasil: ____.
- [ ] **Holder 18650, GPS NEO-6M, MPU6050**: ukur dimensi untuk dicocokkan ke casing.

## 1. Daya Vest (tanpa ESP32 terpasang)
- [ ] **Setel boost ke 5,0 V dulu**, sebelum disambung ke apa pun: input 3,7 V dari power supply, putar trimmer, ukur output. Hasil: ____ V (target 5,0 ± 0,1).
- [ ] TP4056: colok USB-C tanpa baterai, ukur tegangan OUT. Dengan baterai terpasang: LED merah (charging) menyala, lalu biru/hijau saat penuh.
- [ ] Baterai 18650 terpasang, ukur `VBAT_RAW` di PCB: ____ V (3,0–4,2).
- [ ] Ukur `BAT_SENSE` (tengah R6/R7): harus separuh `VBAT_RAW`. Hasil: ____ V.
- [ ] Ukur 5V di pin 5V DevKit dan `VBOOST_5V`. Selisih = drop D1 (SS14, sekitar 0,3–0,5 V). Hasil: ____ V.
- [ ] Ukur arus tanpa beban (hanya boost): ____ mA.

## 2. Vest: boot dan sensor
- [ ] Upload `vest_node`. Serial menunjukkan `Boot: MPU=1 LoRa=1 wake=other`. Jika `MPU=0`: cek I2C (SDA IO21, SCL IO22, alamat 0x68). Jika `LoRa=0`: cek CS IO5, RST IO25, DIO0 IO26, antena.
- [ ] **3V3**: ukur 3V3_SYS = ____ V (3,2–3,4).
- [ ] **Gating GPS**: `GPS_EN` (IO4) LOW → `GPS_3V3` ≈ 3,3 V; hi-Z → `GPS_3V3` ≈ 0 V. Hasil ON: ____ V, OFF: ____ V.
- [ ] **Gating XKC-Y25**: `XKC_EN` (IO32) HIGH → `XKC_5V` ≈ 5 V; LOW → ≈ 0 V. Hasil ON: ____ V, OFF: ____ V.
- [ ] **GPS**: di luar ruangan, NMEA terbaca dan fix didapat dalam ____ detik. Paket LoRa berisi lat/lon (bukan `NOFIX`).
- [ ] **MPU6050**: jatuhkan alat ke kasur dari ±1 m. Ambang jatuh (0,4 g / 2,5 g) memicu `FALL`? Tidak memicu saat diayun/diguncang biasa? Catat nilai yang berhasil: ____ g / ____ g.
- [ ] **Sensor air**: celupkan XKC-Y25 ke air. `WATER_SIG` (IO34) berubah dan `MOB` terkirim setelah 3 detik. Percikan singkat < 3 detik tidak memicu.
- [ ] **Tombol power (IO13)**: tekan = tidur (serial `Sleep...`), tekan lagi = bangun.
- [ ] **Tombol SOS (IO27)**: tahan 2 detik = `SOS` terkirim. Saat tidur, tekan SOS membangunkan alat dan langsung mengirim (3x ulang).
- [ ] **Baterai di paket**: mV di paket ≈ nilai multimeter (selisih < 50 mV). Kalibrasi `BAT_DIV`. Hasil: ____.

## 3. Gateway
- [ ] Upload `gateway`. Serial `{"boot":true,"lora":1,"sd":1}`. Jika `sd":0`: cek kartu SD (FAT32), CS IO13, kabel.
- [ ] Sirine lepas dulu, ukur gate IRLZ44N: 0 V saat idle, ≈ 3,3 V saat sirine ON.
- [ ] Sambung sirine/beban uji (jangan langsung sirine penuh): LED + resistor dulu, lalu sirine. Arus sirine ____ A, jalur 5V DevKit tidak jatuh di bawah 4,5 V.
- [ ] **Hanya satu port USB** dicolok (micro-USB DevKit). Jangan pernah dua sumber 5 V bersamaan.
- [ ] Mute: kirim `M` di serial, sirine berhenti.

## 4. Tautan LoRa Vest → Gateway
- [ ] Frekuensi sama (915 MHz default kedua firmware). Antena terpasang di kedua sisi.
- [ ] Jarak 1 m: paket `HB` (heartbeat tiap 30 s) diterima. Catat RSSI: ____ dBm.
- [ ] Jarak 10, 50, 100 m (terbuka): RSSI ____ / ____ / ____ dBm; paket hilang? ____ %.
- [ ] Simulasikan `SOS`: sirine Gateway bunyi dalam < 2 detik; `/pandu.csv` bertambah satu baris.
- [ ] Simulasikan `FALL` dan `MOB`: pola sirine berbeda (200 ms vs 500 ms).
- [ ] Matikan Vest: setelah 90 detik Gateway mencetak `vest_lost`.
- [ ] Paket asing (kirim string acak dari modul lain) diabaikan (`bad_packet`).

## 5. Helmet
- [ ] LiPo + TP4056: ukur `VBAT_SW` (setelah saklar) ≈ tegangan baterai ____ V; ukur 3V3 output SuperMini = ____ V (harus 3,3 V, di baterai 3,3-4,2 V).
- [ ] Cek di board SuperMini: pin 5V melewati regulator (jangan memberi 4,2 V ke pin 3V3). Colok USB SuperMini sambil baterai terpasang: tidak ada arus balik ke USB (ukur arus), tidak ada panas.
- [ ] Isi baterai lewat TP4056 USB-C: LED charging menyala, suhu normal.
- [ ] Upload `helmet_node`. Serial: `helm dipakai=0`.
- [ ] Sentuh sensor TTP223: setelah 2 siklus (≈ 8–16 s) `helm dipakai=1`. Lepas: berubah ke 0 setelah 3 siklus.
- [ ] Tombol GPIO4: tekan = OFF (tidur tanpa timer), tekan lagi = ON.
- [ ] **Arus rata-rata** (ampere-meter seri dengan baterai, rata-rata ≥ 60 s): ____ mA. Arus saat tidur: ____ µA. Target < 2 mA. Perkiraan umur CR2032 = 220 mAh ÷ arus = ____ jam.
- [ ] Tegangan saat burst BLE (osiloskop jika ada, atau pantau brownout): tidak ada reset acak.
- [ ] Lepas LED daya SuperMini dan ukur ulang arus: ____ mA.

## 6. Vest ↔ Helmet (BLE)
- [ ] Helm dipakai: paket LoRa Vest berisi field helm `1` setelah ≤ 24 s.
- [ ] Helm dilepas: field berubah ke `0`. Helm dimatikan/jauh > 30 s: `2`.
- [ ] Beberapa helm PANDU berdekatan: Vest tidak salah menangkap helm lain? (belum ada ID pasangan)
- [ ] Jarak BLE maksimum (helm ke Vest di badan): ____ m.
- [ ] Arus Vest naik berapa dengan scan BLE terus-menerus? ____ mA (perkiraan +10–15 mA).

## 7. Uji ketahanan
- [ ] Vest aktif penuh (GPS + BLE + LoRa) sampai baterai 3,3 V: ____ jam. Target ≥ 8 jam (satu shift).
- [ ] Uji percikan air pada casing/plug USB (hanya klaim "tahan percikan" kalau lolos).
- [ ] Uji getar/jatuh ringan: tidak ada sambungan lepas.
- [ ] Charging di dalam casing: suhu TP4056 tidak > 60 °C.

## Catatan hasil
| Tanggal | Bagian | Hasil | Tindak lanjut |
|---|---|---|---|
| | | | |
