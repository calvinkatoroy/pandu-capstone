# Checklist sebelum memesan PCB (per 11 Nov 2026)

Tujuan: PCB1, PCB2, PCB3 yang dipesan **tepat** terhadap modul fisik (ukuran, pin, jarak), jalur tembaga sesuai permintaan dosen, dan tanpa error DRC/netlist. Satu PCB salah = uang dan waktu hilang; jangan pesan kalau ada satu pun gerbang di bawah belum lulus.

Status tiap angka: **T** = TERBUKTI (diukur/dijalankan), **D** = DUGAAN (listing, datasheet, ingatan), **B** = BELUM DICEK. Hanya T yang boleh dipakai sebagai dasar memesan. Semua D dan B di bawah harus jadi T.

## 0. Jalur ke PCB siap dipesan (checklist per tahap, 11 Nov 2026)
Urutan menurut ketergantungan: tahap 1 menentukan apakah tahap 3 perlu diulang; tahap 8 hanya setelah semua tahap lain lulus. Detail gerbang ada di bagian 1 sampai 8 di bawah.

**Tahap 0. Sudah selesai di salinan EasyEDA `Pandu-Capstone-v3-footprint-fix` (terbukti di `.tel` dan DRC)**
- [x] Netlist PCB1/2/3 diekspor ulang dan `check_netlist.py` lulus; DRC 0 di ketiganya; aturan jalur default 16 mil.
- [x] PCB3: siren dihapus. PCB1/PCB3: footprint Ra-02 25,4 mm. PCB1: `BAT_NEG` terpisah dari GND, pembagi sensor air `R8`/`R9`. PCB2: stub `$1N31` dihapus. Silk GPS PCB1 25 x 35 mm (posisi terpusat, D).

**Tahap 1. Ukuran modul: dinyatakan final oleh Calvin (11 Nov), tidak perlu jangka sorong lagi**
- [x] Angka ukuran di bagian 2 (kolom "Ukur baru") dipakai apa adanya sebagai ukuran final. Statusnya tetap **D** sampai cetak 1:1 di tahap 5 lulus; jangan disebut T.
- [ ] Hal non-ukuran yang tetap harus dipastikan (bukan soal jangka sorong): urutan pin GPS (4), microSD (6), GY-521; catu microSD (5 V atau 3,3 V); port TP4056 (Type-C atau micro-USB); warna kabel dan tegangan keluaran XKC-Y25-V (kering/basah); posisi header microSD terhadap tepi modul; pin 5V/3V3 SuperMini.
- [ ] Semua modul sudah ada di tangan (G1: TP4056 kedua dan MT3608).

**Tahap 2. Uji listrik di breadboard (G9)**
- [ ] TP4056: `B-` terpisah dari GND, uji pengisian dan proteksi.
- [ ] Pembagi sensor air: tegangan di IO34 saat kering dan basah (target sekitar 3,3 V).
- [ ] SuperMini: 5V lewat regulator onboard dan dioda ke VBUS; 4,2 V tidak masuk pin 3V3.
- [ ] microSD: catu sesuai modul.

**Tahap 3. Sesuaikan desain dengan hasil tahap 1 dan 2** (satu perubahan, satu simpan, satu DRC)
- [ ] Koreksi footprint yang berbeda dari modul (pad TP4056, urutan pin GPS/microSD/GY-521, lubang baut).
- [x] PCB1: `U10` sudah footprint `CONN-TH_B4B-XH-A-LF-SN` (JST XH 4 pin 2,5 mm, 11 Nov): pad 1 = SIG, 2 = VCC (5 V), 3 = GND, pad 4 tidak tersambung (keputusan Calvin: kabel XH 4 pin, pin 4 dibiarkan kosong). Terbukti di `PCB1.tel` (net tidak berubah), rute ulang 214 jalur/15 via/100%, copper di-rebuild, DRC 0. Urutan fisik kabel ke pad 1-3 masih DUGAAN.
- [x] PCB1 `R8`/`R9`, dicek di EasyEDA 11 Nov (tidak ada perubahan di EasyEDA): `R8` (10K) dan `R9` (20K) berfootprint 0603 dengan nilai terisi, sama dengan `R2` (10K); ketiganya masih device generik `Res_0603` tanpa nomor part pabrikan/LCSC, sedangkan `R3`-`R7` sudah `0603WAF1003T5E` (100k). Spesifikasi beli sudah ada di `BOM_V2.md` bagian B (20 k, 0603, 1%, beli 4; 10 k, 0603, 1%, beli 8). Nomor LCSC hanya perlu kalau PCB dipesan dengan perakitan (PCBA) JLCPCB: **keputusan Calvin**; bila ya, pilih part 0603 1% di perpustakaan EasyEDA lalu cek nilainya sebelum Gerber/BOM diekspor. Posisi (DRC 0, 100% terhubung): `R8` di (140 mil, 2530 mil), `R9` di (140 mil, 2300 mil), kolom di tepi kiri bawah, tepat di bawah ujung holder 18650 (terlihat dari tampilan, bukan diukur).
- [ ] PCB1: tinjau dengan Calvin apakah `R8`/`R9` sebaiknya dipindah dekat `U10` atau pin IO34 (sekarang di sudut kiri bawah; jarak jalur ke `U10` dan IO34 belum diukur). Memindah berarti rute ulang.
- [x] PCB3: microSD **di luar PCB, lewat kabel ke header `H1` (1x6)** (keputusan 11 Nov, diserahkan ke Claude oleh Calvin/Rafif; belum ditinjau Calvin). Alasan: tidak ada ruang bebas 42 x 24 mm di papan 55,88 x 77,47 mm (dari tampilan EasyEDA, bukan diukur), jadi garis luar modul **tidak digambar** dan papan, footprint, serta rute tidak berubah (netlist PCB3 tetap). Konsekuensi yang masih terbuka: (a) casing Gateway harus punya ruang terpisah untuk modul 42 x 24 mm (D) dan jalur kabel 6 kawat; (b) kabel jumper pendek (sekitar 10 cm, DUGAAN) agar SPI SD stabil, belum diuji; (c) urutan pin `H1` terhadap silkscreen modul dan catu 5 V/3,3 V masih B (tahap 1), jadi label pin tidak dicetak di silkscreen sampai terverifikasi; (d) posisi `H1` di tepi papan perlu dicek Calvin supaya kabel tidak terhalang Ra-02/DevKit. Alternatif bila ditolak: PCB3 diperbesar (rute ulang).
- [x] Jalur daya 25 mil (11 Nov, aturan net `power25mil` 25 mil, jalur lain tetap 16 mil): PCB1 net `VBAT_RAW`, `VBAT_POS`, `VBOOST_5V`, `5V_DK` (rute ulang 223 jalur/14 via/100%, copper di-rebuild, DRC 0, papan tetap 107,95 x 95,25 mm); PCB2 net `VBAT_RAW`, `VBAT_POS`, `VBAT_SW` (45 jalur/3 via/100%, DRC 0, 31,6 x 99,1 mm). Netlist PCB1 identik dengan sebelumnya. Lebar jalur hasil rute diperiksa visual (jalur daya jelas lebih tebal) dan dari aturan, belum diukur satu per satu. PCB3 tidak punya net daya baterai; 5V_SYS dan 3V3 di PCB3 masih 16 mil.
- [ ] Rute ulang tiap kali footprint berubah lagi (Unroute All, Auto Route, rebuild copper, Check DRC).
- [ ] Hilangkan net satu pin yang tersisa (mis. `VBUS_5V` di PCB1).

**Tahap 4. Ukuran dan casing (G7)**
- [ ] Putuskan dengan Tri Yoga: casing mana untuk board mana, atau kecilkan PCB (konsekuensi: rute ulang). Casing laporan 55 x 65 x 23 mm tidak muat PCB1 dan PCB2.
- [ ] Bekukan ukuran papan.

**Tahap 5. Cetak 1:1 di kertas (G8)**
- [ ] Cetak skala 100% (matikan "fit to page"), cek dengan penggaris, pasang semua modul asli di atas cetakan. Pin harus pas tanpa dipaksa; kalau tidak, kembali ke tahap 3. Lulus tahap ini = ukuran naik dari D ke T.

**Tahap 6. Pemeriksaan akhir desain**
- [ ] Skematik: tidak ada pin mengambang (selain 8 pin DevKit tanpa pad); DRC 0.
- [ ] Netlist cocok dengan pin map firmware (`HANDOVER.md`); tidak memakai IO6-11.
- [ ] Silkscreen: tanda pin 1, polaritas, nama board; lebar jalur sesuai (16 mil, daya 25 mil).
- [ ] Ditinjau oleh reviewer kedua (Calvin atau Rafif).

**Tahap 7. Ekspor produksi (G10)**
- [ ] Ekspor ulang `.tel` terakhir, jalankan `check_netlist.py`, commit ke `v3`.
- [ ] Ekspor Gerber (plus BOM dan Pick and Place bila perlu), buka di penampil Gerber, bandingkan dengan EasyEDA; simpan di `hardware/gerber/` (isi lama tidak valid, jangan dipesan).

**Tahap 8. Persetujuan dan pesan (G11)**
- [ ] Persetujuan tertulis Calvin (dan Rafif); tanda tangan ketua hanya setelah ACC dosen. Jangan klik "Order PCB" sebelum itu.
- [ ] Setelah dipesan: kirim ke Tri Yoga STEP 3D PCB, outline DXF, dan koordinat konektor, tombol, lubang baut.

## 1. Gerbang (urut; semua harus lulus)
| # | Gerbang | Penanggung jawab | Status |
|---|---|---|---|
| G1 | Semua modul fisik sudah ada di tangan (termasuk TP4056 kedua dan boost MT3608, yang per 28 Okt **belum ada**; tact switch 3 pcs) | Rafif/Gibran | B |
| G2 | Semua ukuran di bagian 2 terisi dan selisih terhadap footprint <= 0,2 mm. **11 Nov: Calvin menyatakan ukuran sudah final, jangka sorong tidak diperlukan lagi**; status naik ke T setelah cetak 1:1 (G8) lulus | Calvin | D (final menurut Calvin) |
| G3 | Footprint PCB1/2/3 sama dengan modul (bagian 3), semua pin/pad tervalidasi | Agen 1-3 + Calvin | sebagian |
| G4 | Skematik = PCB (Import Changes tanpa perubahan tak terduga), netlist diekspor ulang dan `check_netlist.py` OK | Agen 1-3 | B |
| G5 | DRC PCB: 0 masalah; skematik: tidak ada pin mengambang selain 8 pin DevKit tanpa pad | Agen 1-3 | PCB1, PCB3 di salinan: 0 |
| G6 | Jalur sesuai dosen (bagian 5) | Agen 1-3 | sebagian |
| G7 | Outline PCB cocok dengan casing (bagian 6) | Calvin + Tri Yoga | **belum cocok** |
| G8 | Cetak 1:1 di kertas lulus untuk ketiga board (bagian 4) | Calvin | B |
| G9 | Uji baterai dan charging dengan modul asli lulus (checklist daya di `CHECKLIST_UJI_RAKIT.md` bagian 1) | Gibran/Rafif | B |
| G10 | Gerber baru diekspor dari proyek final, dibuka di penampil Gerber, dibandingkan dengan tampilan EasyEDA | Calvin | B |
| G11 | Persetujuan tertulis Calvin (dan Rafif) sebelum klik Order | Calvin | B |

## 2. Ukuran fisik modul (final menurut Calvin 11 Nov; pengukuran jangka sorong tidak diperlukan lagi; T/D dicatat)
Pengukuran 5 dan 28 Okt memakai penggaris (akurasi sekitar 0,5 mm). Ukur ulang semua kolom "Ukur baru".

**Riset web 11 Nov (`docs/RISET_KOMPONEN.md`)**: jarak deret Ra-02 breakout kemungkinan **25,4 mm** (bukan 26,0 mm yang ada di footprint); TP4056 Type-C punya tiga angka berbeda (27,5 / 28,5 / 29 mm); lubang 1,0 mm untuk pin header 0,64 mm sudah standar. Tanpa jangka sorong: pakai uji tusuk kertas 1:1 (coba 25,4 dan 26,0 untuk Ra-02) dan pindai di scanner dengan penggaris.

| Modul | Parameter | Footprint sekarang | Ukur lama (sumber) | Ukur baru (isi) |
|---|---|---|---|---|
| ESP32 DevKit V1 30 pin (Vest) | jarak tengah deret kiri-kanan | 25,4 mm | 25,4 mm (5 Nov, penggaris) D | **25,4 mm** (standar 1,0", tim 11 Nov) D |
| | pitch pin; jumlah pin | 2,54 mm; 15/sisi | sama | 2,54 mm; 15/sisi (standar) D |
|  | panjang x lebar papan | silk 28,3 x 51,5 mm | 51,5 x 28,5 mm (5,15 x 2,85 cm, 28 Okt, penggaris) D | **51 x 28 mm** (tim 11 Nov) D |
| | **diameter/diagonal pin header; diameter lubang** | lubang 1,0 mm, pad oval 1,524 x 1,9 | belum | pin ____ mm, rule: lubang = diagonal pin + 0,2 s.d. 0,3 mm |
| | letak konektor USB (tengah, ujung papan) | | | ____ |
| | urutan pin sesuai silkscreen papan (VIN..EN kiri, 3V3..IO23 kanan) | pad 1..30 | konfirmasi 5 Nov D | cek satu per satu ____ |
| ESP32 DevKit 38 pin (Gateway) | jarak deret (25,4 atau 22,86?), jumlah pin 19/sisi, papan (BOM "ESP32 U": 4,8 x 2,8 cm) | 38 pin | jumlah 19/sisi cocok (5 Nov); papan 48 x 28 mm ("ESP32U" 4,8 x 2,8 cm, 28 Okt) D | **deret 25,4 mm** (standar terdekat) D; papan **48,26 mm** (tim 11 Nov, = 19 x 2,54, kemungkinan hitungan) D; tim menulis "48,26 x 25,4": arti 25,4 (jarak deret atau lebar papan) belum dipastikan |
| Ra-02 breakout | jarak tengah antar deret | 25,4 mm (`Ra02_Breakout_2x8_25_4mm`, sudah dipasang di PCB1 `U6` dan PCB3 `U1` di salinan EasyEDA, 11 Nov) | 26 mm (5 Nov) D | **25,4 mm** (tim 11 Nov, standar 10 x 2,54) D. Berkas sumber dikoreksi (disetujui Calvin 11 Nov). Footprint sudah diganti di PCB1 dan PCB3; tetap D sampai diuji tusuk 1:1 |
|  | pitch, panjang deret (7 x 2,54 = 17,78), papan |  | 28 x 20,5 mm (2,8 x 2,05 cm, 28 Okt, penggaris) D; 8 pin/sisi | ____ |
| | urutan pin tiap deret (atas: GND NSS MOSI MISO SCK DIO5 DIO4 GND; bawah: GND GND 3.3V RST DIO0 DIO1 DIO2 DIO3) | pad 1 = GND | foto 5 Nov | ____ |
| | header jantan tersolder ke sisi bawah, tinggi, posisi konektor U.fl dan jaraknya ke tepi PCB | | | ____ |
| TP4056 HW-373 Type-C | panjang x lebar papan | silk 27,1 x 16,7 | **28,5 x 17 (5 Nov) vs 27,5 x 17 (28 Okt)**: selisih 1 mm, ukur ulang | **26 x 17 mm** (tim 11 Nov, menggantikan 28,5/27,5) D. Silk footprint di EasyEDA (dibaca dari properti garis, 11 Nov) sudah 26,24 x 17,1 mm, jadi cocok dalam 0,25 mm; angka 27,1 sebelumnya salah baca; tidak diubah |
| | pad kiri-kanan (c-c) | 23,45 mm | sekitar 24 mm | 24 mm (angka lama, tidak ada standar) D |
| | OUT-/OUT+ ; B-/B+ (c-c) | 14,36 ; 8,02 mm | 14,5 ; 8,0 mm | 14,5 ; 8,0 mm (angka lama, tidak ada standar) D |
| | diameter lubang pad, urutan pad (IN+, IN-, OUT+, OUT-, B+, B-), posisi dan ukuran port USB-C | lubang 1,2 | | ____ |
| GY-521 (MPU6050) | papan 20 x 16 mm; 8 pin satu sisi pitch 2,54; urutan pin (VCC..INT); posisi dan diameter lubang baut | urutan footprint **belum dicek** | 20 x 16 mm (2 x 1,6 cm, 28 Okt, penggaris) D; 8 pin satu sisi | ____ |
| GPS NEO-6M (GY-GPS6MV2) | papan 35 x 25 mm (tim 11 Nov, menggantikan 35 x 26,5); 4 pin satu sisi; urutan (VCC, RX, TX, GND?); lubang baut | belum dicek | 35 x 26,5 mm (3,5 x 2,65 cm, 28 Okt, penggaris) D; 4 pin satu sisi | **35 x 25 mm** D; silk footprint PCB1 diubah dari 26,8 x 35,85 jadi 25 x 35 mm (11 Nov, terpusat pada titik asal footprint, posisi terhadap pad DUGAAN; lingkaran lubang baut sekarang menyentuh garis luar); urutan pin dan lubang baut masih B |
| ESP32-C3 SuperMini | papan 22,5 x 18 mm (standar, menggantikan 22,4 x 13,8 yang janggal); 8 pin/sisi; **jarak antar deret**; pin 3V3/5V/GND/GPIO4 | belum dicek | 22,4 x 13,8 mm (2,24 x 1,38 cm, 28 Okt, penggaris) D; 8 pin/sisi | **22,5 x 18 mm, 8 pin/sisi** (standar SuperMini, tim 11 Nov) D; jarak deret sekitar 15,24 mm (0,6") adalah **dugaan paling lemah**, ukur |
| Boost MT3608 (belum dibeli) | papan sekitar 37 x 17 mm (listing D), pad IN+, IN-, OUT-, OUT+, header 1x4 | | | ____ |
| Modul microSD | papan 42 x 24 mm (tim 11 Nov, menggantikan 29 x 41,5; kelas Catalex dengan level shifter dan regulator); header 1x6 (urutan pin, level logika) | belum dicek | 29 x 41,5 mm (2,9 x 4,15 cm, 28 Okt, penggaris) D | **42 x 24 mm** D; urutan pin dan catu (5 V atau 3,3 V) masih B |
| Holder 18650 | 76,5 x 20,5 mm; jarak pin/pad terminal; tinggi dengan sel | belum dicek terhadap footprint BT1 | 76,5 x 20,5 mm (7,65 x 2,05 cm, 28 Okt, penggaris) D; tinggi holder + sel sekitar 21 mm D | ____ |
| Tact switch (3 pcs: SOS, power Vest, on/off Helmet) | ukuran 6 x 6 mm (BOM 28 Okt), jarak kaki, THT atau SMD | **PCB memakai SMD TS-1088; yang dibeli beda** | 6 x 6 mm (0,6 x 0,6 cm, 2 pin, 28 Okt) D; jumlah 3 | ____ |
| Konektor sensor air XKC-Y25-V | header XH 2,54 mm 4 pin, urutan (coklat VCC, kuning sinyal, biru GND, hitam opsi) | | | ____ |

**Catatan 11 Nov:** kolom "Ukur baru" diisi dari angka yang disampaikan tim (metode ukur belum dicatat) dan dari standar terdekat. **Semua berstatus D, belum ada yang T.** Konflik yang diselesaikan dengan angka tim: TP4056 (26 x 17 menggantikan 28,5/27,5), GPS (35 x 25), microSD (42 x 24), SuperMini (22,5 x 18). Masih terbuka: arti "25,4" pada DevKit 38 pin Gateway, jarak deret SuperMini, diameter pin header, urutan pin GY-521/GPS/microSD/XKC. **Ra-02:** berkas sumber (`make_ra02.py`, `Ra02_Breakout_2x8_25.4mm.kicad_mod`) sudah dikoreksi ke 25,4 mm dengan persetujuan Calvin (11 Nov, disampaikan Rifat); **footprint di EasyEDA PCB1 dan PCB3 sudah diganti ke `Ra02_Breakout_2x8_25_4mm` (11 Nov, di salinan `Pandu-Capstone-v3-footprint-fix`)**: rute ulang dengan aturan jalur 16 mil (sebelumnya default PCB1 dan PCB3 di salinan masih 10 mil), auto-route 100%, DRC tanpa masalah (PCB1 107,95 x 95,25 mm, PCB3 55,88 x 77,47 mm tidak berubah), netlist PCB1/PCB3 diekspor ulang dan `check_netlist.py` OK. Berkas sumber lama menomori pad bawah 2,2,3,.. (pad 1 hilang); sudah diperbaiki di `make_ra02.py`. **Silk 11 Nov:** TP4056 sudah 26,24 x 17,1 mm di footprint (cocok, tidak diubah; "27,1" salah baca), jarak pad masih angka lama; GPS di PCB1 diubah ke 25 x 35 mm (terpusat, DUGAAN, DRC bersih); microSD (PCB3 `H1`) **tidak diubah**: footprintnya hanya header 1x6 tanpa garis luar modul, dan posisi header terhadap tepi modul 42 x 24 mm belum diketahui. Port TP4056 belum dipastikan Type-C atau micro-USB (26 x 17 lazim untuk micro-USB).

## 3. Validasi footprint dan netlist (tiap board)
Untuk setiap komponen: nomor pad = nomor pin simbol = nomor pin fisik. Cara: (a) dari modul ke tabel pin (bagian 2), (b) tabel pin ke simbol, (c) simbol ke net di `.tel`.
- [ ] **DevKit V1 (PCB1 U3)**: 30 pad dinamai `J2-n`/`J3-n`. Pemetaan: VIN=J2-19, GND=J2-14, IO13=J2-15, IO12=J2-13, IO14=J2-12, IO27=J2-11, IO26=J2-10, IO25=J2-9, IO33=J2-8, IO32=J2-7, IO35=J2-6, IO34=J2-5, VN=J2-4, VP=J2-3, EN=J2-2, 3V3=J2-1 | GND=J3-1, IO15=J3-16, IO2=J3-15, IO4=J3-13, IO16=J3-12, IO17=J3-11, IO5=J3-10, IO18=J3-9, IO19=J3-8, IO21=J3-6, RX0=J3-5, TX0=J3-4, IO22=J3-3, IO23=J3-2. Bandingkan dengan silkscreen papan fisik.
- [ ] **Ra-02 (PCB1 U6, PCB3 U1)**: pad 1 = GND, 16 pad nomor unik, 25,4 mm (berkas sumber; salinan EasyEDA masih 26,0 sampai diganti). Net: 3V3, 4x GND, NSS=IO5, SCK=IO18, MISO=IO19, MOSI=IO23, RST (Vest IO25, Gateway IO14), DIO0=IO26, DIO1-5 NC. Pin `LORA_ANT`/header antena tidak ada lagi (antena via U.fl di breakout).
- [ ] **PCB3 tanpa sirine (keputusan 11 Nov)**: hapus rangkaian sirine dari skematik dan PCB: `Q1` (2N7002), `R1` 220 ohm (gate), `R3` 100 k (pull-down gate), terminal `U2` 3,81 mm, net `SIREN_DRV` (IO4). Pertahankan `R2` 10 k (pull-up SD_CS). Pastikan tidak ada net yatim (IO4 bebas) dan tidak ada ratline setelah penghapusan. Rute ulang, DRC.
- [ ] **PCB1 Q1/Q2 = AO3401A (P-ch)**, Q5 = 2N7002: G/S/D benar; gating GPS (`GPS_EN`=IO4) dan XKC (`XKC_EN`=IO32) aktif sesuai logika.
- [x] **TP4056 (PCB1, PCB2)**: baterai negatif hanya ke `B-` (net `BAT_NEG`); `OUT-` dan `IN-` ke GND sistem (agar proteksi DW01 tidak terlewati, temuan A2). **PCB1 selesai 11 Nov** di salinan EasyEDA (`BAT_NEG` = `BT1.2` + `U7.3`; `U7.4`/`U7.6` tetap GND), terbukti di `PCB1.tel` dan dicek `check_netlist.py pcb1`. PCB2 sudah benar sejak 8 Okt (`BAT_NEG` = `H2.2` + `U7.3`).
- [x] **XKC-Y25-V**: pembagi `R8` 10 k (seri) / `R9` 20 k (ke GND) ke `WATER_SIG` (IO34); `R1` dihapus. **PCB1 selesai 11 Nov** (`XKC_OUT` = `R8.1` + `U10.1`; `WATER_SIG` = `R8.2` + `R9.1` + IO34; R8 dan R9 ditaruh di strip kiri papan, kiri `BT1`). Belum: tegangan OUT kering/basah belum diukur (K1); konektor `U10` masih 3 pin, belum XH 4 pin; R9 bernilai 20 k dengan device generik `Res_0603`, pilih part saat BOM final.
- [ ] **PCB2 SuperMini**: pin 5V lewat regulator onboard dan dioda ke VBUS belum diverifikasi di board fisik; jangan beri 4,2 V ke pin 3V3.
- [ ] PCB2: `SAW1` sudah diganti header jumper `J1`; TTP223 dan `TOUCH_SIG` dihapus; stub `$1N31` di `U1` pin 11 **dihapus 11 Nov di salinan EasyEDA** (terbukti di `PCB2.tel`, tidak ada net satu pin; aturan jalur default 16 mil, rute ulang 42 jalur/3 via/100%, DRC "No issues found"; lebar jalur hasil rute belum diukur satu per satu). Konfirmasi bahwa baterai Helmet (18650 + holder atau LiPo) terhubung lewat header `H2` dan footprint cocok dengan yang dibeli.
- [ ] Setelah footprint final: ekspor ulang `PCB1.tel`, `PCB2.tel`, `PCB3.tel`, jalankan `python hardware/netlist/check_netlist.py` (di folder `netlist`). Salinan `.tel` saat ini adalah per 6-8 Okt dan **usang** untuk PCB1 dan PCB3.
- [ ] Item 8 pin simbol DevKit tanpa pad diterima (hanya peringatan skematik).
- [ ] Tidak ada net satu pin (mengambang) selain yang disengaja.

## 4. Cetak 1:1 (uji fisik di kertas)
1. Dari EasyEDA cetak/ekspor PDF tiap board pada skala 100% (Print: Scale 100%, tanpa "fit to page"). Ukur garis/outline hasil cetak dengan jangka sorong untuk memastikan skala 100% (toleransi 0,2 mm).
2. Letakkan modul di atas kertas, tusuk pin/header ke lubang pad (lubangi kertas dengan jarum bila perlu). **Lulus** bila semua pin masuk tanpa dipaksa dan offset <= 0,2 mm; bila modul tidak dapat dilepas dari header lewat pad, ukur selisih.
3. Periksa juga: modul tidak bertabrakan (silkscreen), port USB/U.fl/konektor menghadap tepi yang benar, lubang baut cocok, tinggi modul tidak menabrak yang lain.
4. Foto hasil dan simpan di `docs/screenshots/`; catat angka di bagian 2.

## 5. Jalur tembaga (permintaan dosen) dan aturan DRC
- Lebar default semua net sinyal **16 mil**; net daya diusahakan lebih lebar (25 mil untuk `VBAT_RAW`, `VBAT_POS`, `VBOOST_5V`, 5V) bila clearance memungkinkan. Pelebaran dengan menimpa jalur (bulk) memicu 188 pelanggaran: pakai Unroute All dan Auto Route ulang, lalu Rebuild Copper.
- Kapasitas arus (perkiraan IPC-2221, 1 oz, kenaikan 10 °C): 16 mil sekitar 1,2 A, 25 mil sekitar 1,9 A. Arus pengisian TP4056 default sekitar 1 A (R-prog 1,2 k; audit A7 menyarankan R-prog sekitar 2 k = sekitar 580 mA untuk baterai 1200 mAh).
- Pengecualian hanya bila fisik tidak memungkinkan (leher pad SOT-23/0603): catat net, panjang, lebar sebenarnya.
- Verifikasi: Design Manager > aturan jalur/jarak, lalu DRC. Bandingkan lebar minimum yang benar-benar ada (kolom "Track" di Check DRC atau filter objek). Tulis hasil di laporan agen. Nilai 16 mil dari Calvin; minta konfirmasi tertulis dosen bila perlu.
- Clearance, lebar jalur minimum, ukuran via/lubang: pastikan di atas batas pabrik. Pabrikan belum tercatat di repo (asumsi JLCPCB via EasyEDA); cek kapabilitas di situsnya saat memesan.
- DRC: 0 masalah. Tanpa jalur menggantung, tanpa copper yang basi (jalankan Rebuild All sebelum DRC), tanpa ratline.
- Pastikan ada: label versi di silkscreen (mis. `PANDU PCB1 v3`), orientasi pin 1, label konektor/polaritas (BAT+, BAT-, 5V, ANT, SOS), titik uji 3V3/5V/GND/BAT (P1-8), lubang baut sesuai casing.

## 6. Cocokkan dengan casing (G7)
- PCB1 107,95 x 95,25 mm; PCB2 1245 x 3900 mil = 31,6 x 99,1 mm (per 8 Okt, cek ulang); PCB3 55,88 x 77,47 mm. Casing Vest di SCAD v5: lebar PCB 108, tinggi 95,25, dinding 2 mm, celah 1 mm, standoff 9 mm.
- Casing di laporan Pekan 11 (Tri Yoga): **55 x 65 x 23 mm** tidak muat PCB1 (Vest) dan PCB2. Putuskan dengan Tri Yoga: casing mana untuk board mana, atau kecilkan PCB (konsekuensi: rute ulang).
- Lokasi konektor yang harus jatuh pada lubang casing: USB-C TP4056, micro/USB-C DevKit, SMA/U.fl, SW1/SW2, konektor XKC. Ekspor koordinatnya (lihat `AGENT_PLAN.md`).

## 7. Keputusan yang harus dikunci sebelum memesan
- Pabrikan dan perakitan: solder tangan semua (R/C 0603, SOT-23, SMA, tantalum case B) atau minta perakitan? Bila tangan, 0603 dan SOT-23 sulit; pertimbangkan ukuran 0805.
- Gateway tanpa sirine: tombol mute (P3-3) dan dioda flyback (P3-4) tidak diperlukan lagi. LED status Gateway (pakai LED onboard DevKit atau tidak) dan LED indikator Vest (K2) masuk atau tidak. Peringatan alarm hanya di dashboard; firmware Gateway masih memuat kode sirine (IO4) dan perlu disesuaikan.
- Baterai Helmet: 18650 + holder (sama dengan Vest) atau LiPo; cara menyambung.
- Cadangan daya Gateway (K5), pembagi baterai Helmet (K4).
- Jumlah PCB per board dan cadangan (modul fisik tidak bisa diperbaiki bila PCB salah).

## 8. Tanda tangan sebelum memesan (isi)
| Board | Gerber diekspor | DRC 0 | netlist OK | cetak 1:1 lulus | casing cocok | Calvin | Rafif |
|---|---|---|---|---|---|---|---|
| PCB1 | | | | | | | |
| PCB2 | | | | | | | |
| PCB3 | | | | | | | |

## 9. Catatan status teknis (per 5 Nov, salinan EasyEDA `Pandu-Capstone-v3-footprint-fix`)
- PCB1: DevKit V1 30 pin + Ra-02 breakout terpasang, H1 dihapus, rute ulang 16 mil, DRC 0, ratline 0, 27 net, papan 107,95 x 95,25 mm.
- PCB3: Ra-02 breakout (pad 1 = GND), Q1 = 2N7002, H2 dihapus, 16 mil, DRC 0, ratline 0, papan 55,88 x 77,47 mm. **Rangkaian sirine (Q1, R1, R3, U2) kini harus dihapus (11 Nov)**, sehingga DRC dan routing PCB3 perlu diulang. **Skematik PCB3 belum disamakan** (U1 masih footprint lama, H2 masih ada); Import Changes akan mengembalikan perubahan, jangan diterapkan tanpa mencentang.
- PCB2: belum disentuh di salinan; semua koreksi 8 Okt (SAW1, BAT_NEG, TTP223, LiPo+TP4056) ada di proyek tim, belum diaudit terhadap modul fisik.
- Footprint TP4056 (PCB2) cocok dalam toleransi 0,5 mm per audit 5 Nov, perlu ukur ulang dengan jangka sorong.
- Sisa item personal library di salinan (jangan dipakai): device kosong `ESP32_DevKitV1_30P_J2J3`, device `ESP32-DevKitV1-30P`, footprint `ESP32_DevKitV1_30P` dan `ESP32_DevKitV1_30P_25.4mm` (setengah ternomori).
