# Pertanyaan untuk Indomaker (kirim lewat WA 0812-2009-8675) dan daftar verifikasi sebelum memesan

Dibuat 16 Nov 2026. Ketentuan pabrik yang sudah diketahui (dari situs mereka, dikonfirmasi ulang lewat pencarian): jalur min 0,4 mm, clearance min 0,5 mm, via 1,0 mm, lubang kaki komponen 1,1 mm, ukuran PCB min 10 x 10 cm, format Gerber (PDF ada biaya tambahan), pengerjaan 3 hari kerja dengan masking/silkscreen dan 4 hari kerja double layer (<3 pcs menurut situs; hasil pencarian menyebut <10 pcs), finishing tin plating, pemotongan dengan alat khusus. Situs mereka tidak menjelaskan hal-hal di bawah.

## Pertanyaan untuk pabrik (salin ke WA)
1. Clearance minimum 0,5 mm itu hanya antar jalur, atau juga antar pad dan antara jalur ke pad? Footprint SOT-23 (pitch 0,95 mm) punya celah antar pad sekitar 0,3 mm; apakah boleh?
2. Lubang kaki komponen 1,1 mm: apakah bor selalu 1,1 mm, atau lubang yang lebih besar (mis. 1,2 mm untuk pad TP4056) diterima? Kami menyeragamkan semua ke 1,1 mm.
3. Via 1,0 mm: berapa diameter pad (annular ring) minimum? Kami memakai pad via 1,6 mm.
4. Lebar cincin pad komponen minimum? Pad kami 1,524 x 1,9 mm dengan lubang 1,1 mm.
5. Apakah lubang bertembaga (plated through hole) dan lubang NPTH (baut, tanpa tembaga) dibuat? Diameter NPTH minimum?
6. Ukuran minimum 10 x 10 cm: papan kami 107,95 x 95,25 mm, 31,6 x 99,1 mm, dan 54,6 x 100,3 mm. Apakah ditagih per luas papan sebenarnya, atau minimal 10 x 10 cm per papan? Bolehkah dua papan digabung dalam satu panel dan dipotong?
7. Tinggi/lebar silkscreen minimum dan lebar garis minimum? (Silkscreen footprint kami 0,12-0,15 mm di beberapa komponen.)
8. Jarak minimum jalur/tembaga ke tepi papan (outline)? Kami memakai 20 mil (0,5 mm).
9. Sudut papan membulat (radius 100 mil) dan outline persegi panjang: ada biaya tambahan?
10. Ketebalan papan standar (1,6 mm?), tebal tembaga (1 oz?), dan warna masking apa yang tersedia untuk double layer.
11. File yang diminta: Gerber saja, atau juga file drill (Excellon) terpisah? Format ekspor EasyEDA (One Key Export) diterima?
12. Contoh biaya untuk 3 papan di atas dan lama pengerjaan.

## Verifikasi di sisi kami sebelum memesan (status per 16 Nov)
| Item | Status |
|---|---|
| DRC EasyEDA 0 untuk PCB1, PCB2, PCB3 dengan aturan Indomaker | **T**: dijalankan ulang 16 Nov setelah memuat ulang proyek (PCB1, DRC 0; PCB2 dan PCB3 DRC 0 pada 15 Nov) |
| Jalur 100% terhubung | **T**: log auto-route 100% untuk ketiganya |
| Skematik dan PCB sinkron (tidak ada perubahan tersisa di Import Changes) | **T**: dicek 16 Nov untuk PCB1 dan PCB3 (daftar kosong, tidak diterapkan); PCB2 tidak diubah netlistnya |
| Pour GND PCB3 menutupi seluruh papan | **T secara visual** (tampilan EasyEDA 16 Nov, pola pour sampai ke tepi outline); belum dilihat di penampil Gerber |
| Proyek tidak diubah orang lain sejak perubahan 15 Nov | **T**: daftar proyek menunjukkan modifikasi terakhir oleh calvinwkatoroy 15 Nov 23:46 (cek ulang sebelum ekspor) |
| Lubang THT 1,1 mm masih berlaku setelah muat ulang | **T** (Gerber percobaan 16 Nov): file drill PTH hanya berisi bor 1,09982 mm untuk pad komponen (PCB1 74, PCB2 10, PCB3 60 lubang, sama dengan jumlah pad) dan 1,001 mm untuk via (PCB1 15, PCB3 3, PCB2 0) |
| Netlist `.tel` diekspor ulang | **B**: konektivitas tidak berubah (Import Changes kosong), tetapi file di repo belum diekspor ulang dari tata letak baru |
| Gerber percobaan | **T sebagian**: diekspor 16 Nov (izin Calvin), diperiksa dengan skrip `hardware/tools/gerber_*.py` dan dirender sendiri ke `docs/screenshots/gerber_render_pcb1..3.png` (bukan penampil Gerber resmi). Semua lapisan ada; ukuran outline PCB1 107,95 x 95,25, PCB2 31,623 x 99,06, PCB3 54,61 x 100,33 mm; lebar jalur hanya 0,406 mm (16 mil) dan 0,635 mm (25 mil), tidak ada yang lebih tipis; satu lubang NPTH 3,2 mm di PCB1 (baut/holder). File zip tidak dimasukkan ke repo. Belum dibuka di penampil Gerber pihak ketiga |
| Uji tusuk kertas 1:1 | **T menurut Calvin (21 Nov)**: dicetak di kertas dan dicocokkan dengan modul yang dibeli, ukurannya sesuai. Belum dicatat: papan mana saja yang dicetak (PCB1/2/3), apakah memakai layout 16 Nov (PCB3 baru), dan modul mana yang belum bisa dicocokkan (MT3608 dan TP4056 kedua belum dibeli) |
| Footprint cocok modul fisik (Ra-02 25,4 mm, jarak deret SuperMini dan DevKit 38 pin, pad TP4056 dan MT3608, urutan pin microSD dan GPS) | **T untuk ukuran/posisi pin menurut uji tusuk Calvin 21 Nov** (modul yang sudah dibeli); urutan fungsi pin (GPS, microSD, GY-521) dan MT3608/TP4056 kedua tetap B |
| Tact switch cocok footprint | **B** (PCB memakai SMD TS-1088, yang dibeli 6 x 6 mm THT/SMD belum dipastikan) |
| Posisi konektor/U.fl/baut PCB3 vs casing Gateway | **B** (tata letak PCB3 berubah 15 Nov) |
| Tri Yoga diberi tahu urutan "PCB dulu, casing mengikuti" | **B** |

## Hasil pemeriksaan Gerber percobaan (16 Nov 2026)
- Pour GND (lapisan bawah PCB1 dan PCB3) digambar dengan goresan 0,2032 dan 0,254 mm (8 dan 10 mil) di bagian "Copper" file Gerber; ini isi tembaga, bukan jalur, tetapi karena lebar goresannya di bawah 0,4 mm **tanyakan ke pabrik** apakah aman (tambahkan ke pertanyaan 7/8). PCB2 tidak memakai pour.
- Lubang NPTH 3,2 mm tanpa tembaga (PCB1 5 buah, PCB2 4, PCB3 4 sejak 21 Nov: 4 lubang baut M3 per papan); tanyakan apakah dibuat dan toleransinya (pertanyaan 5).
- Hasil render sendiri tidak menunjukkan jalur melintasi pad lain, jalur di luar outline, atau pour yang tidak menutupi papan. Render menggambar sudut outline membulat sebagai garis lurus (artefak render).
