// Integritas + autentikasi paket LoRa PANDU (audit K2). Dipakai bersama oleh vest_node dan gateway
// (build_flags = -I../common). Format paket di udara:  <badan paket>*<8 hex>
// 8 hex = 4 byte pertama HMAC-SHA256(PANDU_KEY, badan paket). Paket tanpa tanda ini atau dengan tanda salah dibuang Gateway.
// Lapisan di bawahnya: CRC LoRa (LoRa.enableCrc) dan sync word unik (PANDU_SYNC_WORD) di kedua sisi.
//
// KUNCI: set PANDU_KEY di config.h masing-masing firmware (nilai SAMA di Vest dan Gateway, jangan di-commit).
// Tanpa config.h dipakai kunci dev di bawah, jadi cukup untuk uji meja tapi TIDAK mengautentikasi apa pun (kuncinya ada di repo).
// Keterbatasan: tidak ada perlindungan replay (paket sah yang direkam bisa dikirim ulang). Gateway hanya membuang duplikat (vest_id, seq) dalam 60 s.
#pragma once
#include <Arduino.h>
#include "mbedtls/md.h"

#ifndef PANDU_KEY
#define PANDU_KEY "pandu-dev-key-GANTI"
#define PANDU_KEY_IS_DEFAULT 1
#else
#define PANDU_KEY_IS_DEFAULT 0
#endif

constexpr uint8_t PANDU_SYNC_WORD = 0x5A;   // bukan 0x12 (default library) dan bukan 0x34 (LoRaWAN publik)
constexpr size_t  PANDU_MAC_HEX   = 8;

// Tulis 8 karakter hex + NUL ke out[9].
inline void panduMac(const char *body, size_t len, char out[PANDU_MAC_HEX + 1]) {
  uint8_t h[32];
  mbedtls_md_hmac(mbedtls_md_info_from_type(MBEDTLS_MD_SHA256),
                  (const unsigned char *)PANDU_KEY, strlen(PANDU_KEY),
                  (const unsigned char *)body, len, h);
  for (int i = 0; i < 4; i++) snprintf(out + i * 2, 3, "%02x", h[i]);
}

// Verifikasi paket "<badan>*<mac>". Bila sah, body diisi badan tanpa tanda.
inline bool panduVerify(const String &pkt, String &body) {
  int star = pkt.lastIndexOf('*');
  if (star < 0 || (size_t)(pkt.length() - star - 1) != PANDU_MAC_HEX) return false;
  char want[PANDU_MAC_HEX + 1];
  panduMac(pkt.c_str(), star, want);
  uint8_t diff = 0;   // banding waktu-konstan
  for (size_t i = 0; i < PANDU_MAC_HEX; i++) diff |= (uint8_t)(want[i] ^ pkt[star + 1 + i]);
  if (diff) return false;
  body = pkt.substring(0, star);
  return true;
}
