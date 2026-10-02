// ============================================================
// P.A.N.D.U — Helmet Node Casing (v3: Euroslot mount, PERKIRAAN)
// Komponen: ESP32-C3 SuperMini + CR2032 (badan modul)
//           + TTP223 (pad terpisah, kabel flex ke harness webbing)
// ============================================================
// MOUNTING: pakai slot aksesoris universal "Euroslot" di sisi shell
// helm (lebar 30mm, standar lintas-brand -- earmuff/faceshield pakai
// slot yang sama). Ini titik pasang AMAN krn di luar zona benturan
// crown (celah shell-harness 25-32mm wajib kosong, ANSI Z89.1).
//
// TTP223 TIDAK lagi di badan modul ini -- ditaruh di pad kecil
// terpisah + kabel flex pendek ke webbing harness (titik yang
// beneran deket/nempel kepala). Nggak dimodelkan detail di sini,
// cuma catatan posisi.
//
// PERKIRAAN yang masih perlu diverifikasi:
//   - Kedalaman & ketebalan slot Euroslot (lebar 30mm relatif pasti,
//     tapi depth/thickness tab blade belum ketemu data resminya)
//   - Panjang kabel flex TTP223 ke titik kontak harness
// ============================================================

/* [Render Control] */
explode_factor = 0; // [0:0.1:3]
dxf_view = "none"; // [none, front, top, side]

/* [Dimensi Casing utama (mm)] */
case_w   = 34;   // badan modul, muat ESP32-C3 SuperMini + CR2032
case_h   = 24;
case_t   = 11;  // direvisi dari 9mm -- 9mm nggak cukup buat MCU(4mm)+baterai(3.2mm)+dinding 2x
corner_r = 6;
wall     = 1.5;
lid_t    = 1.5;

/* [Euroslot tab (PERKIRAAN kedalaman & tebal, lebar 30mm cukup pasti)] */
slot_w = 30;   // standar Euroslot, lintas-brand
slot_t = 2.5;  // PERKIRAAN -- verifikasi ke slot fisik
slot_depth = 10; // PERKIRAAN -- seberapa dalam tab masuk ke slot

/* [ESP32-C3 SuperMini] */
mcu_w = 22.5;
mcu_h = 18;
mcu_t = 4;

/* [CR2032] */
batt_d = 20;
batt_t = 3.2;

avail_w = case_w - wall*2;
avail_h = case_h - wall*2;

module rounded_rect(w, h, r) {
    offset(r = r) offset(delta = -r) square([w, h], center = true);
}

module bottom_shell() {
    shell_h = case_t - lid_t;
    difference() {
        linear_extrude(height = shell_h) rounded_rect(case_w, case_h, corner_r);
        translate([0, 0, wall - 0.02])
            linear_extrude(height = shell_h)
                offset(delta = -wall) rounded_rect(case_w, case_h, corner_r);
    }
}

module lid() {
    linear_extrude(height = lid_t) rounded_rect(case_w, case_h, corner_r);
}

// Tab Euroslot -- blade pipih menonjol dari belakang casing
module euroslot_tab() {
    translate([0, 0, -slot_depth/2])
        cube([slot_w, slot_t, slot_depth], center = true);
}

module mcu_board() {
    translate([0, 0, 0])
        cube([mcu_w, mcu_h, mcu_t], center = true);
}

module battery() {
    translate([0, 0, 0])
        cylinder(d = batt_d, h = batt_t, center = true, $fn = 48);
}

module assembly(explode = explode_factor) {
    shell_h = case_t - lid_t;

    color("SteelBlue") bottom_shell();
    color("Gray") euroslot_tab();

    translate([0, 0, wall + mcu_t/2 + explode*10])
        color("LimeGreen") mcu_board();

    translate([0, 0, wall + mcu_t + batt_t/2 + explode*20])
        color("Orange") battery();

    translate([0, 0, shell_h + explode*35])
        color([0.27, 0.31, 0.47, 0.85]) lid();
}

if (dxf_view == "front") {
    projection(cut = false) assembly(0);
} else if (dxf_view == "top") {
    projection(cut = false) rotate([90, 0, 0]) assembly(0);
} else if (dxf_view == "side") {
    projection(cut = false) rotate([0, 90, 0]) assembly(0);
} else {
    assembly();
}

// ---- Cek dimensi (MCU + baterai ditumpuk krn slot mount = casing sempit) ----
w_fits = max(mcu_w, batt_d) <= avail_w;
h_fits = max(mcu_h, batt_d) <= avail_h;
t_needed = wall + mcu_t + batt_t + wall;
t_fits = t_needed <= case_t;
slot_ok = slot_w <= case_w;

echo(str("=== HASIL CEK DIMENSI HELMET NODE (v3, Euroslot mount, PERKIRAAN) ==="));
echo(str("Lebar casing: ", case_w, " mm | komponen terlebar: ", max(mcu_w, batt_d), " mm -- ",
    w_fits ? "MUAT" : "TERLALU SEMPIT"));
echo(str("Tinggi casing: ", case_h, " mm | komponen tertinggi: ", max(mcu_h, batt_d), " mm -- ",
    h_fits ? "MUAT" : "TERLALU PENDEK"));
echo(str("Tebal casing: ", case_t, " mm | butuh (MCU+baterai ditumpuk+dinding): ", t_needed, " mm -- ",
    t_fits ? "MUAT" : "TERLALU TIPIS, naikkan case_t"));
echo(str("Slot Euroslot 30mm muat di lebar casing ", case_w, "mm: ", slot_ok ? "YA" : "TIDAK, lebarkan case_w"));
echo("CATATAN: slot_t & slot_depth masih PERKIRAAN. TTP223 dipasang terpisah (pad + flex cable ke harness webbing), tidak termodelkan di file ini.");
