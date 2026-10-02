# Riwayat progres PANDU, Pekan 2–5 (ringkasan agar Pekan 6 tidak redundan)

Sumber: laporan kemajuan kelompok dan laporan individu Calvin (WEEK_2–WEEK_5).

| Pekan | Tanggal | Yang sudah dilaporkan |
|---|---|---|
| 2 | 31 Agt–5 Sep | On-site visit kapal SPJM (Tanjung Priok). Verifikasi spesifikasi komponen. **Sensor BME680 dipangkas** (tidak relevan). Draft BoM. Masalah: spesifikasi belum IP67. Skenario diubah ke Proof of Concept. Progres total 16,25%. |
| 3 | 7–12 Sep | **Skematik 3 unit selesai** di EasyEDA Pro (Vest, Helmet, Edge Gateway). Pemesanan komponen dimulai. Draft 3D casing Fusion 360 dan blueprint 2D 55×65×18 mm. Wireframe dashboard (Figma). Progres 24,25%. |
| 4 | 14–19 Sep | Laporan menyatakan **PCB Vest dan Helmet "selesai"**, Edge Gateway masih kendala routing. Order komponen 80%. Validasi OpenSCAD: casing direvisi 18→23 mm tebal dan 65→70 mm tinggi (baterai 18650). Progres 27,25%. |
| 5 | 21–26 Sep | Dashboard: marine pilot view dan supervisor view, wireframe HTML/CSS/JS (repo `calvinkatoroy/pandu-dashboard`). Menunggu hardware stack dan endpoint ESP32. |

## Yang BARU di Pekan 6 (jangan dilaporkan ulang sebagai hasil lama)

- **Routing ulang PCB1** sampai bersih DRC. Klaim "PCB Vest selesai" di Pekan 4 ternyata belum final. Placement dirombak. Papan 108×95 mm, tombol dan modul diatur ulang.
- **Casing Vest Node dibuat ulang mengikuti PCB**: 114×101×30,6 mm. Ini menggantikan 55×65×23/70 mm dari Pekan 4. Termasuk bukaan USB, SMA, dan 2 tombol, serta modul boost yang digantung di tutup.
- **Perubahan desain**: buzzer dihapus dari Vest, sensor air diganti **XKC-Y25 (VCC 5 V via boost)**, TP4056 dipindah ke Bottom, trek daya dilebarkan (20 mil).
- **PCB3 (Edge Gateway) diselesaikan.** PCB1 dan PCB3 dibuat lebih kompak.
- **Audit 3 board** dan **export Gerber ketiganya** (belum boleh dipesan, lihat bawah).
- **Verifikasi skematik PCB1 pin-per-pin** (`PCB1_Verifikasi_Skematik.md`). Temuan: AMS1117 tidak bisa 3,3 V dari Li-ion, dua sumber 3V3 diparalel, tact switch dipakai sebagai saklar daya, pin GND RA-02 kurang.

## Catatan konsistensi

- BME680 sudah dibuang sejak **Pekan 2**. Keputusan "tidak pakai VL53L0X" belum tercatat di laporan mana pun. Itu perubahan scope baru, catat di Pekan 6.
- Skematik sedang diperbaiki (U3/C1/C2 dihapus, pin 5V ESP32 ke boost), jadi Gerber lama tidak dipesan dulu.
- Angka "akurasi sensor 96,2%" muncul di semua laporan kelompok tanpa data pengujian. Cek ulang sebelum dikumpulkan.
- Laporan Pekan 4 menyebut ESP32-C3 dan DevKitM-1, sedangkan proposal menyebut ESP32-WROOM-32. Samakan.
