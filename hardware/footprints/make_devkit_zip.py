# Build a minimal KiCad 6 project zip holding the DOIT DevKit V1 30-pin footprint (pads 1..30, 25.4 mm rows)
# for EasyEDA Pro File>Import>KiCad. Pad coords from syauqibilfaqih/ESP32-DevKit-V1-DOIT (MIT); drill widened 0.8->1.0.
import zipfile, uuid
L, R, Y0, P = -11.92754, 13.47246, 17.019813, 2.54
pads = [(str(i+1), L, Y0-i*P) for i in range(15)] + [(str(i+16), R, Y0-i*P) for i in range(15)]
u = lambda: str(uuid.uuid4())
def line(x1,y1,x2,y2,layer="F.SilkS",w=0.2): return f'(fp_line (start {x1} {y1}) (end {x2} {y2}) (layer "{layer}") (width {w}) (tstamp {u()}))'
def rect(x1,y1,x2,y2,layer="F.SilkS"): return "\n    ".join([line(x1,y1,x2,y1,layer),line(x2,y1,x2,y2,layer),line(x2,y2,x1,y2,layer),line(x1,y2,x1,y1,layer)])
pad = lambda n,x,y: f'(pad "{n}" thru_hole oval (at {x:.5f} {y:.5f} 270) (size 1.524 1.9) (drill 1.0) (layers *.Cu *.Mask) (tstamp {u()}))'
fp = f'''(footprint "ESP32_DevKitV1_30P" (layer "F.Cu") (at 100 100) (tedit 0) (tstamp {u()})
    (attr through_hole)
    (fp_text reference "U**" (at 0 -28) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))) (tstamp {u()}))
    (fp_text value "ESP32_DevKitV1_30P" (at 0 28) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))) (tstamp {u()}))
    {rect(-13.33,-26.4,14.97,25.1)}
    {rect(-2.81,21.86,4.81,26.114179)}
    {chr(10).join("    "+pad(*p) for p in pads).strip()}
)'''
pcb = f'''(kicad_pcb (version 20211014) (generator pcbnew)
  (general (thickness 1.6))
  (paper "A4")
  (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen") (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user) (46 "B.CrtYd" user "B.Courtyard") (47 "F.CrtYd" user "F.Courtyard") (48 "B.Fab" user) (49 "F.Fab" user))
  (setup (pad_to_mask_clearance 0))
  (net 0 "")
  {fp}
)
'''
with zipfile.ZipFile("ESP32_DevKitV1_30P_kicad6_import.zip","w",zipfile.ZIP_DEFLATED) as z:
    z.writestr("devkit/devkit.kicad_pcb", pcb)
    z.writestr("devkit/devkit.kicad_pro", "{}")
n = pcb.count("(pad "); assert n==30 and abs((R-L)-25.4)<1e-6; print("ok",n,"pads, row gap",round(R-L,3))
