"""Cek netlist EasyEDA (Allegro .tel) vs pin map firmware. Jalankan: python check_netlist.py"""
import re, sys
J2 = "3V3 EN IO36 IO39 IO34 IO35 IO32 IO33 IO25 IO26 IO27 IO14 IO12 GND IO13 SD2 SD3 CMD 5V".split()
J3 = "GND IO23 IO22 TX0 RX0 IO21 GND IO19 IO18 IO5 IO17 IO16 IO4 IO0 IO2 IO15 SD1 SD0 CLK".split()
FLASH = {"SD0", "SD1", "SD2", "SD3", "CMD", "CLK"}  # IO6-11 (flash), jangan dipakai

def parse(path):
    txt = open(path, encoding="utf-8").read()
    nets = {}
    for m in re.finditer(r"^'?([^'\n;]+)'?\s*;\s*((?:.|\n)*?)(?=^'?[^'\n;]+'?\s*;|\$SCHEDULE)", txt.split("$NETS")[1], re.M):
        nets[m.group(1).strip()] = re.sub(r",\s*\n", " ", m.group(2)).split()
    return nets

def devkit(pin):  # "U3.J2-15" -> "IO13"
    m = re.match(r"U\d+\.J([23])-(\d+)$", pin)
    return (J2 if m.group(1) == "2" else J3)[int(m.group(2)) - 1] if m else None

def check(path, expect):
    nets, bad = parse(path), 0
    for net, io in expect.items():
        got = {devkit(p) for p in nets.get(net, []) if devkit(p)}
        ok = got == {io}
        bad += not ok
        print(f"  {'OK ' if ok else 'ERR'} {net:10} -> {sorted(got)} (harus {io})")
    for net, pins in nets.items():
        if len(pins) == 1: print(f"  WARN net satu pin (mengambang): {net} {pins}"); 
        for p in pins:
            if devkit(p) in FLASH: bad += 1; print(f"  ERR pin flash dipakai: {net} {p}")
    return bad

pcb1 = dict(PWR_BTN="IO13", BTN_SOS="IO27", WATER_SIG="IO34", GPS_EN="IO4", XKC_EN="IO32", GPS_RX="IO17", GPS_TX="IO16",
            LORA_CS="IO5", LORA_RST="IO25", LORA_DIO0="IO26", SPI_MOSI="IO23", SPI_MISO="IO19", SPI_SCK="IO18", I2C_SDA="IO21", I2C_SCL="IO22")
# PCB3 = pure gateway (11 Nov 2026): tanpa sirine, jadi tidak ada SIREN_DRV/IO4.
pcb3 = dict(LORA_CS="IO5", LORA_RST="IO14", LORA_DIO0="IO26", SD_CS="IO33", SD_SCK="IO25", SD_MISO="IO35", SD_MOSI="IO32", SPI_MOSI="IO23", SPI_MISO="IO19", SPI_SCK="IO18")
# Pemakaian: python check_netlist.py [pcb1] [pcb2] [pcb3]   (tanpa argumen = semua board)
want = {a.lower() for a in sys.argv[1:]} or {"pcb1", "pcb2", "pcb3"}
e = 0
if "pcb1" in want:
    print("PCB1"); e += check("PCB1.tel", pcb1)
    n1 = parse("PCB1.tel"); gnd1 = set(n1.get("GND", []))
    # P1-1 / audit A2: negatif baterai hanya ke B- TP4056 (BAT_NEG), supaya proteksi DW01 tidak terlewati.
    # OUT- (U7.4) dan IN- (U7.6) ke GND sistem; B- (U7.3) dan BT1.2 TIDAK boleh di GND.
    ok = {"BT1.2", "U7.3"} <= set(n1.get("BAT_NEG", [])); e += not ok
    print(f"  {'OK ' if ok else 'ERR'} BAT_NEG = BT1.2 + U7.3 {sorted(n1.get('BAT_NEG', []))}")
    bad = {"BT1.2", "U7.3"} & gnd1; e += bool(bad)
    print(f"  {'OK ' if not bad else 'ERR'} B- dan baterai negatif tidak di GND {sorted(bad)}")
    ok = {"U7.4", "U7.6"} <= gnd1; e += not ok
    print(f"  {'OK ' if ok else 'ERR'} TP4056 OUT- (U7.4) dan IN- (U7.6) di GND")
    # P1-3 / audit A4: output XKC-Y25 (bisa 5 V) ke IO34 lewat pembagi R8 10k (seri) dan R9 20k (ke GND); R1 pull-up dihapus.
    ok = {"R8.1", "U10.1"} == set(n1.get("XKC_OUT", [])); e += not ok
    print(f"  {'OK ' if ok else 'ERR'} XKC_OUT = R8.1 + U10.1 {sorted(n1.get('XKC_OUT', []))}")
    ok = {"R8.2", "R9.1", "U3.J2-5"} == set(n1.get("WATER_SIG", [])); e += not ok
    print(f"  {'OK ' if ok else 'ERR'} WATER_SIG = R8.2 + R9.1 + IO34 (U3.J2-5) {sorted(n1.get('WATER_SIG', []))}")
    ok = "R9.2" in gnd1; e += not ok
    print(f"  {'OK ' if ok else 'ERR'} R9.2 di GND")
    r1 = [n for n, pins in n1.items() if any(p.startswith("R1.") for p in pins)]; e += bool(r1)
    print(f"  {'OK ' if not r1 else 'ERR'} R1 (pull-up lama) sudah dihapus {r1}")
if "pcb3" in want:
    print("PCB3"); e += check("PCB3.tel", pcb3)
    n3 = parse("PCB3.tel")
    if any(n.upper().startswith("SIREN") for n in n3): e += 1; print("  ERR net sirine masih ada di PCB3")
    # Ra-02 breakout: pad 1 = GND, 16 pad; pemetaan pad dari docs/LORA_RA02_BREAKOUT.md
    for net, pad in {"LORA_CS": "U1.15", "SPI_MOSI": "U1.14", "SPI_MISO": "U1.13", "SPI_SCK": "U1.12", "LORA_RST": "U1.4", "LORA_DIO0": "U1.5", "3V3": "U1.3"}.items():
        ok = pad in n3.get(net, []); e += not ok
        print(f"  {'OK ' if ok else 'ERR'} Ra-02 {pad} di {net}")
    gnd = {f"U1.{i}" for i in (1, 2, 9, 16)}; ok = gnd <= set(n3.get("GND", [])); e += not ok
    print(f"  {'OK ' if ok else 'ERR'} Ra-02 GND di pad 1,2,9,16")
    # microSD H1 (1x6): GND, 5V_SYS, MISO, MOSI, SCK, CS  (urutan pin modul fisik BELUM diverifikasi)
    for net, pad in {"GND": "H1.1", "5V_SYS": "H1.2", "SD_MISO": "H1.3", "SD_MOSI": "H1.4", "SD_SCK": "H1.5", "SD_CS": "H1.6"}.items():
        ok = pad in n3.get(net, []); e += not ok
        print(f"  {'OK ' if ok else 'ERR'} microSD {pad} di {net}")

# PCB2: tidak ada TTP223/TOUCH_SIG, negatif baterai terpisah dari GND (proteksi TP4056)
if "pcb2" in want:
    print("PCB2"); n2 = parse("PCB2.tel"); bad2 = 0
    for name, must in {"BAT_NEG": {"H2.2", "U7.3"}, "VBAT_RAW": {"J1.1", "U7.1"}, "VBAT_SW": {"J1.2", "U1.16"}}.items():
        ok = must <= set(n2.get(name, [])); bad2 += not ok
        print(f"  {'OK ' if ok else 'ERR'} {name} {sorted(n2.get(name, []))}")
    if "TOUCH_SIG" in n2: bad2 += 1; print("  ERR TOUCH_SIG masih ada")
    if {"H2.2", "U7.3"} & set(n2.get("GND", [])): bad2 += 1; print("  ERR B- atau baterai negatif masih di GND")
    # stub net satu pin (mis. $1N31 di U1.11) tidak boleh ada
    stub = {n: p for n, p in n2.items() if len(p) == 1}; bad2 += bool(stub)
    print(f"  {'OK ' if not stub else 'ERR'} tidak ada net satu pin (stub) {stub}")
    e += bad2
sys.exit(1 if e else 0)
