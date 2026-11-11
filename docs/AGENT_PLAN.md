# Rencana 3 agen paralel (satu board per agen, akun berbeda)

Tujuan: membawa PCB1, PCB2, PCB3 ke kondisi siap pesan sesuai `docs/PRE_ORDER_PCB.md`. Agen **tidak memesan PCB** dan tidak menyentuh proyek tim. Pengukuran fisik dikerjakan manusia (Calvin); agen memakai angka dari `PRE_ORDER_PCB.md` bagian 2 dan berhenti bila angkanya masih D/B.

| Agen | Board | Branch | Folder milik (hanya tulis di sini) | Perkiraan |
|---|---|---|---|---|
| 1 | PCB1 Vest Node | `v3-pcb1` | `hardware/pcb1/`, `docs/agent/pcb1.md` | L |
| 2 | PCB2 Helmet Node | `v3-pcb2` | `hardware/pcb2/`, `docs/agent/pcb2.md` | M |
| 3 | PCB3 Edge Gateway | `v3-pcb3` | `hardware/pcb3/`, `docs/agent/pcb3.md` | M |

## Aturan bersama (hindari bentrok)
1. Baca dulu `CLAUDE.md` dan `docs/PRE_ORDER_PCB.md`. Berkas bersama (`CLAUDE.md`, `PRE_ORDER_PCB.md`, `FOOTPRINT_SPEC_V3.md`, `LORA_RA02_BREAKOUT.md`, `BOM_V2.md`, `HANDOVER.md`, `hardware/footprints/`, `hardware/netlist/check_netlist.py`) **hanya dibaca**. Usul perubahan ditulis di laporan agen sendiri; Calvin yang menggabungkan.
2. Buat branch dari `v3` (`git switch -c v3-pcbN v3`), commit di situ, `git push origin v3-pcbN`. Jangan push ke `v3`/`main`, jangan force-push.
3. Footprint bersama **dibekukan**: Ra-02 (PCB1 dan PCB3), TP4056 (PCB1 dan PCB2). Bila agen menemukan footprint bersama salah, jangan ubah diam-diam: hentikan bagian itu, tulis temuan (ukuran, bukti), lapor Calvin. Dua agen dengan footprint Ra-02 berbeda = PCB tidak konsisten.
4. Akun EasyEDA berbeda: library pribadi Calvin tidak terlihat. Impor footprint dari berkas di `hardware/footprints/` ke library akun sendiri (File > Import > KiCad > "Extract Libraries"; cara menembus dialog berkas ada di `CLAUDE.md`). Setelah impor, **verifikasi** jumlah pad, penomoran unik, jarak, dan bahwa hasilnya sama dengan spesifikasi (DevKit V1: 30 pad, jarak deret 25,4 mm; Ra-02: 16 pad, 25,4 mm, pad 1 = GND). Ra-02 di EasyEDA salinan Calvin dibuat dengan Footprint Wizard (DIP-16, rentang kaki 26 mm (salinan lama; berkas sumber kini 25,4 mm)), `make_ra02.py` dan `Ra02_Breakout_2x8_25.4mm.kicad_mod` adalah padanan berkas; cocokkan sebelum dipakai.
5. Langkah 0 (wajib, semua agen): pastikan akun bisa **mengedit** proyek EasyEDA yang akan dikerjakan. Pilihan, urutan: (a) Calvin mengundang akun agen sebagai anggota proyek salinan `Pandu-Capstone-v3-footprint-fix`, agen hanya membuka dan mengedit board miliknya; (b) bila tidak bisa edit bersamaan, agen membuat salinan proyek sendiri dan mengirim hasilnya (Gerber, netlist, screenshot) lewat branch; Calvin yang menyatukan. **Cara penggabungan ke satu proyek belum teruji**; jangan berasumsi. Bila akses gagal, berhenti dan lapor.
6. Sesi cloud tidak bisa menjangkau Chrome lokal; pekerjaan EasyEDA harus dari sesi lokal dengan Claude-in-Chrome. Cloud boleh untuk dokumen dan analisis netlist.
7. UI EasyEDA rapuh: satu perubahan, satu simpan, satu DRC; screenshot sesudah tiap langkah penting; jangan `ctrl+a` di kanvas.
8. Setiap temuan ditulis dengan status T/D/B. Tidak ada klaim "cocok" tanpa angka.

## Deliverable per agen (semua ke `hardware/pcbN/` di branch sendiri)
- `pcbN.tel` (netlist ekspor terbaru) dan hasil `check_netlist.py`.
- `Gerber_PCBN_<tanggal>.zip`, **diekspor tetapi jangan dipesan**, dan tangkapan layar Gerber di penampil Gerber.
- `drc.png` (DRC 0), `pcb_top.png`, `pcb_3d.png` (opsional), `schematic.png`.
- `pcbN_step.step` (ekspor 3D PCB) dan `pcbN_outline.dxf` (outline), untuk pemodelan 3D casing setelah pesan.
- `pcbN_koordinat.md`: tabel posisi (mm, relatif sudut kiri-atas papan) untuk konektor/USB/U.fl/SMA/tombol/lubang baut, ukuran papan, dan tinggi komponen tertinggi.
- `docs/agent/pcbN.md`: laporan (format di bawah).
- PDF cetak 1:1 tiap board (`pcbN_1to1.pdf`) siap dicetak Calvin.

### Format laporan agen
1. Ringkasan satu paragraf dan status gerbang G3-G6, G10 untuk board ini.
2. Tabel komponen: ref, part, footprint, status ukuran (T/D/B), catatan.
3. Daftar net dan hasil `check_netlist.py`.
4. Lebar jalur: aturan yang dipakai, lebar terkecil yang benar-benar ada, daftar pengecualian dan alasannya.
5. DRC: jumlah, tangkapan layar, tanggal.
6. Item yang masih menunggu manusia (ukuran, keputusan) dan usulan perubahan berkas bersama.

## Agen 1: PCB1 Vest Node (L)
Kondisi awal (T, 5 Nov di salinan Calvin): DevKit V1 30 pin dan Ra-02 breakout terpasang, jalur 16 mil, DRC 0, 27 net, papan 107,95 x 95,25 mm.
Tugas:
1. P1-1: pisahkan negatif baterai (`BAT_NEG` = `BT1.2` + `U7` B-; `U7` OUT- dan IN- ke GND). Verifikasi di netlist; tulis hasil.
2. P1-3: sensor air XKC-Y25-V: header XH 4 pin, `R8` 10 k / `R9` 20 k ke `WATER_SIG`, `R1` dihapus, kapasitor 100 uF + 100 nF di `VBOOST_5V`.
3. Footprint GY-521, GPS, TP4056, boost MT3608, BT1 (holder 18650), SW1/SW2, konektor XKC dicocokkan ke tabel ukuran (setelah Calvin mengisi); bila belum terisi, tandai B dan lanjut tugas lain.
4. P1-4: jalur daya (`VBAT_RAW`, `VBAT_POS`, `VBOOST_5V`, 5V) ke 25 mil bila clearance cukup; sinyal tetap 16 mil. P1-8: titik uji, label versi, orientasi/polaritas.
5. Cocokkan jalur USB DevKit (menghadap ke dalam papan, akses di casing) dan posisi U.fl/SMA dan SW1/SW2 dengan lubang casing; ekspor `pcb1_koordinat.md`.
6. Rute ulang, Rebuild Copper, DRC 0, `PCB1.tel`, `check_netlist.py`, Gerber, cetak 1:1 PDF.
Perhatian: pengganti keputusan (mis. K2 LED/haptic) hanya bila Calvin memutuskan.

## Agen 2: PCB2 Helmet Node (M)
Kondisi awal: koreksi 8 Okt ada di proyek tim (SAW1 menjadi header jumper `J1`, `BAT_NEG`, TTP223 dihapus, LiPo + TP4056), belum diaudit terhadap modul fisik dan **belum dikerjakan di salinan Calvin**. Mulai dari salinan terbaru proyek.
Tugas:
1. Audit tiap komponen terhadap tabel ukuran: SuperMini (jarak deret dan pin), TP4056, header baterai `H2`/holder, `J1`, SW1, C2 (tantalum). Tandai T/D/B.
2. P2-4 dan P2-6: pin map SuperMini (GPIO4, 3V3, 5V, GND) dengan modul fisik; hapus stub `$1N31` di `U1` pin 11; outline sesuai komponen sebenarnya dan casing (tunggu keputusan casing).
3. Netlist: `BAT_NEG` terpisah (B-), `OUT-`/`IN-` ke GND, `VBAT_SW` ke pin 5V SuperMini; `check_netlist.py` PCB2 lulus.
4. Jalur 16 mil semua, daya 25 mil bila muat; DRC 0; Gerber; cetak 1:1; STEP dan outline; `pcb2_koordinat.md`.
5. Tandai ke Calvin: keputusan baterai Helmet (18650 + holder atau LiPo), pin 5V vs regulator, K4 (pembagi baterai).

## Agen 3: PCB3 Edge Gateway (M)
Kondisi awal (T, 5 Nov di salinan Calvin; sirine baru dihapus kemudian): PCB Ra-02 breakout, Q1 = 2N7002, H2 dihapus, 16 mil, DRC 0, papan 55,88 x 77,47 mm; **skematik belum disamakan**.
Tugas:
1. Samakan skematik dengan PCB: `U1` footprint Ra-02 breakout, hapus `H2`, label `LORA_ANT` di pin 1 -> GND (pad 1 breakout = GND). Setelah itu Import Changes di PCB3 **tidak boleh** menunjukkan perubahan tak terduga (centang hanya yang disengaja).
2. **Hapus rangkaian sirine** (keputusan 11 Nov, Gateway = pure gateway): `Q1`, `R1`, `R3`, terminal `U2`, net `SIREN_DRV` (IO4) di skematik dan PCB; pertahankan `R2` (pull-up SD_CS). Tanpa Q1, item G/S/D dan arus sirine tidak berlaku. Tombol mute dan dioda flyback batal.
3. Validasi DevKit 38 pin (jarak deret, 19 pin/sisi, pad J2/J3) terhadap modul fisik dan urutan header microSD `H1` (1x6).
4. Ukuran papan: boleh membesar seminimal mungkin bila perlu; dengan sirine dihapus, usulkan apakah papan bisa mengecil (jangan ubah tanpa Calvin); catat alasan.
5. Jalur 16 mil, DRC 0, ekspor `PCB3.tel` dan `check_netlist.py` (pin map SD SCK=IO25, MISO=IO35, MOSI=IO32, CS=IO33; LoRa IO18/19/23, CS IO5, RST IO14, DIO0 IO26; `SIREN_DRV` dihapus dari ekspektasi `pcb3` di skrip), Gerber, cetak 1:1, STEP/outline, koordinat.

## Prompt awal (tempel ke tiap agen; ganti N)
```
Kamu agen N untuk proyek PANDU. Baca CLAUDE.md, docs/PRE_ORDER_PCB.md, dan docs/AGENT_PLAN.md (bagian "Aturan bersama" dan "Agen N") di repo pandu-capstone, branch v3.
Kerjakan hanya board PCBN. Branch kerja v3-pcbN. Jangan memesan PCB, jangan edit proyek tim, jangan ubah berkas bersama atau footprint bersama.
Langkah 0: pastikan akses edit ke proyek EasyEDA; bila gagal, berhenti dan lapor.
Semua klaim harus berstatus T/D/B; tanpa ukuran fisik T, tandai B dan lanjutkan tugas lain.
Selesai: commit ke v3-pcbN, push, dan tulis docs/agent/pcbN.md sesuai format di AGENT_PLAN.md.
```

## Peran manusia (Calvin, tidak bisa diwakili agen)
- Mengisi kolom "Ukur baru" di `PRE_ORDER_PCB.md` bagian 2 dengan jangka sorong, sebelum atau sambil agen bekerja (agen berhenti di item yang masih B).
- Cetak 1:1 dan uji tusuk modul (bagian 4), keputusan bagian 7, koordinasi casing dengan Tri Yoga, pembelian modul yang belum ada (TP4056 kedua, MT3608, tact switch, buzzer/sirine), undang akun agen ke proyek EasyEDA.
- Menggabungkan hasil tiga branch, memilih satu proyek final, mengekspor Gerber final, dan menyetujui pesanan (tabel tanda tangan bagian 8).

## Setelah PCB dipesan: pemodelan 3D casing
Bahan per board: `pcbN_step.step`, `pcbN_outline.dxf`, `pcbN_koordinat.md`, ukuran modul (jangka sorong), tinggi tiap modul. Casing Vest di `weekly/WEEK_6/PANDU_VestNode_Casing.scad` v5 harus diperbarui (dimensi dan keputusan casing: lihat `PRE_ORDER_PCB.md` bagian 6). Casing Helmet dan Gateway belum ada.
