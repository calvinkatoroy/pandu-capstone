"""Footprint Ra-02 breakout (2 deret 1x8, 2,54 mm, jarak deret 25,4 mm) -> berkas untuk diimpor ke EasyEDA Pro.
Keluaran: Ra02_Breakout_2x8_25.4mm.kicad_mod (sumber) dan Ra02_Breakout_2x8_25_4mm_import.zip (File > Import > KiCad > Extract Libraries).

Pad bernomor 1..16 UNIK dan sama dengan pin simbol Ra-02 di skematik (netlist tidak berubah):
  atas  (kiri ke kanan): 16 15 14 13 12 11 10 9  = GND NSS MOSI MISO SCK DIO5 DIO4 GND
  bawah (kiri ke kanan):  1  2  3  4  5  6  7 8  = GND GND 3.3V RST DIO0 DIO1 DIO2 DIO3
(Versi 11 Nov sebelumnya menomori pad bawah 2,2,3,.. sehingga pad 1 hilang dan pad 2 ganda; diperbaiki.)
Pandangan atas, modul portrait, U.fl kiri-bawah. Nama footprint tanpa titik (format netlist Allegro tidak mendukung titik).
25,4 mm = angka tim 11 Nov (status D, belum diukur jangka sorong). Ubah ROW / PITCH bila ukuran fisik beda."""
import zipfile
PITCH, ROW = 2.54, 25.4
TOP = [16, 15, 14, 13, 12, 11, 10, 9]
BOT = [1, 2, 3, 4, 5, 6, 7, 8]
NAME = f"Ra02_Breakout_2x8_{ROW:g}mm".replace(".", "_")
pads = []
for row, nums in ((-ROW / 2, TOP), (ROW / 2, BOT)):
    for i, n in enumerate(nums):
        x = (i - 3.5) * PITCH
        pads.append(f'  (pad "{n}" thru_hole circle (at {x:.3f} {row:.3f}) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask"))')
body = f'''  (fp_text reference "REF**" (at 0 -16) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value "Ra-02 breakout" (at 0 16) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text user "U.FL" (at -6 9) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
  (fp_rect (start -10.25 -14) (end 10.25 14) (layer "F.SilkS") (width 0.12) (fill none))
{chr(10).join(pads)}'''
out = f'(footprint "{NAME}" (version 20211014) (generator pandu) (layer "F.Cu")\n{body}\n)\n'
open(f"Ra02_Breakout_2x8_{ROW:g}mm.kicad_mod", "w", encoding="utf-8").write(out)

# Zip impor: proyek KiCad 6 minimal berisi satu footprint (pola sama dengan make_devkit_zip_j2j3.py)
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
    z.writestr("ra02/ra02.kicad_pcb", pcb)
    z.writestr("ra02/ra02.kicad_pro", "{}")

nums = sorted(int(p.split('(pad "')[1].split('"')[0]) for p in pads)
assert nums == list(range(1, 17)), nums            # 16 pad, nomor unik 1..16
assert abs(ROW - 25.4) < 1e-9 and "." not in NAME
print("ok:", NAME, "16 pad unik, jarak deret", ROW, "mm")
