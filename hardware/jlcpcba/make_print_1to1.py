"""PDF cetak 1:1 (A4, skala 100%) PCB1-3 dari Gerber + FlyingProbeTesting.json.
Pakai: python make_print_1to1.py  ->  cetak_1to1_PCB1-3.pdf (3 halaman, satu papan per halaman).
Isi: garis papan, silkscreen (garis dan lingkaran), pad (SMD terisi abu, THT berlingkar dengan lubang bersilang), batang skala 100 mm.
Cetak dengan 'Ukuran sebenarnya / Actual size / 100%', BUKAN 'Fit to page'. Cek batang 100 mm dengan penggaris."""
import json, math, re, sys, zipfile
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

BASE = "2026-11-23/"
BOARDS = [("PCB1 Vest Node (versi modul MT3608)", BASE + "Gerber_PCB1_modul_2026-11-23.zip"),
          ("PCB2 Helmet Node", BASE + "Gerber_PCB2_2026-11-23.zip"),
          ("PCB3 Edge Gateway", BASE + "Gerber_PCB3_2026-11-23.zip")]
A4W, A4H = 210.0, 297.0


def gerber_strokes(text):
    """Kembalikan (strokes[(lebar, [(x,y)..])], flashes[(x,y,diam)], bbox) dari Gerber mm 4.5."""
    assert "MOMM" in text or "Dimensions in millimeters" in text
    fs = re.search(r"%FSLAX(\d)(\d)Y(\d)(\d)\*%", text)
    dec = int(fs.group(2)); div = 10.0 ** dec
    ap = {}
    for m in re.finditer(r"%ADD(\d+)([CR]),([\d.]+)(?:X([\d.]+))?\*%", text):
        ap[m.group(1)] = (m.group(2), float(m.group(3)), float(m.group(4) or m.group(3)))
    body = re.sub(r"%[^%]*%", "", text)
    body = re.sub(r"G04[^*]*\*", "", body)
    strokes, flashes = [], []
    x = y = 0.0; cur = None; mode = 1; line = None
    for cmd in body.split("*"):
        cmd = cmd.strip()
        if not cmd or cmd.startswith("M02"):
            continue
        m = re.fullmatch(r"(?:G54)?D(\d+)", cmd)
        if m and int(m.group(1)) >= 10:
            cur = m.group(1); continue
        m = re.fullmatch(r"(?:G(0[123]))?(?:X(-?\d+))?(?:Y(-?\d+))?(?:I(-?\d+))?(?:J(-?\d+))?(?:D0([123]))?", cmd)
        if not m:
            continue
        g, X, Y, I, J, d = m.groups()
        if g: mode = int(g)
        nx = int(X) / div if X is not None else x
        ny = int(Y) / div if Y is not None else y
        w = ap.get(cur, ("C", 0.15, 0.15))[1]
        if d == "2":
            line = None
        elif d == "3":
            flashes.append((nx, ny, w)); line = None
        elif d == "1" or (d is None and (X is not None or Y is not None)):
            if line is None or line[0] != w:
                line = (w, [(x, y)]); strokes.append(line)
            if mode == 1 or I is None:
                line[1].append((nx, ny))
            else:
                cx, cy = x + int(I) / div, y + int(J or 0) / div
                r = math.hypot(x - cx, y - cy)
                a0 = math.atan2(y - cy, x - cx); a1 = math.atan2(ny - cy, nx - cx)
                if mode == 2:  # searah jarum jam
                    while a1 >= a0: a1 -= 2 * math.pi
                else:
                    while a1 <= a0: a1 += 2 * math.pi
                n = max(6, int(abs(a1 - a0) / (math.pi / 24)))
                for k in range(1, n + 1):
                    a = a0 + (a1 - a0) * k / n
                    line[1].append((cx + r * math.cos(a), cy + r * math.sin(a)))
        x, y = nx, ny
    return strokes, flashes


def build(zpath, title, c, page):
    z = zipfile.ZipFile(zpath)
    names = {n.split("/")[-1]: n for n in z.namelist()}
    rd = lambda n: z.read(names[n]).decode("utf-8", "replace")
    out, _ = gerber_strokes(rd("Gerber_BoardOutlineLayer.GKO"))
    pts = [p for s in out for p in s[1]]
    xmin, xmax = min(p[0] for p in pts), max(p[0] for p in pts)
    ymin, ymax = min(p[1] for p in pts), max(p[1] for p in pts)
    bw, bh = xmax - xmin, ymax - ymin
    ox, oy = 15.0, A4H - 25.0 - bh          # pojok kiri-bawah papan di halaman (mm)
    T = lambda px, py: ((ox + px - xmin) * mm, (oy + py - ymin) * mm)
    assert bw < A4W - 20 and bh < A4H - 90, "papan tidak muat A4"

    c.setPageSize((A4W * mm, A4H * mm))
    # papan
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.5)
    for w, p in out:
        pp = c.beginPath(); pp.moveTo(*T(*p[0]))
        for q in p[1:]: pp.lineTo(*T(*q))
        c.drawPath(pp, stroke=1, fill=0)
    # silkscreen atas
    sk, fl = gerber_strokes(rd("Gerber_TopSilkscreenLayer.GTO"))
    c.setStrokeColorRGB(0.35, 0.35, 0.35)
    for w, p in sk:
        c.setLineWidth(max(w, 0.12) * mm)
        pp = c.beginPath(); pp.moveTo(*T(*p[0]))
        for q in p[1:]: pp.lineTo(*T(*q))
        c.drawPath(pp, stroke=1, fill=0)
    # pad dari data flying probe (mil -> mm)
    d = json.load(open_probe(z, names))
    seen = set()
    for r in d["pins"]["rows"]:
        key = (r[1], round(r[2]), round(r[3]))
        if key in seen: continue
        seen.add(key)
        px, py = r[2] * 0.0254, r[3] * 0.0254
        sx, sy = r[9] * 0.0254, r[10] * 0.0254
        if int(round(r[13] or 0)) % 180 == 90: sx, sy = sy, sx
        X, Y = T(px, py)
        thru = (r[11] or 0) > 0
        c.setLineWidth(0.25 * mm)
        if thru:
            c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(1, 1, 1)
        else:
            c.setStrokeColorRGB(0.2, 0.2, 0.2); c.setFillColorRGB(0.82, 0.82, 0.82)
        if r[8] == "C":
            c.circle(X, Y, sx / 2 * mm, stroke=1, fill=1)
        else:
            c.rect(X - sx / 2 * mm, Y - sy / 2 * mm, sx * mm, sy * mm, stroke=1, fill=1)
        if thru:
            hd = r[11] * 0.0254
            c.setLineWidth(0.2 * mm); c.setFillColorRGB(1, 1, 1)
            c.circle(X, Y, hd / 2 * mm, stroke=1, fill=1)
            c.line(X - 0.9 * mm, Y, X + 0.9 * mm, Y); c.line(X, Y - 0.9 * mm, X, Y + 0.9 * mm)
    # lubang tak berpad (lubang baut) dari GKO tidak ada; pad THT besar sudah tergambar
    # teks info + batang skala
    c.setFillColorRGB(0, 0, 0); c.setStrokeColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12); c.drawString(15 * mm, (A4H - 12) * mm, f"{title}  |  halaman {page}/3")
    c.setFont("Helvetica", 9)
    c.drawString(15 * mm, (A4H - 18) * mm, f"Papan {bw:.2f} x {bh:.2f} mm, tampak atas (top). CETAK 100% / Actual size, BUKAN 'Fit to page'. 23 Nov 2026.")
    c.setLineWidth(0.4 * mm)
    y0 = 32.0
    c.line(15 * mm, y0 * mm, 115 * mm, y0 * mm)
    for k in range(0, 101, 10):
        h = 3 if k % 50 == 0 else 1.8
        c.line((15 + k) * mm, y0 * mm, (15 + k) * mm, (y0 + h) * mm)
    c.setFont("Helvetica", 8)
    c.drawString(15 * mm, (y0 - 4.5) * mm, "Batang skala: harus tepat 100 mm di penggaris. Tidak 100 mm = skala printer salah, atur ulang.")
    c.drawString(15 * mm, (y0 - 9) * mm, "Cara uji: taruh modul di atas kertas, tusuk lubang pinnya; pin harus masuk ke lingkaran lubang bersilang.")
    c.showPage()


def open_probe(z, names):
    import io
    return io.TextIOWrapper(io.BytesIO(z.read(names["FlyingProbeTesting.json"])), encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    c = canvas.Canvas("cetak_1to1_PCB1-3.pdf", pagesize=(A4W * mm, A4H * mm))
    for i, (t, z) in enumerate(BOARDS, 1):
        build(z, t, c, i)
        print("ok", t)
    c.save()
    print("tersimpan: cetak_1to1_PCB1-3.pdf")
