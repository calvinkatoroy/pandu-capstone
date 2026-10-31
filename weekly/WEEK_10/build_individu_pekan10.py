"""Laporan pekanan individu Pekan 10 (26-31 Okt 2026), template sama dengan laporan Pekan 7.

Sumber isi: docs/REKAP_RABU_28_OKT_2026.md, docs/AUDIT_V3.md, docs/PROGRESS_PEKAN10.txt, git log.
Jam kerja bertanda * adalah estimasi dari jejak file dan sesi; sesuaikan dengan catatan pribadi.
"""
import copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = "../WEEK_7/LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 7.docx"
OUT = "LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 10.docx"
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
st(T[0].rows[6].cells[1].paragraphs[0], "10")
st(T[0].rows[7].cells[1].paragraphs[0], "26 - 31 Oktober 2026")

# ---------------- B. target ----------------
fill(T[1], [
    ["1", "Konfirmasi komponen yang sudah dibeli terhadap BOM dan ukuran modul, serta keputusan baterai dan komponen pendukung",
     "Daftar ukuran modul, keputusan desain (baterai 18650, tanpa saklar geser, 2N7002), daftar beli MOSFET/dioda/resistor (BOM_V2 bagian 7-8)", SELESAI],
    ["2", "Integrasi Vest Node, Helmet Node, dan Edge Gateway di breadboard serta uji tautan LoRa Vest ke Gateway",
     "Log serial tiga node, paket asli Vest diterima Gateway (RSSI -84 sampai -92 dBm)", SELESAI],
    ["3", "Integrasi Gateway ke backend dan dashboard",
     "Event diterima endpoint ingest (accepted), dashboard menampilkan Vest 01 secara real-time, simulasi SOS menjadi BAHAYA", SELESAI],
    ["4", "Audit menyeluruh firmware, backend, dashboard, dan PCB",
     "docs/AUDIT_V3.md (4 kritis, 7 tinggi, 8 sedang, 3 proses)", SELESAI],
    ["5", "Revisi PCB: pelebaran jalur tembaga sesuai permintaan dosen",
     "Sebagian: uji pelebaran massal menimbulkan 188 pelanggaran DRC dan dibatalkan (PCB1 kembali DRC bersih); rute ulang dan revisi PCB2/PCB3 belum selesai", BELUM],
])

# ---------------- C. logbook ----------------
fill(T[2], [
    ["Senin - Selasa (26 - 27 Okt)",
     "Belum tercatat (isi manual bila ada kegiatan)", "-", "-"],
    ["Rabu (28 Okt)",
     "Konfirmasi daftar belanja dan ukuran modul terhadap BOM, riset live (TP4056, MT3608, XKC-Y25, baterai 18650 vs LiPo); cek PCB1 di EasyEDA lewat browser control dan uji pelebaran jalur (188 pelanggaran DRC, dibatalkan); daftar MOSFET/dioda/resistor; panduan rakit dan uji tiga node; troubleshooting Vest (error I2C, g=4,8) dan Gateway (WiFi 2,4 GHz, pin IO35); uji tautan LoRa; Supabase lokal di Docker, migrasi 0006, dukungan http:// pada Gateway; uji ujung ke ujung dan dashboard; audit menyeluruh",
     "7*", "BOM_V2.md, AUDIT_V3.md, log serial, 0006_fix_signup_trigger.sql, screenshot dashboard (Gambar 1-3)"],
    ["Kamis - Sabtu (29 - 31 Okt)",
     "Rekap kegiatan pekan, draft progres minggu ke-10, commit dan push dua repository, pembaruan Laporan Kemajuan Pekan 10 (Google Docs), penyusunan laporan individu",
     "3*", "docs/REKAP_RABU_28_OKT_2026.md, docs/PROGRESS_PEKAN10.txt, commit ea2e4ae (branch v3), branch redesign-peta-melayang"],
])
st(P[8], "Total Jam Kerja Minggu Ini: 10 Jam (estimasi; sesuaikan dengan catatan pribadi)")

# ---------------- D. realisasi ----------------
lst(12, 4, [
    "Mengonfirmasi komponen yang dibeli terhadap BOM beserta ukuran modul (SuperMini, DevKit V1, Ra-02, GPS NEO-6M, GY-521, TP4056, microSD, MT3608, holder 18650); memutuskan baterai Helmet dan Vest sama-sama 18650 1200 mAh (tanpa LiPo), saklar geser diganti jumper, buzzer sebagai sirine, MOSFET IRLZ44N diganti 2N7002, R1 PCB1 dihapus dan R8/R9 ditambahkan untuk pembagi sensor XKC-Y25-V; menyusun daftar beli MOSFET, dioda, dan resistor untuk versi breadboard dan versi PCB.",
    "Memeriksa PCB1 di EasyEDA Pro lewat browser control (jalur 10 mil, clearance 0,2 mm, DRC bersih 124 item) dan menguji pelebaran jalur permintaan dosen: pelebaran massal ke 16 mil dan 25 mil menimbulkan 188 pelanggaran DRC sehingga dibatalkan dan desain dikembalikan ke kondisi bersih; kesimpulannya perlu rute ulang atau board lebih besar.",
    "Membantu troubleshooting hardware dan firmware pada rangkaian breadboard: error I2C MPU6050 (masalah kontak), WiFi Gateway (jaringan hanya 5 GHz, lalu band 2,4 GHz diaktifkan), pin baterai IO35 yang mengambang (dipasang pembagi tegangan demo), dan konflik port COM; tautan LoRa Vest ke Gateway terbukti dengan paket asli (RSSI -84 sampai -92 dBm, SNR sekitar 9,8 dB).",
    "Menyiapkan backend lokal (Supabase di Docker, port dipindah ke 563xx karena bentrok port yang dicadangkan Windows), menerapkan migrasi 0001-0006 (0006 memperbaiki bug pendaftaran akun), menambah dukungan http:// pada firmware Gateway untuk uji LAN, lalu membuktikan alur Vest, LoRa, Gateway, WiFi, ingest, database, dan dashboard; simulasi SOS mengubah status dashboard menjadi BAHAYA secara real-time.",
    "Menyusun audit menyeluruh (AUDIT_V3.md: 4 temuan kritis, 7 tinggi, 8 sedang, 3 proses) dengan akar masalah dan bukti, merekap kegiatan pekan, menyusun draft progres minggu ke-10, serta commit dan push seluruh perubahan ke dua repository.",
])
lst(17, 4, [
    "docs/BOM_V2.md (bagian 7 ukuran komponen dan bagian 8 daftar beli) dan keputusan desain pekan ini",
    "docs/AUDIT_V3.md, docs/REKAP_RABU_28_OKT_2026.md, docs/PROGRESS_PEKAN10.txt",
    "supabase/migrations/0006_fix_signup_trigger.sql, supabase/config.toml (pandu-dashboard), dan firmware/gateway/src/main.cpp (dukungan http://)",
    "Commit ea2e4ae (pandu-capstone, branch v3) dan branch redesign-peta-melayang (pandu-dashboard) di GitHub; Laporan Kemajuan Pekan 10 (Google Docs) diperbarui",
])

# ---------------- E. capaian teknis ----------------
fill(T[3], [
    ["Hardware", "Integrasi tiga node di breadboard dan revisi PCB (pelebaran jalur)",
     "Tiga node terintegrasi di breadboard dengan daya USB dan tautan LoRa terbukti; revisi PCB berjalan (pelebaran massal dibatalkan, perlu rute ulang); baterai belum diintegrasikan", "70%"],
    ["Software", "Integrasi Gateway ke backend dan dashboard",
     "Alur Gateway, ingest, database, dan dashboard berjalan dengan Supabase lokal; project Supabase bersama belum ada; temuan kritis audit (K1-K4) belum diperbaiki", "75%"],
    ["Mekanik", "Tidak ada target mekanik pekan ini",
     "Tidak dikerjakan; tinggi casing 2,1 cm dicatat mengikuti baterai", "-"],
    ["Pengujian", "Uji integrasi dan tautan LoRa",
     "Vest ke Gateway ke dashboard lulus uji; g=4,8 saat diam, SD Gateway (sd:0), uji basah XKC, GPS luar ruangan, serta SOS dan jatuh dari hardware ke dashboard belum", "60%"],
    ["Dokumentasi", "BOM, audit, rekap, dan progres pekan",
     "BOM_V2 bagian 7-8, AUDIT_V3, rekap pekan, progres minggu ke-10, dan laporan individu", "90%"],
])
st(P[24], (
    "Pekan ini pekerjaan Calvin berfokus pada integrasi dan pembuktian. Seluruh komponen utama sudah sesuai BOM dan tiga node dirangkai di breadboard. "
    "Alur utama Vest Node, LoRa 433 MHz, Edge Gateway, WiFi, Supabase, hingga dashboard terbukti berjalan dengan hardware asli (RSSI -84 sampai -92 dBm), dan simulasi SOS mengubah dashboard menjadi BAHAYA secara real-time. "
    "Pengujian masih memakai daya USB; integrasi baterai dijadwalkan Senin agar rangkaian compact, dan PCB dipesan setelah penggunaan baterai terbukti. "
    "Revisi PCB sedang berjalan karena dosen meminta jalur dilebarkan; pelebaran massal menimbulkan 188 pelanggaran DRC sehingga dibatalkan dan perlu rute ulang. "
    "Audit menyeluruh menghasilkan daftar perbaikan prioritas (alarm yang bisa ditolak server, LoRa tanpa CRC, deteksi jatuh gagal diam-diam, kalibrasi MPU6050, SD Gateway). "
    "Pembagian tugas: Gibran dan Rafif troubleshooting hardware, Calvin membantu hardware dan troubleshooting firmware, Rifat troubleshooting dashboard."))

# ---------------- F. kendala ----------------
fill(T[4], [
    ["1", "Error I2C berulang pada MPU6050 di breadboard (masalah kontak kabel)",
     "Pembacaan akselerometer tidak stabil, uji fitur jatuh tertunda", "Sedang"],
    ["2", "WiFi 'kalpinoo' hanya 5 GHz sehingga ESP32 Gateway tidak dapat tersambung",
     "Gateway tidak bisa mengunggah data ke backend sampai band 2,4 GHz diaktifkan", "Sedang"],
    ["3", "Pin baterai IO35 mengambang membuat bat_mv acak dan event ditolak server; server menolak seluruh event termasuk alarm, dan Gateway membuang event yang ditolak",
     "Alarm SOS/jatuh berisiko hilang bila baterai hampir habis atau pembagi lepas", "Tinggi"],
    ["4", "Project Supabase lama tidak dapat dijangkau (NXDOMAIN) dan port Supabase lokal bentrok dengan port yang dicadangkan Windows",
     "Backend uji harus dibuat ulang secara lokal; tim belum punya backend bersama", "Sedang"],
    ["5", "Pelebaran jalur PCB1 secara massal menimbulkan 188 pelanggaran clearance",
     "Permintaan dosen belum terpenuhi; PCB belum bisa dipesan", "Tinggi"],
    ["6", "Akselerometer terbaca g=4,8 saat diam dan microSD Gateway tidak terbaca (sd:0)",
     "Deteksi jatuh dan antrean offline Gateway belum dapat diandalkan", "Sedang"],
])
st(P[27], (
    "Sebagian besar kendala muncul karena pengujian pertama dilakukan di breadboard tanpa kalibrasi: kontak kabel yang longgar, pin ADC yang mengambang, dan jaringan WiFi yang tidak kompatibel dengan ESP32. "
    "Audit menunjukkan akar masalah yang lebih dalam pada validasi server dan penanganan event yang ditolak, serta firmware sensor yang tidak memeriksa kesehatan MPU6050. "
    "Pelebaran jalur gagal karena board PCB1 sudah rapat; jalur tidak bisa dilebarkan tanpa rute ulang atau memperbesar board."))

# ---------------- G. tindakan korektif ----------------
fill(T[5], [
    ["Error I2C MPU6050 dan WiFi hanya 5 GHz",
     "Memperbaiki kontak kabel breadboard dan mengaktifkan band 2,4 GHz pada router (selesai 28 Okt)",
     "Calvin, Gibran, Rafif", "28 Oktober 2026 (selesai)"],
    ["bat_mv acak dan alarm bisa ditolak server (K1)",
     "Pembagi tegangan demo pada IO35 (selesai); server mengubah nilai non-kritis di luar rentang menjadi null dan Gateway tidak membuang alarm yang ditolak (belum)",
     "Calvin, Rifat", "7 November 2026"],
    ["Backend belum bersama",
     "Membuat atau mengonfirmasi project Supabase bersama dan menerapkan migrasi 0001-0006, fungsi ingest, dan secret",
     "Rifat, Calvin", "7 November 2026"],
    ["Pelebaran jalur PCB (permintaan dosen)",
     "Rute ulang atau memperbesar board; melebarkan jalur daya bertahap per net sambil memeriksa DRC; memeriksa skematik PCB2 dan PCB3 terhadap netlist; pesan PCB setelah uji baterai",
     "Calvin, Gibran, Rafif", "7 November 2026"],
    ["g=4,8, SD Gateway, dan keamanan LoRa",
     "Kalibrasi MPU6050 (WHO_AM_I, range, 1 g), memeriksa wiring dan kartu SD Gateway, mengaktifkan CRC dan sync word LoRa, menaikkan timeout upload ke 15-20 detik",
     "Calvin, Gibran", "7 November 2026"],
])

# ---------------- H. dokumentasi (3 gambar dashboard) ----------------
IMG = "img/"
figs = [
    (IMG + "dash_peta_aman.jpg", 11.0, "Gambar 1. (28 Okt) Dashboard PANDU (halaman Peta) menampilkan Vest 01 berstatus AMAN dengan baterai 69% dan RSSI -60 dBm, GW1 online, dari data asli Vest Node lewat LoRa dan Gateway ke Supabase lokal."),
    (IMG + "dash_peta_warning.jpg", 9.5, "Gambar 2. (28 Okt) Dashboard setelah baterai demo turun: Vest 01 berstatus WARNING (baterai rendah) dan posisi belum tersedia (NOFIX), RSSI -88 dBm."),
    (IMG + "dash_log.jpg", 11.0, "Gambar 3. (28 Okt) Halaman Log: event HB dari Vest 1 (stage Aman dan Warning) dan satu event SOS (stage Bahaya) dari simulasi uji, beserta baterai, status helm, dan RSSI."),
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
st(P[54], "Pembagian tugas pekan 10: Gibran dan Rafif troubleshooting rangkaian hardware secara langsung, Calvin membantu mereka dan troubleshooting firmware, Rifat troubleshooting dashboard. Target Senin: integrasi dengan baterai agar compact; PCB dipesan setelah baterai terbukti.")
st(P[55], "Koordinasi BOM dan pengadaan: konfirmasi daftar belanja terhadap BOM dan ukuran modul; modul pengisi daya (TP4056) kedua dan boost MT3608 untuk daya baterai Vest, serta MOSFET, dioda, dan resistor versi PCB, perlu dipastikan sebelum pemesanan PCB.")
st(P[56], "Koordinasi dengan dosen: dosen meminta jalur tembaga PCB dilebarkan; revisi sedang dikerjakan.")
st(P[58], "Berperan mengonfirmasi komponen terhadap BOM dan memutuskan baterai serta komponen pendukung, memeriksa dan menguji pelebaran jalur PCB1 di EasyEDA, membantu troubleshooting hardware dan firmware (I2C MPU6050, WiFi Gateway, pin baterai IO35, tautan LoRa), menyiapkan backend Supabase lokal dan memperbaiki bug pendaftaran akun, menambah dukungan http:// pada firmware Gateway, membuktikan alur Vest ke dashboard, menyusun audit menyeluruh, rekap, dan draft progres, serta commit dan push perubahan ke dua repository.")

# ---------------- J. evaluasi diri ----------------
st(P[61], "Alur ujung ke ujung terbukti dengan hardware asli (Vest, LoRa, Gateway, Supabase, dashboard) dalam satu pekan, dan hasil uji dicatat dengan bukti log dan screenshot.")
st(P[62], "Audit menyeluruh menemukan akar masalah yang tidak terlihat dari uji biasa (alarm ditolak server dan dibuang Gateway, LoRa tanpa CRC, deteksi jatuh gagal diam-diam), sehingga bisa diperbaiki sebelum PCB dipesan.")
st(P[63], "Percobaan pelebaran jalur dibatalkan dengan cepat setelah DRC menunjukkan pelanggaran, sehingga desain PCB1 tetap bersih dan semua perubahan pekan ini ter-commit dan ter-push.")
st(P[65], "Perubahan massal pada PCB (pelebaran semua jalur) dilakukan tanpa menghitung ruang yang tersedia; perlu rencana per net dan cek DRC bertahap.")
st(P[66], "Pencatatan jam kerja dan kegiatan harian belum rutin (hanya Rabu dan akhir pekan yang tercatat); uji SOS, jatuh, dan MOB dari hardware belum dilakukan penuh.")
st(P[67], "Perbaikan temuan kritis audit (K1-K4), kalibrasi MPU6050, dan SD Gateway belum dikerjakan; project Supabase bersama belum dibuat.")
st(P[69], "Pin ADC yang mengambang dan jaringan WiFi 5 GHz adalah penyebab umum kegagalan uji di breadboard; periksa keduanya lebih awal.")
st(P[70], "Validasi di server harus menolak data yang salah tanpa membuang alarm; event keselamatan tidak boleh hilang diam-diam.")
st(P[71], "Satu backend bersama dan commit yang rutin mencegah pekerjaan hanya ada di satu laptop.")

# ---------------- K. rencana pekan berikutnya ----------------
fill(T[6], [
    ["1", "Integrasi baterai Vest dan Helmet (18650, TP4056, boost) agar compact; uji daya dan pengisian; pesan PCB setelah penggunaan baterai terbukti",
     "Prototipe berbaterai dan keputusan pemesanan PCB", "6 Jam"],
    ["2", "Revisi PCB pelebaran jalur (rute ulang atau board lebih besar), DRC 0, cek skematik PCB2 dan PCB3 terhadap netlist",
     "PCB1-PCB3 siap diekspor", "8 Jam"],
    ["3", "Firmware: kalibrasi MPU6050, perbaikan K1-K4 hasil audit, naikkan timeout upload, perbaiki SD Gateway",
     "Firmware terbarui dan hasil uji", "8 Jam"],
    ["4", "Uji SOS, jatuh, MOB, GPS luar ruangan, dan sensor air; buat project Supabase bersama bersama Rifat",
     "Hasil uji lapangan dan backend bersama", "6 Jam"],
])

# ---------------- L. persetujuan ----------------
# Tanda tangan Calvin dipertahankan dari template; tanda tangan ketua dihapus (harus ditandatangani sendiri).
st(P[79], "Tanggal: 31 Oktober 2026")
st(P[85], "Tanggal: 31 Oktober 2026")
for dr in P[84]._p.findall('.//' + qn('w:drawing')):
    dr.getparent().remove(dr)
d.save(OUT)
print("OK", OUT)
