# Spesifikasi footprint V3 (5 Nov 2026)

Sumber: ukuran modul fisik diukur Calvin (5 Nov), footprint dibaca dari EasyEDA Pro. Angka penggaris akurat sekitar 0,5 mm; pastikan dengan jangka sorong atau cetak 1:1 sebelum pesan PCB.

## Temuan
| Board | Komponen | Footprint sekarang | Modul fisik | Status |
|---|---|---|---|---|
| PCB3 | Ra-02 (U1) | `WIRELM-SMD_RA-02-BL` (modul telanjang, pad SMD 2 mm, penomoran 1-16 telanjang) | Breakout 28 x 20 mm, header 2,54 mm | **SALAH, ganti** |
| PCB1 | Ra-02 (U6) | sama (menurut netlist 6 Okt; PCB1 live belum dibuka) | sama | **Diduga salah, cek** |
| PCB1 | DevKit (U3) | `ESP32-DEVKITC-32D`, 19 pin per sisi | DevKit V1, 15 pin per sisi | **SALAH, ganti** |
| PCB3 | DevKit (U5) | 19 pin per sisi | 19 pin per sisi | Jumlah pin cocok |
| PCB2 | TP4056 (U7) | `PWRM-TH_TP4056`, 6 pad lubang 1,2 mm | HW-373 Type-C | Cocok dalam toleransi |

## Ra-02 breakout (dua deret 1x8)
- Pitch 2,54 mm; panjang deret 7 x 2,54 = 17,78 mm.
- **Jarak antar deret 26,0 mm** (tengah ke tengah), deret ada di dua ujung panjang modul; modul 27 sampai 28 x 20,5 mm.
- Pemetaan pin: `LORA_RA02_BREAKOUT.md` (**urutan di silkscreen modul belum diverifikasi**).
- Cara paling mudah: dua header betina 1x8 terpisah, 26,0 mm antar pusat, atau satu footprint kustom 16 pad.

## TP4056 HW-373 Type-C
- Papan 28,5 x 17 mm.
- Pad kanan (dari tengah): OUT-/OUT+ berjarak 14,5 mm, B-/B+ berjarak 8,0 mm.
- Pad kiri-kanan (tengah ke tengah): sekitar 24 mm.
- Footprint di EasyEDA (dibaca dari properti pad, perkiraan): kiri-kanan 23,45 mm, OUT 14,36 mm, B 8,02 mm, lubang 1,2 mm. Selisih sekitar 0,5 mm di arah panjang, masih dalam toleransi pengukuran.
- Silkscreen footprint sekitar 27,1 x 16,7 mm, sedikit lebih kecil dari papan; beri jarak aman ke komponen tetangga.

## DevKit V1 (Vest, 15 pin per sisi)
- Jarak antar deret belum diketahui; urutan pin di silkscreen belum dikonfirmasi.
- Pemetaan ke net memakai nama GPIO (IO13, IO27, IO34, dst.), bukan nomor pin.

## Salinan kerja
Proyek EasyEDA `Pandu-Capstone-v3-footprint-fix` (pribadi, milik Calvin) adalah salinan proyek tim per 5 Nov. Semua perubahan footprint dikerjakan di sana; proyek tim tidak disentuh.

## Status 5 Nov (salinan EasyEDA `Pandu-Capstone-v3-footprint-fix`)
- PCB3 selesai di salinan: footprint Ra-02 breakout (pad 1 = GND), Q1 = 2N7002 (SOT-23), header antena H2 dihapus, jalur 16 mil, auto-route, copper di-rebuild, DRC 0, ratline 0, ukuran papan tetap 55,88 x 77,47 mm.
- Belum: PCB1 (Ra-02 dan DevKit V1 15 pin, jarak deret 25,4 mm), cek pin D/S Q1, cetak 1:1 untuk cek fisik, adopsi ke proyek tim.
- PCB1 (Ra-02): footprint breakout terpasang, header antena H1 dihapus, U6 dipindah ke kanan-bawah, konektor sensor air U10 digeser, jalur 16 mil auto-route, DRC 0, ratline 0 (27 net), ukuran papan tetap 107,95 x 95,25 mm. DevKit di PCB1 masih footprint 19 pin (salah untuk modul 15 pin), menunggu penggantian.

## Status 5 Nov malam: DevKit PCB1 selesai (salinan EasyEDA)
- Footprint DevKit V1 30 pin dari repo `syauqibilfaqih/ESP32-DevKit-V1-DOIT` (MIT): 30 pad, jarak deret 25,4 mm, pitch 2,54 mm, lubang diperlebar 0,8 -> 1,0 mm. Pad **dinamai persis pin simbol U3** (`J2-n`/`J3-n`) lewat file impor KiCad, jadi skematik tidak diubah dan tidak ada pemetaan manual. Generator: `hardware/footprints/make_devkit_zip_j2j3.py` -> `ESP32_DevKitV1_30P_J2J3_import.zip` (File > Import > KiCad > Extract Libraries).
- Pad 1..30 -> pin: VIN=J2-19, GND=J2-14, IO13=J2-15, IO12=J2-13, IO14=J2-12, IO27=J2-11, IO26=J2-10, IO25=J2-9, IO33=J2-8, IO32=J2-7, IO35=J2-6, IO34=J2-5, VN=J2-4, VP=J2-3, EN=J2-2 | 3V3=J2-1, GND=J3-1, IO15=J3-16, IO2=J3-15, IO4=J3-13, IO16=J3-12, IO17=J3-11, IO5=J3-10, IO18=J3-9, IO19=J3-8, IO21=J3-6, RX0=J3-5, TX0=J3-4, IO22=J3-3, IO23=J3-2.
- Pin simbol tanpa pad (memang tidak ada di DevKit V1): J2-16, J2-17, J2-18, J3-7 (GND kedua), J3-14, J3-17, J3-18, J3-19. EasyEDA menampilkan ini sebagai peringatan/error skematik, bukan error DRC PCB.
- PCB1 di salinan: U3 = footprint baru, U6 (Ra-02) footprint breakout juga disamakan di SKEMATIK, H1 dihapus dari skematik, label LORA_ANT di pin 1 U6 diganti GND (pad 1 breakout = GND), Unroute All + Auto Route, Rebuild Copper, DRC 0, ratline 0, 27 net, ukuran papan tetap.
- PENTING: skematik PCB3 (U1 Ra-02, H2) belum disamakan; "Import Changes" di PCB3 akan mengembalikan footprint lama dan menambah H2 kalau tidak dicentang.
- Belum: cek ukuran lubang/pin fisik, cetak 1:1, adopsi ke proyek tim, perbaikan klaim GPS/jatuh di dokumen.
