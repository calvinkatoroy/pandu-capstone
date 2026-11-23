# Audit footprint PCB1-3 terhadap sumber open source (23 Nov 2026 malam)

Branch: `v3-opensource-footprints`. Status memakai: **T** = TERBUKTI (dijalankan / diukur), **D** = DUGAAN (listing, repo orang lain, ingatan), **B** = BELUM DICEK.
Angka "sekarang" dibaca dari `FlyingProbeTesting.json` di Gerber 23 Nov (jarak antar pusat pad, mm). Angka tim dari `docs/PRE_ORDER_PCB.md` dan `docs/FOOTPRINT_SPEC_V3.md`.
File open source yang diunduh ada di `hardware/footprints/opensource/` (hanya dibaca, tidak dijalankan). **Tidak ada satu pun yang diukur di modul fisik**, jadi semua tetap D sampai ada uji tusuk kertas 1:1 atau jangka sorong.

## 1. Yang memakai header sekarang
| Papan | Part | Jenis | Keterangan |
|---|---|---|---|
| PCB1 | U2 (MT3608) | **sudah dihilangkan** | header betina 1x4 diganti 4 pad modul rata (commit 050ea22) |
| PCB2 | J1 | header **jantan** 2 pin | jumper/saklar baterai, lihat bagian 4 |
| PCB3 | H1 | header **jantan** 6 pin | kabel ke modul microSD (modul di luar PCB), lihat bagian 4 |
| lainnya | U3, U6, U7, U8, U9, U10, DevKit PCB3, Ra-02 PCB3 | **tanpa header** | lubang disolder langsung ke pin modul (tidak ada header betina di BOM) |

## 2. Perbandingan per modul
| Part | Footprint sekarang | Sumber open source | Selisih | Putusan |
|---|---|---|---|---|
| DevKit V1 30 pin (PCB1 U3) | 15 pad/sisi, deret 25,40, lubang 1,1 | `syauqibilfaqih/ESP32-DevKit-V1-DOIT` (MIT), sudah dipakai | 0 | **Sudah open source.** Pertahankan |
| DevKitC 38 pin (PCB3 U5) | 19 pad/sisi, deret 25,40 | tidak diunduh (Espressif tidak ketemu di pencarian) | - | Standar DevKitC 25,4 mm (D). Pertahankan |
| Ra-02 breakout (PCB1 U6, PCB3 U1) | 2 x 8, deret **25,40**, lubang 1,1 | `pavolilan2005/Libreria_kicad-lora-sx1278-THT`: deret **25,00**, lubang 0,914 | 0,4 mm | **Konflik.** Tengahkan ke 25,2 + lubang 1,2 mm (lihat bagian 3) |
| MT3608 (PCB1 U2) | 4 pad, **31,55 x 7,20**, lubang 1,5, pad 5 x 3 | SnapMagic Generic (sumber sekarang) dan `kubabuda/misc_footprints`: **31,00 x 6,50**, lubang 1,25, pad 5 x 3,5 | 0,55 dan 0,70 mm | **Dua sumber beda.** Tengahkan ke 31,3 x 6,85, pad 5 x 3,5, lubang 1,5 |
| TP4056 HW-373 Type-C (PCB1 U7, PCB2 U7) | 6 lubang 1,1; kiri-kanan 23,44; OUT 14,36; B 8,02 | `kubabuda` `4056E_LiIon_loader_prot`: kiri-kanan 21,46, bukan HW-373 | 2 mm | **Tidak ada footprint HW-373 open source.** Pakai angka tim (24 / 14,5 / 8,0). Selisih 0,55 mm di L-R: besarkan lubang ke 1,3 mm |
| GY-521 (PCB1 U8) | 8 pin 1 sisi, pitch 2,54, rentang 17,78 | `Hathu7543/...GY521` dan `nppc/KiCadCustomLibs`: sama, 17,78, board 21 x 16 | 0 | **Cocok.** Pertahankan |
| NEO-6M GY-GPS6MV2 (PCB1 U9) | 4 pin 1 sisi, pitch 2,54, rentang 7,62 | hanya footprint modul NEO-6M telanjang (SMD) | - | **Tidak ada footprint breakout GY.** Pertahankan, urutan pin B |
| ESP32-C3 SuperMini (PCB2 U1) | **SMD** 16 pad, deret **16,00**, pad 2,1 x 1,8, pitch 2,54 | `mrtnvgr`: THT deret **15,24**; `zentarot` (Elecrow): **18,60** atau **18,00** | tiga angka berbeda | **RISIKO TERTINGGI.** Lihat bagian 3 |
| XKC-Y25-V konektor (PCB1 U10) | JST B4B-XH-A, 4 pin, pitch **2,50**, lubang 1,1 | KiCad resmi `Connector_JST` XH B4B 1x04 P2.50: pitch 2,50, lubang 0,95 | 0 | **Cocok.** (Catatan: dokumen lama menulis "XH 2,54", yang benar 2,50) |
| microSD (PCB3 H1) | 1x6, pitch 2,54, rentang 12,70 | `josejacomeb/KiCad-MicroSD-Card-Adapter` (GPL-3): 1x6, pitch 2,54, rentang 12,70 | 0 | Cocok untuk pin. Posisi badan modul B |
| Holder 18650 (BT1) | BH-18650-A1AJ005, jarak pin **70,00**, lubang 1,1 | `kubabuda` `16850_cell_casket`: **76,97** (holder lain) | 7 mm | **Tidak sebanding.** Holder yang dibeli belum dicocokkan; tim hanya mengukur badan 76,5 x 20,5 |
| Tombol KH-6X6X9H-STM | 4 pad, 9,10 x 4,50 (LCSC) | footprint pabrikan via LCSC | - | Pin 1 dan 4 diagonal, T dari Gerber |

## 3. Yang tidak bisa disamakan dengan open source dan caranya
- **Prinsip:** karena tidak ada pengukuran fisik, jangan pilih salah satu angka. Ambil titik tengah dan lebarkan lubang supaya pin yang meleset 0,2 mm tetap masuk (lubang 1,2 mm untuk pin 0,64 mm memberi kelonggaran sekitar 0,28 mm per sisi).
- **Ra-02:** 25,2 mm c-c, pad 1,8, lubang 1,2. Menutup 25,0 sampai 25,4.
- **MT3608:** 31,3 x 6,85, pad 5 x 3,5, lubang 1,5.
- **TP4056:** lubang 1,3 mm, pad 2,0. Jarak tetap angka tim.
- **SuperMini:** tiga sumber, tiga angka, dan modulnya belum diukur. Footprint SMD sekarang tidak sengaja menutup 15,24 sampai 18,0 (pad 2,1 mm di 16,0 c-c). Rekomendasi: pad SMD diperpanjang menjadi 3,6 mm supaya menutup 15,24 sampai 18,6, dan modul disolder rata di atasnya lewat lubang pad modul. Kalau modul sudah punya pin header terpasang, cara ini tidak bisa; **cek apakah modul punya header atau tidak**.
- Uji tanpa jangka sorong: cetak PCB 1:1 (skala 100%, bukan "fit to page"), taruh tiap modul di atas kertas dan tusuk lubang pinnya. Itu bukti T yang paling murah.

## 4. J1 dan H1
- **J1 (PCB2)**: 2 pin, pin 1 = `VBAT_RAW` (keluaran OUT+ TP4056), pin 2 = `VBAT_SW` (pin 5V SuperMini, `U1.16`). Fungsinya jumper atau saklar daya Helmet: dilepas, baterai terputus dari ESP32-C3. Tanpa J1 atau jembatan solder, Helmet selalu hidup selama baterai tersambung. Pilihan: (a) dua lubang kosong untuk kabel atau slide switch (tanpa header), (b) jembatan tembaga permanen.
- **H1 (PCB3)**: 6 pin ke modul microSD (42 x 24 mm, D). Menempel langsung berarti badan modul duduk di atas PCB dan butuh area kosong 42 x 24 mm di luar DevKit dan Ra-02, serta slot kartu harus menghadap tepi. Itu perubahan tata letak PCB3.

## 5. Hasil DFM JLC (jlcdfm.com, Gerber 23 Nov, T)
| Papan | Merah | Peringatan | Catatan |
|---|---|---|---|
| PCB1 (modul) | annular ring 8 (4 lubang baut x 2 sisi, pad sama dengan lubang), tht-to-smd 1, silkscreen ke pad 50, silkscreen ke lubang 36 | solder mask exposing trace 1, silk line width 51, PTH without pad 2 | **Pad spacing merah yang lama (via 0,02 mm dari pad Q2) sudah hilang** |
| PCB2 | silkscreen ke pad 54, silkscreen ke lubang 16 | silk line width 9, PTH without pad 10 | tidak ada merah di jalur, pad, atau drill |
| PCB3 | annular ring 8 (lubang baut), silkscreen ke pad 6 | short slot 38, silk line width 14, PTH without pad 8 | "short slot" 38 cocok dengan 38 lubang DevKit; DUGAAN lubangnya oval |
- Belum dijalankan: DFM SMT (butuh unggah BOM + CPL), akan muncul di JLC setelah order.

## 6. Usulan perubahan EasyEDA (menunggu persetujuan Calvin)
1. U2 MT3608: pad 31,3 x 6,85, pad 5 x 3,5, lubang 1,5.
2. U6 dan U1 Ra-02: deret 25,2, pad 1,8, lubang 1,2.
3. U7 TP4056 (PCB1 dan PCB2): lubang 1,3, pad 2,0.
4. U1 SuperMini (PCB2): pad SMD 3,6 mm; keputusan jadi setelah dicek modul punya header atau tidak.
5. J1 PCB2: header dihapus, jadi dua lubang kosong (atau jembatan), sesuai pilihan.
6. H1 PCB3: ditunda sampai diputuskan modul microSD menempel atau tetap kabel.
7. Setiap perubahan: rute ulang, DRC 0, ekspor Gerber/BOM/CPL baru, ganti baris di keranjang JLC, lalu DFM ulang.
