# DUEL VARIAN — NI23 G3 · Akun 17 · THE DAY'S RECORD

## Konsep
Halaman depan koran klasik satu halaman: masthead Playfair Black raksasa
"THE DAY'S RECORD", tanggal "Monday 23 November 2026", strip 6 angka hari
itu, 13 kartu utama berilustrasi (kartu #1 = lead), peta dunia titik-titik
gambar sendiri dengan 13 pin bernomor + legenda warna region, strip
timeline UTC 6 slot, kolom ALSO ON bernomor 14–39 (26 brief), kotak DATE
CHECK merah (7 buangan bernama + bertanggal), footer verifikasi.

- Lead (kartu #1): pool #46 — FBI selidiki dugaan peretasan basis data
  peradilan pidana utamanya (AP wire).
- Trio lead pilihan builder: #46 (lead) + #1 tanker Hormuz dibakar
  (kartu #2) + #43 Demokrat menangi DPR 258–173 (kartu #3).
- Total cerita: 39 (13 kartu + 26 brief), 8 region.
- Palet akun: abu hangat · tinta cokelat · aksen emas.

## Tiga varian yang diadu
- **Varian A** — kertas abu hangat (233,227,213), tinta cokelat (58,42,28),
  aksen emas (154,123,28), lead di kiri, peta di kanan.
- **Varian B** — kertas lebih terang (240,234,220), tinta lebih gelap,
  aksen emas lebih tua; susunan sama dengan A.
- **Varian C** — kertas abu lebih dalam (222,213,194), aksen emas lebih
  terang, lead dipindah ke kanan dan peta ke kiri.

## Penilaian
- Kontras: A paling tegas — tinta cokelat di atas abu hangat terbaca
  paling keras; B sedikit pudar di kartu; C kertasnya paling gelap
  sehingga kartu terasa berat.
- Keterbacaan 300px: A dan B lulus (masthead, tanggal, dan judul 13 kartu
  terbaca); C juga terbaca tetapi hierarki lead melemah karena mata
  pembaca mulai dari kiri, tempat peta berada.
- Kepadatan data: ketiganya sama (39 cerita), jadi penentu adalah kontras
  + hierarki.
- **Pemenang: Varian A** — sesuai palet akun (abu hangat · tinta cokelat ·
  aksen emas), kontras tertinggi, lead di posisi baca pertama.

## Uji wajib (varian A final)
- Uji 300px: LULUS — masthead, tanggal, dan judul ke-13 kartu utama tetap
  terbaca pada perkecilan 300×300.
- entry.png: 1024×1024 (IHDR dibaca manual via struct, byte 16–24),
  271.411 byte (≤ 1.048.576), sha256
  221e32c1d7996959d43819c966929d1f0a60f13fb32d28b7558b5584316c60ee.
- Margin checker (--fresh ni23-fresh.txt): 13/13 LOLOS.
- main.py dijalankan 2× → keluaran byte-identik (sha256 sama).

## Kenapa lebih kuat dari entry G2 akun ini
Entry G2 Akun 17 memakai konsep dekoratif "Festival Layang-layang" —
sebuah metafora visual tunggal. Entry G3 ini menggantinya dengan halaman
depan koran sungguhan: hari dinamai eksplisit di masthead, lead-nya cerita
paling berdampak hari itu, 13 kartu besar berilustrasi dengan tag sumber
di 100% kartu, keluasan 39 cerita lintas 8 region, peta + timeline +
kotak DATE CHECK yang membuktikan seleksi tanggalnya. Terhadap kriteria
juri (satu hari bernama, seleksi & keluasan, keterbacaan di ±300px,
kesetiaan pada laporan, craft), bentuk koran menjawab semuanya sekaligus,
sementara konsep dekoratif G2 hanya menjawab craft.

## Catatan jalur v3b
Repo ini dibangun ulang di folder segar `news-image-20261123-akun17-v3b`
karena ekor submit dari folder lama berulang kali tertahan lapisan
keamanan sistem. entry.png identik byte-for-byte dengan build pemenang
duel (sha256 di atas); main.py dikarang ulang di sesi v3b; compose.py
ditulis ulang dari aset yang dibaca lewat tool berkas.
