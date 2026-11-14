# Ringkasan pekan ini dan rencana berikutnya (14 Nov 2026)

Fokus pekan ini: membawa PCB1 (Vest), PCB2 (Helmet), dan PCB3 (Gateway) ke kondisi siap dipesan. Acuan: checklist tahap 0-8 di `docs/PRE_ORDER_PCB.md` bagian 0. Semua perubahan desain dikerjakan di salinan EasyEDA `Pandu-Capstone-v3-footprint-fix`; proyek tim tidak disentuh. Semua commit ada di branch `v3` (terakhir `de960c6`, sudah di-push).

Label status: **T** terbukti (ada log/DRC/netlist), **D** dugaan, **B** belum dicek.

## 1. Yang sudah dikerjakan

### PCB1 Vest
- Negatif baterai terpisah (`BAT_NEG` = BT1.2 + U7.3), pembagi XKC R8 10k / R9 20k ke IO34, R1 dihapus. **T** (netlist, `check_netlist.py`).
- Konektor sensor air `U10` diganti JST XH 4 pin (pin 4 kosong, keputusan Calvin). Urutan kabel fisik ke pad 1-3: **D**.
- Jalur daya 25 mil (`VBAT_RAW`, `VBAT_POS`, `VBOOST_5V`, `5V_DK`), sinyal 16 mil. Rute 223 jalur/14 via/100%, DRC 0. **T** dari log dan DRC; lebar tiap jalur belum diukur satu per satu.
- Net satu pin `VBUS_5V` dihapus (pin IN+ TP4056 sengaja kosong). **T**.
- Skematik dirapikan: 27 flag No Connect, kabel sisa `LORA_ANT` dihapus. DRC skematik: Fatal 0, Error 1 (8 pin simbol DevKit tanpa pad, sudah diketahui), Warn 3. **T**.
- Silkscreen GPS diubah ke 25 x 35 mm (terpusat, posisi terhadap pad **D**). TP4056 sudah cocok (26,24 x 17,1 mm).
- R8/R9 dicek: footprint 0603 dan nilai terisi, device masih generik `Res_0603`.
- Label `PANDU PCB1 v3` di Top Silkscreen.

### PCB2 Helmet
- Stub `$1N31` di U1.11 dihapus, jalur default 16 mil, jalur daya 25 mil (`VBAT_RAW`, `VBAT_POS`, `VBAT_SW`). Rute 45 jalur/4 via/100%, DRC 0. **T**.
- `check_netlist.py` kini menolak net satu pin di PCB2. **T**.
- Label `PANDU PCB2 v3`.

### PCB3 Gateway
- Keputusan microSD: **modul di luar PCB, dihubungkan kabel ke header `H1`** (tidak ada ruang 42 x 24 mm di papan 55,88 x 77,47 mm; belum ditinjau Calvin).
- Rute ulang 92 jalur/4 via/100%, net `5V_SYS` 25 mil, DRC 0, ukuran papan tetap. Netlist identik dengan repo. **T**.
- Label `PANDU PCB3 v3`.

### Dokumen dan proses
- `docs/PRE_ORDER_PCB.md`: jalur tahap 0-8 sebagai checklist, status tiap item diperbarui.
- `CLAUDE.md`: urutan kerja **PCB dan semua modul fix dulu, baru casing dimodelkan dan dicetak 3D; casing mengikuti PCB**.
- `check_netlist.py`: exit 0, 50 OK, tanpa peringatan net satu pin.

## 2. Belum selesai atau belum terbukti
- **Semua ukuran modul masih D.** Belum ada cetak 1:1 dan belum ada pengukuran jangka sorong yang tercatat.
- **Pad dan urutan pin belum bisa dikoreksi** sampai data fisik ada (lihat tahap 1).
- Belum ada uji breadboard (TP4056 B-, pembagi air IO34, SuperMini 5V/3V3, catu microSD).
- Folder `gerber/` yang ada tidak valid; Gerber baru belum dibuat.
- Casing laporan 55 x 65 x 23 mm tidak muat PCB1/PCB2 dan akan diganti; Tri Yoga **belum diberi tahu** urutan baru.
- Sisa peringatan skematik: label `BAT_SENSE` ganda (tidak berbahaya), part `U6`/`U2`/`U3` tidak cocok dengan Supplier Part.
- Label silkscreen belum lengkap: polaritas `H2` PCB2, tombol SOS/PWR, titik uji, tanda pin 1 konektor (sengaja ditunda sampai pad dikoreksi dan dirute ulang).
- Silkscreen footprint PCB1 dan PCB3 punya garis 0,12-0,15 mm; dugaan di bawah batas minimum JLCPCB (cek spesifikasi pabrik).

### Tambahan 14 Nov (siang)
- Skematik **Helmet** (13 No Connect) dan **Gateway** (28 No Connect) dibersihkan: Helmet Fatal 0/Error 0/Warn 0; Gateway Fatal 0/Error 0/Warn 1 (part vs Supplier Part). Netlist ketiga board setelah itu identik dengan repo. **T**.
- Label `PANDU PCB1/2/3 v3` di Top Silkscreen, DRC 0 ketiganya. **T**.
- **Gerber percobaan** PCB1-3 diekspor dan diperiksa dengan skrip: lapisan lengkap, outline tertutup dan sama dengan ukuran papan. Bukan final, tidak disimpan di repo. **T** untuk struktur; pencocokan visual di penampil Gerber belum.
- Izin: PCB3 (Gateway) boleh diperbesar; PCB1 dan PCB2 tidak. Usulan PCBA: **PCB saja** (menunggu keputusan).
- Sisa firmware dari sebelumnya: perbaikan `validateEvent` di server, field `sens` pada ingest, timeout T4, uji hardware K1-K4.

## 3. Rencana berikutnya (berurutan)

**A. Butuh Calvin / Rafif (benda fisik), paling menahan**
1. Tahap 1, hal non-ukuran: urutan pin GPS (4), microSD (6), GY-521 (8); catu microSD (5 V atau 3,3 V); port TP4056 (Type-C atau micro-USB); diameter lubang dan urutan pad TP4056; jarak deret SuperMini dan pin 5V/3V3; warna kabel dan tegangan XKC; posisi header microSD terhadap tepi modul; apakah `AD0` GY-521 punya pull-down di modul.
2. Tahap 2, uji breadboard: TP4056 B- terpisah dari GND, pembagi air di IO34, SuperMini 5V/3V3, catu microSD.
3. Beri tahu Tri Yoga urutan baru (PCB dan modul fix dulu, casing mengikuti).

**B. Butuh keputusan**
4. Pesan dengan perakitan (PCBA) JLCPCB atau tidak. Bila ya, `R2`/`R8`/`R9` perlu part pabrikan/LCSC.
5. Posisi `R8`/`R9` di PCB1: tetap di sudut kiri bawah atau dekat `U10`/IO34 (memindah berarti rute ulang).
6. Setujui pendekatan microSD PCB3 (kabel di luar PCB) atau pilih memperbesar PCB3.

**C. Sudah dikerjakan 14 Nov (tanpa data baru)**
7. ~~Bersihkan skematik Helmet dan Gateway~~ selesai.
8. Titik uji dan label tombol/`H2` **ditunda sengaja**: dikerjakan sekali bersama rute ulang setelah pad dikoreksi (langkah 10).
9. ~~Gerber percobaan~~ diekspor dan diperiksa dengan skrip. Sisa: buka di penampil Gerber untuk pencocokan visual, dan cek garis silk tipis ke spesifikasi JLCPCB.

**D. Setelah data tahap 1-2 ada**
10. Koreksi pad TP4056, GPS, GY-521, microSD, SuperMini dan XH sesuai data; rute ulang; DRC; ekspor netlist; `check_netlist.py`.
11. Tahap 5: cetak 1:1 skala 100% dan pasang semua modul asli. Lulus berarti ukuran naik dari D ke T dan ukuran papan dibekukan.
12. Tahap 6: tinjauan akhir oleh reviewer kedua (Calvin atau Rafif).
13. Tahap 7: ekspor Gerber final dan validasi.
14. Tahap 8: persetujuan Calvin dan Rafif. **PCB tidak dipesan sebelum Calvin mengizinkan.**
15. Setelah ukuran beku: paket untuk Tri Yoga (STEP 3D, outline DXF, koordinat konektor/tombol/lubang baut, tinggi komponen), lalu casing dimodelkan dan dicetak.
