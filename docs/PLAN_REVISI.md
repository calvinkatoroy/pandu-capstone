# Plan revisi PANDU (EasyEDA, firmware, dokumen, dashboard)

Dasar: [AUDIT_V2.md](AUDIT_V2.md) (kode temuan A1.., B1.., C1.., D1..) dan definisi proyek terbaru dari Calvin.
Ukuran pekerjaan: S = kecil (menit), M = sedang (sekitar satu sesi), L = besar (beberapa sesi). Perkiraan kasar, bukan janji.

## Keputusan yang sudah dikunci
- MOB = jatuh, lalu basah (>=3 s) dalam 60 s. FALL sendiri = danger. SOS manual = danger. Basah saja = bukan alarm.
- Tahap: 1 aman, 2 warning (helm tidak dekat), 3 danger. Status terpisah: tidak terjangkau dan inaktif (paket OFF).
- Helm: tombol on/off + beacon BLE + RSSI. Tanpa sensor sentuh. Baterai LiPo + TP4056 (bukan CR2032).
- Sampai 8 Vest, ID tetap 1-8 (firmware) + ID perangkat dari MAC. Heartbeat 30 s dengan jitter, paket biner kompak, SF10-12.
- Gateway di dermaga: WiFi, cloud (Supabase atau Firebase), microSD hanya buffer offline (store-and-forward), buzzer lokal, NTP.
- Alarm hilang saat normal, bisa di-mute dan dihapus operator. Danger yang kehilangan kontak tetap sampai operator mengakui.
- Demo awal tanpa LoRa (lihat TUTORIAL_DEMO_TANPA_LORA.md).

## Keputusan yang masih menunggu
| # | Pertanyaan | Mempengaruhi |
|---|---|---|
| K1 | Varian XKC-Y25 (NPN atau tegangan) dan polaritasnya: ukur saat modul datang | PCB1 rangkaian IO34 |
| K2 | Indikator di Vest (LED/haptic): masuk atau dibuang dari BOM | PCB1 |
| K3 | Dashboard untuk overseer atau pandu? Tombol "I'm safe" dan "Hold to send SOS" dibuang atau dipertahankan (butuh downlink) | APP, Gateway |
| K4 | Baterai helm perlu dilaporkan di dashboard? | PCB2 (pembagi), beacon |
| K5 | Cadangan daya Gateway (UPS atau power bank) | PCB3, casing |
| K6 | Cloud: Supabase atau Firebase (tanya Rafif) | Gateway, APP |

## Gerbang sebelum PCB dipesan
Semua harus terpenuhi: (1) cek modul fisik di bawah selesai, (2) revisi EasyEDA selesai dan DRC 0, (3) tes demo Vest + Helmet lulus, (4) tautan LoRa Vest ke Gateway lulus di breadboard, (5) Gerber lama di repo ditandai tidak valid.

## Fase 0: Persiapan (S)
1. Di EasyEDA buat salinan project ("Pandu-Capstone-v2.1-backup") sebelum mengedit apa pun, supaya bisa dikembalikan.
2. Git: tag `v2.1` pada commit sekarang, kerja revisi di branch baru `v3`.
3. Pindahkan Gerber lama (10-03, 10-06) ke `hardware/gerber/_obsolete/` dan tandai di README.

## Fase 1: Cek modul fisik (M, Calvin, sebelum edit PCB)
Hasilnya ditulis di bagian 7 `TUTORIAL_BREADBOARD.md`.
| Item | Yang diukur/dicek |
|---|---|
| ESP32 DevKit | Jarak tengah lubang kiri-kanan (25,4 atau 22,86 mm), ukuran papan |
| Modul LoRa XL1276-P01 | Lebar dan jarak deret pad, panjang modul, pita 868M atau 915M (kotak yang terisi), jarak pitch 2 mm |
| TP4056 HW-373 | Urutan pad kiri ke kanan (OUT−, B−, B+, OUT+ dari foto), ukuran papan, posisi USB-C |
| GY-521 | Urutan pin header dan jarak, posisi lubang baut |
| GPS NEO-6M | Urutan pin (VCC, RX, TX, GND?), ukuran, konektor antena |
| SuperMini | Pin map (GPIO4, 3V3, 5V, GND), apakah pin 5V lewat regulator (ukur 3V3 dengan 4 V di pin 5V), dioda ke VBUS |
| Boost MT3608 | Urutan pad IN+, IN-, OUT-, OUT+ |
| Modul microSD | Urutan pin header, level logika |
| XKC-Y25 | Varian, tegangan output saat kering dan basah (K1) |
| Sensor air murah | Konektor S/+/- |

## Fase 2: Revisi EasyEDA

### Cara kerja (dari HANDOVER, UI rapuh)
- Satu perubahan, satu simpan, satu DRC. Net label tepat di ujung pin. Jangan `ctrl+a` kecuali fokus pasti di kolom input.
- Alur PCB: Design > Update PCB from Schematic (Apply Changes) > Route > Unroute All > Auto Route (Run) > Tools > Copper Manager Rebuild All > DRC.
- Setelah tiap board: ekspor netlist (`.tel`), jalankan `check_netlist.py`, ekspor Gerber (jangan klik Order PCB), simpan di `hardware/`.

### PCB2 Helmet (M) kerjakan lebih dulu, paling kecil
| # | Tugas | Kode audit |
|---|---|---|
| P2-1 | Ganti `SAW1` dengan saklar geser sungguhan (SPDT/SPST THT 2,54 mm) atau header 2 pin + jumper; perbarui footprint | A1 |
| P2-2 | Pisahkan negatif baterai: net `BAT_NEG` = `H2.2` + pin `B-` TP4056; hanya `OUT-` dan `IN-` ke GND | A2 |
| P2-3 | Hapus TTP223 (`H1`) dan net `TOUCH_SIG` | A5 |
| P2-4 | Cocokkan pin map SuperMini (`U1` pin 13 GPIO4, 14 3V3, 16 5V) dengan modul fisik | A12 |
| P2-5 | (jika K4) pembagi baterai ke satu GPIO ADC | K4 |
| P2-6 | Kecilkan outline setelah TTP223 dilepas, DRC, Gerber, netlist | |

### PCB1 Vest (L)
| # | Tugas | Kode audit |
|---|---|---|
| P1-1 | Pisahkan negatif baterai: `BAT_NEG` = `BT1.2` + `U7.3 (B-)`; `U7.4 (OUT-)` dan `U7.6 (IN-)` ke GND | A2 |
| P1-2 | Ganti footprint LoRa `U6` ke RFM95 (pinout fisik), sambung ulang ANT, GND, 3V3, RST (IO25), DIO0 (IO26), NSS (IO5), SCK/MISO/MOSI | A3 |
| P1-3 | Sensor air: sesuai K1. Siapkan pembagi `R8` 10 k dan `R9` 20 k (bisa tidak dipasang) di `WATER_SIG`; `R1` pull-up hanya untuk varian open-collector | A4 |
| P1-4 | Lebarkan `VBAT_RAW`, `VBOOST_5V`, `VBAT_POS` ke sekitar 25 mil | A13 |
| P1-5 | (jika K2) LED atau haptic + resistor ke GPIO bebas | A11 |
| P1-6 | Cocokkan footprint GY-521, TP4056, GPS, DevKit dengan hasil Fase 1 | A12 |
| P1-7 | (opsional) lepas jalur TX ESP ke GPS | A14 |
| P1-8 | Titik uji untuk 3V3, 5V, GND, BAT, WATER; label versi di silkscreen | |
| P1-9 | Route ulang (papan padat, kemungkinan perlu geser komponen), DRC, Gerber, netlist | |

### PCB3 Gateway (M)
| # | Tugas | Kode audit |
|---|---|---|
| P3-1 | Ganti footprint LoRa `U1` ke RFM95 | A3 |
| P3-2 | Pindahkan microSD ke bus SPI terpisah: usul `SD_SCK`=IO25, `SD_MISO`=IO35 (input-only, cukup), `SD_MOSI`=IO32, `SD_CS`=IO33; hindari pin strapping (0, 2, 5, 12, 15). LoRa tetap di IO18/19/23 | A8 |
| P3-3 | Tombol mute (tact ke GND di IO27, pull-up internal); LED status memakai LED onboard DevKit (IO2) | A9 |
| P3-4 | Dioda flyback (1N4148/1N5819) di terminal sirine, bisa tidak dipasang untuk buzzer elektronik | A15 |
| P3-5 | Cocokkan urutan header microSD `H1` dengan modul fisik | A12 |
| P3-6 | (jika K5) konektor cadangan daya | A10 |
| P3-7 | DRC, Gerber, netlist | |

### Setelah ketiganya
- Perbarui `check_netlist.py` agar mencakup PCB2 dan pin map baru PCB3.
- Pembaruan `hardware/README.md` dan HANDOVER dengan daftar Gerber yang valid.

## Fase 3: Firmware (M-L)
| # | Tugas | Kode audit |
|---|---|---|
| F-1 | Paket biner v2: ID Vest, nomor urut, jenis (HB, SOS, FALL, MOB, OFF), lat, lon, baterai, helm, usia posisi, opsional sat/HDOP | B2, B9 |
| F-2 | Vest: FALL lalu MOB (sudah di kode, perlu uji), paket OFF saat tidur, jitter heartbeat, ID di NVS (set lewat serial) | B1, B6 |
| F-3 | Pairing: beacon helm membawa ID, Vest hanya menerima ID pasangannya | B7 |
| F-4 | LoRa: SF, BW, daya lewat konstanta dua sisi; ACK untuk SOS dengan ulang sampai diterima | B3, B6 |
| F-5 | Gateway: WiFi, NTP, dorong ke server, antrean di SD (store-and-forward), SD di SPI kedua, pemetaan tahap 1/2/3, tombol mute | B4, A8, A9 |
| F-6 | Tes logika di laptop (native test) untuk FALL/MOB, tahap, timeout, antrean | |
| F-7 | Kalibrasi: ambang jatuh, air, RSSI helm dengan data nyata | B5 |

## Fase 4: Dashboard (M-L, Rafif + Calvin)
1. Sepakati skema data JSON (id, seq, waktu, jenis, lat, lon, baterai, helm, rssi, usia posisi).
2. Backend (K6): tabel `events`, `vests` (last_seen); Realtime untuk push ke web.
3. Web/PWA: daftar sampai 8 pandu dengan warna tahap, peta live (Leaflet + OpenStreetMap), log kejadian, mute dan hapus alarm, notifikasi saat danger.
4. Ganti `APP/index.html` statis dengan versi terhubung ke data; sesuaikan elemen yang tidak ada di hardware (C5, C6).
5. Status "tidak terjangkau" setelah 3 heartbeat hilang; "inaktif" jika paket OFF.

## Fase 5: BOM dan dokumen (S-M)
- Perbarui BOM sheet dengan `BOM_V2.md` dan hasil revisi (RFM95, saklar, pembagi, tombol mute, dioda).
- Rapikan HANDOVER, hapus catatan usang, perbarui checklist dan tutorial breadboard (TTP223, CR2032).
- Laporan Pekan 6 dan 7: perubahan scope, temuan audit, hasil tes.

## Fase 6: Uji dan pesan PCB
1. Demo Vest + Helmet lulus (TUTORIAL_DEMO_TANPA_LORA.md).
2. Modul LoRa kedua datang, tautan Vest ke Gateway di breadboard, survei RSSI di beberapa jarak.
3. Tes XKC (hujan, keringat, celup), tes baterai dan charging dengan TP4056 yang benar.
4. Gerbang PCB terpenuhi, baru pesan. Setelah PCB datang: ulangi checklist rakit.
5. Casing Helmet dan Gateway, update casing Vest.

## Urutan kerja yang disarankan
Fase 0 → Fase 1 (paralel: Fase 3 F-1 s/d F-3) → Fase 2 (PCB2, lalu PCB3, lalu PCB1) → Fase 3 F-4 s/d F-6 → Fase 4 → Fase 6.

## Risiko
- Jarak 5 km di atas laut belum terbukti; antena Gateway harus tinggi, perlu survei lapangan.
- XKC terhadap keringat dan hujan hanya terbukti lewat tes nyata.
- Umur baterai Vest kemungkinan sekitar 4-5 jam (perkiraan kasar), di bawah target satu shift.
- Auto-router PCB1 padat; tiap perubahan dapat memerlukan penempatan ulang.
