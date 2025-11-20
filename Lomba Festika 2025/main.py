import csv
import random
import os
import sys
import time


R = "\033[0m"         
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def warna(text, color):
    return f"{color}{text}{R}"



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def getch():
    try:
        
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    except ImportError:
  
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch


def loading_animation(text, duration=1.9):
    print(f"\n{CYAN}{text}{R}", end='', flush=True)
    for _ in range(int(duration / 0.5)):
        print(f"{CYAN}.{R}", end='', flush=True)
        time.sleep(0.2)
    print('')  



def normalisasi(teks):
    return teks.lower().replace(" ", "")


def cek_cocok_per_bahan(input_bahan, row):
    bahan_list = [normalisasi(b) for b in input_bahan.split()]
    nama = normalisasi(row[0])
    bahan_utama = normalisasi(row[7])
    bahan_tambahan = normalisasi(row[8])
    instruksi = normalisasi(row[12])

    matched, unmatched = [], []
    for b in bahan_list:
        if b in nama or b in bahan_utama or b in bahan_tambahan or b in instruksi:
            matched.append(b)
        else:
            unmatched.append(b)
    return matched, unmatched


def cek_cocok_dan_filter_bahan(input_bahan, data_rows):
    hasil = []
    for row in data_rows:
        if len(row) < 13:
            continue
        matched, _ = cek_cocok_per_bahan(input_bahan, row)
        if matched:
            hasil.append(row)
    return hasil


def dapatkan_berdasarkan_budget(input_budget, data_rows, jumlah=10):
    try:
        budget = int(input_budget)
    except ValueError:
        return [], 0

    valid_rows = []
    for row in data_rows:
        if len(row) >= 13 and row[9].strip().isdigit():
            harga = int(row[9])
            if harga <= budget:
                valid_rows.append((row, harga))

    valid_rows.sort(key=lambda x: x[1])
    sampled = random.sample(valid_rows, min(jumlah, len(valid_rows)))
    return [row for row, _ in sampled], budget


def tampilkan_tabel_gizi(kalori, protein, lemak, karbo, serat):
    print(f"\n{BOLD}{UNDERLINE}📊 Nilai Gizi (per porsi){R}")
    print(f"{YELLOW}╔══════════════╦════════════╗{R}")
    print(f"{YELLOW}║ {CYAN}{'Nutrisi':<12}{YELLOW} ║ {GREEN}{'Jumlah':<10}{YELLOW} ║{R}")
    print(f"{YELLOW}╠══════════════╬════════════╣{R}")
    rows = [
        ("Kalori",     f"{kalori} kkal", ""),
        ("Protein",    f"{protein} g",   GREEN),
        ("Lemak",      f"{lemak} g",     YELLOW),
        ("Karbohidrat",f"{karbo} g",     BLUE),
        ("Serat",      f"{serat} g",     CYAN),
    ]
    
    for label, nilai, col in rows:
        warna_nilai = col if col else ""
        print(f"{YELLOW}║ {label:<12} ║ {warna_nilai}{nilai:>10}{YELLOW} ║{R}")
    print(f"{YELLOW}╚══════════════╩════════════╝{R}")


def tampilkan_detail_menu(row):
    if len(row) < 14:
        print(f"{RED}⚠️  Data menu tidak lengkap, tidak bisa menampilkan detail.{R}")
        return

    print(f"\n{BOLD}{GREEN}🍽️  {row[0].upper()}{R}")
    print(f"{YELLOW}{'─' * len(row[0])}{R}")

    print(f"• {CYAN}Kategori{R}     : {row[1]}")
    print(f"• {GREEN}Harga{R}        : Rp{int(row[9]):,}".replace(",", "."))
    print(f"• {BLUE}Waktu Masak{R}  : {row[10]} menit")
    print(f"• {CYAN}Kesulitan{R}    : {row[11]}")

    deskripsi = row[12].strip() if row[12] else "(tidak ada deskripsi)"
    print(f"\n{BOLD}📝 Deskripsi:{R}")
    print(f"  {deskripsi}")

    print(f"\n{BOLD}Bahan:{R}")
    bahan_utama_clean = row[7].replace(';', ', ') if row[7] else "(tidak ada)"
    bahan_tambahan_clean = row[8].replace(';', ', ') if row[8] else "(tidak ada)"
    print(f"• {CYAN}Utama{R}     : {bahan_utama_clean}")
    print(f"• {CYAN}Tambahan{R}  : {bahan_tambahan_clean}")

    try:
        k = int(row[2]) if row[2].isdigit() else 0
        p = float(row[3]) if row[3].replace('.', '', 1).isdigit() else 0.0
        l = float(row[4]) if row[4].replace('.', '', 1).isdigit() else 0.0
        kb = float(row[5]) if row[5].replace('.', '', 1).isdigit() else 0.0
        s = float(row[6]) if row[6].replace('.', '', 1).isdigit() else 0.0
        tampilkan_tabel_gizi(k, p, l, kb, s)
    except:
        print(f"{RED}⚠️  Data gizi tidak lengkap.{R}")

    print(f"\n{BOLD}📜 Instruksi:{R}")
    instruksi = row[13].strip() if row[13] else "(tidak ada instruksi tersedia.)"
    if instruksi:
        steps = [s.strip() for s in instruksi.split('. ') if s.strip()]
        if len(steps) == 1 and '.' in instruksi and not instruksi.replace('.', '').replace(',', '').replace(' ', '').isdigit():
             raw_steps = instruksi.split('.')
             steps = [s.strip() for s in raw_steps if s.strip() and not s.strip().replace(',', '').replace('.', '').replace(' ', '').isdigit()]

        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")
    else:
        print("  (Tidak ada instruksi tersedia.)")




def tampilkan_daftar_bahan(hasil, input_bahan):
    print(f"\n{GREEN}✅ Ditemukan {len(hasil)} menu:{R}")
    for i, row in enumerate(hasil, 1):
        matched, unmatched = cek_cocok_per_bahan(input_bahan, row)
        harga = int(row[9])
        status = f"{GREEN}(✅ Semua bahan){R}" if not unmatched else f"{YELLOW}(⚠️ {len(matched)}/{len(matched)+len(unmatched)}){R}"
        print(f"{i:2}. {GREEN}{row[0]}{R} (Rp{harga:,}) {status}".replace(",", "."))
        if unmatched:
            print(f"     {RED}✗ Tidak ditemukan: {', '.join(unmatched)}{R}")
    print(f"\n{CYAN}Pilih nomor, 'acak', utawa 0 kanggo  balik.{R}")


def tampilkan_daftar_budget(hasil, budget):
    print(f"\n{GREEN}✅ Ditemukne {len(hasil)} menu ning budget Rp{budget:,}:{R}".replace(",", "."))
    for i, row in enumerate(hasil, 1):
        h = int(row[9])
        print(f"{i:2}. {GREEN}{row[0]}{R} (Rp{h:,})".replace(",", "."))
    print(f"\n{CYAN}Pilih nomor, 'acak', utawa 0 kanggo balik.{R}")



def menu_setelah_detail(daftar_func=None, *args):
    while True:
        print(f"\n{CYAN}Bar iki arep nyapo?{R}")
        if daftar_func:
            print(f"  {GREEN}1.{R} balik ning menu rekomendasi")
            print(f"  {BLUE}2.{R} Balik ning beranda")
            print(f"  {RED}0.{R} Metu soko aplikasi")
        
        p = input(f"{YELLOW}➤ Pilihen ("
                  + ("1/" if daftar_func else "")
                  + "2/0): "
                  + R).strip()
        
        if daftar_func and p == "1":
            clear_screen()
            daftar_func(*args)
            return 'daftar'
        elif p == "2":
            clear_screen()
            return 'beranda'
        elif p == "0":
            print(f"\n{GREEN}🙏 Matur suwun pun mampir, kapan-kapan maneh ya🙌{R}")
            exit()
        else:
            print(f"{RED}❌ Diomongi 1/2/0 kok mbatek{R}")



def rekomendasi_berdasarkan_bahan(data_rows):
    print(f"\n{BOLD}{CYAN}🔍 Rekomendasi miturut bahane mawon{R}")
    input_bahan = input(f"{YELLOW}Ketiken bahan sing ana (pisahkan dengan koma): {R}").strip()
    perbaikan_input = input_bahan.replace (",","")

    if not perbaikan_input:
        print(f"{RED}❌ kowe ngetik apa? ngantuk ta?{R}")
        input("\nPenceten Enter kanggo balik")
        return

    
    loading_animation("sik tak golekna sing cocok...")
    
    hasil = cek_cocok_dan_filter_bahan(perbaikan_input, data_rows)
    if not hasil:
        print(f"\n{RED}❌ Ora ana menu sing cocok karo :{perbaikan_input}{R}")
        input("\nPencet Enter Kanggo balik")
        return

    hasil.sort(key=lambda x: int(x[9]) if x[9].isdigit() else 0)
    tampilkan_daftar_bahan(hasil, perbaikan_input)

    while True:
        pilih = input(f"{YELLOW}➤ Pilihan: {R}").strip().lower()
        if pilih == 'acak':
            clear_screen()
            row = random.choice(hasil)
            print(f"\n{GREEN}🎲 Rekomendasi acak: {row[0]}{R}")
            tampilkan_detail_menu(row)
            hasil_aksi = menu_setelah_detail(tampilkan_daftar_bahan, hasil, input_bahan)
            if hasil_aksi == 'beranda':
                return

        elif pilih.isdigit():
            idx = int(pilih)
            if idx == 0:
                break
            elif 1 <= idx <= len(hasil):
                clear_screen()
                tampilkan_detail_menu(hasil[idx-1])
                hasil_aksi = menu_setelah_detail(tampilkan_daftar_bahan, hasil, input_bahan)
                if hasil_aksi == 'beranda':
                    return
            else:
                print(f"{RED}❌ Pilihan ora ana, Ngantuk ta?{R}")
        else:
            print(f"{RED}❌ Apa sing diketik iku? gak eruh aku{R}")


def rekomendasi_berdasarkan_budget(data_rows):
    print(f"\n{BOLD}{CYAN}💰 Rekomendasi Berdasarkan Budget{R}")
    inp = input(f"{YELLOW}Ketiken budget maksimalmu (contoh: 20000): {R}").strip()

    # --- Animasi Loading ---
    loading_animation("Sik tak golekna sing cocok...")
    
    hasil, budget = dapatkan_berdasarkan_budget(inp, data_rows)
    if not hasil:
        try:
            b = int(inp)
        except:
            b = inp
        print(f"\n{YELLOW}ℹ️  Ora ana sing regane Rp{b:,}.{R}. Dikerasi maneh kerjane ya".replace(",", "."))
        input("\nPencet Enter kanggo balik...")
        return

    tampilkan_daftar_budget(hasil, budget)

    while True:
        pilih = input(f"{YELLOW}➤ Pilihan: {R}").strip().lower()
        if pilih == 'acak':
            clear_screen()
            row = random.choice(hasil)
            print(f"\n{GREEN}🎲 Rekomendasi acak: {row[0]}{R}")
            tampilkan_detail_menu(row)
            hasil_aksi = menu_setelah_detail(tampilkan_daftar_budget, hasil, budget)
            if hasil_aksi == 'beranda':
                return

        elif pilih.isdigit():
            idx = int(pilih)
            if idx == 0:
                break
            elif 1 <= idx <= len(hasil):
                clear_screen()
                tampilkan_detail_menu(hasil[idx-1])
                hasil_aksi = menu_setelah_detail(tampilkan_daftar_budget, hasil, budget)
                if hasil_aksi == 'beranda':
                    return
            else:
                print(f"{RED}❌ Pilihan ora ana, Ngantuk ta?{R}")
        else:
            print(f"{RED}❌ Apa sing diketik iku? gak eruh aku{R}")



def tampilkan_beranda():
    print(f"{YELLOW}╔════════════════════════════════════════════╗{R}")
    print(f"{YELLOW}║              🍜 Sinau RESEP 🌶️              ║{R}")
    print(f"{YELLOW}║             Apikasi Rekomendasi            ║{R}")
    print(f"{YELLOW}║               Khas Jawa Timur              ║{R}")
    print(f"{YELLOW}╠════════════════════════════════════════════╣{R}")
    print(f"║ {GREEN}[1]{R} 🔍 rekomendasi miturut bahane mawon    {R}║")
    print(f"║ {GREEN}[2]{R} 💰 rekommendasi miturut budgete mawon  {R}║")
    print(f"║                                            ║")
    print(f"║ {RED}[0]{R} 🚪 Keluar                             {R} ║")
    print(f"{YELLOW}╚════════════════════════════════════════════╝{R}")
    print(f"\n{CYAN}➤ Pencet tombol (1, 2, atau 0) tanpa Enter...{R}")



def main():
    data_rows = []
    try:
        with open('dataset_makanan_jawa.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row and len(row) >= 13:
                    data_rows.append(row)
    except FileNotFoundError:
        clear_screen()
        print(f"\n{RED}❌ File 'dataset_makanan_jawa.csv' ora ketemu{R}")
        return
    except Exception as e:
        clear_screen()
        print(f"\n{RED}❌ Error: {e}{R}")
        return

    if not data_rows:
        clear_screen()
        print(f"\n{RED}⚠️  Dataset kosong.{R}")
        return

    print(f"\n{GREEN}✅ Dataset dimuat: {len(data_rows)} menu.{R}")
    input(f"{CYAN}Penceten Enter Kanggo Nglekasi {R}")
    clear_screen()


    while True:
        tampilkan_beranda()
        try:
            key = getch().strip()
            clear_screen()

            if key == "1":
                rekomendasi_berdasarkan_bahan(data_rows)
            elif key == "2":
                rekomendasi_berdasarkan_budget(data_rows)
            elif key == "0":
                print(f"\n{GREEN}🙏 Matur suwun pun mampir, kapan-kapan maneh ya🙌{R}")
                break
            else:
                print(f"{RED}❌ Ndak ana pilihan'{key}'. Penceten sembarang kanggo lanjut{R}")
                getch()
                continue

        except KeyboardInterrupt:
            clear_screen()
            print(f"\n\n{YELLOW}⏹️  Program dindekne karo sing ngengge, kapan-kapan maneh ya!!{R}")
            break
        except Exception as e:
            clear_screen()
            print(f"\n{RED}❌ Kowe mencet apa? manut instruksi ae lah {R}")
            print("Penceten sembarang kanggo balik...")
            getch()


if __name__ == "__main__":
    main()
