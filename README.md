# Dokumen Sistem Manajemen Keuangan Pribadi (CLI)

Alat berbasis command-line yang sederhana, aman, dan efisien untuk melacak pemasukan dan pengeluaran harian Anda.

## Fitur
- **Sederhana & Ringan**: Tidak memerlukan instalasi database berat atau library tambahan. Data disimpan dalam format JSON (`finance_data.json`) yang mudah dibaca.
- **Akses Aman**: Perlindungan dengan PIN sederhana.
- **Pelacakan Transaksi**: Catat Pemasukan dan Pengeluaran dengan kategori.
- **Anggaran (Budgeting)**: Atur anggaran dan dapatkan peringatan.
- **Laporan**: Ringkasan bulanan dan analisis pengeluaran terbesar.

## Instalasi

1.  **Prasyarat**: Pastikan Anda telah menginstal Python 3.10+.
2.  **Tanpa Dependensi**: Tidak perlu `pip install`. Semua menggunakan library bawaan Python.

## Penggunaan

Jalankan aplikasi:
```bash
python main.py
```

### Penggunaan Pertama
- Saat pertama kali dijalankan, sistem akan membuat file `finance_data.json` secara otomatis.
- Anda akan diminta untuk membuat PIN baru.

### Navigasi
- Gunakan tombol angka untuk memilih menu.
- Ikuti petunjuk di layar.

## Struktur Proyek
- `main.py`: Antarmuka CLI.
- `logic.py`: Logika bisnis.
- `database_handler.py`: Penyimpanan data (JSON).
- `data_keuangan.json`: File penyimpanan data (dibuat otomatis).
