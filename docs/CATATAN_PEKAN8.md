# Catatan Pekan 8 (bahan laporan; belum final)

Pekan 7 dibiarkan apa adanya (kondisi 10 Okt: satu modul XL1276, belum ada modul pengganti). Semua di bawah masuk **Pekan 8**.

## Sudah terjadi (sejak 12 Okt)
- Modul dibeli: sepasang LoRa Ra-02 SX1278 433 MHz (breakout 28x20 mm), antena pegas 433 MHz U.fl 3 dBi, sensor air XKC-Y25-V. Modul XL1276 lama tidak dipakai.
- Keputusan: pita LoRa **433 MHz** (SX1278 tidak bisa 915/920). Firmware Vest, Gateway, `test_lora_one` = `433E6`. Kompilasi OK, belum diuji di hardware.
- Dokumen: `LORA_RA02_BREAKOUT.md` (pinout, pemetaan net, footprint, daftar ukur), BOM, plan, checklist, tutorial diperbarui.
- `test_lora_one` jadi tes tautan dua modul (RX dengan RSSI/SNR).
- Dashboard (repo pandu-dashboard): audit keamanan dan perbaikan (role profil, device key, insiden ganda, validasi ingest, aturan helm 30 s, rate limit, batch insert), 21 tes lolos.

- Firmware paket v2: Vest (vest_id, seq di RTC, paket OFF, jitter heartbeat) dan Gateway (parse v1/v2, buang duplikat radio, NTP, antrean microSD, unggah batch HTTPS ke Edge Function). Kompilasi OK; **belum diuji di hardware maupun terhadap Supabase asli**.
- Perbaikan kontrak: kunci idempotensi diubah ke (gateway_id, vest_id, seq, received_at) karena seq 16-bit berulang (migrasi 0005 di pandu-dashboard).

## Belum (jangan ditulis sebagai selesai)
- Tes tautan LoRa dua modul (RSSI, SNR, jarak nyata).
- Ukur jarak deret header breakout, ukur output XKC-Y25-V (kering/basah).
- Footprint PCB1/PCB3 diganti, DRC, Gerber baru.
- Migrasi 0003/0004 dan deploy Edge Function di Supabase (menunggu Rafif/tim).
- Regulasi 433 MHz dicek, deck dan Google Doc disesuaikan.

- XKC-Y25-V: spesifikasi dari halaman produk resmi (digital, 5-24 V, dinding <= 20 mm); sisa: ukur tegangan OUT dan fungsi kawat hitam. PCB1 perlu header XH 4 pin, pembagi R8/R9, kapasitor di VBOOST_5V.
