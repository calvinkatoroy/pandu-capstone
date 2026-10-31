# AUDIT V3 PANDU (28 Okt 2026)

Cakupan: firmware Vest, Gateway, Helmet; backend dan dashboard (`pandu-dashboard`); PCB (EasyEDA); hasil uji nyata hari ini (Vest, LoRa, Gateway, Supabase lokal, dashboard).
Label bukti: **[TERBUKTI]** = terlihat di log, tes, atau kode; **[DUGAAN]** = kesimpulan dari gejala, belum dikonfirmasi di hardware.

## Hasil otomatis
| Pemeriksaan | Hasil |
|---|---|
| Dashboard `tsc -b` | Lulus |
| Dashboard vitest | 23/23 lulus |
| `npm audit --omit=dev` | 2 moderate (react-router: open redirect, deserialisasi SSR; dashboard SPA tanpa SSR, risiko rendah) |
| Build firmware Vest, Gateway (dengan `config.h`) | Lulus |
| DRC PCB1 (EasyEDA) | 0 masalah pada desain saat ini (124 item) |
| Alur ujung ke ujung: Vest, LoRa, Gateway, ingest, dashboard | Jalan (HB masuk, SOS simulasi memicu Bahaya) |

## KRITIS (keselamatan atau kehilangan data)
| # | Temuan | Akar masalah | Bukti | Perbaikan |
|---|---|---|---|---|
| K1 | **Alarm SOS/FALL/MOB bisa ditolak server dan dibuang Gateway** | `validateEvent` menolak seluruh event bila `bat_mv` di luar 2500-4500, `lat/lon/rssi` di luar rentang, termasuk event alarm. Gateway menghapus (ack) semua event dari antrean setelah HTTP 200, termasuk yang `rejected` | **[TERBUKTI]** hari ini `bat_mv=1950` menghasilkan `accepted:0, rejected`; batch dihapus dari antrean. Baterai hampir habis (<2,5 V), pembagi lepas, atau BAT_DIV salah akan membuang SOS | Server: untuk semua event, nilai non-kritis di luar rentang diubah jadi `null` (hanya `type`, `vest_id`, `seq`, `received_at` yang menolak). Gateway: event `rejected` bertipe alarm jangan dibuang diam-diam (simpan di file dead-letter dan cetak peringatan) |
| K2 | **Paket LoRa tanpa CRC, sync word, atau autentikasi** | Tidak ada `enableCrc()`, `setSyncWord()`, atau tanda tangan di Vest maupun Gateway; library Arduino-LoRa default CRC mati | **[TERBUKTI]** grep tidak menemukan satu pun panggilan itu | `LoRa.enableCrc()` dan `setSyncWord()` unik di kedua sisi. Tambah kode integritas (mis. HMAC pendek 4 byte atau checksum) agar SOS palsu dan HB palsu "Aman" tidak diterima |
| K3 | **SOS dari bangun deep sleep dikirim tanpa posisi** | `lastLat/lastLon/lastFixAt` hanya di RAM, hilang saat deep sleep; GPS baru dinyalakan saat bangun | **[TERBUKTI]** dari kode (`sendPkt`, `static` di RAM); kontrak sudah punya `pos_age_s` untuk kasus ini | Simpan posisi terakhir di `RTC_DATA_ATTR` beserta waktu, kirim dengan `pos_age_s` |
| K4 | **Deteksi jatuh gagal diam-diam** | `accelG()` mengembalikan 1,0 g bila baca gagal; `mpuOk` hanya dicek saat boot; tidak ada re-init; `mpuWrite` tidak memeriksa hasil; tidak ada cek WHO_AM_I atau baca ulang register | **[TERBUKTI]** hari ini ratusan `Wire Error 263/-1` sementara alat tampak normal (`g=1.00`). `g=4.80` saat diam (seharusnya ~1,0) | Cek `WHO_AM_I`, verifikasi register range, retry dan re-init saat gagal, kirim flag kesehatan sensor di heartbeat, kalibrasi 1 g di awal. Penyebab `g=4.8`: **[DUGAAN]** range ±8 g tidak terterap (skala 4×) ditambah toleransi modul; perlu baca register mentah untuk memastikan |

## TINGGI
| # | Temuan | Akar masalah | Bukti | Perbaikan |
|---|---|---|---|---|
| T1 | Pendaftaran akun terbuka | Tab "Daftar" aktif; semua user `authenticated` boleh membaca posisi, nama pemakai, dan insiden (RLS `auth.role() = 'authenticated'`) | **[TERBUKTI]** kode login dan migrasi 0001 | Matikan signup publik atau role awal `pending` yang tidak bisa membaca; admin menyetujui |
| T2 | Pemakai tidak tahu SOS terkirim | LoRa satu arah, tidak ada ACK, LED, atau buzzer di Vest | **[TERBUKTI]** kode | Tambah umpan balik lokal (LED/getar) dan ACK dari Gateway bila perlu |
| T3 | Sirine Gateway hanya bisa dimute lewat serial | Tidak ada tombol fisik; tabel `commands` tidak dibaca firmware | **[TERBUKTI]** kode Gateway | Tombol mute fisik; atau Gateway membaca perintah dari server |
| T4 | Upload sering timeout setelah idle | Timeout 8 s lebih pendek dari cold start fungsi | **[TERBUKTI]** `http:-11`, Kong mencatat 499 | Naikkan timeout ke 15-20 s |
| T5 | SD Gateway tidak berfungsi (`sd:0`) | Modul tidak merespons (`f_mount failed (3)`); kemungkinan VCC 5 V, wiring, atau kartu | **[TERBUKTI]** log; penyebab pasti belum diketahui | Cek VIN, D25/D35/D32/D33, kartu FAT32. Tanpa SD, antrean hanya 64 event di RAM |
| T6 | Rahasia dan konfigurasi | `setInsecure()` pada HTTPS (key rawan disadap); key dev lama pernah ada di riwayat repo; `.env.example` memuat URL project yang sudah tidak ada | **[TERBUKTI]** kode, riwayat git, DNS NXDOMAIN | Pasang CA root; rotasi key; perbarui `.env.example` |
| T7 | Migrasi 0001 membuat signup gagal | Fungsi trigger tanpa `search_path`/skema `public` | **[TERBUKTI]** "Database error saving new user", log Auth | Sudah diperbaiki di `0006_fix_signup_trigger.sql`; harus dijalankan juga di project hosted |

## SEDANG
| # | Temuan | Bukti | Perbaikan |
|---|---|---|---|
| S1 | Sensor air XKC: firmware masih memakai ambang analog 1000 mV; polaritas dan fungsi kabel hitam belum diukur; belum diuji basah | **[TERBUKTI]** kode; kering terbaca 142 mV | Uji basah, tentukan polaritas, sesuaikan kode |
| S2 | Baterai: `BAT_DIV` belum dikalibrasi; pembagi 100 k/100 k bersumber impedansi tinggi, perlu 100 nF di ADC (ada di PCB, tidak di breadboard); pembagi demo dari 3V3 bukan baterai asli | **[TERBUKTI]** angka 284-1950 mV saat pin mengambang | Kalibrasi dengan multimeter, pasang kapasitor |
| S3 | Ambang jatuh mepet offset sensor (`FREEFALL_G` 0,6 vs offset 0,3-0,5) | **[TERBUKTI]** komentar di kode | Kalibrasi awal, uji jatuh berulang |
| S4 | "Helm dipakai" hanya dari BLE + RSSI (-85 dBm) tanpa sensor pakai; helm di meja dekat Vest terbaca dipakai | **[TERBUKTI]** kode; RSSI uji -54 sampai -82 dBm | Kalibrasi ambang, pertimbangkan sensor pakai |
| S5 | Gateway: `LoRa.receive()` tidak dipanggil (mengandalkan RX_SINGLE lewat `parsePacket`); antrean RAM bisa tersangkut bila SD hidup tapi tulis gagal | **[TERBUKTI]** kode | `LoRa.receive()` sekali setelah `begin`; `qPending` perhatikan `ramQ` |
| S6 | PCB: semua jalur 10 mil; pelebaran massal ke 16/25 mil menimbulkan 188 pelanggaran DRC (sudah dibatalkan); masalah lama di `AUDIT_V2.md` (TP4056 B-/OUT-, footprint DevKit V1 dan Ra-02, SAW1, dll.) | **[TERBUKTI]** DRC | Perbesar board atau rute ulang; lebarkan jalur daya bertahap sambil cek DRC |
| S7 | Dashboard: `react-router` 2 advisori moderate | **[TERBUKTI]** `npm audit` | Perbarui bila tidak merusak |
| S8 | Banyak Vest, LoRa ALOHA tanpa ACK: tabrakan paket bila 8 Vest | desain | Jitter sudah ada; pertimbangkan ACK atau slot |

## PROSES DAN REPO
| # | Temuan | Perbaikan |
|---|---|---|
| R1 | Dua commit redesign dashboard (`redesign-peta-melayang`) hanya ada di laptop; banyak perubahan belum di-commit di dua repo (0006, config Supabase lokal, dukungan `http://` Gateway, BOM, AUDIT_V3) | Commit dan push |
| R2 | Project Supabase bersama tidak ada (NXDOMAIN lewat 1.1.1.1 dan 8.8.8.8); migrasi, fungsi `ingest`, dan secret belum ada di project aktif | Buat atau konfirmasi project, deploy |
| R3 | Dokumen eksternal (Google Doc, Canva, sheet BOM) masih menyebut 915/920 MHz; SX1278 hanya 433 MHz | Perbarui |

## Belum diverifikasi (jangan dianggap aman)
Uji basah XKC dan polarity; kalibrasi MPU di hardware; GPS fix di luar ruangan; SD card; jangkauan LoRa nyata (RSSI -87 dBm pada jarak dekat tergolong lemah, cek antena); daya baterai Vest (MT3608 dan TP4056 belum lengkap); skematik PCB2 dan PCB3 terhadap netlist; uji jatuh dan SOS dari hardware ke dashboard.
