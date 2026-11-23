# Audit hardware sebelum pesan PCB + PCBA (JLCPCB)

Per 23 Nov 2026. Cakupan: PCB1 Vest, PCB2 Helmet, PCB3 Gateway. **Firmware diaudit di dokumen terpisah.**
Status: `TERBUKTI` (ada ukuran/log/hasil), `DUGAAN` (listing/datasheet/ingatan), `BELUM DICEK`.
Aturan: jangan klaim selesai tanpa bukti; jangan menekan "Order" tanpa izin Calvin; jangan push ke `main`.

## 0. Keputusan yang berubah
- 14-15 Nov: PCB saja ke Indomaker, komponen disolder sendiri.
- **23 Nov: PCBA via JLCPCB**, part yang tersedia dirakit langsung oleh JLCPCB. Modul (DevKit, Ra-02, GY-521, GPS, TP4056, MT3608, XKC) tetap dipasang sendiri lewat female header.
- Angka aturan JLCPCB di dokumen ini = `DUGAAN` sampai dicek di halaman kapabilitas JLCPCB.
- Item aturan Indomaker (bagian 1 lama) tidak berlaku lagi kecuali pesan PCB polos ke Indomaker.

## 1. Aturan pabrik (JLCPCB)
| # | Item | Status |
|---|---|---|
| 1.1 | Jalur min, clearance min, via, lubang THT, annular ring sesuai kapabilitas JLCPCB | DUGAAN, lebih kuat (23 Nov, hasil pencarian web, halaman resmi belum dibuka langsung): JLCPCB 2 layer 1 oz min jalur/jarak sekitar 4-5 mil, bor min 0,15-0,3 mm (sumber saling beda). Desain kita 16 mil / 20 mil / via 1,0 mm / THT 1,1 mm jauh di atas batas, jadi hampir pasti lolos. Konfirmasi di https://jlcpcb.com/capabilities/pcb-capabilities dan DFM JLC (7.4) |
| 1.2 | Ukuran PCB (PCB1 107,95 x 95,25; PCB2 31,6 x 99,1; PCB3 54,6 x 100,3 mm) diterima, tidak ada syarat min 10 x 10 cm | DUGAAN |
| 1.3 | Jumlah layer, tebal, finishing (HASL/ENIG), warna solder mask dipilih | BELUM DICEK |
| 1.4 | Jarak tembaga ke tepi papan, lubang M3 NPTH 3,2 mm, jarak pad ke tepi | BELUM DICEK (cek di Gerber viewer) |
| 1.5 | Lebar dan tinggi silkscreen terbaca, tidak menimpa pad | BELUM DICEK |
| 1.6 | Panelisasi: satu file per PCB atau digabung; V-cut/tab-route bila digabung | BELUM DICEK |

## 2. Skematik dan elektrikal
| # | Item | Status |
|---|---|---|
| 2.1 | DRC PCB1/2/3 = 0 | TERBUKTI (23 Nov, 22:36-22:52) |
| 2.2 | Import Changes dari skematik kosong di PCB1/2/3 | TERBUKTI |
| 2.3 | Ratlines PCB3 = 0 (PCB1/2 lewat DRC) | TERBUKTI PCB3 |
| 2.4 | Satu-satunya error DRC skematik = U3 8 pin tanpa pad (J2-16/17/18, J3-7/14/17/18/19) | TERBUKTI |
| 2.5 | Delapan pin U3 tanpa pad **tidak dipakai** net manapun yang perlu | BELUM DICEK |
| 2.6 | Netlist cocok dengan pin firmware | TERBUKTI untuk PCB1 (`PCB1.tel` vs `vest_node/main.cpp` dan tes breadboard) dan PCB3 (`PCB3.tel` vs `gateway/main.cpp`), 23 Nov. Netlist hasil ekspor BARU dan `check_netlist.py` BELUM DICEK (`PCB2.tel` usang) |
| 2.6a | Tes breadboard (`test_gps`, `test_water`) tidak menyalakan switch daya: di PCB1 GPS butuh IO4 LOW, XKC butuh IO32 HIGH | TERBUKTI dari kode; berlaku saat tes di PCB, bukan blocker pesan |
| 2.7 | Pin strapping (IO0/2/5/12/15), IO6-11 tidak dipakai, IO34-39 hanya input | BELUM DICEK |
| 2.8 | Anggaran arus: boost MT3608 vs beban 5 V, regulator 3V3 DevKit vs GPS + Ra-02 + IMU (+SD di PCB3), arus TP4056 vs baterai 1200 mAh | BELUM DICEK |
| 2.9 | Mapping pad TP4056 (U7) ke net: pad THT 6 buah, 4 di X 1650 mil, 2 di X 727 mil | TERBUKTI pad ada; pemetaan fungsi BELUM DICEK vs modul fisik |
| 2.10 | Q1 (2N7002): pin G/D/S di footprint sama dengan datasheet part LCSC | BELUM DICEK |
| 2.11 | Pull-up/pull-down yang dibutuhkan (I2C GY-521, EN, tact, XKC_EN) ada | BELUM DICEK |
| 2.12 | Polaritas baterai: pad 1 holder = VBAT_POS = terminal + holder asli | BELUM DICEK (fisik) |
| 2.13 | Proteksi baterai 18650 (ada PCM atau tidak), merek, kapasitas | BELUM DICEK |

## 3. Footprint vs benda fisik (paling berisiko)
| # | Item | Status |
|---|---|---|
| 3.1 | Ukuran dan jarak deret semua modul lolos cetak 1:1 | DUGAAN (laporan Calvin 21 Nov, detail per modul belum dirinci) |
| 3.2 | DevKit V1 30 pin: jarak deret 25,4 mm, urutan pin | TERBUKTI (5 Nov) |
| 3.3 | Ra-02 breakout: jarak deret 25,4 mm, urutan pin | TERBUKTI (11 Nov) |
| 3.4 | Urutan pin GPS (HW-248 / GPS6MV2, NEO-6M): silkscreen kiri ke kanan **VCC, RX, TX, GND** (4 lubang, header di tepi atas) | TERBUKTI (foto 23 Nov) cocok dengan netlist PCB1 U9.1 VCC(GPS_3V3), U9.2 RX(GPS_RX), U9.3 TX(GPS_TX), U9.4 GND. Nama net dari sisi modul: GPS_RX = IO17 (TX2) ke RX modul, GPS_TX = IO16 (RX2) dari TX modul, benar silang. Posisi pad U9 di footprint EasyEDA BELUM DICEK |
| 3.5 | Urutan pin GY-521 (MPU-6050): dari atas **VCC, GND, SCL, SDA, XDA, XCL, AD0, INT** (8 pin, header 1 baris) | TERBUKTI (foto 23 Nov). Netlist PCB1: U8.8 VCC, U8.7 GND, U8.6 SCL, U8.5 SDA, jadi simbol bernomor terbalik (pin 1 = INT). Benar hanya jika pad 8 di footprint ada di ujung VCC; BELUM DICEK di EasyEDA. XDA/XCL/AD0/INT tidak dihubungkan (AD0 ada pull-down di modul, DUGAAN) |
| 3.6 | Urutan pin modul microSD (PCB3): dengan slot kartu di atas, header di bawah kiri ke kanan **GND, VCC, MISO, MOSI, SCK, CS** (6 pin) | TERBUKTI (foto 23 Nov) cocok persis dengan H1.1 GND, H1.2 5V_SYS, H1.3 SD_MISO, H1.4 SD_MOSI, H1.5 SD_SCK, H1.6 SD_CS. Modul punya regulator AMS1117 dan IC level shifter (terbaca di foto), jadi VCC 5 V benar (batas tegangan DUGAAN). Pitch dan lubang H1 di footprint BELUM DICEK |
| 3.6a | Q1 (switch GPS) dan Q2 (switch XKC) di PCB1: topologi netlist (pin 2 = 3V3/5V, pin 3 = beban, gate ditarik ke 3V3/5V) berarti **harus P-channel**, bukan 2N7002 (N-channel). Cek part LCSC dan footprint tiap Q | Firmware vest menyebut Q1 = P-MOSFET (gate LOW = ON), cocok dengan topologi. **TERBUKTI di EasyEDA PCB1 (23 Nov): Q1 dan Q2 = AO3401A, LCSC C15127, kelas Basic Part, "1 P-Channel"**, jadi P-channel sesuai. Ada juga **Q5 = 2N7002 (C8545, N-channel)** di PCB1; fungsinya BELUM DICEK (audit lama menyebut Q1 = C8545, itu salah nama). Urutan pin G/D/S footprint vs datasheet AO3401A BELUM DICEK |
| 3.7 | Footprint tact switch: kaki dan jarak sesuai part yang dibeli | BELUM DICEK (belum diganti) |
| 3.8 | MT3608: pin IN+/IN-/OUT+/OUT-, jarak lubang | BELUM DICEK |
| 3.9 | Konektor sensor air XKC-Y25-V (jumlah pin, urutan) | BELUM DICEK |
| 3.10 | Holder 18650 `BH-18650-A1AJ005`: jenis pin, tiang penempatan, jarak pad, lubang | BELUM DICEK (pad: lubang 40,2 mil, pad 63 mil = TERBUKTI di EasyEDA saja) |
| 3.11 | TP4056 HW-373: kaki modul benar-benar mencuat di sisi bawah, panjangnya | BELUM DICEK (fisik) |
| 3.12 | Cetak tusuk kertas 1:1 ulang untuk PCB1/2/3 versi terbaru (setelah BT1/J1/H2 dipindah) | BELUM DICEK |

## 4. Layout 2D
| # | Item | Status |
|---|---|---|
| 4.1 | Lebar jalur daya PCB1: VBAT_POS, VBAT_RAW, BAT_NEG, VBOOST_5V = 0,635 mm | TERBUKTI |
| 4.2 | Lebar jalur daya PCB2: semua VBAT*/BAT_NEG = 25 mil | TERBUKTI |
| 4.3 | Lebar jalur daya PCB3: 5V_SYS = 25 mil; 3V3 = 25 mil | TERBUKTI (23 Nov): rule net 3V3 diganti ke `power25mil`, net 3V3 di-unroute lalu auto-route; Property List: 6 jalur 3V3 semuanya 25 mil (2 Top, 4 Bottom), 0 via, ratlines 0, DRC "No issues found" (141 item) |
| 4.4 | Jalur sinyal 16 mil (aturan dosen) | TERBUKTI via aturan default |
| 4.5 | Jarak holder ke DevKit di PCB1 = 4,3 mm | TERBUKTI (ruler 2D) |
| 4.6 | Keep-out antena Ra-02 dan antena ESP32 bebas tembaga/pour | BELUM DICEK |
| 4.7 | Pour GND utuh, tidak ada pulau tembaga, Rebuild All dijalankan | BELUM DICEK (DRC 0 saja) |
| 4.8 | USB DevKit dan USB-C TP4056 bisa dijangkau kabel (PCB1: USB di dalam via kabel ekstensi) | BELUM DICEK |
| 4.9 | Silkscreen: label tiap modul, penanda pin 1, tanda +/- baterai, nama board + versi | BELUM DICEK |
| 4.10 | Test point untuk power rail dan UART (opsional) | BELUM DICEK |
| 4.11 | Tombol (SOS IO27, power IO13, PCB2 GPIO4) mudah dijangkau | BELUM DICEK |

## 5. 3D dan mekanik
| # | Item | Status |
|---|---|---|
| 5.1 | Tidak ada tabrakan komponen tinggi (3D atas) | BELUM DICEK ulang setelah perubahan terakhir |
| 5.2 | PCB2: pad TP4056 1-3 jatuh di dalam area holder, pad 4 di tepi | TERBUKTI geometris; bentrok fisik tergantung cara pasang |
| 5.3 | PCB2 sisi bawah dilihat nyata | BELUM DICEK (kamera 3D EasyEDA tak bisa; pakai Flip Board 2D atau cetak 1:1) |
| 5.4 | Tinggi total PCB2 + holder bawah (~20 mm ekstra), diberi tahu ke Tri Yoga | BELUM DICEK |
| 5.5 | STEP 3D, outline DXF, koordinat konektor/tombol/lubang baut diekspor untuk Tri Yoga | BELUM DICEK |
| 5.6 | 4 lubang baut M3 di tiap PCB sesuai casing | TERBUKTI ada di PCB (21 Nov); kecocokan casing BELUM DICEK |
| 5.7 | Casing mengikuti PCB, bukan sebaliknya; jangan cetak casing sebelum PCB beku | Aturan tim |

## 6. PCBA (JLCPCB), bagian baru
| # | Item | Status |
|---|---|---|
| 6.1 | Daftar part yang dirakit JLC vs dipasang sendiri per PCB | BELUM DICEK |
| 6.2 | Tiap part rakitan punya nomor LCSC; footprint EasyEDA sama dengan part LCSC | BELUM DICEK |
| 6.3 | Q1: PCB1 C8545 vs PCB3 C50176485, satukan bila bisa | BELUM DICEK |
| 6.4 | Female header untuk modul: tipe, pitch 2,54 mm, tinggi, ada di LCSC | BELUM DICEK |
| 6.5 | Tact switch: part LCSC dipilih, footprint cocok | BELUM DICEK |
| 6.6 | Stok semua part cukup; hindari part yang habis/Extended berlebihan (biaya setup per jenis) | BELUM DICEK |
| 6.7 | Part THT dan part sisi bawah (holder 18650 PCB2) dirakit JLC atau disolder sendiri | DUGAAN dari pencarian web 23 Nov (harga bisa beda, cek kuotasi): JLC hanya merakit dua sisi di tier Standard (setup sekitar US$51 vs sekitar US$8 Economic satu sisi); part THT di sisi bawah juga dihitung dua sisi. Rekomendasi: pasang holder 18650 PCB2 sendiri, biarkan semua part rakitan JLC di sisi atas supaya bisa Economic |
| 6.7a | Biaya THT di JLC: biaya per sambungan sekitar US$0,016-0,017 plus biaya tenaga solder tangan per pesanan sekitar US$3,5-7,9 | DUGAAN (sumber berbeda) |
| 2.1a | EasyEDA menampilkan estimasi PCB 54,61 x 100,33 mm 2 layer 5 pcs = US$6,40 (PCB3, hanya referensi, bukan kuotasi) | TERBUKTI dilihat di layar 23 Nov |
| 4.7a | Copper Manager PCB3 hanya punya satu pour: POUR1 di Bottom, net GND, prioritas 1; Top tidak ada pour. Rebuild All dijalankan 23 Nov | TERBUKTI (PCB3). Bentuk pour, pulau, dan PCB1/2 BELUM DICEK |
| 3.5a | U8 GY-521 PCB1: footprint 8 pad satu baris vertikal, pad 1 (INT, tanpa net) di ujung atas pada rotasi 0; netlist menaruh VCC di pad 8 (ujung bawah). Apakah ujung bawah footprint = ujung VCC modul asli tergantung orientasi; BELUM DICEK, putuskan lewat cetak 1:1 |
| 6.8 | BOM CSV (Comment, Designator, Footprint, LCSC Part #) diekspor dari EasyEDA | BELUM DICEK |
| 6.9 | CPL (posisi) diekspor; cek rotasi dan titik asal tiap part di preview JLC | BELUM DICEK |
| 6.10 | Penanda polaritas part rakitan (dioda, LED, IC, tact) sama dengan orientasi CPL | BELUM DICEK |
| 6.11 | Biaya total (PCB + part + setup + kirim + bea) dihitung dan disetujui | BELUM DICEK |

## 7. File keluaran
| # | Item | Status |
|---|---|---|
| 7.1 | Gerber, drill, BOM, CPL, netlist baru diekspor dari salinan EasyEDA untuk PCB1/2/3 | BELUM DICEK (semua Gerber di repo usang: PCB1/PCB3 6 Okt, PCB2 8 Okt) |
| 7.2 | `PCB1.tel`, `PCB2.tel`, `PCB3.tel` diekspor ulang | BELUM DICEK (`PCB2.tel` masih berisi H2 header 2 pin dan J1 lama) |
| 7.3 | Gerber dibuka di viewer: outline, lubang, NPTH, silkscreen, solder mask | BELUM DICEK |
| 7.4 | Unggahan ke JLCPCB: preview, DFM check dari JLCPCB lolos | BELUM DICEK |
| 7.5 | Download berkas butuh izin eksplisit Calvin | Aturan |

## 8. Dokumen dan repo
| # | Item | Status |
|---|---|---|
| 8.1 | `docs/PRE_ORDER_PCB.md`: ganti Indomaker ke JLCPCB, tambah holder PCB2, J1 pindah, BT1 PCB1, lebar jalur | BELUM DICEK |
| 8.2 | `docs/BOM_V2.md`: tambah kolom LCSC dan penanda rakit JLC / pasang sendiri | BELUM DICEK |
| 8.3 | `HANDOVER.md` bagian atas usang; `CLAUDE.md` baris pabrik Indomaker diperbarui | BELUM DICEK |
| 8.4 | Ganti nama H2 jadi BT1 di skematik PCB2 (kosmetik) | BELUM DICEK |
| 8.5 | Memori dan catatan status tim diperbarui | BELUM DICEK |

## 9. Uji fungsi hardware (bukan firmware)
| # | Item | Status |
|---|---|---|
| 9.1 | Tes kabel RST (IO25) dan DIO0 (IO26) Ra-02 (`firmware/lora_rst_dio0`) | DILAPORKAN Calvin 23 Nov: berfungsi; log serial tidak disimpan (belum TERBUKTI berlog) |
| 9.2 | Link LoRa dua modul | DILAPORKAN Calvin 23 Nov: bisa; tanpa log |
| 9.3 | Ra-02 kedua korslet 3,3 V: dibuang atau diganti | DILAPORKAN Calvin 23 Nov: sudah beli Ra-02 baru, link jalan; belum ada log |
| 9.4 | Modul TP4056 + baterai + MT3608 hidup di breakout (tegangan dan arus terukur) | BELUM DICEK |
| 9.5 | Pengukuran sesudah PCB datang: kontinuitas tiap rail, tidak ada short 3V3/5V/GND sebelum modul dicolok | Rencana |

## 10. Persetujuan (gerbang akhir)
- [ ] Semua item bagian 1-8 berstatus TERBUKTI atau diterima Calvin sebagai risiko
- [ ] Biaya disetujui
- [ ] Rafif (ketua) setuju
- [ ] Calvin memberi izin tertulis di chat untuk mengunduh berkas dan menekan Order

## Blocker paling mungkin
1. Tact switch belum final (3.7, 6.5)
2. Urutan pin GPS/GY-521/microSD belum diverifikasi (3.4-3.6)
3. Holder 18650 sisi bawah PCB2: bentrok TP4056 dan opsi rakit JLC (5.2, 6.7)
4. LCSC match dan stok part (6.2, 6.6)
5. Netlist dan Gerber usang (7.1-7.2)

## Pembagian kerja

### A. Harus Calvin (butuh benda fisik, keputusan, atau izin)
| Item | Yang dilakukan |
|---|---|
| ~~3.4-3.6~~ | ~~Foto silkscreen GPS, GY-521, microSD~~ SELESAI 23 Nov |
| 3.7, 6.5 | Pilih tact switch yang dibeli; ukur jarak kaki, atau kirim link/nomor LCSC |
| 2.12 | Cek tanda + dan - pada holder 18650 asli vs pad 1 = VBAT_POS |
| 3.10, 3.11 | Pegang holder dan TP4056: jenis pin holder, tiang penempatan, panjang kaki TP4056 yang tembus |
| 2.13 | Catat merek, kapasitas, ada/tidak proteksi baterai 18650 |
| 3.12 | Cetak 1:1 PCB1/2/3 versi terbaru, tusuk dengan modul asli |
| 3.8, 3.9 | Ukur MT3608 dan konektor XKC (jarak lubang, jumlah pin) |
| 9.1-9.4 | Tes breadboard: `lora_rst_dio0`, link LoRa dua modul, ganti Ra-02 yang korslet, ukur TP4056 + MT3608 |
| 6.7, 6.11 | Putuskan: holder dirakit JLC atau disolder sendiri; setujui biaya total |
| 5.4 | Kabari Tri Yoga: casing Helmet butuh sekitar 20 mm ekstra, casing mengikuti PCB |
| 7.4, 7.5 | Izinkan download berkas dan klik Order sendiri (atau beri izin eksplisit) |
| 10 | Persetujuan akhir Calvin dan Rafif |

### B. Bisa dikerjakan Claude (lewat EasyEDA di Chrome, file repo, dan referensi web)
| Item | Yang dilakukan |
|---|---|
| 4.3 | Lebarkan 3V3 PCB3 ke 25 mil, rute ulang, DRC |
| 2.5 | Cek 8 pin U3 tanpa pad tidak dipakai net apa pun |
| 2.6, 2.7, 2.11 | Bandingkan netlist dengan pin map HANDOVER, cek strapping, pull-up |
| 2.8 | Hitung anggaran arus dari datasheet dan BOM |
| 2.10 | Cek G/D/S footprint Q1 vs datasheet |
| 4.6, 4.7, 4.9 | Cek keep-out antena, pour GND, silkscreen di 2D |
| 5.1, 5.3 | Cek 3D atas dan tampilan Flip Board sisi bawah PCB2 |
| 1.x | Cek kapabilitas JLCPCB di situs mereka dan bandingkan dengan aturan desain |
| 6.1-6.4, 6.6, 6.8 | Susun BOM per PCB dengan kolom LCSC, cek stok dan Basic/Extended, pilih female header |
| 6.9, 6.10 | Cek rotasi dan titik asal CPL setelah diekspor |
| 8.1-8.5 | Perbarui `PRE_ORDER_PCB.md`, `BOM_V2.md`, `HANDOVER.md`, `CLAUDE.md`, rename H2 ke BT1, perbarui memori |
| 5.5 | Siapkan paket STEP/DXF/koordinat untuk Tri Yoga (ekspor perlu izin download) |
| Audit firmware | Dokumen terpisah |

### C. Dikerjakan bersama (Claude menjalankan, Calvin mengizinkan)
- Ekspor ulang netlist, Gerber, BOM, CPL (7.1-7.3): file diunduh ke folder repo setelah Calvin bilang boleh.
- Unggah ke JLCPCB sampai halaman preview dan DFM check (7.4): Calvin login, tidak ada klik Order tanpa izin.

### Urutan saran
1. Calvin: kirim foto (3.4-3.6), pilih tact switch (3.7), cek polaritas holder (2.12).
2. Claude (paralel): item bagian B, mulai dari 4.3, 2.5-2.11, JLCPCB kapabilitas, BOM + LCSC.
3. Calvin: cetak 1:1 versi terbaru (3.12).
4. Bersama: ekspor, DFM check JLCPCB, persetujuan, order.

## Status PCB1 (23 Nov 2026, sesi EasyEDA salinan v3, tersimpan)
| Cek | Status |
|---|---|
| DRC PCB1 setelah semua perubahan | TERBUKTI: No issues found, 141 item; netlist PCB = skematik (error netlist hilang setelah skematik disamakan) |
| Ratlines | TERBUKTI 0 (panel Net) |
| Layer part: semua di Top, kecuali U7 (modul TP4056) di Bottom | TERBUKTI (Property List). Part rakitan JLC tidak ada di Bottom, jadi Economic masuk akal (DUGAAN sampai kuotasi) |
| Lebar jalur daya: 5V_DK, VBAT_POS, VBAT_RAW, VBOOST_5V = 0,635 mm (25 mil) | TERBUKTI (Property List semua track). 3V3_SYS dan sinyal = 16 mil (default) |
| Add into BOM = No: BT1, U3, U6, U7, U8, U9 (PCB dan skematik) | TERBUKTI di PCB; di skematik terbaca No lewat zoom kecil |
| LCSC: U2=C2718488 (female 1x4, stok 149.370; pengganti C9900236824 yang stok 0), R2/R8=C25804, R9=C4184 | TERBUKTI (dibaca ulang di PCB dan skematik) |
| Stok JLC 23 Nov: C15127, C8545, C25803, C25804, C4184, C14663, C16133, C720477 (Basic), C52023869 SS14 (1.111), C144395 XH, C2718488 | TERBUKTI dari Parts Library JLC; stok berubah tiap hari |
| Netlist vs firmware (pin map) | TERBUKTI untuk `PCB1.tel` lama (check_netlist.py semua OK); `.tel` baru belum diekspor |
| Pin Q1/Q2/Q5: pin1=G, pin2=S, pin3=D sesuai netlist (Q1.1 GPS_EN gate, Q1.2 3V3 source, Q1.3 GPS_3V3 drain; Q5.1 XKC_EN gate, Q5.2 GND, Q5.3 XKC_G; Q2.1 XKC_G gate, Q2.2 VBOOST source, Q2.3 XKC_5V drain) | DUGAAN (urutan pin datasheet AO3401A dan 2N7002 dari ingatan; verifikasi di datasheet LCSC) |
| Firmware cocok dengan hardware: GPS_EN LOW=ON dengan pull-up R3, XKC_EN HIGH=ON, PWR_BTN pull-up internal RTC, SOS aktif-HIGH dengan R2 pull-down | TERBUKTI dari kode `vest_node/src/main.cpp` vs netlist |
| Strapping: hanya IO5 (LORA_CS) yang strapping dipakai; IO0/2/12/15 tidak dipakai; IO34 dan IO35 hanya input | DUGAAN (pin table ESP32 dari ingatan) |
| 8 pin U3 tanpa pad tidak dipakai | TERBUKTI untuk `PCB1.tel` lama (tidak ada di net manapun) |
| Cetak 1:1 versi terbaru + semua modul menempel | BELUM DICEK, hanya Calvin |
| Polaritas holder, pad TP4056 vs modul fisik, MT3608, konektor XKC, tact | BELUM DICEK (fisik) |
| Keep-out antena, pour utuh tanpa pulau, silkscreen, 3D | BELUM DICEK (terlihat hatch keep-out di area antena DevKit) |
| Ekspor Gerber/BOM/CPL dan unggah preview JLC | BELUM DICEK (perlu izin unduh) |

## Update 23 Nov 2026 malam: PCB1/2/3 dikerjakan, berkas PCBA diekspor
| Cek | Status |
|---|---|
| Tact switch SW1/SW2 PCB1 dan SW1 PCB2 diganti ke KH-6X6X9H-STM, LCSC C2837535, SMD 6x6 tinggi 9 mm (Extended, stok 34.020 per 23 Nov); tombol dipasang dari luar lewat ekstensi | TERBUKTI di EasyEDA (Replace + kawat skematik + import ke PCB). Pad 1-4 footprint vs simbol mengikuti perpustakaan LCSC, belum diukur |
| PCB1: SW1 dipindah ke kanan atas (X 68, Y 136 mm) dan SW2 (X 88, Y 136 mm) karena footprint 6x6 menabrak lubang TP4056; PWR_BTN, BTN_SOS dirute ulang otomatis | TERBUKTI DRC 0 setelah rute ulang |
| PCB2: SW1 digeser ke Y -3110 mil dari -2960 mil (menabrak C2), PWR_BTN dirute ulang; PCB2 tidak punya pour (Copper Manager kosong) | TERBUKTI DRC 0 |
| PCB3: DRC 0 (54,61 x 100,33 mm); semua part di Top | TERBUKTI |
| Add into BOM = No: PCB1 (BT1, U2, U3, U6, U7, U8, U9, U10), PCB2 (H2, J1, U1, U7), PCB3 (H1, U1, U5) | TERBUKTI (dialog impor menampilkan persis perubahan itu) |
| LCSC terisi: PCB1 R2/R8 C25804, R9 C4184, U2 C2718488 (di luar BOM); PCB2 C1 C19702 (10uF 0603, Basic, stok 9,67 juta); PCB3 R2 C25804 | TERBUKTI di BOM hasil ekspor |
| Netlist baru diekspor (`hardware/netlist/PCB1..3.tel` diganti) dan `check_netlist.py` semua OK | TERBUKTI |
| BOM, CPL (disaring hanya part BOM), Gerber PCB1-3 diekspor ke `hardware/jlcpcba/2026-11-23/` | TERBUKTI (berkas ada, isi BOM dibaca). Designator `SW2(SOSButton)` diganti `SW2` di BOM dan CPL |
| Preview rotasi CPL di JLC, DFM JLC, kuotasi | BELUM DICEK |
| Cetak 1:1 versi terbaru | DILAPORKAN Calvin: semua modul cocok; tanpa foto atau ukuran. Tombol 6x6 baru dan posisinya belum dicetak |
