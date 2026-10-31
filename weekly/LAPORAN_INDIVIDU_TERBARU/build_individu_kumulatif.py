"""Laporan individu paling mutakhir (kumulatif Pekan 2-7).

Basis: laporan Pekan 7 (template yang sama persis, tanda tangan dan gambar dipertahankan atas persetujuan ketua).
Isi: ringkasan Pekan 2-7 dari laporan individu Pekan 2-7 (docx), Audit_Progresi_Pekan2-7.md, dan Riwayat_Progres_Pekan2-5.md.
Tidak memuat kejadian Pekan 8.
"""
import copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = "../WEEK_7/LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 7.docx"
OUT = "LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 2-7 (Kumulatif).docx"
d = docx.Document(SRC)
P = list(d.paragraphs)  # snapshot indeks W7
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
    """Ganti n paragraf list mulai indeks `first` dengan len(texts) paragraf (kloning paragraf terakhir bila perlu)."""
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


BELUM = ["☑ Belum", "☐ Selesai"]      # termasuk "sebagian" (dijelaskan di kolom luaran)
SELESAI = ["☐ Belum", "☑ Selesai"]

# ---------------- A. identitas ----------------
st(T[0].rows[6].cells[1].paragraphs[0], "2 sampai 7 (laporan kumulatif)")
st(T[0].rows[7].cells[1].paragraphs[0], "31 Agustus - 10 Oktober 2026")

# ---------------- B. target (satu baris per pekan) ----------------
fill(T[1], [
    ["1", "Pekan 2: Finalisasi spesifikasi komponen wearable (Vest Node dan Helmet Node), on-site visit ke kapal SPJM (Tanjung Priok), dan kontribusi penyusunan Bill of Materials (BoM)",
     "Dokumen spesifikasi komponen final, catatan observasi lapangan, draft BoM dengan tautan pembelian", SELESAI],
    ["2", "Pekan 3: Persiapan perancangan mockup dashboard awal, dukungan review skematik Vest Node, Helmet Node, dan Edge Gateway, serta pemantauan finalisasi system design sebelum procurement",
     "Wireframe dan draft mockup dashboard (Figma), masukan teknis kebutuhan data dashboard, catatan review desain sistem", SELESAI],
    ["3", "Pekan 4: Lanjutan mockup dashboard, validasi dimensi casing Vest Node Master dan Helmet Node dengan model parametrik OpenSCAD, dukungan diskusi routing PCB Edge Gateway dan pemesanan komponen",
     "Draft lanjutan mockup, render 3D dan catatan revisi dimensi casing (18 ke 23 mm, 65 ke 70 mm), masukan prioritas PCB dan pemesanan", SELESAI],
    ["4", "Pekan 5: Mockup dashboard sesuai layout device final, pemantauan pemesanan komponen dan routing PCB Edge Gateway, penyesuaian referensi visual dengan casing 23/70 mm",
     "Sebagian: wireframe interaktif dashboard (tampilan marine pilot dan supervisor) dan repository GitHub selesai; pemantauan pemesanan/PCB Gateway dan penyesuaian visual dengan casing tidak dikerjakan", BELUM],
    ["5", "Pekan 6: Audit skematik 3 PCB dan perbaikan desain, perancangan ulang casing Vest Node, cross-check BOM, finalisasi fitur dashboard dan tech stack",
     "Sebagian: skematik/PCB terkoreksi (DRC 0 error), Gerber 3 board (belum dipesan), casing Vest Node v5, daftar selisih BOM selesai; fitur dashboard dan tech stack belum dikerjakan", BELUM],
    ["6", "Pekan 7: Prototipe breadboard Vest dan Helmet, firmware 3 node, uji fitur satu per satu, audit desain terhadap definisi proyek dan revisi PCB, verifikasi modul fisik dan order PCB, finalisasi dashboard dan tech stack",
     "Sebagian: prototipe + firmware 3 node, uji fitur lewat serial, AUDIT_V2 (9 temuan kritis), PCB2 dan PCB3 direvisi (DRC 0 error), BOM v2 selesai; footprint LoRa belum diganti, order PCB ditunda, dashboard dan tech stack belum", BELUM],
])

# ---------------- C. logbook (satu baris per pekan) ----------------
fill(T[2], [
    ["Pekan 2 (31 Agt - 5 Sep)",
     "On-site visit ke kapal SPJM (Tanjung Priok) dan wawancara pandu kapal; verifikasi spesifikasi komponen wearable (MCU, IMU, GPS, LoRa); keputusan memangkas BME680 dan revisi arsitektur sistem; penyusunan BoM; finalisasi dokumentasi observasi",
     "23", "Checklist observasi, foto on-site visit, catatan verifikasi, notulensi, draft BoM"],
    ["Pekan 3 (7 - 12 Sep)",
     "Riset referensi UI/UX, wireframe dan draft mockup dashboard di Figma (peta live tracking, status alarm, log insiden); diskusi data skematik dengan tim hardware; review skematik Vest Node, Helmet Node, Edge Gateway di EasyEDA Pro",
     "22", "Referensi desain, sketsa wireframe, draft mockup (Figma), notulensi, catatan review skematik"],
    ["Pekan 4 (14 - 19 Sep)",
     "Penyesuaian draft mockup dengan blueprint casing; model parametrik OpenSCAD casing Vest Node dan Helmet Node; simulasi validasi dimensi (baterai 18650 tidak muat) dan revisi 18 ke 23 mm, 65 ke 70 mm; diskusi routing PCB Gateway dan pemesanan komponen; render akhir",
     "23", "Model OpenSCAD, render 3D casing, notulensi diskusi"],
    ["Pekan 5 (21 - 26 Sep)",
     "Riset aplikasi marine pilot (SEAiq Pilot, SafePilot Pro) dan lone worker safety; diskusi dengan Rafif tentang dua tampilan dashboard; wireframe interaktif HTML/CSS/JS (peta, telemetri, SOS hold-to-confirm); repository GitHub dan kolaborator; update laporan kelompok",
     "20", "github.com/calvinkatoroy/pandu-dashboard; screenshot wireframe"],
    ["Pekan 6 (28 Sep - 3 Okt)",
     "Review proposal dan riwayat Pekan 2-5; perubahan scope Vest Node (tanpa VL53L0X dan BME680); audit skematik PCB1 dan redesain daya (tanpa AMS1117, boost 5 V, tombol power GPIO, MOSFET untuk GPS dan XKC-Y25); audit dan perbaikan PCB3; footprint ESP32 ke DevKitC V4; cross-check BOM; repository pandu-capstone dan HANDOVER.md; tantalum 100 uF di PCB2; ekspor Gerber 3 board; TP4056 diputar; casing Vest Node v5",
     "22*", "EasyEDA Pandu-Capstone; Audit_Skematik_Status.md; hardware/gerber/; PANDU_VestNode_Casing.scad; github.com/calvinkatoroy/pandu-capstone"],
    ["Pekan 7 (5 - 10 Okt)",
     "Riset pribadi (deteksi jatuh dan MOB, deep sleep, LoRa, BLE RSSI, GPS, arsitektur Gateway ke cloud); netlist PCB1-PCB3 dan check_netlist.py; revisi v2 PCB; firmware Vest, Helmet, Gateway; perakitan dan uji breadboard (FALL, SOS, sensor air, GPS, BLE + RSSI); audit penuh AUDIT_V2 (9 temuan kritis); revisi PCB2 dan PCB3 (DRC 0); BOM v2, tutorial, checklist, PLAN_REVISI; debug reset ESP32 dan crash BLE; koreksi Laporan Kemajuan Pekan 7 dan audit progres",
     "23", "Commit Git (branch v3: fd760d8, c07ba35, cde3e0a, 9ba8900); firmware/; hardware/netlist/; docs/AUDIT_V2.md, BOM_V2.md; Gambar 7-11"],
])
st(P[8], "Total Jam Kerja Pekan 2-7: 133 Jam (23 + 22 + 23 + 20 + 22* + 23). *Pekan 6: yang tercatat di laporan asli hanya Kamis-Sabtu (22 jam); jam Senin-Rabu belum dicatat.")

# ---------------- D. realisasi ----------------
lst(12, 4, [
    "Pekan 2: On-site visit ke kapal SPJM (Tanjung Priok), verifikasi spesifikasi komponen wearable (MCU, IMU, GPS, LoRa), keputusan memangkas sensor BME680 dan revisi arsitektur sistem (Wearable - Edge - Cloud - Dashboard), serta penyusunan draft BoM.",
    "Pekan 3-5: Riset referensi dan wireframe dashboard monitoring (Figma), lalu wireframe interaktif HTML/CSS/JS dengan dua tampilan pengguna (marine pilot dan supervisor) dan repository github.com/calvinkatoroy/pandu-dashboard; masukan kebutuhan data dashboard pada review skematik Vest Node, Helmet Node, dan Edge Gateway.",
    "Pekan 4: Validasi dimensi casing Vest Node Master dan Helmet Node dengan model parametrik OpenSCAD; simulasi menunjukkan baterai 18650 tidak muat sehingga casing direvisi (ketebalan 18 ke 23 mm, tinggi 65 ke 70 mm).",
    "Pekan 6: Audit skematik tiga PCB (AMS1117 tidak mendapat 3,3 V dari Li-ion, dua sumber 3V3 paralel, tombol sesaat dipakai sebagai saklar daya, pin antena RA-02 salah ke GND, rangkaian EN Gateway hilang), redesain daya Vest Node (baterai 18650 > TP4056 > boost 5 V, tombol power GPIO, gating GPS dan XKC-Y25 lewat MOSFET), footprint ESP32 ke DevKitC V4, DRC 0 error, Gerber 3 board (belum dipesan), casing Vest Node v5 (114 x 101 x 36,6 mm), cross-check BOM, repository pandu-capstone dan HANDOVER.md.",
    "Pekan 7: Merakit prototipe breadboard Vest Node dan Helmet Node dan menguji satu per satu: FALL (ambang free-fall 0,6 g), SOS (tahan 2 detik), sensor air analog (ambang 1000 mV), GPS (dapat satelit, fix lemah di dalam ruangan), beacon BLE Helmet dengan pembacaan RSSI oleh Vest; firmware tiga node sesuai definisi proyek (MOB = jatuh lalu basah >= 3 detik dalam 60 detik, status helm dari ambang RSSI -85 dBm yang belum dikalibrasi, paket PANDU,V1, mode demo tanpa LoRa, perbaikan crash BLE saat deep sleep).",
    "Pekan 7: Audit seluruh desain terhadap definisi proyek (AUDIT_V2.md: 9 temuan kritis) yang mengoreksi klaim PCB final pada Pekan 4, 6, dan 7; PCB2 Helmet (BAT_NEG, TTP223 dihapus, SAW1 diganti header) dan PCB3 Gateway (microSD di bus SPI terpisah) direvisi hingga DRC 0 error; netlist PCB1-PCB3 diverifikasi dengan skrip; Gerber lama dipindahkan ke _obsolete dan tidak boleh dipesan; BOM v2, tutorial, checklist, rencana revisi, serta koreksi Laporan Kemajuan Pekan 7.",
])
lst(17, 4, [
    "Dokumen spesifikasi komponen wearable, draft BoM dengan tautan pembelian, dan revisi arsitektur sistem tanpa BME680 (Pekan 2)",
    "Wireframe dan draft mockup dashboard (Figma) serta wireframe interaktif HTML/CSS/JS di repository pandu-dashboard (Pekan 3-5)",
    "Model parametrik OpenSCAD casing Vest Node dan Helmet Node dengan render 3D (Pekan 4); casing Vest Node v5, 114 x 101 x 36,6 mm (Pekan 6)",
    "Skematik dan PCB1-PCB3 terkoreksi, Audit_Skematik_Status.md, Gerber 3 board (3 Okt, tidak berlaku setelah audit Pekan 7), repository pandu-capstone dan HANDOVER.md, daftar selisih BOM (Pekan 6)",
    "Firmware Vest, Helmet, Gateway dan sketsa uji per fitur (firmware/, branch v3), docs/AUDIT_V2.md, BOM_V2.md, PLAN_REVISI.md, tutorial demo dan breadboard, checklist uji rakit (Pekan 7)",
    "PCB2 dan PCB3 hasil revisi (DRC 0 error), netlist PCB1-PCB3 dan check_netlist.py, docs/LAPORAN_PEKAN7_REVISI.md, Audit_Progresi_Pekan2-7.md (Pekan 7)",
])

# ---------------- E. capaian teknis ----------------
fill(T[3], [
    ["Hardware", "Spesifikasi wearable (Pekan 2), audit skematik dan perbaikan PCB1-3 (Pekan 6), verifikasi dan revisi hasil audit (Pekan 7)",
     "Spesifikasi final; PCB1-3 terkoreksi DRC 0 (Pekan 6), lalu audit Pekan 7 menemukan kesalahan: PCB2 dan PCB3 direvisi (DRC 0); PCB1 (BAT_NEG, footprint LoRa, sensor air) dan Gerber baru belum", "60%"],
    ["Software", "Mockup dan wireframe dashboard (Pekan 3-5), firmware 3 node (Pekan 7)",
     "Wireframe interaktif dashboard (2 tampilan); firmware Vest, Helmet, Gateway; Gateway baru ter-compile; paket biner v2, WiFi/cloud, dan tech stack backend belum", "70%"],
    ["Mekanik", "Validasi dimensi casing (Pekan 4), casing Vest Node v5 (Pekan 6)",
     "Model OpenSCAD tervalidasi, casing Vest Node v5 114 x 101 x 36,6 mm; casing Helmet dan Gateway belum; dimensi antar dokumen belum konsisten", "70%"],
    ["Pengujian", "Validasi dimensi casing (Pekan 4), uji fitur di breadboard (Pekan 7)",
     "Simulasi dimensi casing; FALL, MOB, SOS, air, GPS, BLE + RSSI diuji lewat serial; LoRa, Gateway, kalibrasi RSSI, GPS luar ruangan, dan baterai belum", "60%"],
    ["Dokumentasi", "Dokumentasi observasi, audit, BOM, tutorial, koreksi laporan",
     "Laporan pekanan, observasi lapangan, Audit_Skematik_Status, repository + HANDOVER.md, BOM v2, tutorial, checklist, audit progres Pekan 2-7", "90%"],
])
st(P[24], (
    "Selama Pekan 2-7 pekerjaan Calvin bergerak dari riset lapangan dan perancangan menuju implementasi dan verifikasi. "
    "Pekan 2 menghasilkan verifikasi spesifikasi wearable, revisi arsitektur (tanpa BME680), dan draft BoM setelah on-site visit ke SPJM. "
    "Pekan 3-5 berfokus pada dashboard (wireframe Figma, lalu wireframe interaktif dua tampilan) dan validasi dimensi casing dengan OpenSCAD (18 ke 23 mm, 65 ke 70 mm). "
    "Pekan 6 berfokus pada audit skematik tiga PCB, redesain daya Vest Node, Gerber baru, casing v5, dan cross-check BOM; scope Vest Node disederhanakan (tanpa VL53L0X dan BME680). "
    "Pekan 7 beralih ke prototipe breadboard, firmware tiga node, uji fitur satu per satu, dan audit penuh terhadap definisi proyek yang menemukan 9 temuan kritis, sehingga klaim PCB final pada Pekan 4, 6, dan 7 dikoreksi: PCB2 dan PCB3 sudah direvisi (DRC 0 error), PCB1 dan footprint LoRa belum, dan Gerber lama dibatalkan. "
    "Progres total proyek yang dilaporkan kelompok: sekitar 16,25% (Pekan 2), 24,25% (Pekan 3), 28% (Pekan 4), dan 29% (Pekan 5-6); klaim kelompok Pekan 7 sebesar 52,25% dikoreksi dalam audit progres menjadi usulan berbasis bukti 44,25% (keputusan final ada pada tim). "
    "Belum dikerjakan: uji tautan LoRa Vest ke Gateway, Gateway WiFi/cloud, dashboard dengan data nyata, dan keputusan tech stack backend."))

# ---------------- F. kendala ----------------
fill(T[4], [
    ["1", "Spesifikasi awal belum memenuhi standar IP67 dan sensor BME680 tidak relevan dengan hasil observasi lapangan (Pekan 2)",
     "Pembelian komponen wearable tertunda di awal; revisi arsitektur dan BoM", "Sedang"],
    ["2", "Dimensi casing awal (55 x 65 x 18 mm) tidak memuat baterai 18650; angka dimensi berubah-ubah antar dokumen (23/70 mm, lalu 114 x 101 x 30,6 dan 36,6 mm) (Pekan 3-6)",
     "Casing harus direvisi sebelum cetak 3D, jadwal fabrikasi berisiko, dan belum ada satu angka dimensi final", "Sedang"],
    ["3", "Desain dibuat sebelum komponen final dipastikan: footprint ESP32 dan LoRa tidak cocok modul fisik, USB menghadap ke dalam papan, BOM melebihi dana (Rp2,495 jt vs Rp2 jt) (Pekan 6-7)",
     "PCB belum bisa dipesan; uji tautan LoRa Vest ke Gateway tertunda (baru 1 modul); pembelian komponen tertunda", "Tinggi"],
    ["4", "Audit Pekan 7 menemukan kesalahan kritis pada desain yang sudah dilaporkan final di Pekan 4-6 (SAW1 salah komponen, proteksi TP4056 terlewati, SD berbagi SPI dengan LoRa)",
     "Gerber 3 dan 6 Okt tidak berlaku; PCB1 belum direvisi; laporan sebelumnya perlu dikoreksi", "Tinggi"],
    ["5", "Dashboard bergantung pada hardware stack dan endpoint ESP32 yang belum didefinisikan (Pekan 5-7)",
     "Dashboard baru berupa wireframe; skema data belum ada; fitur final dan tech stack mobile belum bisa dikunci", "Sedang"],
    ["6", "ESP32 reset (brownout) saat BLE dan GPS menyala dengan daya USB, crash BLE saat deep sleep, dan GPS NEO-6M cold start lama dengan antena keramik (Pekan 7)",
     "Demo dan uji tidak stabil; posisi GPS lambat didapat", "Sedang"],
])
st(P[27], (
    "Kendala berasal dari beberapa pola: spesifikasi awal belum mempertimbangkan kondisi kerja basah di kapal (Pekan 2); blueprint casing belum memperhitungkan toleransi dinding cetak 3D di sekitar baterai 18650 (Pekan 4); "
    "dan desain Pekan 4-6 dinyatakan final sebelum diverifikasi terhadap modul fisik dan definisi proyek, karena footprint dibuat dari library dan belum diuji di breadboard (Pekan 6-7). "
    "Dashboard tertahan karena endpoint dan format data perangkat belum dapat difinalkan sementara PCB Edge Gateway masih dirouting. "
    "Masalah daya dan crash BLE muncul karena uji pertama dilakukan lewat kabel USB tanpa kapasitor dan dengan modul BLE aktif."))

# ---------------- G. tindakan korektif ----------------
fill(T[5], [
    ["Spesifikasi belum IP67 dan BME680 tidak diperlukan (Pekan 2)",
     "Mengkalibrasi ulang spesifikasi komponen wearable sebelum checkout pembelian; memangkas BME680 dari arsitektur dan BoM",
     "Calvin, M Gibran Arya Avicena", "8 September 2026"],
    ["Dimensi casing tidak cukup untuk baterai 18650 dan tidak konsisten antar dokumen",
     "Revisi ketebalan 23 mm dan tinggi 70 mm yang divalidasi di OpenSCAD (selesai); casing Vest Node v5 mengikuti PCB; satu angka dimensi final perlu disepakati dengan Yoga",
     "Calvin, Yoga", "26 September 2026 (revisi); angka final menunggu konfirmasi"],
    ["Footprint LoRa tidak cocok / pita belum jelas",
     "Beli sepasang modul identik (SX1276 915/920 MHz, breakout header 2,54 mm), ukur jarak pin, lalu ganti footprint PCB1 dan PCB3",
     "Calvin, Rafif", "17 Oktober 2026"],
    ["Kesalahan kritis pada desain lama",
     "Jalankan PLAN_REVISI Fase 0-2: Gerber lama ke _obsolete, revisi PCB2/PCB3 (selesai), revisi PCB1, DRC 0, ekspor Gerber baru hanya setelah uji LoRa lolos",
     "Calvin", "17 Oktober 2026"],
    ["Reset ESP32 dan GPS lambat",
     "Kabel USB pendek dan tebal, kapasitor 100 uF di 3V3, build demo_usb; perbaikan crash BLE (tanpa deinit saat sleep); GPS diuji di luar ruangan, pertimbangkan antena aktif",
     "Calvin", "17 Oktober 2026"],
    ["Dashboard bergantung pada endpoint ESP32 dan BOM melebihi dana",
     "Menentukan skema data/endpoint bersama tim hardware (spesifikasi paket v2); BOM v2 selesai Pekan 7, pembelian komponen yang kurang menunggu keputusan tim",
     "Calvin, Rafif, Gibran", "17 Oktober 2026"],
])

# ---------------- H. dokumentasi (11 gambar) ----------------
IMG = "img/"
figs = [
    (IMG + "w4_1.png", 11.9, "Gambar 1. (Pekan 4) Hasil simulasi render 3D casing Vest Node Master untuk validasi kesesuaian dimensi internal komponen (baterai 18650, PCB, modul LoRa/GPS) menggunakan OpenSCAD."),
    (IMG + "w4_2.png", 11.9, "Gambar 2. (Pekan 4) Hasil simulasi render 3D casing Helmet Node untuk validasi kesesuaian dimensi internal komponen (ESP32-C3 SuperMini, CR2032, tab mounting Euroslot) menggunakan OpenSCAD."),
    (IMG + "w5_1.png", 5.1, "Gambar 3. (Pekan 5) Wireframe mockup dashboard mobile PANDU (tampilan marine pilot): status keselamatan pilot, live tracking posisi, telemetri perangkat, dan tombol SOS (hold-to-confirm). Repository: github.com/calvinkatoroy/pandu-dashboard"),
    (IMG + "w6_1.png", 12.0, "Gambar 4. (Pekan 6) Layout PCB1 Vest Node Master setelah audit (ESP32-DevKitC V4, TP4056, boost 5 V, RA-02), DRC 0 error. Catatan: audit Pekan 7 menunjukkan PCB1 masih perlu revisi."),
    (IMG + "w6_2.png", 10.5, "Gambar 5. (Pekan 6) Layout PCB3 Edge Gateway setelah diganti ke DevKitC V4, DRC 0 error. Catatan: PCB3 direvisi lagi di Pekan 7 (microSD di bus SPI terpisah)."),
    (IMG + "w6_3.png", 12.0, "Gambar 6. (Pekan 6) Render casing Vest Node v5 (OpenSCAD, PETG) berukuran 114 x 101 x 36,6 mm. Repository: github.com/calvinkatoroy/pandu-capstone"),
    (IMG + "fig1_prototipe.jpg", 14, "Gambar 7. (Pekan 7) Prototipe breadboard Vest Node (kiri) dan Helmet Node (kanan); daya dan serial lewat USB laptop (foto dari Laporan Kemajuan Pekan 7)."),
    (IMG + "fig2_log_uji.jpg", 11, "Gambar 8. (Pekan 7) Log serial hasil uji: Helmet Node (beacon BLE, counter, tombol ON/OFF) di atas dan Vest Node (status helm, RSSI, sensor air, jendela MOB, GPS, g) di bawah."),
    (IMG + "fig3_daya.jpg", 12, "Gambar 9. (Pekan 7) Baterai Doublepow 18650 1200 mAh pada holder (kiri) dan modul TP4056 HW-373 USB-C (kanan) untuk uji daya prototipe (8 Okt 2026). Pad B-/B+/OUT-/OUT+ dicocokkan dengan skematik."),
    (IMG + "fig4_easyeda.jpg", 11, "Gambar 10. (Pekan 7) EasyEDA: skematik PCB2 Helmet setelah revisi, BAT_NEG dipisah dari GND agar proteksi TP4056 aktif (atas); Import Changes PCB3 yang memindahkan microSD ke bus SPI sendiri, net SD_MISO, SD_MOSI, SD_SCK, SD_CS (bawah)."),
    (IMG + "fig5_kegiatan.jpg", 14, "Gambar 11. (Pekan 7) Foto kegiatan kelompok: diskusi dan penyusunan desain (kiri) dan komponen yang sudah datang (kanan) (foto dari Laporan Kemajuan Pekan 7)."),
]
pairs = [(P[41], P[42]), (P[43], P[44]), (P[45], P[46]), (P[47], P[48]), (P[49], P[50])]
tpl_pic, tpl_cap = copy.deepcopy(P[49]._p), copy.deepcopy(P[50]._p)
anchor = P[50]._p
for _ in range(len(figs) - len(pairs)):
    pe, ce = copy.deepcopy(tpl_pic), copy.deepcopy(tpl_cap)
    anchor.addnext(pe)
    pe.addnext(ce)
    anchor = ce
    pairs.append((Paragraph(pe, P[49]._parent), Paragraph(ce, P[49]._parent)))
for (pp, cp), (path, w, cap) in zip(pairs, figs):
    for dr in pp._p.findall('.//' + qn('w:drawing')):
        dr.getparent().remove(dr)
    run = pp.runs[0] if pp.runs else pp.add_run()
    run.add_picture(path, width=Cm(w))
    st(cp, cap)

# ---------------- I. kontribusi ----------------
st(P[54], "Rapat tim tanggal: 3 September 2026 (evaluasi hasil on-site visit dan revisi arsitektur); 11 September 2026 (review skematik rangkaian dan progres perancangan); 18 September 2026 (progres routing PCB Edge Gateway dan status pemesanan komponen); 22 September 2026 (bersama Rafif: target pengguna dan data dashboard).")
st(P[55], "Diskusi teknis: revisi arsitektur sistem dan keputusan memangkas BME680 (Pekan 2); kebutuhan data dashboard dari skematik dan penyesuaian dengan blueprint casing (Pekan 3-4); user role dashboard (Pekan 5); perubahan scope Vest Node tanpa VL53L0X dan BME680, cross-check BOM dengan Rafif dan Gibran, serah-terima desain lewat repository dan HANDOVER.md (Pekan 6); penyelarasan definisi proyek (MOB = jatuh DAN air, tiga stage, Gateway di dermaga dengan WiFi dan cloud, sampai 8 Vest), hasil audit, dan daftar komponen yang belum ada (Pekan 7).")
st(P[56], "Koordinasi dengan dosen: Tidak ada sesi khusus dengan dosen pembimbing pada Pekan 2-7; pembahasan dilakukan internal tim.")
st(P[58], "Berperan dalam merancang ulang arsitektur sistem dan menyusun BoM (Pekan 2), membangun wireframe dan mockup dashboard serta repository dashboard (Pekan 3-5), memvalidasi dimensi casing dengan model parametrik OpenSCAD (Pekan 4), mengaudit skematik tiga PCB, mendesain ulang daya Vest Node, merouting ulang PCB1-PCB3 hingga DRC 0 error, mengekspor Gerber, merancang ulang casing Vest Node v5, melakukan cross-check BOM, dan menyiapkan repository dan HANDOVER.md (Pekan 6), serta merakit dan menguji prototipe Vest dan Helmet, menulis firmware tiga node, mengaudit desain terhadap definisi proyek, merevisi PCB Helmet dan Gateway, menyusun BOM v2, tutorial, dan rencana revisi, serta mengoreksi laporan kelompok dan menyusun audit progres Pekan 2-7 (Pekan 7).")

# ---------------- J. evaluasi diri ----------------
st(P[61], "On-site visit dan revisi arsitektur (Pekan 2) serta validasi dimensi casing dengan simulasi parametrik (Pekan 4) menemukan masalah sebelum pengadaan dan fabrikasi.")
st(P[62], "Audit skematik (Pekan 6) dan audit penuh terhadap definisi proyek (Pekan 7) menangkap kesalahan kritis sebelum PCB dipesan; uji prototipe satu per satu menemukan masalah nyata (ambang jatuh dan sensor air, GPS lemah, brownout, crash BLE) yang tidak terlihat di skematik.")
st(P[63], "Kolaborasi dengan Rafif, tim hardware, dan tim mekanik berjalan lancar, dan semua perubahan terdokumentasi dan terlacak di repository (commit, netlist terverifikasi dengan skrip, rencana revisi bertahap).")
st(P[65], "Desain dinyatakan final di laporan (Pekan 4, 6, dan 7) sebelum diverifikasi terhadap modul fisik dan definisi proyek; klaim progres harus mengikuti bukti uji, bukan selesainya gambar.")
st(P[66], "Ketergantungan dashboard ke hardware tidak dikomunikasikan sejak awal sehingga dashboard baru berupa wireframe dan tech stack belum diputuskan; dimensi casing dan spesifikasi LoRa tidak konsisten antar dokumen.")
st(P[67], "Modul LoRa belum diverifikasi sampai Pekan 7 dan modul kedua belum dibeli; logbook perlu diisi harian (jam Pekan 6 belum lengkap); komunikasi dengan dosen pembimbing perlu ditingkatkan.")
st(P[69], "Observasi lapangan, verifikasi di breadboard, dan pengukuran modul fisik harus dilakukan sebelum desain PCB dinyatakan final.")
st(P[70], "Toleransi dinding cetak 3D, port USB, dan akses fisik harus dipertimbangkan sejak desain PCB dan blueprint casing; uji daya (kabel, kapasitor, brownout) dan perilaku sleep dicek sejak awal.")
st(P[71], "Satu sumber kebenaran untuk spesifikasi (definisi proyek, BOM, laporan) dan koordinasi software-hardware lebih awal mencegah klaim yang berbeda antar dokumen dan bottleneck antar pekan.")

# ---------------- K. rencana pekan berikutnya (rencana Pekan 8, dari laporan Pekan 7) ----------------
fill(T[6], [
    ["1", "Beli sepasang modul LoRa identik, ukur modul, ganti footprint PCB1 dan PCB3, revisi PCB1 (BAT_NEG, sensor air, lebar trek), DRC 0",
     "PCB1 dan PCB3 siap diekspor", "6 Jam"],
    ["2", "Uji tautan LoRa Vest ke Gateway (SF, daya, jarak), kalibrasi RSSI helm dan ambang jatuh, uji GPS di luar ruangan",
     "Hasil uji LoRa, kalibrasi, dan PDR", "8 Jam"],
    ["3", "Persiapan presentasi UTS (17 Okt) dan demo breadboard; spesifikasi paket biner v2 (ID Vest, nomor urut); koordinasi dashboard dengan Rafif",
     "Demo UTS dan spesifikasi paket v2", "4 Jam"],
])

# ---------------- L. persetujuan ----------------
# Tanda tangan Calvin dan Rafif dipertahankan dari laporan sebelumnya atas persetujuan ketua.
# Tanggal tanda tangan: 23 Oktober 2026 (permintaan Calvin).
st(P[79], "Tanggal: 23 Oktober 2026")
st(P[85], "Tanggal: 23 Oktober 2026")
d.save(OUT)
print("OK", OUT)
