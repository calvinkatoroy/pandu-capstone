import copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = "../WEEK_5/LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 5.docx"
OUT = "LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 6.docx"
d = docx.Document(SRC)
P = list(d.paragraphs)  # snapshot of W5 indices
T = d.tables


def st(p, text):
    rs = p.runs
    if not rs:
        p.add_run(text)
        return
    rs[0].text = text
    for r in rs[1:]:
        r._r.getparent().remove(r._r)


def fill(t, data):
    while len(t.rows) - 1 < len(data):
        t._tbl.append(copy.deepcopy(t.rows[-1]._tr))
    while len(t.rows) - 1 > len(data):
        t._tbl.remove(t.rows[-1]._tr)
    for r, vals in zip(t.rows[1:], data):
        for c, v in zip(r.cells, vals):
            if isinstance(v, list):
                for p, x in zip(c.paragraphs, v):
                    st(p, x)
            else:
                st(c.paragraphs[0], v)


def lst(first, n, texts):
    """Replace list paragraphs P[first:first+n] with texts (clone/remove as needed)."""
    last = P[first + n - 1]
    parent = last._parent
    cur = last._p
    extra = []
    for _ in range(len(texts) - n):
        new = copy.deepcopy(last._p)
        cur.addnext(new)
        cur = new
        extra.append(Paragraph(new, parent))
    for p, t in zip(P[first:first + n] + extra, texts):
        st(p, t)
    for i in range(len(texts), n):
        P[first + i]._p.getparent().remove(P[first + i]._p)


# A. identitas
ident = T[0]
st(ident.rows[6].cells[1].paragraphs[0], "6")
st(ident.rows[7].cells[1].paragraphs[0], "28 September - 3 Oktober 2026")

# B. target
fill(T[1], [
    ["1", "Audit skematik 3 PCB (Vest, Helmet, Edge Gateway) dan perbaikan desain PCB hingga siap fabrikasi",
     "Skematik & PCB terkoreksi, DRC 0 error, Gerber baru", ["☐ Belum", "☑ Selesai"]],
    ["2", "Merancang ulang casing Vest Node mengikuti PCB final",
     "Model OpenSCAD casing + render + validasi dimensi", ["☐ Belum", "☑ Selesai"]],
    ["3", "Cross-check BOM dengan desain dan komponen yang sudah dibeli",
     "Daftar selisih BOM vs desain", ["☐ Belum", "☑ Selesai"]],
    ["4", "Finalisasi daftar fitur dashboard & tech stack aplikasi mobile (rencana Pekan 5)",
     "Daftar fitur & keputusan tech stack", ["☑ Belum", "☐ Selesai"]],
])

# C. logbook
fill(T[2], [
    ["Senin (28 Sep)", "[ISI: kegiatan 28 Sep]", "[ISI]", "-"],
    ["Selasa (29 Sep)", "[ISI: kegiatan 29 Sep]", "[ISI]", "-"],
    ["Rabu (30 Sep)", "[ISI: kegiatan 30 Sep]", "[ISI]", "-"],
    ["Kamis (1 Okt)",
     "Review proposal & riwayat Pekan 2-5; menetapkan perubahan scope Vest Node (tanpa VL53L0X/BME680, fokus jatuh & sensor air); audit skematik PCB1 dan redesain daya (tanpa AMS1117, boost 5 V, tombol power GPIO, MOSFET untuk GPS & XKC-Y25); perbaikan skematik, update PCB dan routing ulang PCB1 (DRC 0 error)",
     "8", "EasyEDA project Pandu-Capstone; Audit_Skematik_Status.md"],
    ["Jumat (2 Okt)",
     "Audit dan perbaikan PCB3 Edge Gateway; mengganti footprint ESP32 PCB1 & PCB3 ke DevKitC V4 sesuai komponen yang dibeli; cross-check BOM (Google Sheets) dengan desain; membuat repository GitHub pandu-capstone dan HANDOVER.md",
     "7", "github.com/calvinkatoroy/pandu-capstone"],
    ["Sabtu (3 Okt)",
     "Menambah kapasitor tantalum 100 uF di PCB2; ekspor Gerber 3 board; memutar TP4056 agar USB-C menghadap dinding; membuat ulang casing Vest Node v5 (OpenSCAD); audit dan update Laporan Kemajuan Kelompok Pekan 6 (bagian Calvin)",
     "7", "hardware/gerber/; PANDU_VestNode_Casing.scad; commit Git"],
])
st(P[8], "Total Jam Kerja Minggu Ini: [ISI] Jam")

# D
lst(12, 4, [
    "Audit skematik tiga PCB dan perbaikan temuan: AMS1117 tidak mendapat 3,3 V dari Li-ion, dua sumber 3V3 paralel, tombol sesaat dipakai sebagai saklar daya, pin 1 RA-02 (antena) salah terhubung ke GND, GND tambahan RA-02 belum tersambung, ESP32 Gateway tanpa rangkaian EN/program, gate MOSFET sirine tanpa pull-down.",
    "Redesain daya Vest Node: baterai 18650 > TP4056 > boost 5 V; tombol power berupa tact switch GPIO (toggle deep sleep di firmware, tahan air dengan boot karet); GPS dan sensor air XKC-Y25 dihemat lewat MOSFET.",
    "Penyesuaian footprint ESP32 PCB1 dan PCB3 ke DevKitC V4 (komponen yang dibeli), routing ulang, DRC 0 error / 0 ratline pada ketiga board; PCB2 ditambah tantalum 100 uF di rel CR2032.",
    "Perancangan ulang casing Vest Node v5 (PETG, 114 x 101 x 36,6 mm), cross-check BOM, pembuatan repository dan HANDOVER.md, serta audit dan update Laporan Kemajuan Kelompok Pekan 6 bagian Calvin.",
])
lst(17, 4, [
    "Gerber baru PCB1, PCB2, PCB3 (hardware/gerber/, 3 Okt 2026; belum dipesan) dan dokumen Audit_Skematik_Status.md",
    "Model casing Vest Node v5 (PANDU_VestNode_Casing.scad) beserta render dan validasi dimensi — repository: github.com/calvinkatoroy/pandu-capstone",
    "Daftar selisih BOM vs desain (hapus VL53L0X/BME680; tambah XKC-Y25, boost 5 V, MOSFET, antena + SMA, dll.)",
    "Repository pandu-capstone (weekly, hardware, docs) + HANDOVER.md dan update Laporan Kemajuan Kelompok Pekan 6 (bagian Calvin)",
])

# E
fill(T[3], [
    ["Hardware", "Audit skematik & perbaikan PCB1-3, Gerber siap",
     "Skematik terkoreksi, PCB DevKitC V4, DRC 0 error, Gerber 3 board (belum dipesan)", "90%"],
    ["Software", "-", "-", "-"],
    ["Mekanik", "Casing Vest Node mengikuti PCB final",
     "Casing v5 (OpenSCAD) tervalidasi dimensi; Helmet & Gateway belum", "70%"],
    ["Pengujian", "-", "-", "-"],
    ["Dokumentasi", "Dokumentasi audit, BOM, handover, laporan",
     "Audit_Skematik_Status, repo + HANDOVER.md, update laporan kelompok", "100%"],
])
st(P[24], "Pekan ini pekerjaan Calvin berfokus pada hardware: audit skematik ketiga PCB, redesain daya Vest Node (tanpa AMS1117, boost 5 V, tombol power GPIO, gating GPS dan sensor air lewat MOSFET), penyesuaian footprint ESP32 ke DevKitC V4, serta pembuatan Gerber baru dengan DRC 0 error. Scope Vest Node disederhanakan (tanpa VL53L0X dan BME680) untuk menghindari false positive. Casing Vest Node dibuat ulang (v5) mengikuti PCB, dan cross-check BOM menemukan sejumlah selisih yang perlu ditindaklanjuti. PCB belum dipesan karena ukuran fisik modul (ESP32, LoRa, TP4056, boost) masih harus diverifikasi. Finalisasi fitur dashboard dan tech stack mobile belum dikerjakan pekan ini.")

# F
fill(T[4], [
    ["1", "Desain awal tidak cocok dengan komponen yang dibeli: footprint ESP32 salah (DevKitC V4) dan modul LoRa yang dibeli (SX1276 915 MHz) bukan Ra-02",
     "PCB harus diubah; order PCB ditunda hingga pinout dan ukuran modul fisik terverifikasi", "Tinggi"],
    ["2", "Port USB beberapa modul menghadap ke dalam papan sehingga tidak terjangkau dari dinding casing",
     "Orientasi TP4056 diputar dan DevKit memakai kabel ekstensi micro-USB panel-mount; casing perlu dicek ulang dengan modul asli", "Sedang"],
    ["3", "BOM belum diperbarui dan melebihi dana (Rp2,495 jt vs Rp2 jt); beberapa komponen belum ada",
     "Pembelian XKC-Y25, boost 5 V, SMD, dan antena tertunda; perlu keputusan tim", "Sedang"],
])
st(P[27], "Desain awal dibuat sebelum komponen final dibeli sehingga terdapat ketidaksesuaian footprint dan sistem daya; audit baru dilakukan pekan ini. Tim juga belum memperbarui BOM sehingga selisih baru ditemukan saat cross-check.")

# G
fill(T[5], [
    ["Footprint/pinout tidak cocok komponen fisik",
     "Memakai ukuran resmi DevKitC V4 sementara; ukur modul fisik (jarak baris pin ESP32, pinout LoRa, TP4056, boost) sebelum order PCB",
     "Calvin", "10 Oktober 2026"],
    ["USB tidak terjangkau dari dinding casing",
     "TP4056 diputar 180 derajat, ekstensi micro-USB panel-mount untuk DevKit; verifikasi dimensi dengan modul asli",
     "Calvin", "10 Oktober 2026"],
    ["BOM selisih dengan desain dan melebihi dana",
     "Hapus VL53L0X/BME680 (hemat Rp250 rb), tambah komponen yang kurang, update sheet bersama Rafif/Gibran",
     "Calvin, Rafif, Gibran", "10 Oktober 2026"],
])

# H: ganti drawing P41 dengan 3 figur
IMG = "img/"
figs = [
    (IMG + "pcb1_final.png", 14, "Gambar 1. Layout PCB1 Vest Node Master setelah audit (ESP32-DevKitC V4, TP4056, boost 5 V, RA-02), DRC 0 error."),
    (IMG + "pcb3_final.png", 14, "Gambar 2. Layout PCB3 Edge Gateway setelah diganti ke DevKitC V4, DRC 0 error."),
    (IMG + "casing_v5.png", 12, "Gambar 3. Render casing Vest Node v5 (OpenSCAD, PETG) berukuran 114 x 101 x 36,6 mm. Repository: github.com/calvinkatoroy/pandu-capstone"),
]
pic_p, cap_p = P[41], P[42]
for dr in pic_p._p.findall('.//' + qn('w:drawing')):
    dr.getparent().remove(dr)
tpl_pic, tpl_cap = copy.deepcopy(pic_p._p), copy.deepcopy(cap_p._p)
anchor = cap_p._p
for i, (path, w, cap) in enumerate(figs):
    if i == 0:
        pp, cp = pic_p, cap_p
    else:
        pe, ce = copy.deepcopy(tpl_pic), copy.deepcopy(tpl_cap)
        anchor.addnext(pe)
        pe.addnext(ce)
        anchor = ce
        pp, cp = Paragraph(pe, pic_p._parent), Paragraph(ce, pic_p._parent)
    run = pp.runs[0] if pp.runs else pp.add_run()
    run.add_picture(path, width=Cm(w))
    st(cp, cap)

# I
st(P[46], "Diskusi tim: penetapan perubahan scope Vest Node (tanpa VL53L0X dan BME680; fokus deteksi jatuh dengan MPU-6050 dan sensor air) bersama anggota kelompok")
st(P[47], "Koordinasi BOM: cross-check daftar komponen dengan Rafif dan Gibran (komponen yang sudah dibeli vs desain) serta serah-terima desain lewat repository dan HANDOVER.md")
st(P[48], "Koordinasi dengan dosen: Belum ada sesi khusus minggu ini; pembahasan dilakukan internal tim")
st(P[50], "Berperan dalam mengaudit skematik ketiga PCB, mendesain ulang daya Vest Node, memperbaiki dan merouting ulang PCB1-PCB3 hingga DRC 0 error, mengekspor Gerber, merancang ulang casing Vest Node (OpenSCAD), melakukan cross-check BOM, serta menyiapkan repository dan dokumentasi (HANDOVER.md, laporan kelompok bagian Calvin).")

# J
st(P[53], "Audit skematik sebelum order PCB menemukan banyak kesalahan desain (daya, pin RA-02, rangkaian EN) yang tertangkap sebelum fabrikasi.")
st(P[54], "Keputusan scope (tanpa VL53L0X/BME680) cepat disepakati dan menyederhanakan desain serta mengurangi biaya.")
st(P[55], "Ketiga PCB dan casing Vest Node selesai desain dengan validasi otomatis (DRC dan cek dimensi).")
st(P[57], "Desain dibuat sebelum komponen final dipastikan sehingga banyak yang harus diulang; BOM dan desain perlu disinkronkan lebih awal.")
st(P[58], "Fitur dashboard dan tech stack aplikasi mobile belum dikerjakan pekan ini karena fokus hardware.")
st(P[59], "Ukuran fisik modul belum diverifikasi sehingga order PCB tertunda; perlu jadwal pengecekan fisik.")
st(P[61], "Desain PCB harus mengacu pada modul yang benar-benar dibeli (nama listing dan ukuran), bukan hanya simbol library.")
st(P[62], "Port USB dan akses fisik harus dipertimbangkan sejak desain PCB karena menentukan desain casing.")
st(P[63], "Audit kelistrikan (sumber daya, pin strapping, pull-up/down) wajib dilakukan sebelum fabrikasi.")

# K
fill(T[6], [
    ["1", "Ukur modul fisik (ESP32, LoRa, TP4056, boost) dan sesuaikan footprint/casing", "Verifikasi dimensi & pinout modul", "3 Jam"],
    ["2", "Pesan modul yang kurang, update BOM, lalu order PCB", "BOM final & PCB dipesan", "3 Jam"],
    ["3", "Uji rakit perfboard dan mulai firmware (deep sleep, GPS_EN/XKC_EN, deteksi jatuh); lanjut fitur dashboard", "Prototipe awal & firmware dasar", "6 Jam"],
])

# L: tanda tangan dikosongkan, tanggal
for i in ():
    for dr in P[i]._p.findall('.//' + qn('w:drawing')):
        dr.getparent().remove(dr)
st(P[71], "Tanggal: 3 Oktober 2026")
st(P[77], "Tanggal: 3 Oktober 2026")
d.save(OUT)
