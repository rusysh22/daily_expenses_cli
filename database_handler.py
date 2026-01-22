import json
import os
import hashlib

# Kita buat class (wadah) untuk mengurus semua urusan Save/Load data
class DatabaseHandler:
    def __init__(self, nama_file="data_keuangan.json"):
        # Ini dijalankan pertama kali saat DatabaseHandler dipanggil
        self.nama_file = nama_file
        
        # Struktur data awal (kosong)
        # Kita pakai Dictionary (kamus) biar gampang
        self.data = {
            "pengaturan": {},       # Untuk simpan PIN
            "transaksi": [],        # Untuk daftar belanja/gaji
            "anggaran": {}          # Untuk batas budget
        }
        
        # Coba buka file lama, kalau tidak ada buat baru
        self.buka_database()

    def buka_database(self):
        # Cek apakah file sudah ada?
        if os.path.exists(self.nama_file):
            # Kalau ada, kita baca isinya
            try:
                with open(self.nama_file, 'r') as file:
                    self.data = json.load(file)
            except:
                # Kalau gagal baca (file rusak), kita buat baru aja
                print("File rusak, membuat database baru...")
                self.simpan_database()
        else:
            # Kalau belum ada, kita simpan data kosong tadi
            self.simpan_database()

    def simpan_database(self):
        # Menyimpan data di memori ke dalam file jadi permanen
        with open(self.nama_file, 'w') as file:
            # indent=4 biar tulisannya rapi menjorok ke dalam
            json.dump(self.data, file, indent=4)

    def atur_pin(self, pin_angka):
        # Kita ubah PIN jadi kode rahasia (hash) biar tidak bisa dibaca orang
        # sha256 itu algoritma pengacaknya
        kode_rahasia = hashlib.sha256(pin_angka.encode()).hexdigest()
        
        self.data["pengaturan"]["pin"] = kode_rahasia
        self.simpan_database() # Jangan lupa disimpan!

    def cek_pin(self, pin_input):
        # Kita acak input user dengan cara yang sama
        kode_input = hashlib.sha256(pin_input.encode()).hexdigest()
        
        # Ambil kode rahasia yang asli dari data
        kode_asli = self.data["pengaturan"].get("pin")
        
        # Bandingkan, kalau sama berarti PIN benar
        if kode_input == kode_asli:
            return True
        else:
            return False

    def apakah_sudah_setup(self):
        # Cek apakah sudah ada PIN tersimpan?
        if "pin" in self.data["pengaturan"]:
            return True
        else:
            return False

    def tambah_transaksi(self, tanggal, kategori, jumlah, deskripsi, cara_bayar, tipe):
        # Hitung ID (nomor urut) otomatis
        id_baru = len(self.data["transaksi"]) + 1
        
        # Bungkus data dalam dictionary
        transaksi_baru = {
            "id": id_baru,
            "tanggal": tanggal,
            "kategori": kategori,
            "jumlah": jumlah,
            "deskripsi": deskripsi,
            "cara_bayar": cara_bayar,
            "tipe": tipe # 'pemasukan' atau 'pengeluaran'
        }
        
        # Masukkan ke dalam list transaksi
        self.data["transaksi"].append(transaksi_baru)
        self.simpan_database()

    def ambil_semua_transaksi(self):
        # Berikan semua data transaksi ke peminta
        return self.data["transaksi"]

    def atur_budget(self, kategori, batas_jumlah):
        # Simpan batas uang untuk kategori tertentu
        self.data["anggaran"][kategori] = batas_jumlah
        self.simpan_database()

    def ambil_semua_budget(self):
        return self.data["anggaran"]
