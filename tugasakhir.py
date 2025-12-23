import requests
import json
from datetime import datetime, timedelta

def tampilkan_header():
    """Menampilkan header aplikasi"""
    print("=" * 60)
    print("          APLIKASI JADWAL SHOLAT INDONESIA ")
    print("=" * 60)
    print()

def ambil_jadwal_sholat(kota, negara="Indonesia", tanggal=None):
    """
    Mengambil data jadwal sholat dari API Aladhan
    
    Parameters:
    - kota: Nama kota (string)
    - negara: Nama negara (default: Indonesia)
    - tanggal: Tanggal dalam format DD-MM-YYYY (opsional)
    
    Returns:
    - Dictionary berisi data jadwal sholat atau None jika gagal
    """
    try:
        
        base_url = "https://api.aladhan.com/v1/timingsByCity"
        
        params = {
            "city": kota,
            "country": negara,
            "method": 20
        }
        
        # Jika ada parameter tanggal
        if tanggal:
            params["date"] = tanggal
        
        print(f"\ Mengambil data untuk {kota}...")
        response = requests.get(base_url, params=params, timeout=10)
        
        # Cek status code
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                return data['data']
            else:
                print(" Data tidak ditemukan")
                return None
        else:
            print(f" Error: Status code {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print(" Koneksi timeout. Coba lagi nanti.")
        return None
    except requests.exceptions.ConnectionError:
        print(" Tidak dapat terhubung ke internet.")
        return None
    except Exception as e:
        print(f" Terjadi kesalahan: {str(e)}")
        return None

def tampilkan_jadwal(data):
    """
    Menampilkan jadwal sholat dalam format tabel
    
    Parameters:
    - data: Dictionary berisi data jadwal sholat
    """
    if not data:
        return
    
    timings = data['timings']
    date_info = data['date']
    
    
    print("\n" + "=" * 60)
    print(f" Tanggal: {date_info['readable']}")
    print(f" Hijriah: {date_info['hijri']['day']} {date_info['hijri']['month']['en']} {date_info['hijri']['year']}")
    print("=" * 60)
    
    
    print(f"\n{'WAKTU SHOLAT':<20} {'JAM':<15}")
    print("-" * 35)
    
    
    waktu_sholat = {
        'Fajr': 'Subuh',
        'Dhuhr': 'Dzuhur',
        'Asr': 'Ashar',
        'Maghrib': 'Maghrib',
        'Isha': 'Isya'
    }
    
    
    for key_api, nama_indo in waktu_sholat.items():
        waktu = timings[key_api].split(' ')[0] 
        print(f" {nama_indo:<17} {waktu:<15}")
    
    print("-" * 35)
    
    
    print(f"\n  Imsak (10 menit sebelum Subuh): {timings['Imsak'].split(' ')[0]}")
    print(f" Terbit Matahari (Sunrise): {timings['Sunrise'].split(' ')[0]}")
    print(f" Tengah Malam (Midnight): {timings['Midnight'].split(' ')[0]}")

def cari_waktu_terdekat(data):
    """
    Mencari waktu sholat terdekat dari waktu sekarang
    
    Parameters:
    - data: Dictionary berisi data jadwal sholat
    """
    if not data:
        return
    
    timings = data['timings']
    now = datetime.now()
    
    waktu_sholat = {
        'Subuh': timings['Fajr'],
        'Dzuhur': timings['Dhuhr'],
        'Ashar': timings['Asr'],
        'Maghrib': timings['Maghrib'],
        'Isya': timings['Isha']
    }
    
    print("\n" + "=" * 60)
    print(" WAKTU SHOLAT TERDEKAT")
    print("=" * 60)
    
    waktu_terdekat = None
    selisih_terkecil = None
    
    for nama, waktu_str in waktu_sholat.items():
        
        waktu = waktu_str.split(' ')[0]
        jam, menit = map(int, waktu.split(':'))
        
        waktu_sholat_obj = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
        
        
        selisih = (waktu_sholat_obj - now).total_seconds()
        
        
        if selisih > 0:
            if selisih_terkecil is None or selisih < selisih_terkecil:
                selisih_terkecil = selisih
                waktu_terdekat = (nama, waktu)
    
    if waktu_terdekat:
        nama, waktu = waktu_terdekat
        jam_tersisa = int(selisih_terkecil // 3600)
        menit_tersisa = int((selisih_terkecil % 3600) // 60)
        
        print(f"\n Waktu sholat terdekat: {nama} ({waktu})")
        print(f"  Sisa waktu: {jam_tersisa} jam {menit_tersisa} menit")
    else:
        print("\n Semua waktu sholat hari ini telah berlalu.")
        print("   Waktu sholat berikutnya: Subuh besok")

def tampilkan_menu():
    """Menampilkan menu pilihan"""
    print("\n" + "=" * 60)
    print("MENU:")
    print("1. Lihat jadwal sholat hari ini")
    print("2. Lihat jadwal sholat besok")
    print("3. Lihat jadwal sholat pada tanggal tertentu")
    print("4. Cari waktu sholat terdekat")
    print("5. Ganti kota")
    print("6. Keluar")
    print("=" * 60)

def main():
    """Fungsi utama program"""
    tampilkan_header()
    
    
    print("Masukkan nama kota di Indonesia:")
    print("Contoh: Jakarta, Surabaya, Bandung, Yogyakarta, Medan, dll.")
    kota = input("\n  Kota: ").strip()
    
    if not kota:
        print(" Nama kota tidak boleh kosong!")
        return
    
    
    while True:
        tampilkan_menu()
        pilihan = input("\nPilih menu (1-6): ").strip()
        
        if pilihan == "1":
            
            data = ambil_jadwal_sholat(kota)
            if data:
                tampilkan_jadwal(data)
        
        elif pilihan == "2":
            
            besok = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
            data = ambil_jadwal_sholat(kota, tanggal=besok)
            if data:
                tampilkan_jadwal(data)
        
        elif pilihan == "3":
            
            print("\nMasukkan tanggal (format: DD-MM-YYYY)")
            print("Contoh: 25-12-2024")
            tanggal = input("Tanggal: ").strip()
            
            
            if tanggal.count('-') == 2:
                data = ambil_jadwal_sholat(kota, tanggal=tanggal)
                if data:
                    tampilkan_jadwal(data)
            else:
                print(" Format tanggal salah! Gunakan format DD-MM-YYYY")
        
        elif pilihan == "4":
            
            data = ambil_jadwal_sholat(kota)
            if data:
                cari_waktu_terdekat(data)
        
        elif pilihan == "5":
            
            print("\nMasukkan nama kota baru:")
            kota_baru = input("Kota: ").strip()
            if kota_baru:
                kota = kota_baru
                print(f" Kota berhasil diganti ke: {kota}")
            else:
                print(" Nama kota tidak boleh kosong!")
        
        elif pilihan == "6":
            
            print("\n" + "=" * 60)
            print("      Terima kasih telah menggunakan aplikasi ini!")
            print("            Jangan lupa sholat tepat waktu!")
            print("=" * 60)
            break
        
        else:
            print("\n Pilihan tidak valid! Silakan pilih 1-6.")
        
        
        input("\nTekan ENTER untuk melanjutkan...")


if __name__ == "__main__":
    main()