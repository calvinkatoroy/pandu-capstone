import subprocess, re
import os; D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D); NG = os.environ.get("NGSPICE","ngspice")
def sim(net, probes):
    open("t.cir","w").write(net + "\n.op\n.control\nrun\n" + "\n".join(f"print {p}" for p in probes) + "\n.endc\n.end\n")
    out = subprocess.run([NG,"-b","t.cir"],capture_output=True,text=True).stdout
    r = {}
    for p in probes:
        m = re.search(re.escape(p)+r"\s*=\s*([-+0-9.e]+)", out, re.I)
        r[p] = float(m.group(1)) if m else None
    return r

# GPS high-side PMOS (AO3401A-like), gate pull-up 100k ke VBAT, GPIO menggerakkan gate
print("== GPS via Q1 (PMOS, beban 80 ohm ~ 50 mA) ==")
print("Vth  VBAT  GPIO(gate drive) -> V_GPS  I_GPS(mA)")
for vth in (-0.5,-0.9,-1.3):
    for vb in (3.0,4.2):
        for mode in ("GPIO=0V (ON)","GPIO=3.3V (drive high)","GPIO hi-Z (sleep)"):
            drv = {"GPIO=0V (ON)":"VG g1x 0 0\nRG g1x g1 100","GPIO=3.3V (drive high)":"VG g1x 0 3.3\nRG g1x g1 100","GPIO hi-Z (sleep)":""}[mode]
            net=f"""*gps
.model PM PMOS (level=1 vto={vth} kp=2.5 lambda=0.01)
VBAT vbat 0 {vb}
RPU vbat g1 100k
{drv}
M1 gpsv g1 vbat vbat PM W=1 L=1
RGPS gpsv 0 80"""
            v = sim(net,["v(gpsv)"])["v(gpsv)"]
            print(f"{vth:5} {vb:4}  {mode:24} -> {v:6.3f} V  {v/80*1000:6.2f} mA")

# XKC: PMOS Q2 (5V) + NMOS Q5 level shift, gate Q2 pull-up 10k ke 5V, Q5 gate pull-down 100k
print("\n== XKC-Y25 via Q2 + Q5 (VBOOST 5V, beban 5V/10 mA=500 ohm) ==")
for vth in (-0.5,-0.9,-1.3):
    for en in ("XKC_EN=3.3V (ON)","XKC_EN=0V (OFF)","XKC_EN hi-Z (sleep)"):
        drv={"XKC_EN=3.3V (ON)":"VE en 0 3.3","XKC_EN=0V (OFF)":"VE en 0 0","XKC_EN hi-Z (sleep)":""}[en]
        net=f"""*xkc
.model PM PMOS (level=1 vto={vth} kp=2.5 lambda=0.01)
.model NM NMOS (level=1 vto=2.1 kp=0.3 lambda=0.01)
V5 v5 0 5
{drv}
RPD en 0 100k
RPU2 v5 g2 10k
M5 g2 en 0 0 NM W=1 L=1
M2 xkc g2 v5 v5 PM W=1 L=1
RL xkc 0 500"""
        v = sim(net,["v(xkc)"])["v(xkc)"]
        print(f"{vth:5}  {en:22} -> {v:6.3f} V")
