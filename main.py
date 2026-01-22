import sys
import getpass
from datetime import datetime
from database_handler import DatabaseHandler
from logic import FinanceManager

# --- Fungsi-fungsi Pembantu Tampilan ---

def bersihkan_layar():
    # Perintah khusus untuk membersihkan terminal
    print("\033[H\033[J", end="")

def cetak_judul(judul):
    print("\n" + "="*40)
    print(f" {judul}")
    print("="*40)

def minta_input(pertanyaan):
    # Terus tanya sampai user jawab (tidak boleh kosong)
    while True:
        isi = input(pertanyaan).strip()
        if isi != "":
            return isi # Kembalikan hasil ketikan user
        print("Eits, tidak boleh kosong ya!")

def minta_angka(pertanyaan):
    # Pastikan user memasukkan angka, bukan huruf
    while True:
        try:
            return float(minta_input(pertanyaan))
        except ValueError:
            print("Harus masukkan angka ya!")

def minta_tanggal():
    pertanyaan = "Masukkan tanggal (YYYY-MM-DD) [Enter untuk hari ini]: "
    while True:
        isi = input(pertanyaan).strip()
        if isi == "":
            # Kalau kosong, pakai tanggal hari ini
            sekarang = datetime.now()
            return sekarang.strftime("%Y-%m-%d")
            
        # Cek format apakah benar YYYY-MM-DD
        if FinanceManager.cek_format_tanggal(isi):
            return isi
        print("Format salah. Contoh: 2023-12-31")

# --- Program Utama ---
class AplikasiKeuangan:
    def __init__(self):
        # Siapkan database dan logikanya
        self.db = DatabaseHandler()
        self.otak = FinanceManager(self.db)

    def mulai(self):
        bersihkan_layar()
        cetak_judul("Aplikasi Keuangan Siswa")
        
        # Bagian 1: Cek apakah perlu setup PIN baru?
        if not self.otak.cek_status_aplikasi():
            print("Selamat datang! Yuk buat PIN dulu biar aman.")
            while True:
                pin1 = input("Buat PIN (4 angka): ")
                if len(pin1) == 4 and pin1.isdigit():
                    pin2 = input("Ketik PIN lagi: ")
                    if pin1 == pin2:
                        self.otak.buat_pin_baru(pin1)
                        print("Sip, PIN tersimpan! Silakan restart.")
                        return
                    else:
                        print("Wah, PINnya beda.")
                else:
                    print("PIN harus 4 angka ya.")
        
        # Bagian 2: Login
        kesempatan = 3
        while kesempatan > 0:
            pin = getpass.getpass("Masukkan PIN kamu: ")
            if self.otak.login(pin):
                break # PIN benar, lanjut ke menu
            
            kesempatan -= 1
            print(f"PIN Salah. Sisa coba: {kesempatan} kali")
        else:
            # Kalau kesempatan habis
            print("Dilarang masuk!")
            sys.exit()

        # Bagian 3: Masuk Menu Utama
        self.menu_utama()

    def menu_utama(self):
        while True:
            cetak_judul("Menu Utama")
            print("1. Catat Pemasukan (Uang Masuk)")
            print("2. Catat Pengeluaran (Uang Keluar)")
            print("3. Lihat Laporan")
            print("4. Atur Budget (Batas Belanja)")
            print("5. Keluar")
            
            pilihan = input("\nPilih nomor (1-5): ").strip()
            
            if pilihan == '1':
                self.halaman_tambah_transaksi('pemasukan')
            elif pilihan == '2':
                self.halaman_tambah_transaksi('pengeluaran')
            elif pilihan == '3':
                self.halaman_laporan()
            elif pilihan == '4':
                self.halaman_budget()
            elif pilihan == '5':
                print("Dadah! Semangat nabung ya!")
                sys.exit()
            else:
                print("Pilih angka 1 sampai 5 saja.")

    def halaman_tambah_transaksi(self, tipe):
        judul = "Tambah Pemasukan" if tipe == 'pemasukan' else "Tambah Pengeluaran"
        cetak_judul(judul)
        
        tanggal = minta_tanggal()
        
        if tipe == 'pemasukan':
            kategori = minta_input("Kategori (Gaji/Sangu/Bonus): ").lower()
        else:
            kategori = minta_input("Kategori (Makan/Jajan/Transport): ").lower()
            
        jumlah = minta_angka("Jumlah Uang (Rp): ")
        deskripsi = input("Catatan (Boleh kosong): ") # Boleh kosong
        cara_bayar = minta_input("Bayar pakai? (Cash/Debit/OVO): ")

        if tipe == 'pemasukan':
            self.otak.tambah_pemasukan(tanggal, kategori, jumlah, deskripsi, cara_bayar)
            print("Mantap! Uang masuk dicatat.")
        else:
            # Kalau pengeluaran, bisa ada peringatan kalau boros
            peringatan = self.otak.tambah_pengeluaran(tanggal, kategori, jumlah, deskripsi, cara_bayar)
            print("Oke, pengeluaran dicatat.")
            
            if len(peringatan) > 0:
                print("\n!!! PERINGATAN !!!")
                for pesan in peringatan:
                    print(pesan)
        
        input("\nTekan Enter buat lanjut...")

    def halaman_laporan(self):
        cetak_judul("Laporan Keuangan")
        print("Mau lihat laporan bulan apa?")
        print("Format: MM-YYYY (Contoh: 10-2023)")
        
        sekarang = datetime.now()
        bulan_tahun = input(f"Langsung Enter buat bulan ini ({sekarang.month}-{sekarang.year}): ").strip()
        
        try:
            if bulan_tahun == "":
                bulan = sekarang.month
                tahun = sekarang.year
            else:
                # Pisahkan "10-2023" jadi 10 dan 2023
                parts = bulan_tahun.split('-')
                bulan = int(parts[0])
                tahun = int(parts[1])
            
            # Minta data ke Logic
            laporan = self.otak.buat_laporan_bulanan(bulan, tahun)
            
            print(f"\n--- Laporan Bulan {bulan} Tahun {tahun} ---")
            print(f"Total Masuk   : Rp {laporan['total_masuk']:,.2f}")
            print(f"Total Keluar  : Rp {laporan['total_keluar']:,.2f}")
            print(f"Sisa Uang     : Rp {laporan['sisa']:,.2f}")
            print(f"Hemat         : {laporan['persen_hemat']:.1f}%")
            print(f"Jumlah Bon    : {laporan['jumlah_transaksi']}")
            
            if len(laporan['top_pengeluaran']) > 0:
                print("\n5 Pengeluaran Paling Besar:")
                for t in laporan['top_pengeluaran']:
                    print(f"- {t['tanggal']} | {t['kategori']} | Rp {t['jumlah']:,.2f} ({t.get('deskripsi', '')})")
            else:
                print("\nBelum ada pengeluaran nih.")
                
        except:
            print("Format salah. Harusnya Angka-Angka (Contoh: 10-2023)")
            
        input("\nTekan Enter buat lanjut...")

    def halaman_budget(self):
        cetak_judul("Atur Batas Jajan")
        kategori = minta_input("Kategori apa? (Makan/Jajan): ").lower()
        batas = minta_angka(f"Maksimal boleh habis berapa buat {kategori} sebulan?: ")
        
        self.otak.set_budget(kategori, batas)
        print(f"Oke, dibatasi Rp {batas:,.2f} ya buat {kategori}.")
        input("\nTekan Enter buat lanjut...")

# Ini baris yang pertama kali dijalankan komputer
if __name__ == "__main__":
    try:
        app = AplikasiKeuangan()
        app.mulai() # Jalankan aplikasinya
    except:
        # Menangkap error kalau user tekan Ctrl+C buat keluar paksa
        print("\nKeluar aplikasi...")
