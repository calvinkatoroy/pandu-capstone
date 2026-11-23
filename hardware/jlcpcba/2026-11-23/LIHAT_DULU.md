# Berkas pesan JLCPCB PCBA, 23 Nov 2026

Diekspor dari salinan EasyEDA `Pandu-Capstone-v3-footprint-fix` setelah DRC 0 di PCB1, PCB2, PCB3.

- `Gerber_PCBn_*.zip`: unggah ke JLCPCB sebagai Gerber.
- `BOM_Board*_PCBn_*.xlsx`: BOM, hanya part yang dirakit JLC (modul dan holder sudah dikeluarkan lewat "Add into BOM = No"). Kolom `Supplier Part` = nomor LCSC.
- `CPL_PCBn_*.xlsx`: posisi part, sudah disaring hanya part di BOM (tanpa modul di sisi bawah). Designator `SW2(SOSButton)` diganti `SW2` di BOM dan CPL supaya cocok di JLC; label silkscreen tidak berubah.
- Belum dicek di halaman preview JLC (rotasi tiap part). Cek di sana sebelum bayar.
