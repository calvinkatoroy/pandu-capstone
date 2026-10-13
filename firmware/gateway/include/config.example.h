// Salin ke config.h (di-gitignore) lalu isi. Tanpa config.h Gateway tetap jalan offline (serial, SD, sirine) tanpa upload.
#pragma once
#define WIFI_SSID    "nama-wifi"
#define WIFI_PASS    "password-wifi"
#define GATEWAY_ID   "GW1"                                                // harus ada di tabel gateways (seed.sql)
#define INGEST_URL   "https://<project-ref>.supabase.co/functions/v1/ingest"
#define DEVICE_KEY   "isi-dengan-GATEWAY_DEVICE_KEY"                      // sama dengan secret Edge Function; jangan di-commit
