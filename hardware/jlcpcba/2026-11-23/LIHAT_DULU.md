# Berkas pesan JLCPCB PCBA, 23 Nov 2026

Diekspor dari salinan EasyEDA `Pandu-Capstone-v3-footprint-fix` setelah DRC 0 di PCB1, PCB2, PCB3.

- `Gerber_PCBn_*.zip`: unggah ke JLCPCB sebagai Gerber.
- `BOM_Board*_PCBn_*.xlsx`: BOM, hanya part yang dirakit JLC (modul dan holder sudah dikeluarkan lewat "Add into BOM = No"). Kolom `Supplier Part` = nomor LCSC.
- `CPL_PCBn_*.xlsx`: posisi part, sudah disaring hanya part di BOM (tanpa modul di sisi bawah). Designator `SW2(SOSButton)` diganti `SW2` di BOM dan CPL supaya cocok di JLC; label silkscreen tidak berubah.
- Belum dicek di halaman preview JLC (rotasi tiap part). Cek di sana sebelum bayar.

## Update 23 Nov malam: PCB1 versi "modul" (MT3608 dipasang rata)
- `Gerber_PCB1_modul_2026-11-23.zip` dan `CPL_PCB1_modul_2026-11-23.xlsx` menggantikan Gerber/CPL PCB1 sebelumnya. BOM PCB1 tidak berubah.
- U2 sekarang footprint `MT3608_Module_Flat_4pad` (pad 1=VIN+, 2=VIN-, 3=VOUT-, 4=VOUT+), modul di (50, 76) mm. R6 dan R7 digeser ke (43,4; 60) dan (43,4; 62,4). Semua jalur dirute ulang, DRC 0.
- DUGAAN: dimensi pad (7,2 x 31,55 mm, lubang 1,5 mm) dari gambar generik SnapMagic, belum diukur di modul fisik.
- `hardware/netlist/PCB1.tel` diperbarui dari ekspor baru; `check_netlist.py` lolos PCB1-3.
