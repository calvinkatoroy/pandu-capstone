// ============================================================
// P.A.N.D.U — Vest Node Master Casing
// v4: disesuaikan ke PCB1 final (EasyEDA, 4250x4250 mil) --
//     baterai 18650 sekarang di holder BH-18650-1 DI ATAS PCB,
//     buzzer dihapus, jendela GPS dihapus.
// assembly (shell+lid+PCB+holder baterai) + exploded view + DXF 2D export
// ============================================================
// CARA PAKAI (semua lewat GUI OpenSCAD, nggak perlu command line):
//   1. Buka file ini di OpenSCAD
//   2. Window -> Customizer (kalau panel kanan belum muncul)
//   3. Di tab "Render Control": geser slider "explode_factor" buat
//      lihat exploded view, atau pilih "dxf_view" buat siapkan 2D
//   4. Multi-view 3D: pakai menu View -> Top / Front / Right / Diagonal,
//      lalu File -> Export -> Export as Image (PNG)
//   5. Export teknik 2D: set dxf_view ke "front"/"top"/"side" (explode_factor
//      otomatis dipaksa 0 saat export DXF), preview (F5), lalu
//      File -> Export -> Export as DXF
// ============================================================

/* [Render Control] */
// 0 = assembly normal, naikkan buat pisahkan komponen (exploded view)
explode_factor = 0; // [0:0.1:3]
// pilih view buat export DXF 2D -- "none" nampilin model 3D biasa
dxf_view = "none"; // [none, front, top, side]

/* [PCB1 final (mm)] */
// Outline PCB1 di EasyEDA: 4250 x 4250 mil = 107.95 mm
pcb_w = 108;
pcb_h = 108;
pcb_t = 1.6;

/* [Dimensi Casing (mm)] */
wall      = 2;    // asumsi tebal dinding cetak 3D (PETG)
lid_t     = 2;    // tebal tutup/lid atas
pcb_gap   = 1;    // clearance PCB ke dinding tiap sisi
standoff  = 3;    // tinggi tiang penyangga PCB dari lantai casing
corner_r  = 8;    // radius sudut (sesuai blueprint awal R8)

/* [Holder baterai BH-18650-1 di atas PCB] */
// ukuran diukur dari footprint di PCB1 (~21 x 75 mm); TINGGI = ASUMSI
// (sel 18mm + badan holder), VERIFIKASI ke datasheet / holder yang dibeli
hold_w = 21;
hold_l = 75;
hold_h = 21;
// posisi pojok kiri-atas holder dari pojok kiri-atas PCB (dari layout PCB1)
hold_dx = 7.3;
hold_dy = 2.7;

// ---- Dimensi turunan ----
case_w = pcb_w + 2*(wall + pcb_gap);
case_h = pcb_h + 2*(wall + pcb_gap);
// lantai + standoff + PCB + komponen tertinggi + clearance + lid

/* [Modul boost MT3608 -- dipasang pakai KABEL] */
// Modul TIDAK dicolok ke header U2. Header 1x4 U2 di PCB1 (pusat 3500,2000 mil)
// cuma titik sambung kabel 4 pin (IN+ IN- OUT- OUT+). Modul sendiri ditempel
// (double tape / lem) di SISI BAWAH TUTUP, digantung di atas area kosong
// pojok kanan-bawah, jauh dari GPS (antena) dan plunger tombol SOS.
// Koordinat dari pojok kiri-atas PCB (mm), toleransi +-1.5 mm
boost_pos = [86, 100];      // pusat modul
boost_l = 37;               // panjang modul (sejajar sumbu X)
boost_w = 17;               // lebar modul
boost_h = 5.5;              // tebal modul termasuk induktor (ASUMSI)
header_top = 8.5;           // tinggi header U2 + pin di atas PCB (ASUMSI)

// tinggi casing: lantai + standoff + PCB + komponen tertinggi + clearance + lid
// (modul boost menggantung dari tutup, jadi tidak menentukan tinggi casing)
tall_h = hold_h;
case_t = wall + standoff + pcb_t + tall_h + 1 + lid_t;
// dasar modul di atas PCB = sisi dalam tutup - tebal modul
boost_z0 = (case_t - lid_t) - (wall + standoff + pcb_t) - boost_h;

/* [Bukaan casing] */
// Koordinat komponen = posisi (mm) dari POJOK KIRI-ATAS PCB (layout PCB1,
// diukur dari screenshot EasyEDA -- toleransi +-1.5 mm, cek lagi sebelum cetak)
// Fungsi di bawah mengubahnya ke koordinat model (origin di tengah PCB).
function pcb_xy(px, py) = [px - pcb_w/2, pcb_h/2 - py];

pcb_top_z = wall + standoff + pcb_t;   // permukaan atas PCB dari lantai

// Pembagian sisi (tampak atas model, +Y = atas PCB di EasyEDA):
//   KIRI  (-X)  : USB-C charging  -- dekat modul TP4056 (U7)
//   BAWAH (-Y)  : SMA antena LoRa -- dekat RA-02 (U6)
//   TUTUP (+Z)  : tombol power & SOS, via plunger cetak
//   Water level : XKC-Y25 ditempel di SISI DALAM dinding bawah, TANPA lubang
//   GPS         : TANPA jendela (PETG tipis tembus sinyal), antena menghadap atas
//   Buzzer      : dihapus dari desain

// USB-C (ukuran plug + overmold; blueprint lama 8x4 terlalu pas)
usb_w = 10;   usb_h = 5;
usb_pos = pcb_xy(18, 90);              // y tengah modul U7; x tidak dipakai
usb_z   = pcb_top_z + 3;               // tengah colokan ~3 mm di atas PCB
// SMA / pigtail antena LoRa
sma_d   = 8;
sma_pos = pcb_xy(62.4, 0);             // x di dekat pad ANT RA-02
sma_z   = pcb_top_z + 6;
// Tombol (tact switch di PCB, ditekan lewat plunger di tutup)
sw_power = pcb_xy(33.5, 65.4);         // SW1
sw_sos   = pcb_xy(72.2, 87.1);         // SW2 (SOSButton)
sw_h       = 3.5;                      // ASUMSI tinggi tact switch di atas PCB
btn_hole_d = 6;                        // lubang di tutup
plunger_d  = 5;                        // batang plunger (celah 0.5 mm)
plunger_fl = 8;                        // flens penahan di bawah tutup
plunger_gap = 1;                       // celah plunger ke tombol saat diam

module rounded_rect(w, h, r) {
    offset(r = r) offset(delta = -r) square([w, h], center = true);
}

// ---- PART: bottom shell (tray, terbuka di atas) ----
module bottom_shell() {
    shell_h = case_t - lid_t;
    difference() {
        linear_extrude(height = shell_h) rounded_rect(case_w, case_h, corner_r);
        // offset(delta=-wall) dari profil yang SAMA -> bentuk konsentris presisi,
        // menghindari warning "not a valid 2-manifold" dari CGAL
        translate([0, 0, wall - 0.02])
            linear_extrude(height = shell_h)
                offset(delta = -wall) rounded_rect(case_w, case_h, corner_r);

        // USB-C di dinding kiri (-X): kotak membujur menembus dinding
        translate([-case_w/2, usb_pos[1], usb_z])
            cube([wall*4, usb_w, usb_h], center = true);
        // SMA di dinding bawah (-Y): silinder membujur menembus dinding
        translate([sma_pos[0], -case_h/2, sma_z])
            rotate([90, 0, 0]) cylinder(d = sma_d, h = wall*4, center = true, $fn = 48);
    }
}

// ---- PART: lid / tutup atas (dengan 2 lubang tombol) ----
module lid() {
    difference() {
        linear_extrude(height = lid_t) rounded_rect(case_w, case_h, corner_r);
        for (p = [sw_power, sw_sos])
            translate([p[0], p[1], -0.1])
                cylinder(d = btn_hole_d, h = lid_t + 0.2, $fn = 40);
    }
}

// ---- PART: plunger tombol (cetak terpisah, 2x: power & SOS) ----
// z=0 = permukaan atas PCB. Batang menembus lubang tutup, flens menahan
// plunger supaya tidak lepas keluar, ujung atas menonjol 1.2 mm di atas tutup.
module plunger() {
    shell_h  = case_t - lid_t;
    z0       = sw_h + plunger_gap;                  // dasar batang
    z_lid_in = shell_h - pcb_top_z;                 // sisi dalam tutup
    shaft_h  = (z_lid_in + lid_t + 1.2) - z0;
    translate([0, 0, z0])
        cylinder(d = plunger_d, h = shaft_h, $fn = 40);
    translate([0, 0, z_lid_in - 1.5])
        cylinder(d = plunger_fl, h = 1.5, $fn = 40);
}

// ---- PART: PCB (representasi visual, centered di origin lokal) ----
// ---- PART: modul boost MT3608 di atas header U2 (representasi visual) ----
// z=0 = permukaan atas PCB; panjang modul sejajar sumbu X
module boost_module() {
    p = pcb_xy(boost_pos[0], boost_pos[1]);
    translate([p[0], p[1], boost_z0 + boost_h/2])
        cube([boost_l, boost_w, boost_h], center = true);
}

module pcb() {
    cube([pcb_w, pcb_h, pcb_t], center = true);
}

// ---- PART: holder baterai di atas PCB (representasi visual) ----
// posisi dihitung dari pojok kiri-atas PCB, z=0 = permukaan atas PCB
module battery_holder() {
    translate([-pcb_w/2 + hold_dx + hold_w/2,
                pcb_h/2 - hold_dy - hold_l/2,
                hold_h/2])
        cube([hold_w, hold_l, hold_h], center = true);
}

// ---- ASSEMBLY dengan exploded view ----
// explode_factor=0 -> semua rapat (assembly normal)
// explode_factor naik -> tiap part menjauh dari posisi assembly-nya
module assembly(explode = explode_factor) {
    shell_h = case_t - lid_t;
    pcb_z   = wall + standoff + pcb_t/2;

    color("SteelBlue") bottom_shell();

    translate([0, 0, pcb_z + explode*30]) {
        color("LimeGreen") pcb();
        translate([0, 0, pcb_t/2])
            color("Orange") battery_holder();

    }

    // plunger tombol (ikut naik bareng lid biar kelihatan di exploded view)
    for (p = [sw_power, sw_sos])
        translate([p[0], p[1], pcb_top_z + explode*60])
            color("Gold") plunger();

    // modul boost digantung di sisi bawah tutup -> ikut naik bareng tutup
    translate([0, 0, wall + standoff + pcb_t + explode*60])
        color("Crimson") boost_module();

    translate([0, 0, shell_h + explode*60])
        color([0.27, 0.31, 0.47, 1]) lid(); // alpha dibikin 1 (full opaque) -- alpha<1 bikin OpenSCAD preview (F5) salah urut render transparency
}

// ---- OUTPUT: 3D assembly, atau proyeksi 2D (buat export DXF) ----
// Rotasi dipilih supaya hasil projection() = tampak muka sesuai nama view:
//   front -> tanpa rotasi   (bidang X-Y, case_w x case_h)
//   top   -> rotate([90,0,0]) (bidang X-Z, case_w x case_t)
//   side  -> rotate([0,90,0]) (bidang Y-Z, case_h x case_t)
if (dxf_view == "front") {
    projection(cut = false) assembly(0);
} else if (dxf_view == "top") {
    projection(cut = false) rotate([90, 0, 0]) assembly(0);
} else if (dxf_view == "side") {
    projection(cut = false) rotate([0, 90, 0]) assembly(0);
} else {
    assembly();
}

// ---- Cek dimensi (jalan tiap render, lihat panel Console) ----
shell_h_check = case_t - lid_t;
hold_z_top    = wall + standoff + pcb_t + hold_h; // atas holder baterai
hold_t_fits   = hold_z_top <= shell_h_check;
hold_in_pcb   = (hold_dx + hold_w <= pcb_w) && (hold_dy + hold_l <= pcb_h);

echo(str("=== HASIL CEK DIMENSI ==="));
echo(str("Casing luar        : ", case_w, " x ", case_h, " x ", case_t, " mm"));
echo(str("Area PCB           : ", pcb_w, " x ", pcb_h, " mm"));
echo(str("Holder baterai di dalam PCB: ",
    hold_in_pcb ? "MUAT" : "KELUAR dari PCB, cek hold_dx/hold_dy"));
echo(str("Holder baterai muat di tinggi shell: shell=", shell_h_check,
    "mm, atas holder=", hold_z_top, "mm -- ",
    hold_t_fits ? "MUAT" : "NONGOL, naikkan standoff/case_t atau kecilkan lid_t"));
boost_c = pcb_xy(boost_pos[0], boost_pos[1]);
boost_in_pcb = (abs(boost_c[0]) + boost_l/2 <= pcb_w/2 + pcb_gap) && (abs(boost_c[1]) + boost_w/2 <= pcb_h/2 + pcb_gap);
echo(str("Modul boost di dalam rongga casing: ",
    boost_in_pcb ? "MUAT" : "KELUAR dari rongga -- geser atau perkecil modul"));
echo(str("Modul boost: dasar ", boost_z0, "mm di atas PCB, header U2 setinggi ", header_top,
    "mm -- ", boost_z0 > header_top ? "AMAN, tidak menimpa header" : "BENTUR header"));
echo(str("PERLU VERIFIKASI: hold_h (tinggi holder), tinggi modul boost, dan tinggi ESP32 DevKit + header."));
echo(str("PERLU VERIFIKASI: tinggi komponen di bawah modul boost (ESP32/GPS/switch) harus < ", boost_z0, "mm; panjang kabel 4 pin dari U2 ke modul ~", 40, "mm."));
