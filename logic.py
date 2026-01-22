from database_handler import DatabaseHandler
from datetime import datetime

# Class ini otak dari aplikasi kita
class FinanceManager:
    def __init__(self, db_handler):
        # Kita butuh database untuk simpan data
        self.db = db_handler

    def login(self, pin):
        # Cek apakah PIN benar?
        return self.db.cek_pin(pin)

    def buat_pin_baru(self, pin):
        self.db.atur_pin(pin)

    def cek_status_aplikasi(self):
        # Cek apakah ini pertama kali buka?
        return self.db.apakah_sudah_setup()

    def tambah_pemasukan(self, tanggal, kategori, jumlah, deskripsi, cara_bayar):
        # Panggil database untuk simpan, tipe='pemasukan'
        self.db.tambah_transaksi(tanggal, kategori, jumlah, deskripsi, cara_bayar, 'pemasukan')

    def tambah_pengeluaran(self, tanggal, kategori, jumlah, deskripsi, cara_bayar):
        # Simpan pengeluaran
        self.db.tambah_transaksi(tanggal, kategori, jumlah, deskripsi, cara_bayar, 'pengeluaran')
        
        # Setelah simpan, kita cek apakah boros?
        return self.cek_budget(tanggal, kategori)

    def set_budget(self, kategori, jumlah):
        self.db.atur_budget(kategori, jumlah)

    def cek_budget(self, tanggal_str, kategori):
        # Daftar peringatan (warning)
        pesan_peringatan = []
        
        # Ambil bulan dan tahun dari tanggal transaksi
        try:
            # Ubah teks "2023-10-01" jadi tanggal komputer
            tanggal_obj = datetime.strptime(tanggal_str, "%Y-%m-%d")
            bulan_ini = f"{tanggal_obj.year}-{tanggal_obj.month:02d}" # Jadinya "2023-10"
        except:
            return [] # Kalau tanggal salah, abaikan dulu

        # Ambil batas budget dari database
        semua_budget = self.db.ambil_semua_budget()
        
        # Kalau kategori ini punya budget, kita cek
        if kategori in semua_budget:
            batas = semua_budget[kategori]
            
            # Hitung total belanja bulan ini di kategori ini
            total_belanja = 0
            semua_transaksi = self.db.ambil_semua_transaksi()
            
            for t in semua_transaksi:
                # Cek apakah ini pengeluaran?
                # Cek apakah bulannya sama?
                # Cek apakah kategorinya sama?
                if t['tipe'] == 'pengeluaran' and \
                   t['tanggal'].startswith(bulan_ini) and \
                   t['kategori'] == kategori:
                    total_belanja += t['jumlah']
            
            # Bandingkan total dengan batas
            if total_belanja > batas:
                pesan_peringatan.append(f"AWAS: Kamu sudah BOROS di '{kategori}'! (Batas: {batas}, Terpakai: {total_belanja})")
            elif total_belanja >= (batas * 0.9): # Jika sudah pakai 90%
                pesan_peringatan.append(f"HATI-HATI: Budget '{kategori}' hampir habis. (Batas: {batas}, Terpakai: {total_belanja})")
                
        return pesan_peringatan

    def buat_laporan_bulanan(self, bulan, tahun):
        # Format bulan dan tahun biar mudah dicari "YYYY-MM"
        kode_bulan = f"{tahun}-{bulan:02d}"
        
        semua_transaksi = self.db.ambil_semua_transaksi()
        
        # Siapkan variabel penghitung
        total_masuk = 0
        total_keluar = 0
        daftar_belanja = []
        
        count_transaksi = 0

        for t in semua_transaksi:
            # Ambil yang tanggalnya cocok dengan bulan ini
            if t['tanggal'].startswith(kode_bulan):
                count_transaksi += 1
                
                if t['tipe'] == 'pemasukan':
                    total_masuk += t['jumlah']
                elif t['tipe'] == 'pengeluaran':
                    total_keluar += t['jumlah']
                    daftar_belanja.append(t)
        
        # Hitung sisa uang
        tabungan = total_masuk - total_keluar
        
        # Hitung persen tabungan (kalau ada pemasukan)
        if total_masuk > 0:
            persen_hemat = (tabungan / total_masuk) * 100
        else:
            persen_hemat = 0.0
            
        # Cari 5 pengeluaran terbesar
        # Kita urutkan daftar_belanja dari yang terbesar (reverse=True)
        daftar_belanja.sort(key=lambda x: x['jumlah'], reverse=True)
        top_5 = daftar_belanja[:5] # Ambil 5 saja
        
        # Kembalikan hasil laporan dalam bungkusan dictionary
        return {
            "total_masuk": total_masuk,
            "total_keluar": total_keluar,
            "sisa": tabungan,
            "persen_hemat": persen_hemat,
            "top_pengeluaran": top_5,
            "jumlah_transaksi": count_transaksi
        }

    # Fungsi statis (bisa dipanggil tanpa buat object)
    @staticmethod
    def cek_format_tanggal(teks_tanggal):
        try:
            # Coba ubah teks jadi tanggal
            datetime.strptime(teks_tanggal, '%Y-%m-%d')
            return True # Berhasil
        except:
            return False # Gagal
