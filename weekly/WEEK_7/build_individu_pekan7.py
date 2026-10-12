import copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = "../WEEK_6/LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 6.docx"
OUT = "LAPORAN PEKANAN INDIVIDU - Calvin Wirathama Katoroy - Pekan 7.docx"
d = docx.Document(SRC)
P = list(d.paragraphs)  # snapshot indeks W6
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


BELUM = ["☑ Belum", "☐ Selesai"]
SELESAI = ["☐ Belum", "☑ Selesai"]

# A. identitas
st(T[0].rows[6].cells[1].paragraphs[0], "7")
st(T[0].rows[7].cells[1].paragraphs[0], "5 - 10 Oktober 2026")

# B. target
fill(T[1], [
    ["1", "Verifikasi modul fisik (pinout, ukuran) dan penyesuaian footprint PCB/casing (rencana Pekan 6)",
     "Daftar verifikasi modul; footprint disesuaikan. Sebagian: pinout LoRa dan TP4056 dicek, footprint LoRa belum diganti", BELUM],
    ["2", "Pesan modul yang kurang, update BOM, lalu order PCB (rencana Pekan 6)",
     "BOM v2 selesai (docs/BOM_V2.md); order PCB sengaja ditunda karena audit menemukan kesalahan desain", BELUM],
    ["3", "Merakit prototipe breadboard Vest Node dan Helmet Node serta membuat firmware Vest, Helmet, Gateway",
     "Prototipe breadboard + firmware 3 node (firmware/)", SELESAI],
    ["4", "Menguji fitur satu per satu: FALL, MOB, SOS, sensor air, GPS, beacon BLE + RSSI helm",
     "Log serial per fitur; sketsa uji firmware/test_*. LoRa Vest ke Gateway belum diuji", SELESAI],
    ["5", "Audit desain terhadap definisi proyek dan revisi PCB Helmet dan Gateway hasil audit",
     "docs/AUDIT_V2.md, PCB2 dan PCB3 direvisi (DRC 0 error), netlist + skrip pengecek", SELESAI],
    ["6", "Finalisasi daftar fitur dashboard dan tech stack (terbawa dari Pekan 5-6)",
     "Daftar fitur dan keputusan tech stack", BELUM],
])

# C. logbook
fill(T[2], [
    ["Senin (5 Okt)",
     "Riset pribadi: referensi deteksi jatuh dengan akselerometer (fase free-fall dan benturan) dan logika MOB (jatuh digabung sensor air) untuk menetapkan ambang awal; mempelajari wake-up deep sleep ESP32 (ext0/ext1) dan pin strapping untuk firmware Vest dan Helmet",
     "2", "Catatan riset; firmware/vest_node (ambang jatuh/MOB, wake SOS)"],
    ["Selasa (6 Okt)",
     "Membuat netlist PCB1-PCB3 dan skrip pengecek pin (check_netlist.py), memperbaiki polaritas tombol SOS di firmware (aktif-HIGH sesuai skematik); revisi v2 PCB (header antena, kapasitor bulk, dioda backfeed 5 V, USB tunggal Gateway, pull-up SD_CS, IRLZ44N, pembagi tegangan baterai IO35, tombol on/off Helmet GPIO4); firmware Vest (SOS membangunkan dari deep sleep, scanner BLE status helm), firmware Helmet (beacon BLE + deep sleep), firmware Gateway (LoRa RX, pola sirine, log SD); membuat checklist uji rakit dan tutorial breadboard",
     "5", "15 commit Git (93bfe35 s.d. cc2193f); hardware/netlist/; firmware/"],
    ["Rabu (7 Okt)",
     "Riset pribadi: modul LoRa (SX1276/RFM95 vs Ra-02, pita 433/868/915 MHz, SF, bandwidth, waktu udara, dan anggaran link di atas air) untuk target jarak jauh; BLE RSSI untuk estimasi kedekatan helm (interval advertising, daya TX, penghalusan EMA); menyusun rencana uji per fitur",
     "2", "Catatan riset; docs/AUDIT_V2.md (temuan LoRa); rencana uji per fitur"],
    ["Kamis (8 Okt)",
     "Merakit prototipe breadboard Vest dan Helmet dan menguji fitur satu per satu (FALL, SOS, sensor air analog, GPS, modul LoRa, beacon BLE helm + scanner RSSI); memeriksa baterai 18650 + TP4056 (HW-373); PCB2 v2.1 (LiPo + TP4056); audit penuh terhadap definisi proyek (AUDIT_V2: 9 temuan kritis); logika MOB (jatuh lalu basah dalam 60 detik); BOM v2, tutorial demo tanpa LoRa; Gerber lama dipindah ke _obsolete; revisi PCB2 (BAT_NEG, tanpa TTP223, header J1) dan PCB3 (SD di SPI terpisah) hingga DRC 0, netlist terverifikasi",
     "8", "Commit fd760d8, c07ba35, cde3e0a, 9ba8900; docs/AUDIT_V2.md, BOM_V2.md; Gambar 1-4"],
    ["Jumat (9 Okt)",
     "Riset pribadi: GPS NEO-6M (cold start, antena keramik vs aktif, konstelasi GPS-only vs multi-GNSS, parsing NMEA GSV/GSA); arsitektur Gateway ke cloud (store-and-forward microSD, sinkronisasi waktu NTP, ACK untuk SOS) serta pilihan backend real-time untuk dashboard",
     "2", "Catatan riset; firmware/test_gps; docs/AUDIT_V2.md (temuan Gateway/cloud)"],
    ["Sabtu (10 Okt)",
     "Debug reset ESP32 pada Vest (perbaikan crash BLE saat masuk deep sleep, penanda boot, demo tanpa deteksi brownout); evaluasi modul LoRa 433 vs 915 MHz dan rencana pembelian sepasang modul identik; review dan koreksi Laporan Kemajuan Pekan 7; audit dek proposal; menyusun laporan individu dan audit progres",
     "4", "weekly/WEEK_7/; docs/LAPORAN_PEKAN7_REVISI.md"],
])
st(P[8], "Total Jam Kerja Minggu Ini: 23 Jam")

# D
lst(12, 4, [
    "Merakit prototipe breadboard Vest Node (ESP32, MPU6050, GPS NEO-6M, sensor air, tombol SOS dan power) dan Helmet Node (SuperMini + tombol), lalu menguji satu per satu: FALL (ambang free-fall disetel ke 0,6 g), SOS (tahan 2 detik), sensor air analog (ambang 1000 mV), GPS (dapat satelit, fix lemah di dalam ruangan), dan beacon BLE Helmet dengan pembacaan RSSI oleh Vest.",
    "Memperbarui firmware sesuai definisi proyek: MOB = jatuh lalu basah >= 3 detik dalam 60 detik, status helm (dekat/jauh/tidak terdengar) dari ambang RSSI -85 dBm (belum dikalibrasi), paket PANDU,V1 berisi posisi terakhir beserta usianya, mode demo tanpa LoRa, dan perbaikan crash BLE saat deep sleep.",
    "Mengaudit seluruh desain terhadap definisi proyek (AUDIT_V2.md: 9 temuan kritis) dan merevisi PCB2 Helmet (BAT_NEG agar proteksi TP4056 aktif, TTP223 dihapus, SAW1 diganti header) serta PCB3 Gateway (microSD di bus SPI terpisah) hingga DRC 0 error; netlist PCB1-PCB3 diverifikasi dengan skrip.",
    "Menyusun BOM v2, tutorial demo tanpa LoRa, tutorial breadboard, checklist uji rakit, rencana revisi (PLAN_REVISI), serta mengoreksi dan merevisi Laporan Kemajuan Pekan 7; Gerber lama dipindahkan ke _obsolete dan ditandai tidak boleh dipesan.",
])
lst(17, 4, [
    "Firmware Vest, Helmet, Gateway beserta sketsa uji per fitur (firmware/vest_node, helmet_node, gateway, test_*) — repository: github.com/calvinkatoroy/pandu-capstone (branch v3)",
    "docs/AUDIT_V2.md (audit v2), docs/BOM_V2.md, docs/PLAN_REVISI.md, TUTORIAL_DEMO_TANPA_LORA.md dan TUTORIAL_BREADBOARD.md",
    "PCB2 dan PCB3 hasil revisi (DRC 0 error) serta netlist PCB1-PCB3 dan check_netlist.py (hardware/netlist/); Gerber lama di _obsolete (belum ada Gerber baru)",
    "Dokumen koreksi laporan: docs/LAPORAN_PEKAN7_REVISI.md dan tab Pekan 7 (Revisi) pada Laporan Kemajuan Pekan 7; audit progres Pekan 2-7 (Audit_Progresi_Pekan2-7.md)",
])

# E
fill(T[3], [
    ["Hardware", "Verifikasi modul, revisi PCB hasil audit",
     "PCB2 dan PCB3 direvisi, DRC 0 error; PCB1 (BAT_NEG, footprint LoRa, sensor air) dan Gerber baru belum", "60%"],
    ["Software", "Firmware 3 node dan logika sesuai definisi proyek",
     "Firmware Vest, Helmet, Gateway; MOB, status helm via RSSI; Gateway baru ter-compile, belum diuji di papan; paket biner v2, WiFi/cloud belum", "70%"],
    ["Mekanik", "-", "Tidak ada pekerjaan mekanik pekan ini (casing v5 dari Pekan 6)", "-"],
    ["Pengujian", "Uji fitur di breadboard",
     "FALL, MOB, SOS, air, GPS, BLE + RSSI diuji lewat serial; LoRa, Gateway, kalibrasi RSSI, GPS luar ruangan, baterai belum", "60%"],
    ["Dokumentasi", "Audit, BOM, tutorial, koreksi laporan",
     "AUDIT_V2, BOM_V2, tutorial demo dan breadboard, PLAN_REVISI, revisi laporan, audit progres", "90%"],
])
st(P[24], "Pekan ini pekerjaan Calvin bergeser dari desain ke implementasi dan verifikasi. Prototipe breadboard Vest dan Helmet dirakit, firmware tiga node dibuat, dan fitur FALL, MOB, SOS, sensor air, GPS, serta deteksi helm lewat BLE RSSI diuji satu per satu. Audit penuh terhadap definisi proyek menemukan 9 temuan kritis pada desain yang sebelumnya dinyatakan final (saklar Helmet salah komponen, proteksi TP4056 terlewati, footprint LoRa tidak cocok modul fisik, microSD berbagi bus SPI, logika MOB, dan lainnya). PCB2 dan PCB3 sudah direvisi dengan DRC 0 error, sedangkan PCB1 serta footprint LoRa masih menunggu pengukuran modul dan pembelian pasangan modul yang identik. PCB belum dipesan dan Gerber lama dinyatakan tidak berlaku. Uji tautan LoRa, Gateway, dan dashboard belum dikerjakan.")

# F
fill(T[4], [
    ["1", "Footprint LoRa (RA-02) tidak cocok dengan modul fisik (pinout RFM95, pitch lebih kecil dari 2,54 mm), pita modul belum terverifikasi, dan modul kedua belum dibeli",
     "PCB1 dan PCB3 belum bisa dipesan; uji tautan LoRa Vest ke Gateway tertunda (baru 1 modul)", "Tinggi"],
    ["2", "Audit menemukan kesalahan kritis pada desain yang sudah dilaporkan final di Pekan 4-6 (SAW1 salah komponen, proteksi TP4056 terlewati, SD berbagi SPI dengan LoRa)",
     "Gerber 3 dan 6 Okt tidak berlaku; PCB1 belum direvisi; laporan sebelumnya perlu dikoreksi", "Tinggi"],
    ["3", "ESP32 reset (brownout) saat BLE dan GPS menyala dengan daya USB, crash BLE saat deep sleep, dan GPS NEO-6M cold start lama dengan antena keramik",
     "Demo dan uji tidak stabil; posisi GPS lambat didapat", "Sedang"],
])
st(P[27], "Desain Pekan 4-6 dinyatakan final sebelum diverifikasi terhadap modul fisik dan definisi proyek, sehingga kesalahan baru tertangkap setelah prototipe breadboard dan audit pekan ini. Footprint dibuat dari library, bukan dari modul yang benar-benar dibeli. Masalah daya dan crash BLE muncul karena uji pertama dilakukan lewat kabel USB tanpa kapasitor dan dengan modul BLE aktif.")

# G
fill(T[5], [
    ["Footprint LoRa tidak cocok / pita belum jelas",
     "Beli sepasang modul identik (SX1276 915/920 MHz, breakout header 2,54 mm), ukur jarak pin, lalu ganti footprint PCB1 dan PCB3",
     "Calvin, Rafif", "17 Oktober 2026"],
    ["Kesalahan kritis pada desain lama",
     "Jalankan PLAN_REVISI Fase 0-2: Gerber lama ke _obsolete, revisi PCB2/PCB3 (selesai), revisi PCB1, DRC 0, ekspor Gerber baru hanya setelah uji LoRa lolos",
     "Calvin", "17 Oktober 2026"],
    ["Reset ESP32 dan GPS lambat",
     "Kabel USB pendek dan tebal, kapasitor 100 uF di 3V3, build demo_usb; perbaikan crash BLE (tanpa deinit saat sleep); GPS diuji di luar ruangan, pertimbangkan antena aktif",
     "Calvin", "17 Oktober 2026"],
])

# H: tiga figur (ganti gambar W6)
IMG = "img/"
figs = [
    (IMG + "fig1_prototipe.jpg", 14, "Gambar 1. Prototipe breadboard Vest Node (kiri) dan Helmet Node (kanan); daya dan serial lewat USB laptop (foto dari Laporan Kemajuan Pekan 7)."),
    (IMG + "fig2_log_uji.jpg", 12, "Gambar 2. Log serial hasil uji: Helmet Node (beacon BLE, counter, tombol ON/OFF) di atas dan Vest Node (status helm, RSSI, sensor air, jendela MOB, GPS, g) di bawah."),
    (IMG + "fig3_daya.jpg", 12, "Gambar 3. Baterai Doublepow 18650 1200 mAh pada holder (kiri) dan modul TP4056 HW-373 USB-C (kanan) untuk uji daya prototipe (8 Okt 2026). Pad B-/B+/OUT-/OUT+ dicocokkan dengan skematik."),
    (IMG + "fig4_easyeda.jpg", 12, "Gambar 4. EasyEDA: skematik PCB2 Helmet setelah revisi, BAT_NEG dipisah dari GND agar proteksi TP4056 aktif (atas); Import Changes PCB3 yang memindahkan microSD ke bus SPI sendiri, net SD_MISO, SD_MOSI, SD_SCK, SD_CS (bawah)."),
    (IMG + "fig5_kegiatan.jpg", 14, "Gambar 5. Foto kegiatan kelompok: diskusi dan penyusunan desain (kiri) dan komponen yang sudah datang (kanan) (foto dari Laporan Kemajuan Pekan 7)."),
]
pairs = [(P[41], P[42]), (P[43], P[44]), (P[45], P[46])]
tpl_pic, tpl_cap = copy.deepcopy(P[45]._p), copy.deepcopy(P[46]._p)
anchor = P[46]._p
for _ in range(len(figs) - len(pairs)):
    pe, ce = copy.deepcopy(tpl_pic), copy.deepcopy(tpl_cap)
    anchor.addnext(pe)
    pe.addnext(ce)
    anchor = ce
    pairs.append((Paragraph(pe, P[45]._parent), Paragraph(ce, P[45]._parent)))
for (pp, cp), (path, w, cap) in zip(pairs, figs):
    for dr in pp._p.findall('.//' + qn('w:drawing')):
        dr.getparent().remove(dr)
    run = pp.runs[0] if pp.runs else pp.add_run()
    run.add_picture(path, width=Cm(w))
    st(cp, cap)

# I
st(P[50], "Diskusi tim: menyelaraskan definisi proyek (MOB = jatuh DAN air, tiga stage aman/warning/danger, Gateway di dermaga dengan WiFi dan cloud, sampai 8 Vest) dengan implementasi; hasil audit dibagikan lewat repository.")
st(P[51], "Koordinasi BOM dan pengadaan: BOM v2 dan daftar komponen yang belum ada (modul LoRa kedua, boost, MOSFET, sirine, LiPo) untuk Rafif dan Gibran; koreksi Laporan Kemajuan Pekan 7 agar sesuai kondisi sebenarnya.")
st(P[52], "Koordinasi dengan dosen: Tidak ada sesi khusus minggu ini.")
st(P[54], "Berperan merakit dan menguji prototipe Vest dan Helmet, menulis dan memperbarui firmware ketiga node, mengaudit desain terhadap definisi proyek, merevisi PCB Helmet dan Gateway hingga DRC 0 error, menyusun BOM v2, tutorial, dan rencana revisi, serta mengoreksi laporan kelompok dan menyusun audit progres Pekan 2-7.")

# J
st(P[57], "Uji prototipe satu per satu cepat menemukan masalah nyata (ambang jatuh dan sensor air, GPS lemah, brownout, crash BLE) yang tidak terlihat di skematik.")
st(P[58], "Audit terhadap definisi proyek menangkap 9 temuan kritis sebelum PCB dipesan, sehingga biaya fabrikasi yang salah dapat dihindari.")
st(P[59], "Semua perubahan terdokumentasi dan terlacak di repository (commit, netlist terverifikasi dengan skrip, rencana revisi bertahap).")
st(P[61], "Desain dinyatakan final di laporan sebelum diverifikasi; klaim progres harus mengikuti bukti uji, bukan selesainya gambar.")
st(P[62], "Modul LoRa belum diverifikasi sampai Pekan 7 dan modul kedua belum dibeli, sehingga uji tautan LoRa tertunda.")
st(P[63], "Dashboard, Gateway (WiFi, cloud, SD, tahap alarm), dan paket biner v2 belum dikerjakan; mekanik tidak disentuh pekan ini.")
st(P[65], "Verifikasi di breadboard dan ukur modul fisik sebelum menyatakan desain PCB final.")
st(P[66], "Satu sumber kebenaran untuk spesifikasi (definisi proyek, BOM, laporan) mencegah klaim yang berbeda antar dokumen.")
st(P[67], "Uji daya (kabel, kapasitor, brownout) dan perilaku sleep perlu dicek sejak awal, bukan setelah semua modul dipasang.")

# K
fill(T[6], [
    ["1", "Beli sepasang modul LoRa identik, ukur modul, ganti footprint PCB1 dan PCB3, revisi PCB1 (BAT_NEG, sensor air, lebar trek), DRC 0",
     "PCB1 dan PCB3 siap diekspor", "6 Jam"],
    ["2", "Uji tautan LoRa Vest ke Gateway (SF, daya, jarak), kalibrasi RSSI helm dan ambang jatuh, uji GPS di luar ruangan",
     "Hasil uji LoRa, kalibrasi, dan PDR", "8 Jam"],
    ["3", "Persiapan presentasi UTS (17 Okt) dan demo breadboard; spesifikasi paket biner v2 (ID Vest, nomor urut); koordinasi dashboard dengan Rafif",
     "Demo UTS dan spesifikasi paket v2", "4 Jam"],
])

# L: tanggal
# tanda tangan Calvin dan Rafif dipertahankan dari Pekan 6 (atas persetujuan Rafif)
st(P[75], "Tanggal: 10 Oktober 2026")
st(P[81], "Tanggal: 10 Oktober 2026")
d.save(OUT)
print("OK", OUT)
