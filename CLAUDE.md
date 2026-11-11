# CLAUDE.md: PANDU capstone (Kelompok 13)

Per 11 Nov 2026. Bahasa kerja: Indonesia, santai dan ringkas. Pengguna utama: Calvin (Vest/PCB/dokumentasi). Anggota: Rafif (ketua), Gibran, Rifat, Tri Yoga (casing 3D).
Proyek: P.A.N.D.U (Perangkat Alarm Nirkabel Deteksi Urgensi), wearable keselamatan pandu kapal. Dosen: Tomy Abuzairi.

## Aturan paling penting (akurasi)
1. **Jangan klaim "selesai/sudah/cocok" tanpa bukti**: ukuran diukur dengan jangka sorong, atau cetak 1:1, atau DRC/netlist yang dijalankan. Dokumen lama pernah menulis "footprint sudah diganti" padahal belum (ditemukan 5 Nov).
2. **Bedakan tiga status**: `TERBUKTI` (ada ukuran/log/hasil), `DUGAAN` (dari listing/datasheet/ingatan), `BELUM DICEK`. Tulis statusnya.
3. **Jangan menebak angka fisik** (jarak deret, diameter lubang, urutan pin). Kalau tidak ada di `docs/PRE_ORDER_PCB.md` sebagai TERBUKTI, minta Calvin mengukur.
4. **Jangan memesan PCB, menekan "Order PCB", atau mem-push ke `main`** tanpa izin Calvin. Push hanya ke branch kerja.
5. Dokumen di repo bisa usang. Urutan kepercayaan: ukuran fisik terbaru dari Calvin > EasyEDA (salinan kerja) > `docs/PRE_ORDER_PCB.md` > `docs/FOOTPRINT_SPEC_V3.md` > dokumen lain. `HANDOVER.md` bagian atas **usang** (DevKitC V4, XL1276/915 MHz, CR2032, TTP223 sudah tidak berlaku).

## Sumber kebenaran desain
- Proyek EasyEDA Pro tim "Pandu-Capstone" (pemilik akun gibransaja406) **jangan diedit** sampai Calvin bilang adopsi.
- Salinan kerja Calvin: **`Pandu-Capstone-v3-footprint-fix`** (salinan tim per 5 Nov). Semua perbaikan footprint dikerjakan di salinan.
- Repo ini (`calvinkatoroy/pandu-capstone`, branch `v3`) hanya menyimpan ekspor (netlist, Gerber, footprint sumber) dan dokumen.
- Footprint kustom disimpan sebagai berkas di `hardware/footprints/` supaya bisa diimpor akun lain (library pribadi satu akun tidak terlihat akun lain).

## Perangkat keras (keputusan final, jangan diubah tanpa Calvin)
| Board | Isi | Catatan |
|---|---|---|
| PCB1 Vest Node | ESP32 **DevKit V1 30 pin** (15/sisi), Ra-02 SX1278 433 MHz breakout, GY-521 MPU6050, GPS NEO-6M, sensor air XKC-Y25-V (non-kontak), TP4056 HW-373 USB-C, 18650 1200 mAh, boost MT3608 5 V, 2 tact (SOS IO27, power IO13) | Tanpa VL53L0X/BME680, tanpa buzzer. 108 x 95,25 mm |
| PCB2 Helmet Node | ESP32-C3 SuperMini, TP4056 HW-373, baterai, 1 tact (on/off, GPIO4), jumper/saklar baterai | BLE beacon `PANDU-HELM`. Tanpa sensor sentuh TTP223 |
| PCB3 Edge Gateway | ESP32 DevKit **38 pin** (19/sisi), Ra-02 breakout, microSD (SPI sendiri), buzzer/sirine 5 V via MOSFET 2N7002 | WiFi ke Supabase |
- LoRa = **433 MHz** (SX1278), `LORA_FREQ = 433E6`. Modul 868/915 MHz lama tidak dipakai.
- Ra-02 yang dibeli = **breakout 2,54 mm** (bukan modul SMD telanjang). Jarak deret 26,0 mm. Pin: `docs/LORA_RA02_BREAKOUT.md`.
- Pin map firmware dan netlist: `HANDOVER.md` (bagian "Pemetaan pin final", XKC_EN=IO32) dan `hardware/netlist/check_netlist.py`. Jangan pakai IO6-11 (flash); hati-hati strapping IO0/2/5/12/15.
- Sensor yang dibuang: VL53L0X, BME680. Jangan ditambahkan kembali.

## Syarat PCB dari dosen
- **Lebar jalur tembaga diperlebar: 16 mil** (aturan default semua net sinyal) dan jalur daya sebaiknya lebih lebar (`VBAT_RAW`, `VBAT_POS`, `VBOOST_5V`, 5V: 25 mil bila muat). Pelebaran massal pernah memicu 188 pelanggaran DRC; kerjakan dengan rute ulang, bukan menimpa jalur.
- Ukuran papan jangan membesar kecuali perlu; PCB3 boleh membesar seminimal mungkin.

## Alur EasyEDA (UI rapuh, dikendalikan lewat Claude-in-Chrome, tidak bisa dari sesi cloud)
- Satu perubahan, satu simpan, satu DRC. Klik kolom input sebelum mengetik; jangan `ctrl+a` di kanvas (memilih semua objek); `triple_click` untuk mengosongkan kolom.
- Skematik ke PCB: Design > Import Changes from Schematic; **centang hanya baris yang diinginkan** (pernah mencoba mengembalikan footprint lama dan menambah header antena). Lalu Route > Unroute > All, Route > Auto Routing, Tools > Copper Manager > Rebuild All, Check DRC.
- Ganti footprint satu komponen: skematik > pilih komponen > Properties > Footprint "···" > Footprint Manager (proyek-lebar): centang hanya baris target, pilih library Personal, pilih footprint, Update.
- Nama pad bertanda hubung (`J2-5`) tidak bisa diketik di antarmuka (hubung dibuang). Bikin lewat file impor KiCad (File > Import > KiCad > "Extract Libraries"), contoh `hardware/footprints/make_devkit_zip_j2j3.py`.
- Dialog file asli tidak terjangkau: timpa `HTMLInputElement.prototype.click` agar input `type=file` ditempel ke body, lalu `file_upload`. Tips Confirm perlu dua klik.
- Kabel skematik meleset: taruh net label tepat di ujung pin, cek "Pins floating" lewat DRC skematik.
- Simbol DevKit punya 38 pin, footprint V1 hanya 30 pad: 8 pin tanpa pad (J2-16, J2-17, J2-18, J3-7, J3-14, J3-17, J3-18, J3-19) memunculkan peringatan skematik, bukan error DRC PCB.
- Klik daftar log DRC memindah tab (hanya seleksi). Tab bergeser saat membuka tab baru; screenshot sering timeout setelah beban berat.

## Repo
- `docs/` dokumentasi (`PRE_ORDER_PCB.md` checklist pesan PCB, `AGENT_PLAN.md` rencana 3 agen, `FOOTPRINT_SPEC_V3.md`, `BOM_V2.md`, `AUDIT_V3.md`, `LORA_RA02_BREAKOUT.md`).
- `hardware/` `footprints/` (sumber footprint + generator), `netlist/` (`.tel` + `check_netlist.py`), `gerber/` (**semua yang ada belum valid, jangan dipesan**).
- `firmware/` PlatformIO per node. `weekly/WEEK_n/` laporan pekanan (python-docx dari template WEEK_7; `build_individu_pekanN.py`).
- Git: kerja di `v3`. Commit diakhiri `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Jangan commit rahasia (kunci Supabase, WiFi).

## Laporan
Jumlah jam dan persentase di laporan = estimasi kecuali ada catatan. GPS sudah diuji luar ruangan; deteksi jatuh terbukti; nilai diam MPU6050 g=4,8 (seharusnya ~1,0) belum dikalibrasi; microSD `sd:0` = kartu belum dimasukkan. Software pekan 11 hanya sekitar +10%. Tanda tangan ketua hanya setelah ACC.

## Setelah PCB dipesan
Pemodelan 3D casing (Tri Yoga). Butuh dari tiap board: STEP 3D PCB, outline DXF, koordinat konektor/tombol/lubang baut. Lihat bagian Deliverable di `docs/AGENT_PLAN.md`. Catatan: casing yang ada di laporan (55 x 65 x 23 mm) **tidak muat** PCB1 (108 x 95,25 mm); samakan sebelum memesan (item G7 di `PRE_ORDER_PCB.md`).
