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
| Lubang THT 1,1 mm masih berlaku setelah muat ulang | **T sebagian**: terbaca 43,3 mil pada pad DevKit PCB1 setelah perubahan; belum dicek ulang semua pad setelah memuat ulang. Cek ulang: Edit/Find > Pad > Layer = Multi-Layer > Find All, kolom Hole Diameter harus 43.3mil |
| Netlist `.tel` diekspor ulang | **B**: konektivitas tidak berubah (Import Changes kosong), tetapi file di repo belum diekspor ulang dari tata letak baru |
| Gerber dibuka di penampil | **B** (ekspor perlu izin unduh dari Calvin) |
| Uji tusuk kertas 1:1 | **B** (butuh printer dan modul fisik) |
| Footprint cocok modul fisik (Ra-02 25,4 mm, jarak deret SuperMini dan DevKit 38 pin, pad TP4056 dan MT3608, urutan pin microSD dan GPS) | **B/D** (butuh modul fisik) |
| Tact switch cocok footprint | **B** (PCB memakai SMD TS-1088, yang dibeli 6 x 6 mm THT/SMD belum dipastikan) |
| Posisi konektor/U.fl/baut PCB3 vs casing Gateway | **B** (tata letak PCB3 berubah 15 Nov) |
| Tri Yoga diberi tahu urutan "PCB dulu, casing mengikuti" | **B** |
