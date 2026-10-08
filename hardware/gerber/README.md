# Gerber

JANGAN dipesan, semua versi di bawah memuat masalah yang diaudit di docs/AUDIT_V2.md:
- footprint LoRa RA-02 tidak cocok dengan modul XL1276 (RFM95), PCB1 dan PCB3
- proteksi TP4056 terlewati (B- dan OUT- digabung GND), PCB1 dan PCB2
- SAW1 di PCB2 adalah filter SMD, bukan saklar
- TTP223 di PCB2 tidak dipakai lagi

`_obsolete/` = versi lama. Gerber valid berikutnya dibuat dari branch `v3` setelah revisi EasyEDA (docs/PLAN_REVISI.md).
Berkas yang masih ada di folder ini (Gerber_PCB1_2026-10-06, Gerber_PCB2_2026-10-08, Gerber_PCB3_2026-10-06) adalah yang TERBARU sebelum revisi, tetap belum boleh dipesan.
