"""Footprint Ra-02 breakout (2 deret 1x8, 2,54 mm, jarak deret 26,0 mm) -> KiCad .kicad_mod untuk diimpor ke EasyEDA.
Pad bernomor sama dengan pin simbol Ra-02 di skematik (netlist tidak berubah). Pad GND ekstra kiri-bawah diberi nomor 2 (net GND sama).
Pandangan atas, modul portrait, U.fl kiri-bawah. Ubah ROW / PITCH bila ukuran fisik beda."""
PITCH, ROW = 2.54, 26.0
TOP = [16, 15, 14, 13, 12, 11, 10, 9]   # GND NSS MOSI MISO SCK DIO5 DIO4 GND (kiri ke kanan)
BOT = [2, 2, 3, 4, 5, 6, 7, 8]          # GND GND 3.3V RST DIO0 DIO1 DIO2 DIO3
pads = []
for row, nums in ((-ROW / 2, TOP), (ROW / 2, BOT)):
    for i, n in enumerate(nums):
        x = (i - 3.5) * PITCH
        pads.append(f'  (pad "{n}" thru_hole circle (at {x:.3f} {row:.3f}) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask"))')
out = f'''(footprint "Ra02_Breakout_2x8_{ROW:g}mm" (version 20211014) (generator pandu) (layer "F.Cu")
  (fp_text reference "REF**" (at 0 -16) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value "Ra-02 breakout" (at 0 16) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text user "U.FL" (at -6 9) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
  (fp_rect (start -10.25 -14) (end 10.25 14) (layer "F.SilkS") (width 0.12) (fill none))
{chr(10).join(pads)}
)
'''
open(f"Ra02_Breakout_2x8_{ROW:g}mm.kicad_mod", "w", encoding="utf-8").write(out)
assert len(pads) == 16 and abs((ROW) - 26.0) < 1e-9
print(out)
