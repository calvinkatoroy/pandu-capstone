"""Laporan pekanan individu Pekan 11 (2-7 Nov 2026), template sama dengan laporan Pekan 7/10.

Sumber isi: docs/PROGRESS_PEKAN11.txt, docs/FOOTPRINT_SPEC_V3.md, sesi kerja 5 Nov (EasyEDA).
Jam kerja bertanda * adalah estimasi dari jejak sesi; sesuaikan dengan catatan pribadi.
Senin-Rabu tidak punya jejak, dibiarkan "belum tercatat". Persentase capaian adalah estimasi.
"""
import copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = "../WEEK_7/LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 7.docx"
OUT = "LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 11.docx"
d = docx.Document(SRC)
P = list(d.paragraphs)
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


BELUM = ["☑ Belum", "☐ Selesai"]   # termasuk "sebagian" (dijelaskan di kolom luaran)
SELESAI = ["☐ Belum", "☑ Selesai"]

# ---------------- A. identitas ----------------
st(T[0].rows[6].cells[1].paragraphs[0], "11")
st(T[0].rows[7].cells[1].paragraphs[0], "2 - 7 November 2026")

# ---------------- B. target ----------------
fill(T[1], [
    ["1", "Mencocokkan footprint desain PCB dengan modul yang benar-benar dibeli (ukuran fisik diukur langsung)",
     "docs/FOOTPRINT_SPEC_V3.md: Ra-02 (PCB1, PCB3) dan DevKit Vest (PCB1) tidak cocok, TP4056 (PCB2) cocok dalam toleransi 0,5 mm", SELESAI],
    ["2", "Memperbaiki PCB3 (Gateway): breakout Ra-02, MOSFET 2N7002, jalur 16 mil sesuai permintaan dosen",
     "Salinan EasyEDA: DRC 0, ratline 0, ukuran papan tetap. Skematik PCB3 belum disamakan", SELESAI],
    ["3", "Memperbaiki PCB1 (Vest): breakout Ra-02 dan footprint DevKit V1 30 pin, rute ulang jalur 16 mil",
     "Salinan EasyEDA: DRC tanpa masalah, ratline 0, 27 net, skematik disamakan (Gambar 1-3)", SELESAI],
    ["4", "Verifikasi akhir sebelum pemesanan PCB (D/S Q1, cetak 1:1, adopsi ke proyek tim, Gerber)",
     "Sebagian: footprint dan DRC selesai; D/S Q1, cetak 1:1, dan adopsi ke proyek tim belum", BELUM],
    ["5", "Perbaikan firmware hasil audit (K1-K4), kalibrasi MPU6050, timeout upload",
     "Belum dikerjakan; kemajuan software pekan ini sekitar 10 persen", BELUM],
])

# ---------------- C. logbook ----------------
fill(T[2], [
    ["Senin - Rabu (2 - 4 Nov)",
     "Belum tercatat (isi manual bila ada kegiatan, mis. integrasi baterai)", "-", "-"],
    ["Kamis (5 Nov)",
     "Audit footprint terhadap modul fisik dan pengukuran ukuran modul (Ra-02 breakout, DevKit V1, TP4056); perbaikan PCB3 dan PCB1 di salinan EasyEDA (footprint Ra-02 breakout, 2N7002, DevKit V1 30 pin dari sumber terbuka, rute ulang jalur 16 mil, DRC 0); penyamaan skematik PCB1; riset perbandingan EasyEDA dan KiCad",
     "8*", "docs/FOOTPRINT_SPEC_V3.md, hardware/footprints/ (make_ra02.py, make_devkit_zip_j2j3.py), screenshot EasyEDA (Gambar 1-3)"],
    ["Jumat - Sabtu (6 - 7 Nov)",
     "Penyusunan draft progres minggu ke-11 dan laporan individu",
     "2*", "docs/PROGRESS_PEKAN11.txt, laporan individu Pekan 11"],
])
st(P[8], "Total Jam Kerja Minggu Ini: 10 Jam (estimasi; sesuaikan dengan catatan pribadi)")

# ---------------- D. realisasi ----------------
lst(12, 4, [
    "Mengaudit footprint desain terhadap modul yang dibeli: mengukur modul fisik (Ra-02 breakout dengan jarak antar deret 26 mm dan pitch 2,54 mm; DevKit V1 dengan jarak antar deret 25,4 mm; TP4056 Type-C 28,5 x 17 mm), lalu membandingkan dengan footprint di EasyEDA. Hasilnya, Ra-02 di PCB1 dan PCB3 serta DevKit Vest di PCB1 tidak cocok dengan modul; footprint TP4056 di PCB2 cocok dalam toleransi sekitar 0,5 mm; DevKit Gateway di PCB3 jumlah pinnya cocok.",
    "Memperbaiki PCB3 pada salinan proyek EasyEDA (proyek tim tidak disentuh): mengganti Ra-02 menjadi footprint breakout, MOSFET Q1 menjadi 2N7002 sesuai BOM, menghapus header antena, memakai jalur 16 mil sesuai permintaan dosen, lalu rute ulang dan Rebuild Copper; hasil DRC 0 dan semua net terhubung dengan ukuran papan tetap.",
    "Memperbaiki PCB1: memasang footprint Ra-02 breakout dan footprint DevKit V1 30 pin dari repository sumber terbuka. Karena EasyEDA tidak mengizinkan nomor pad bertanda hubung lewat antarmuka, pad dinamai sama dengan pin simbol lewat file impor KiCad sehingga skematik tidak perlu diubah. Skematik disamakan (footprint U6, header H1 dihapus, label LORA_ANT menjadi GND), jalur dirute ulang 16 mil, DRC tanpa masalah dan ratline 0.",
    "Menyusun spesifikasi footprint dan pemetaan pin (FOOTPRINT_SPEC_V3.md), skrip pembuat footprint (make_ra02.py, make_devkit_zip_j2j3.py), riset perbandingan EasyEDA Pro dan KiCad, draft progres minggu ke-11, dan laporan ini.",
])
lst(17, 4, [
    "docs/FOOTPRINT_SPEC_V3.md (temuan, spesifikasi modul, pemetaan pad DevKit V1)",
    "hardware/footprints/: make_ra02.py, make_devkit_zip.py, make_devkit_zip_j2j3.py, ESP32_DevKitV1_30P_J2J3_import.zip",
    "Salinan proyek EasyEDA 'Pandu-Capstone-v3-footprint-fix': PCB1 dan PCB3 DRC bersih (Gambar 1-3)",
    "docs/PROGRESS_PEKAN11.txt dan laporan individu Pekan 11",
])

# ---------------- E. capaian teknis ----------------
fill(T[3], [
    ["Hardware", "Pencocokan footprint PCB dengan modul yang dibeli dan perbaikan PCB1 serta PCB3",
     "Footprint Ra-02 dan DevKit V1 diperbaiki, PCB1 dan PCB3 DRC bersih di salinan; D/S Q1, cetak 1:1, dan adopsi ke proyek tim belum; PCB belum dipesan", "80%"],
    ["Software", "Tidak ada target software besar pekan ini",
     "Kemajuan sekitar 10 persen; perbaikan K1-K4, kalibrasi MPU6050, dan timeout upload belum dikerjakan; project Supabase bersama belum ada", "80%"],
    ["Mekanik", "Tidak ada target mekanik pekan ini",
     "Tidak dikerjakan; ukuran modul yang diukur menjadi dasar kecocokan footprint dan casing", "-"],
    ["Pengujian", "Status uji lapangan dan uji fisik modul",
     "GPS sudah diuji di luar ruangan dan deteksi jatuh terbukti berfungsi (nilai diam g=4,8 belum dikalibrasi); microSD belum diuji karena kartu belum dimasukkan; uji basah sensor air serta SOS dan man-overboard dari hardware ke dashboard belum", "70%"],
    ["Dokumentasi", "Spesifikasi footprint, skrip pembuat footprint, progres, dan laporan",
     "FOOTPRINT_SPEC_V3, skrip footprint, progres minggu ke-11, dan laporan individu", "90%"],
])
st(P[24], (
    "Pekan ini pekerjaan Calvin berfokus pada pencocokan desain PCB dengan modul yang benar-benar dibeli. "
    "Audit footprint terhadap ukuran modul fisik menemukan bahwa Ra-02 (PCB1 dan PCB3) dan DevKit Vest (PCB1) tidak cocok dengan modul, padahal dokumen lama menyebut sudah diganti. "
    "Footprint diperbaiki pada salinan proyek EasyEDA: Ra-02 menjadi breakout 2,54 mm, DevKit menjadi V1 30 pin, MOSFET menjadi 2N7002, jalur 16 mil sesuai permintaan dosen; PCB1 dan PCB3 lolos DRC dengan semua net terhubung dan ukuran papan tetap. "
    "Proyek tim belum diubah; adopsi perubahan, verifikasi D/S Q1, dan cetak 1:1 masih menunggu sebelum PCB dipesan. "
    "Di sisi pengujian, GPS sudah diuji di luar ruangan dan deteksi jatuh terbukti, sedangkan nilai diam akselerometer masih perlu dikalibrasi; kemajuan software pekan ini sekitar 10 persen."))

# ---------------- F. kendala ----------------
fill(T[4], [
    ["1", "Footprint di desain tidak sesuai modul yang dibeli (Ra-02 telanjang vs breakout; DevKitC 38 pin vs DevKit V1 30 pin), sedangkan dokumen lama menyebut sudah diganti",
     "PCB yang dipesan tidak akan bisa dipasangi modul yang sudah dibeli", "Tinggi"],
    ["2", "Library EasyEDA tidak punya DevKit V1 30 pin maupun breakout Ra-02, dan nomor pad bertanda hubung tidak bisa diketik lewat antarmuka",
     "Footprint harus dibuat atau diimpor dari sumber terbuka; penomoran manual 30 pad gagal berulang", "Sedang"],
    ["3", "Impor perubahan dari skematik ke PCB berusaha mengembalikan footprint lama dan menambah header antena",
     "Perbaikan PCB bisa tertimpa kembali bila diterapkan tanpa memeriksa daftar perubahan", "Sedang"],
    ["4", "Antarmuka EasyEDA di browser tidak stabil untuk edit massal (klik canvas bergeser, screenshot timeout)",
     "Proses lebih lambat dan berisiko salah objek", "Sedang"],
    ["5", "Skematik PCB3 belum disamakan dengan PCB-nya dan D/S pin Q1 belum diverifikasi",
     "PCB3 belum siap dipesan", "Sedang"],
])
st(P[27], (
    "Akar masalah footprint adalah dokumen yang menyebut pekerjaan selesai tanpa membandingkan dengan modul fisik; setelah ukuran modul diukur, ketidakcocokan terlihat jelas. "
    "Kendala alat muncul karena library EasyEDA tidak memuat modul yang dibeli, sehingga footprint harus diimpor sebagai file; pendekatan lewat file terbukti lebih andal daripada mengedit pad satu per satu di antarmuka. "
    "Impor perubahan dari skematik harus diperiksa baris demi baris agar perbaikan di PCB tidak tertimpa."))

# ---------------- G. tindakan korektif ----------------
fill(T[5], [
    ["Footprint tidak sesuai modul",
     "Audit terhadap ukuran fisik dan perbaikan di salinan EasyEDA (selesai untuk PCB1 dan PCB3); cetak 1:1 untuk memastikan sebelum pesan",
     "Calvin, Gibran, Rafif", "14 November 2026"],
    ["Skematik PCB3 belum sama dengan PCB, D/S Q1",
     "Menyamakan footprint U1 dan header H2 di skematik PCB3 dan memeriksa pin D/S Q1 terhadap datasheet 2N7002",
     "Calvin", "10 November 2026"],
    ["Adopsi perbaikan ke proyek tim",
     "Menentukan cara memindahkan salinan ke proyek tim agar tidak menimpa pekerjaan anggota lain, lalu ekspor Gerber",
     "Calvin, Gibran", "14 November 2026"],
    ["Nilai diam akselerometer g=4,8 dan temuan kritis audit (K1-K4)",
     "Kalibrasi MPU6050 (WHO_AM_I, range, 1 g), CRC dan sync word LoRa, alarm tidak ditolak server, timeout upload 15-20 detik",
     "Calvin, Gibran", "14 November 2026"],
    ["Uji yang belum selesai",
     "Uji basah sensor air, uji microSD setelah kartu dimasukkan, SOS dan man-overboard dari hardware ke dashboard; project Supabase bersama",
     "Calvin, Rifat", "14 November 2026"],
])

# ---------------- H. dokumentasi (3 gambar EasyEDA) ----------------
IMG = "img/"
figs = [
    (IMG + "footprint_devkit_pad.jpg", 12.0, "Gambar 1. (5 Nov) Footprint DevKit V1 30 pin di Footprint Manager EasyEDA: pad bernama sama dengan pin simbol U3 (J2-19, J2-14, ...), ukuran pad 1,9 x 1,524 mm."),
    (IMG + "pcb1_routed.jpg", 12.0, "Gambar 2. (5 Nov) PCB1 (Vest Node) setelah footprint DevKit V1 dan Ra-02 breakout dipasang dan jalur 16 mil dirute ulang; Ratlines 0, Nets 27."),
    (IMG + "pcb1_drc_bersih.jpg", 12.0, "Gambar 3. (5 Nov) Hasil DRC PCB1: 'DRC Check Complete - No issues found' (124 item diperiksa), ratline 0."),
]
pairs = [(P[41], P[42]), (P[43], P[44]), (P[45], P[46]), (P[47], P[48]), (P[49], P[50])]
for pp, cp in pairs[len(figs):]:
    pp._p.getparent().remove(pp._p)
    cp._p.getparent().remove(cp._p)
for (pp, cp), (path, w, cap) in zip(pairs, figs):
    for dr in pp._p.findall('.//' + qn('w:drawing')):
        dr.getparent().remove(dr)
    run = pp.runs[0] if pp.runs else pp.add_run()
    run.add_picture(path, width=Cm(w))
    st(cp, cap)

# ---------------- I. kontribusi ----------------
st(P[54], "Pembagian tugas pekan 11: Calvin mengaudit footprint terhadap modul fisik dan memperbaiki PCB1 serta PCB3 di EasyEDA; Rafif memimpin uji GPS di luar ruangan dan verifikasi deteksi jatuh di breadboard; Gibran menguji ketahanan sensor MPU6050, mengidentifikasi g=4,8 saat diam, dan mengecek jalur SPI microSD; Rifat mengevaluasi status software dan menyesuaikan layout pin PCB; Tri Yoga memeriksa desain blueprint 2D dan model 3D casing (55 x 65 x 23 mm).")
st(P[55], "Koordinasi BOM dan pengadaan: ukuran modul yang diukur (Ra-02 breakout, DevKit V1, TP4056) menjadi acuan; TP4056 kedua dan boost MT3608 untuk daya baterai Vest masih perlu dipastikan sebelum pemesanan PCB.")
st(P[56], "Koordinasi dengan dosen: permintaan pelebaran jalur tembaga dipenuhi dengan jalur 16 mil pada PCB1 dan PCB3 di salinan EasyEDA; hasil DRC bersih dapat dilaporkan setelah adopsi ke proyek tim.")
st(P[58], "Berperan mengaudit footprint desain terhadap modul fisik, mengukur modul, memperbaiki PCB3 dan PCB1 pada salinan EasyEDA (Ra-02 breakout, DevKit V1 30 pin, 2N7002, rute ulang jalur 16 mil, DRC), menyamakan skematik PCB1, menyusun spesifikasi footprint dan skrip pembuat footprint, meriset perbandingan EasyEDA dan KiCad, serta menyusun draft progres dan laporan pekan ini.")

# ---------------- J. evaluasi diri ----------------
st(P[61], "Ketidakcocokan footprint ditemukan sebelum PCB dipesan karena desain dibandingkan dengan ukuran modul fisik, sehingga biaya dan waktu pemesanan ulang terhindar.")
st(P[62], "Masalah nomor pad bertanda hubung diselesaikan dengan pendekatan lain (file impor) setelah beberapa percobaan manual gagal, dan hasilnya diverifikasi lewat DRC, ratline, dan pencocokan skematik.")
st(P[63], "Semua perubahan dikerjakan di salinan proyek sehingga proyek tim tidak rusak, dan temuan, pemetaan pin, serta langkahnya didokumentasikan.")
st(P[65], "Dokumen lama menyatakan footprint sudah diganti tanpa verifikasi terhadap modul fisik; setiap klaim 'selesai' perlu bukti ukuran atau cetak 1:1.")
st(P[66], "Pencatatan kegiatan harian (Senin sampai Rabu) tidak ada, dan uji fisik (D/S Q1, cetak 1:1, uji basah, SOS dan MOB) masih tertunda.")
st(P[67], "Perbaikan firmware hasil audit (K1-K4), kalibrasi MPU6050, dan project Supabase bersama belum dikerjakan; kemajuan software pekan ini sekitar 10 persen.")
st(P[69], "Ukur modul fisik sebelum menggambar footprint, dan jangan percaya klaim 'sudah diganti' di dokumen tanpa memeriksa desain yang sebenarnya.")
st(P[70], "Untuk modul yang tidak ada di library, membuat footprint sebagai file teks lalu mengimpornya lebih andal daripada mengedit pad lewat antarmuka.")
st(P[71], "Setiap impor perubahan dari skematik ke PCB perlu diperiksa daftar perubahannya agar perbaikan tidak tertimpa.")

# ---------------- K. rencana pekan berikutnya ----------------
fill(T[6], [
    ["1", "Samakan skematik PCB3 dengan PCB-nya, verifikasi D/S Q1, DRC ulang PCB1-PCB3",
     "PCB1-PCB3 konsisten dan DRC bersih", "4 Jam"],
    ["2", "Cetak 1:1 dan cocokkan Ra-02, DevKit V1, dan TP4056 dengan modul fisik; adopsi ke proyek tim, ekspor Gerber",
     "File Gerber siap pesan", "6 Jam"],
    ["3", "Firmware: kalibrasi nilai diam MPU6050, perbaikan K1-K4 hasil audit, naikkan timeout upload",
     "Firmware terbarui dan hasil uji", "8 Jam"],
    ["4", "Uji basah sensor air, uji microSD setelah kartu dimasukkan, SOS dan man-overboard; project Supabase bersama bersama Rifat",
     "Hasil uji lapangan dan backend bersama", "6 Jam"],
])

# ---------------- L. persetujuan ----------------
# Kedua tanda tangan (Calvin dan ketua Rafif) dipertahankan dari template, sesuai permintaan.
st(P[79], "Tanggal: 7 November 2026")
st(P[85], "Tanggal: 7 November 2026")
for i in (P[78], P[84]):  # kecilkan tanda tangan 70% agar halaman terakhir tidak tumpah
    for ex in i._p.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent', '{http://schemas.openxmlformats.org/drawingml/2006/main}ext'):
        ex.set('cx', str(int(int(ex.get('cx'))*.7))); ex.set('cy', str(int(int(ex.get('cy'))*.7)))
d.save(OUT)
print("OK", OUT)
