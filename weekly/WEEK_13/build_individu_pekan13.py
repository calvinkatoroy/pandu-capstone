"""Laporan pekanan individu Pekan 13 (15-21 Nov 2026), template sama dengan laporan Pekan 7/10/11.

Sumber isi: LAPORAN KEMAJUAN Pekan 13 (kelompok), docs/PRE_ORDER_PCB.md, docs/PERTANYAAN_PABRIK_INDOMAKER.md,
log commit v3 (e808b2e ... 21c0e76), hasil Gerber percobaan 16 dan 21 Nov.
Jam kerja bertanda * adalah estimasi dari jejak sesi; sesuaikan dengan catatan pribadi.
17-20 Nov tidak punya jejak, dibiarkan "belum tercatat". Persentase capaian adalah estimasi.
"""
import copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = "../WEEK_7/LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 7.docx"
OUT = "LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 13.docx"
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
st(T[0].rows[6].cells[1].paragraphs[0], "13")
st(T[0].rows[7].cells[1].paragraphs[0], "15 - 21 November 2026")

# ---------------- B. target ----------------
fill(T[1], [
    ["1", "Menyesuaikan PCB1-PCB3 ke aturan Indomaker dan merute ulang hingga DRC 0",
     "DRC 0 dan 100 persen terhubung; PCB3 diperbesar menjadi 54,61 x 100,33 mm", SELESAI],
    ["2", "Memeriksa Gerber percobaan 16 Nov dan menyusun pertanyaan untuk pabrik",
     "Gerber diperiksa dengan skrip; 12 pertanyaan disusun (belum dikirim ke Indomaker)", SELESAI],
    ["3", "Menambah lubang baut M3 di tiap PCB dan ekspor ulang Gerber percobaan (21 Nov)",
     "4 lubang NPTH 3,2 mm per papan, DRC 0, terbaca di drill Gerber", SELESAI],
    ["4", "Jawaban Indomaker, data fisik modul, uji breadboard tahap 2, Gerber final",
     "Sebagian: ukuran modul cocok dengan kertas cetak 1:1 (pengecekan Calvin 21 Nov); jawaban pabrik, tact switch, MT3608, TP4056 kedua, dan Gerber final belum", BELUM],
])

P[5]._p.getparent().remove(P[5]._p)

# ---------------- C. logbook ----------------
fill(T[2], [
    ["Minggu (15 Nov)",
     "Menyesuaikan PCB1-PCB3 ke aturan Indomaker, rute ulang, DRC 0; PCB3 diperbesar",
     "5*", "EasyEDA PCB1-PCB3 (DRC 0); PRE_ORDER_PCB.md bagian 5a"],
    ["Senin (16 Nov)",
     "Ekspor dan periksa Gerber percobaan; susun 12 pertanyaan pabrik",
     "4*", "hardware/tools/gerber_*.py; PERTANYAAN_PABRIK_INDOMAKER.md"],
    ["Selasa - Jumat (17 - 20 Nov)",
     "Belum tercatat", "-", "-"],
    ["Sabtu (21 Nov)",
     "Audit desain; tambah 4 lubang baut M3 per papan, DRC 0; ekspor ulang Gerber; push ke v3",
     "5*", "Commit 21c0e76 (v3); gerber_render_pcb1-3.png"],
])
st(P[8], "Total Jam Kerja Minggu Ini: 14 Jam (estimasi; sesuaikan dengan catatan pribadi)")

# ---------------- D. realisasi ----------------
lst(12, 4, [
    "Menyesuaikan tiga desain PCB dengan batas Indomaker (jalur minimal 0,4 mm atau 16 mil, jarak aman 0,5 mm atau 20 mil, via 1,0 mm, lubang kaki komponen 1,1 mm, jalur daya 25 mil), merute ulang, lalu memeriksa DRC. Hasilnya PCB1 (241 jalur, 15 via, 107,95 x 95,25 mm), PCB2 (55 jalur, tanpa via, 31,623 x 99,06 mm), dan PCB3 (64 jalur, 3 via) semuanya DRC 0. PCB3 diperbesar menjadi 54,61 x 100,33 mm karena pada ukuran lama autoroute hanya menyelesaikan 53,85 persen jalur.",
    "Mengekspor Gerber percobaan 16 Nov dan memeriksanya dengan skrip Python: semua lapisan ada, tepi papan sesuai, lubang komponen hanya 1,1 mm dan via hanya 1,0 mm, jalur sinyal tidak lebih tipis dari 0,406 mm. Garis isi tembaga GND yang lebih tipis (sekitar 0,2 - 0,25 mm) tidak disembunyikan, tetapi dijadikan pertanyaan untuk pabrik bersama celah pad SOT-23, lubang NPTH 3,2 mm, dan panelisasi (total 12 pertanyaan). Gerber 14 Nov dinyatakan tidak berlaku.",
    "Menambah 4 lubang baut M3 (NPTH 3,2 mm, tanpa tembaga dan tanpa net) di sudut PCB1, PCB2, dan PCB3 sebagai dasar dudukan casing. Pada PCB1 lubang kanan-bawah digeser karena hanya 13,5 mil dari pad Ra-02 (batas 20 mil); lubang yang sempat mewarisi net GND dibersihkan agar DRC bersih. Setelah rebuild copper, DRC tetap 0 dan ukuran papan tidak berubah. Ekspor ulang 21 Nov memuat lubang NPTH 3,2 mm: PCB1 5 (4 baru + 1 lubang holder baterai), PCB2 4, PCB3 4; lubang 1,1 mm dan via tidak berubah (74/10/60 dan 15/0/3).",
    "Menyusun CLAUDE.md, daftar periksa pra-pesan PCB (PRE_ORDER_PCB.md, gerbang G1-G11), rencana kerja tiga agen paralel, dan riset ukuran komponen dari web; memperbarui dokumen setelah tiap perubahan dan mendorongnya ke branch v3.",
])
lst(17, 4, [
    "docs/PERTANYAAN_PABRIK_INDOMAKER.md (12 pertanyaan dan tabel verifikasi), docs/PRE_ORDER_PCB.md (aturan Indomaker, posisi lubang baut, keputusan kabel ekstensi USB DevKit Vest)",
    "hardware/tools/gerber_check.py, gerber_tracks.py, gerber_render.py dan docs/screenshots/gerber_render_pcb1-3.png (render dari Gerber 21 Nov)",
    "Salinan proyek EasyEDA 'Pandu-Capstone-v3-footprint-fix': PCB1-PCB3 DRC 0 dengan lubang baut; Gerber percobaan 16 dan 21 Nov (zip lokal, bukan Gerber final dan tidak ada di repository)",
    "Commit 21c0e76 di branch v3 (lubang baut M3 dan hasil Gerber percobaan 21 Nov)",
])

# ---------------- E. capaian teknis ----------------
fill(T[3], [
    ["Hardware", "Penyesuaian PCB1-PCB3 ke aturan Indomaker, lubang baut, dan pemeriksaan Gerber percobaan",
     "DRC 0 di tiga papan, PCB3 diperbesar, lubang baut M3 ditambah; footprint tact switch, MT3608, dan TP4056 kedua belum cocok atau belum dibeli; PCB belum dipesan", "85%"],
    ["Software", "Tidak ada target software pribadi pekan ini",
     "Tidak dikerjakan oleh Calvin pekan ini", "-"],
    ["Mekanik", "Menyediakan dasar untuk casing (lubang baut)",
     "Koordinat lubang baut dicatat di PRE_ORDER_PCB.md; casing baru dimodelkan setelah PCB dibekukan; USB DevKit Vest memakai kabel ekstensi", "50%"],
    ["Pengujian", "Pemeriksaan DRC dan Gerber percobaan",
     "DRC 0 di tiga papan; Gerber 16 dan 21 Nov diperiksa skrip (lubang, via, jalur, tepi); uji breadboard tahap 2 dan jawaban pabrik belum", "75%"],
    ["Dokumentasi", "Daftar periksa pra-pesan, pertanyaan pabrik, hasil Gerber, dan laporan",
     "PRE_ORDER_PCB, PERTANYAAN_PABRIK_INDOMAKER, render Gerber, dan laporan individu", "90%"],
])
st(P[24], (
    "Pekan ini pekerjaan Calvin berfokus pada kesiapan PCB untuk dipesan di Indomaker tanpa PCBA. "
    "Ketiga desain disesuaikan dengan batas pabrik (jalur 16 mil, jarak aman 20 mil, via 1,0 mm, lubang kaki 1,1 mm) dan lolos DRC 0; PCB3 harus diperbesar menjadi 54,61 x 100,33 mm supaya jalur bisa melewati celah pin ESP32 DevKit. "
    "Gerber percobaan 16 Nov dan 21 Nov diperiksa dengan skrip, dan 12 pertanyaan teknis disusun untuk pabrik. Empat lubang baut M3 ditambahkan di tiap papan untuk dasar casing. "
    "PCB belum bisa dipesan: pertanyaan ke Indomaker belum dikirim dan dijawab, footprint tact switch belum cocok dengan komponen yang dibeli, MT3608 dan TP4056 kedua belum ada, dan urutan pin beberapa modul belum dicek ke fisik."))

# ---------------- F. kendala ----------------
fill(T[4], [
    ["1", "Jarak aman 0,5 mm menghalangi jalur di antara pin ESP32 DevKit pada ukuran lama PCB3 (autoroute 53,85 persen)",
     "Jalur tidak lengkap dan DRC gagal", "Tinggi"],
    ["2", "Beberapa batas Indomaker belum dikonfirmasi tertulis: celah pad SOT-23, garis isi tembaga GND yang lebih tipis dari 0,4 mm, lubang NPTH 3,2 mm, panelisasi PCB2 dan PCB3",
     "Gerber final berisiko ditolak pabrik sehingga belum bisa dikirim", "Tinggi"],
    ["3", "Footprint tact switch di PCB1 dan PCB2 (SMD 3,9 x 3,0 mm, 2 pad) tidak sama dengan tact yang dibeli (sekitar 6 x 6 mm); MT3608 dan TP4056 kedua belum dibeli sehingga footprint tidak bisa dicocokkan",
     "Tombol dan modul daya berisiko tidak bisa dipasang pada PCB yang dipesan", "Tinggi"],
    ["4", "Ukuran lubang 1,1 mm diubah di PCB, bukan di library footprint",
     "Import Changes dari skematik bisa mengembalikan lubang ke ukuran lama", "Sedang"],
    ["5", "Lubang baut baru mewarisi net GND dan pada PCB1 terlalu dekat pad Ra-02 (13,5 mil)",
     "DRC memunculkan pelanggaran koneksi dan jarak aman", "Rendah"],
])
st(P[27], (
    "Jarak aman pabrik lebih besar daripada celah antar-pin modul sehingga ukuran PCB3 harus bertambah; ini ditemukan lewat percobaan rute, bukan dari perkiraan. "
    "Batas pabrik yang tidak tertulis jelas (pad SOT-23, garis isi tembaga, NPTH) tidak bisa dipastikan dari Gerber sendiri sehingga perlu jawaban Indomaker. "
    "Perubahan lubang dan footprint harus dicatat dan diperiksa ulang tiap kali Import Changes dijalankan agar tidak kembali ke nilai lama."))

# ---------------- G. tindakan korektif ----------------
fill(T[5], [
    ["Footprint tact switch",
     "Ukur kaki dan jarak tact, ganti footprint SW1/SW2 (PCB1) dan SW1 (PCB2), rute ulang, DRC",
     "Calvin", "28 November 2026"],
    ["Batas pabrik",
     "Kirim 12 pertanyaan ke Indomaker lewat WhatsApp dan catat jawabannya",
     "Calvin, Rafif", "28 November 2026"],
    ["Lubang 1,1 mm",
     "Cek ulang lubang, ekspor ulang netlist dan Gerber percobaan sebelum Gerber final",
     "Calvin", "28 November 2026"],
    ["Data fisik modul",
     "Cek urutan pin GPS, microSD, GY-521; beli MT3608 dan TP4056 kedua; uji breadboard",
     "Calvin, Gibran", "28 November 2026"],
])

# ---------------- H. dokumentasi (3 render Gerber) ----------------
IMG = "img/"
figs = [
    (IMG + "gerber_render_pcb1.png", 10.0, "Gambar 1. (21 Nov) Render PCB1 (Vest Node) dari Gerber percobaan 21 Nov: jalur, pad, outline, dan 4 lubang baut M3 di sudut (render dengan skrip sendiri, bukan tampilan pabrik)."),
    (IMG + "gerber_render_pcb2.png", 3.6, "Gambar 2. (21 Nov) Render PCB2 (Helmet Node) dari Gerber percobaan 21 Nov, dengan 4 lubang baut M3."),
    (IMG + "gerber_render_pcb3.png", 5.2, "Gambar 3. (21 Nov) Render PCB3 (Edge Gateway, 54,61 x 100,33 mm) dari Gerber percobaan 21 Nov, dengan 4 lubang baut M3."),
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
st(P[54], "Pembagian tugas pekan 13: Calvin menyesuaikan PCB ke aturan Indomaker, memeriksa Gerber, menyusun pertanyaan pabrik, dan menambah lubang baut; Rafif mengoordinasikan keputusan PCB tanpa PCBA; Gibran mengatur ulang tata letak PCB3 dan jalur microSD; Rifat menyinkronkan repository v3 dan pin firmware; Tri Yoga memeriksa dampak PCB3 pada casing.")
st(P[55], "Koordinasi BOM: tact switch yang dibeli perlu diukur, MT3608 dan TP4056 kedua belum dibeli; Tri Yoga perlu diberi tahu bahwa tata letak PCB3 berubah.")
st(P[56], "Koordinasi dengan dosen: permintaan pelebaran jalur dipenuhi (jalur sinyal 16 mil, jalur daya 25 mil, DRC 0); hasil dilaporkan di laporan kemajuan.")
st(P[58], "Berperan menyesuaikan PCB1-PCB3 ke aturan Indomaker dan merute ulang sampai DRC 0, memperbesar PCB3, mengekspor dan memeriksa Gerber percobaan dengan skrip, menyusun 12 pertanyaan untuk pabrik, menambah lubang baut M3 di tiga papan, serta memelihara CLAUDE.md, daftar periksa pra-pesan, dan dokumen terkait di repository.")

# ---------------- J. evaluasi diri ----------------
st(P[61], "Setiap perubahan desain langsung dibuktikan dengan DRC dan pemeriksaan Gerber, sehingga masalah (autoroute PCB3, lubang baut dekat pad Ra-02) ditemukan sebelum PCB dipesan.")
st(P[62], "Batas pabrik yang tidak jelas tidak diklaim aman: pertanyaan untuk Indomaker disusun lengkap beserta bukti dari Gerber percobaan.")
st(P[63], "Dokumen, hasil Gerber, dan keputusan (misalnya kabel ekstensi USB DevKit dan posisi lubang baut) terdokumentasi dan terdorong ke branch v3.")
st(P[65], "Pertanyaan ke Indomaker sudah disusun tetapi belum dikirim, jadi jawabannya masih menghambat Gerber final; ketidakcocokan footprint tact switch baru ditemukan di akhir pekan.")
st(P[66], "Pencatatan kegiatan harian 17 - 20 Nov tidak ada, dan data fisik modul (tact switch, MT3608, TP4056 kedua, urutan pin) masih belum lengkap.")
st(P[67], "Tidak ada kemajuan software pribadi pekan ini; kalibrasi MPU6050 dan penyesuaian firmware masih menjadi pekerjaan tim.")
st(P[69], "Cocokkan footprint ke komponen fisik yang benar-benar dibeli, termasuk tombol, sebelum menyatakan PCB siap pesan.")
st(P[70], "Tanyakan batas pabrik yang belum tertulis lebih awal.")
st(P[71], "Periksa ulang lubang dan footprint setelah Import Changes dan sebelum ekspor Gerber.")

# ---------------- K. rencana pekan berikutnya ----------------
fill(T[6], [
    ["1", "Ukur tact, ganti footprint SW1/SW2 (PCB1) dan SW1 (PCB2), DRC",
     "PCB1 dan PCB2 DRC 0 dengan footprint tact yang cocok", "3 Jam"],
    ["2", "Kirim 12 pertanyaan ke Indomaker, catat jawabannya",
     "Jawaban pabrik tercatat di docs/PERTANYAAN_PABRIK_INDOMAKER.md", "2 Jam"],
    ["3", "Cek pin GPS, microSD, GY-521; beli MT3608 dan TP4056; uji breadboard",
     "Data fisik modul lengkap dan terverifikasi", "6 Jam"],
    ["4", "Netlist dan Gerber final setelah persetujuan; data casing ke Tri Yoga",
     "Gerber final siap pesan dan data casing", "5 Jam"],
])

# ---------------- L. persetujuan ----------------
# Kedua tanda tangan (Calvin dan ketua Rafif) dipertahankan dari template, sesuai permintaan.
st(P[79], "Tanggal: 21 November 2026")
st(P[85], "Tanggal: 21 November 2026")
for i in (P[78], P[84]):  # kecilkan tanda tangan 70% agar halaman terakhir tidak tumpah
    for ex in i._p.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent', '{http://schemas.openxmlformats.org/drawingml/2006/main}ext'):
        ex.set('cx', str(int(int(ex.get('cx'))*.7))); ex.set('cy', str(int(int(ex.get('cy'))*.7)))
d.save(OUT)
print("OK", OUT)
