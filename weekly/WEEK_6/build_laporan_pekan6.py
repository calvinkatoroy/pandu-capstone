import docx, copy, os
from docx.shared import Cm

SRC = "LAPORAN_KEMAJUAN_Pekan6_Group13_ORIGINAL.docx"
OUT = "LAPORAN KEMAJUAN_Pekan6_Group13_UPDATED.docx"
d = docx.Document(SRC)
P = d.paragraphs
T = d.tables
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def set_par(p, text):
    runs = p.runs
    if not runs:
        p.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        if r._r.findall('.//' + W + 'drawing'):
            continue
        r._r.getparent().remove(r._r)


def find(prefix):
    for p in P:
        if p.text.strip().startswith(prefix):
            return p
    raise KeyError(prefix)


def cell(t, r, c, text):
    set_par(T[t].rows[r].cells[c].paragraphs[0], text)


def add_row(t):
    tbl = T[t]
    new = copy.deepcopy(tbl.rows[-1]._tr)
    tbl._tbl.append(new)
    return tbl.rows[-1]


def row_set(row, vals):
    for c, v in zip(row.cells, vals):
        set_par(c.paragraphs[0], v)


# header
set_par(find('Periode'), 'Periode \t\t\t: 28 September - 3 Oktober 2026')
p = find('Adhi Rajasa Rafif (2306266943')
for q in P:
    if q.text.strip() == 'Adhi Rajasa Rafif (2306266943':
        set_par(q, 'Adhi Rajasa Rafif (2306266943)')

# 1 ringkasan proyek: koreksi
p = find('Menciptakan perangkat'); set_par(p, p.text.replace('multi-sensor sensor', 'multi-sensor'))
p = find('Sensor giroskop'); set_par(p, p.text.replace('MPU (MPU-6059)', 'MPU-6050'))
p = find('Water contact sensor'); set_par(p, p.text.replace('Water contact sensor', 'Sensor air non-kontak XKC-Y25'))
p = find('LoRaWAN untuk')
set_par(p, p.text.replace('LoRaWAN untuk', 'LoRa (SX1276, 915 MHz) untuk').replace('Jaringan LoRaWAN ini', 'Jaringan LoRa ini'))

# 2 ringkasan kemajuan
set_par(find('Pada pekan ini, kegiatan'),
 "Pada pekan ini, kegiatan proyek PANDU berfokus pada audit dan perbaikan desain hardware sebelum pemesanan PCB. "
 "Skematik tiga unit (Vest Node Master, Helmet Node, Edge Gateway) diaudit pin per pin di EasyEDA Pro dan ditemukan beberapa kesalahan desain yang telah diperbaiki: "
 "regulator AMS1117 tidak dapat menghasilkan 3,3 V dari baterai Li-ion, tombol sesaat dipakai sebagai saklar daya, pin antena modul LoRa tersambung ke GND, "
 "serta rangkaian pemrograman ESP32 pada Edge Gateway belum lengkap. Desain disesuaikan dengan komponen yang telah dibeli (ESP32-DevKitC V4); "
 "sensor anti-crush VL53L0X dan buzzer pada Vest Node dihapus untuk menekan false positive, dan sensor air diganti ke tipe non-kontak XKC-Y25 agar sesuai target IP67. "
 "Ketiga PCB telah lolos DRC (0 error) dan Gerber telah diekspor, namun pemesanan PCB ditunda sampai verifikasi fisik modul (pin LoRa, TP4056, ukuran board ESP32) selesai. "
 "Casing Vest Node dibuat ulang mengikuti PCB final (114 x 101 x 36,6 mm) menggunakan model parametrik OpenSCAD. "
 "Wireframe dashboard dari pekan sebelumnya tetap menjadi acuan visual; finalisasi fitur menunggu definisi endpoint ESP32.")

# 3 target
cell(0, 1, 1, 'Order PCB (ditunda, lihat bagian 10)')
cell(0, 1, 2, ' ☐ Tercapai ☒ Belum')
cell(0, 2, 1, 'Simulasi Assembly 3D (casing Vest Node, OpenSCAD)')
cell(0, 2, 2, ' ☒ Tercapai ☐ Belum')
cell(0, 3, 2, ' [ISI oleh Rafif/Calvin: Tercapai / Belum]')

# 4 realisasi
cell(1, 1, 1, 'Revisi skematik dan PCB, persiapan order PCB')
cell(1, 1, 2, 'Gibran, Rifat, Calvin')
cell(1, 1, 3,
 "Rancangan skematik direvisi untuk mengurangi false positive: sensor jarak anti-crushing dihilangkan (rawan false positive saat pandu menempel dinding kapal), "
 "dan sensor kontak air diganti ke sensor non-kontak XKC-Y25 karena sensor kontak berisiko kemasukan air sehingga sulit mencapai IP67. "
 "Skematik tiga unit diaudit pin per pin dan diperbaiki: AMS1117 dihapus (diganti modul boost 5 V), saklar daya dijadikan input GPIO (deep sleep di firmware), "
 "GPS dan sensor air dikendalikan via MOSFET untuk menghemat daya, pin antena dan GND modul LoRa dikoreksi, rangkaian pemrograman/EN ESP32 Gateway dilengkapi, "
 "serta pull-down gate sirine ditambahkan. Footprint ESP32 disesuaikan dengan board yang dibeli (DevKitC V4). "
 "Hasil: PCB1, PCB2, PCB3 lolos DRC (0 error, semua net ter-route) dan Gerber diekspor pada 3 Oktober 2026. Order PCB ditunda sampai verifikasi fisik modul selesai.")
cell(1, 2, 1, '3D model casing')
cell(1, 2, 2, 'Calvin, Yoga')
cell(1, 2, 3,
 "Casing Vest Node dibuat ulang mengikuti PCB final dengan model parametrik OpenSCAD (PETG, dinding 2 mm): dimensi luar 114 x 101 x 36,6 mm, "
 "bukaan USB-C pengisian (dinding kiri), ekstensi micro-USB ESP32 dan SMA antena LoRa (dinding bawah), plunger tombol power dan SOS pada tutup, "
 "serta modul boost digantung pada tutup. Validasi dimensi otomatis lulus (Gambar 11). Draft 3D awal di Autodesk Fusion 360 (Gambar 1) menjadi referensi bentuk. "
 "[ISI oleh Yoga: status sinkronisasi model Fusion 360 dengan dimensi baru]")
cell(1, 3, 2, 'Rafif, Calvin')

# 5 anggota
cell(2, 1, 1, T[2].rows[1].cells[1].text + "\n[ISI oleh Rafif: kegiatan Pekan 6, mis. konfirmasi pembelian modul dan pembaruan BOM]")
cell(2, 2, 1,
 "Mengaudit skematik tiga unit (Vest Node, Helmet Node, Edge Gateway) pin per pin dan memperbaiki temuan: AMS1117 dihapus (diganti boost 5 V), saklar daya dijadikan input GPIO, "
 "gating GPS dan sensor air via MOSFET, pin antena dan GND modul LoRa, rangkaian ESP32 Gateway, dan pull-down gate sirine.\n"
 "Menyesuaikan PCB dengan komponen yang dibeli (ESP32-DevKitC V4), me-routing ulang ketiga PCB hingga DRC 0 error, dan mengekspor Gerber (tersimpan di repository tim).\n"
 "Membuat ulang casing Vest Node (OpenSCAD) mengikuti PCB final 114 x 101 x 36,6 mm beserta validasi dimensi otomatis.\n"
 "Melakukan cross-check BOM terhadap desain, serta menyusun dokumen audit dan handover.")
cell(2, 2, 2, '90%')
cell(2, 3, 1, T[2].rows[3].cells[1].text + "\n[UPDATE oleh Gibran: status skematik/PCB final dan rencana order PCB]")
cell(2, 4, 1, T[2].rows[4].cells[1].text + "\n[UPDATE oleh Rifat: status PCB Helmet Node dan Edge Gateway]")
cell(2, 5, 1, "[ISI oleh Yoga: kegiatan Pekan 6, mis. sinkronisasi model Fusion 360 dengan dimensi casing terbaru 114 x 101 x 36,6 mm]")
cell(2, 5, 2, '[ISI]')

# 6 hasil implementasi
set_par(find('PCB Design untuk seluruh'),
 "PCB Design untuk seluruh ekosistem PANDU telah selesai dan lolos DRC (0 error): Unit 1 Vest Node Master (107,95 x 95,25 mm, ESP32-DevKitC V4), "
 "Unit 2 Helmet Node (ditambah kapasitor tantalum 100 uF pada rel baterai CR2032), dan Unit 3 Edge Gateway (ESP32-DevKitC V4). "
 "Gerber ketiga unit telah diekspor (3 Oktober 2026) dan belum dipesan.")
set_par(find('Belum ada integrasi fisik'),
 "Belum ada integrasi fisik antar unit. Ketiga PCB telah selesai didesain dan diekspor ke Gerber, namun belum difabrikasi karena menunggu verifikasi fisik modul "
 "(urutan pin modul LoRa, TP4056, modul boost 5 V, dan ukuran board ESP32) serta pembelian modul yang masih kurang (sensor XKC-Y25 dan modul boost 5 V).")
set_par(find('Draft 3D casing P.A.N.D.U selesai dibuat di'),
 "Casing Vest Node dibuat ulang mengikuti PCB final menggunakan model parametrik OpenSCAD (PETG, dinding 2 mm): dimensi luar 114 x 101 x 36,6 mm, "
 "dengan bukaan USB-C pengisian (dinding kiri), ekstensi micro-USB ESP32 dan SMA antena LoRa (dinding bawah), plunger tombol power dan SOS pada tutup (Gambar 11). "
 "Draft 3D awal di Autodesk Fusion 360 (Gambar 1) menjadi referensi bentuk.")
set_par(find('Blueprint 2D presisi dengan dimensi 55 x 65 x 23'),
 "Blueprint 2D awal (55 x 65 x 18 mm) tidak lagi berlaku karena PCB final berukuran 107,95 x 95,25 mm; model casing telah disesuaikan. "
 "[ISI oleh Yoga: sinkronisasi model Fusion 360 dengan dimensi baru]")

# 7 dokumentasi
for pre, suf in (('Gambar 1.', ' (arsip Pekan 3)'), ('Gambar 2.', ' (arsip Pekan 3)'),
                 ('Gambar 3.', ' (versi sebelum perbaikan Pekan 6; lihat Gambar 8)'),
                 ('Gambar 4.', ' (versi sebelum perbaikan; lihat Gambar 9)'),
                 ('Gambar 5.', ' (versi sebelum perbaikan; lihat Gambar 10)')):
    p = find(pre)
    p.runs[-1].text = p.runs[-1].text.rstrip() + suf
cap7 = find('Gambar 7.')


def add_after(anchor, items):
    cur = anchor._p
    for kind, val in items:
        np_ = d.add_paragraph()
        np_.alignment = 1
        if kind == 'img' and os.path.exists(val):
            np_.add_run().add_picture(val, width=Cm(11))
        elif kind == 'img':
            np_.add_run('[' + os.path.basename(val) + ' belum tersedia, tambahkan screenshot]')
        else:
            np_.add_run(val)
        cur.addnext(np_._p)
        cur = np_._p


R = lambda f: os.path.join('img', f)
add_after(cap7, [
    ('img', R('pcb1_final.png')), ('cap', 'Gambar 8. Layout PCB1 Vest Node Master final (ESP32-DevKitC V4, TP4056 di sisi bawah), DRC 0 error.'),
    ('img', R('pcb2_final.png')), ('cap', 'Gambar 9. Layout PCB2 Helmet Node final (ditambah C2 tantalum 100 uF), DRC 0 error.'),
    ('img', R('pcb3_final.png')), ('cap', 'Gambar 10. Layout PCB3 Edge Gateway final (ESP32-DevKitC V4), DRC 0 error.'),
    ('img', R('casing_v5.png')), ('cap', 'Gambar 11. Render casing Vest Node v5 (OpenSCAD), 114 x 101 x 36,6 mm, dengan bukaan USB-C, ekstensi micro-USB, SMA, dan plunger tombol.'),
    ('img', R('casing_v5_exploded.png')), ('cap', 'Gambar 12. Exploded view casing Vest Node v5 (cangkang, PCB, holder baterai, modul boost, tutup, plunger).'),
])

# 8 pengujian
LULUS = ' ☒ Lulus ☐ Tidak'
row_set(T[3].rows[1], [
    'Kesesuaian dimensi internal casing Vest Node v5 terhadap komponen (PCB1 107,95 x 95,25 mm, ESP32-DevKitC V4, holder baterai 18650, TP4056 di sisi bawah, modul boost)',
    'Seluruh komponen muat tanpa overlap/tabrakan',
    'Validasi otomatis OpenSCAD: holder baterai muat (atas holder 33,6 mm vs tinggi shell 34,6 mm), modul boost muat dan tidak menimpa header (dasar boost 16,5 mm vs header 8,5 mm). Dimensi luar 114 x 101 x 36,6 mm.',
    LULUS])
row_set(T[3].rows[2], ['Design Rule Check PCB1, PCB2, PCB3 (EasyEDA Pro)', '0 error DRC dan 0 ratline (semua net ter-route)',
                       'PCB1, PCB2, PCB3: 0 error dan 0 ratline (3 Oktober 2026).', LULUS])
row_set(T[3].rows[3], ['DRC skematik (pin mengambang) PCB1 dan PCB3', 'Seluruh pin yang dipakai tersambung',
                       'Ditemukan dan diperbaiki GND RA-02 dan GPS_EN yang sempat tidak tersambung; peringatan tersisa hanya pin modul yang memang tidak dipakai.', LULUS])
set_par(find('Verifikasi dimensi dilakukan'),
 "Pengujian pekan ini berupa verifikasi desain secara simulasi (belum ada pengujian fisik karena PCB belum difabrikasi). "
 "Dimensi casing divalidasi dengan model parametrik OpenSCAD dan pengecekan otomatis atas kecocokan holder baterai dan modul boost di dalam casing (Gambar 11, 12). "
 "DRC pada ketiga PCB dan DRC skematik berhasil menemukan kesalahan koneksi (pin antena LoRa ke GND, pin GND dan GPS_EN yang tidak tersambung) sebelum Gerber dipesan. "
 "Nilai yang masih berupa asumsi dan perlu diverifikasi pada barang fisik: tinggi modul TP4056 beserta header (8,5 mm) dan tinggi holder baterai.")

# 9 kendala
issues = [
    ("Desain awal tidak cocok dengan komponen yang dibeli (footprint ESP32 17 pin per sisi vs DevKitC V4 38 pin; modul LoRa yang dibeli bukan Ra-02)",
     "Footprint PCB salah sehingga board tidak dapat dipasang dan PCB tidak dapat dipesan",
     "Simbol dan footprint diganti ke DevKitC V4 pada PCB1 dan PCB3; kecocokan modul LoRa menunggu foto/datasheet modul; ukur board fisik sebelum order"),
    ("Port USB TP4056 dan ESP32 menghadap ke dalam papan sehingga tidak terjangkau dari dinding casing",
     "Sulit mengisi baterai dan memprogram setelah dirakit",
     "TP4056 diputar 180 derajat (USB-C ke dinding), ESP32 memakai kabel ekstensi panel-mount micro-USB"),
    ("Kesalahan desain ditemukan saat audit (AMS1117, pin antena LoRa, rangkaian EN/IO0 ESP32 Gateway, dll.)",
     "Berisiko papan tidak berfungsi jika langsung dipesan",
     "Diperbaiki dan diverifikasi DRC; order PCB ditunda sampai verifikasi fisik modul"),
    ("BOM belum sinkron dengan desain (VL53L0X dan BME680 masih tercantum; XKC-Y25, boost 5 V, komponen SMD belum ada)",
     "Anggaran dan pembelian tidak sesuai kebutuhan",
     "Daftar selisih BOM disusun; Rafif memperbarui BOM dan membeli modul yang kurang"),
]
for it in issues:
    row_set(add_row(4), it)

# 10 deviasi
row_set(T[5].rows[5], ['Finalisasi 3D casing', 'Minggu 5', 'Minggu 6',
                       'Casing Vest Node dibuat ulang mengikuti PCB final (114 x 101 x 36,6 mm, OpenSCAD). [ISI oleh Yoga: sinkronisasi model Fusion 360]'])
row_set(add_row(5), ['Order PCB', 'Minggu 5 (target 26 Sep, lalu 3 Okt)', 'Diundur ke Minggu 7',
                     'Audit skematik menemukan kesalahan desain dan footprint ESP32/modul LoRa harus disesuaikan dengan komponen yang dibeli; Gerber sudah siap, order menunggu verifikasi fisik modul.'])
set_par(find('Analisis Deviasi'),
 "Analisis Deviasi\n\nTerdapat penyimpangan positif pada observasi lapangan (Juli 2026) yang memberi keleluasaan menyesuaikan perangkat dengan standar IP67. "
 "Pemodelan 3D casing bergeser ke Minggu 4 untuk memprioritaskan blueprint 2D sesuai arahan dosen. "
 "Pada Minggu 6, pemesanan PCB yang dijadwalkan sebelumnya belum terlaksana: audit skematik menemukan beberapa kesalahan desain yang harus diperbaiki, "
 "serta footprint ESP32 dan modul LoRa harus disesuaikan dengan komponen yang telah dibeli. Perbaikan dan ekspor Gerber telah selesai, "
 "sedangkan order PCB ditunda sampai verifikasi fisik modul selesai (target Minggu 7). "
 "Penundaan ini mencegah biaya fabrikasi ulang, tetapi perlu dijaga agar tidak mengganggu jadwal integrasi sistem.")

# 11 rencana
plan = [
    ("Verifikasi fisik modul (pin LoRa, TP4056, boost, ukuran ESP32) lalu Order PCB", "Gibran, Rifat, Calvin", "10 Oktober 2026"),
    ("Membeli modul yang kurang (XKC-Y25, boost 5 V, komponen SMD) dan memperbarui BOM", "Rafif", "10 Oktober 2026"),
    ("Sinkronisasi model casing Fusion 360 dan casing Helmet Node/Gateway ke PCB baru", "Yoga, Calvin", "17 Oktober 2026"),
    ("Finalisasi fitur dashboard dan tech stack setelah endpoint ESP32 ditetapkan", "Rafif, Calvin", "17 Oktober 2026"),
    ("Perakitan uji (breadboard/perfboard) dan mulai firmware (deep sleep, kontrol GPS/sensor air, deteksi jatuh)", "[ISI]", "24 Oktober 2026"),
]
for i, pv in enumerate(plan, 1):
    row = T[6].rows[i] if i < len(T[6].rows) else add_row(6)
    row_set(row, [str(i)] + list(pv))

# 12 progress
cell(7, 1, 2, '90')
set_par(find('Progress Total ='), 'Progress Total = 31,5%')

# 13 kesimpulan
set_par(find('PCB Design unit vest node'),
 "PCB Design ketiga unit (Vest Node Master, Helmet Node, Edge Gateway) telah selesai dan lolos DRC dengan Gerber yang sudah diekspor. "
 "Audit skematik pada pekan ini menemukan dan memperbaiki beberapa kesalahan desain yang berpotensi membuat papan tidak berfungsi, "
 "dan desain disesuaikan dengan komponen yang telah dibeli (ESP32-DevKitC V4). Sensor anti-crush dan buzzer pada Vest Node dihapus untuk menekan false positive, "
 "dan sensor air diganti ke tipe non-kontak untuk target IP67. Casing Vest Node dibuat ulang mengikuti PCB final. "
 "Pemesanan PCB ditunda sampai verifikasi fisik modul (pin LoRa, TP4056, boost, ukuran ESP32) selesai dan modul yang kurang dibeli. "
 "Di sisi software, wireframe dashboard mobile PANDU telah tersedia; finalisasi fitur dan tech stack aplikasi (Android dan iOS) menunggu kepastian endpoint dari ESP32.")

d.save(OUT)
print('saved', OUT)
