"""Footprint modul boost MT3608 2A (pasang rata, 4 pad sudut) -> berkas impor EasyEDA Pro.
Sumber geometri: SnapMagic "Generic MT3608 DC-DC Step Up Converter 2A Booster Module" (diunduh 23 Nov 2026).
STATUS: DUGAAN. Dimensi dari gambar generik, BELUM dicocokkan dengan modul Calvin (jangka sorong). Ubah konstanta di bawah bila beda.

Pad bernomor 1..4 = pin simbol U2 (netlist PCB1 tidak berubah):
  1 = VIN+  -> VBAT_RAW      2 = VIN-  -> GND
  3 = VOUT- -> GND           4 = VOUT+ -> VBOOST_5V
Pandangan atas: VIN di kanan (x+), VOUT di kiri (x-), sama dengan sumber."""
import zipfile
X, Y = 15.775, 3.6            # pusat pad: +-X (ujung ke ujung 31,55), +-Y (jarak + ke - 7,2)
PAD_W, PAD_H, DRILL = 5.0, 3.0, 1.5
BODY_W, BODY_H = 37.15, 17.2  # badan modul (dari sumber)
NAME = "MT3608_Module_Flat_4pad"
PADS = [(1, +X, -Y), (2, +X, +Y), (3, -X, +Y), (4, -X, -Y)]
pads = [f'  (pad "{n}" thru_hole rect (at {x:.3f} {y:.3f}) (size {PAD_W} {PAD_H}) (drill {DRILL}) (layers "*.Cu" "*.Mask"))' for n, x, y in PADS]
body = f'''  (fp_text reference "REF**" (at 0 -11) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value "MT3608 module" (at 0 11) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text user "VIN+" (at 12 -6.4) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
  (fp_text user "VOUT+" (at -12 -6.4) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
  (fp_rect (start {-BODY_W/2:.3f} {-BODY_H/2:.3f}) (end {BODY_W/2:.3f} {BODY_H/2:.3f}) (layer "F.SilkS") (width 0.12) (fill none))
{chr(10).join(pads)}'''
open(f"{NAME}.kicad_mod", "w", encoding="utf-8").write(f'(footprint "{NAME}" (version 20211014) (generator pandu) (layer "F.Cu")\n{body}\n)\n')
pcb = f'''(kicad_pcb (version 20211014) (generator pcbnew)
  (general (thickness 1.6))
  (paper "A4")
  (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen") (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user) (46 "B.CrtYd" user "B.Courtyard") (47 "F.CrtYd" user "F.Courtyard") (48 "B.Fab" user) (49 "F.Fab" user))
  (setup (pad_to_mask_clearance 0))
  (net 0 "")
  (footprint "{NAME}" (layer "F.Cu") (at 100 100) (attr through_hole)
{body}
  )
)
'''
with zipfile.ZipFile(f"{NAME}_import.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("mt3608/mt3608.kicad_pcb", pcb)
    z.writestr("mt3608/mt3608.kicad_pro", "{}")
assert sorted(p[0] for p in PADS) == [1, 2, 3, 4] and "." not in NAME
print("ok:", NAME, "4 pad, ujung-ke-ujung", 2 * X, "mm, + ke -", 2 * Y, "mm")
