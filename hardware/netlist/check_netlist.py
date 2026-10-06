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
pcb3 = dict(LORA_CS="IO5", LORA_RST="IO14", LORA_DIO0="IO26", SD_CS="IO13", SIREN_DRV="IO4", SPI_MOSI="IO23", SPI_MISO="IO19", SPI_SCK="IO18")
print("PCB1"); e = check("PCB1.tel", pcb1)
print("PCB3"); e += check("PCB3.tel", pcb3)
sys.exit(1 if e else 0)
