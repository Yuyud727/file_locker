#!/usr/bin/env python3
"""
main.py - Program Utama File Locker (CLI Version)

File Locker adalah aplikasi untuk mengenkripsi dan mendekripsi file
menggunakan algoritma AES-256-CBC.

Penggunaan:
    python main.py

Author: [Nama Anda]
Mata Kuliah: [Nama Mata Kuliah]
NIM: [NIM Anda]
"""

import os
import sys
import getpass
from utils import generate_salt, generate_iv, derive_key, get_file_extension
from aes_handler import encrypt_data, decrypt_data
from file_handler import (
    read_file, 
    write_file,
    write_encrypted_file, 
    read_encrypted_file,
    get_output_path_for_decryption,
    ENCRYPTED_EXTENSION
)


def print_banner():
    """Menampilkan banner aplikasi."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ███████╗██╗██╗     ███████╗                           ║
║     ██╔════╝██║██║     ██╔════╝                           ║
║     █████╗  ██║██║     █████╗                              ║
║     ██╔══╝  ██║██║     ██╔══╝                              ║
║     ██║     ██║███████╗███████╗                           ║
║     ╚═╝     ╚═╝╚══════╝╚══════╝                           ║
║                                                           ║
║     ██╗      ██████╗  ██████╗██╗  ██╗███████╗██████╗      ║
║     ██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗     ║
║     ██║     ██║   ██║██║     █████╔╝ █████╗  ██████╔╝     ║
║     ██║     ██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗     ║
║     ███████╗╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║     ║
║     ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ║
║                                                           ║
║         Enkripsi File dengan AES-256-CBC                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Menampilkan menu utama."""
    print("\n" + "=" * 50)
    print("                 MENU UTAMA")
    print("=" * 50)
    print("  [1] Enkripsi File")
    print("  [2] Dekripsi File")
    print("  [3] Tentang Aplikasi")
    print("  [0] Keluar")
    print("=" * 50)


def get_password(confirm: bool = False) -> str:
    """
    Meminta password dari user.
    
    Args:
        confirm: Jika True, minta konfirmasi password
    
    Returns:
        str: Password yang diinput user
    """
    while True:
        password = getpass.getpass("Masukkan password: ")
        
        if len(password) < 4:
            print("⚠️  Password minimal 4 karakter!")
            continue
        
        if confirm:
            password_confirm = getpass.getpass("Konfirmasi password: ")
            if password != password_confirm:
                print("⚠️  Password tidak cocok! Ulangi.")
                continue
        
        return password


def encrypt_file_flow():
    """Alur untuk enkripsi file."""
    print("\n" + "─" * 50)
    print("              ENKRIPSI FILE")
    print("─" * 50)
    
    # Input file path
    filepath = input("Masukkan path file: ").strip()
    
    # Validasi file
    if not os.path.exists(filepath):
        print(f"❌ Error: File tidak ditemukan: {filepath}")
        return
    
    if not os.path.isfile(filepath):
        print("❌ Error: Path bukan file!")
        return
    
    if filepath.endswith(ENCRYPTED_EXTENSION):
        print("❌ Error: File sudah terenkripsi!")
        return
    
    # Input password
    print("\n🔐 Buat password untuk mengunci file:")
    password = get_password(confirm=True)
    
    try:
        # Baca file
        print("\n⏳ Membaca file...")
        file_data = read_file(filepath)
        original_extension = get_file_extension(filepath)
        
        # Generate salt dan IV
        print("⏳ Generating salt dan IV...")
        salt = generate_salt()
        iv = generate_iv()
        
        # Derive key dari password
        print("⏳ Deriving key dari password...")
        key = derive_key(password, salt)
        
        # Enkripsi
        print("⏳ Mengenkripsi data...")
        encrypted_data = encrypt_data(file_data, key, iv)
        
        # Simpan file terenkripsi
        print("⏳ Menyimpan file terenkripsi...")
        output_path = write_encrypted_file(
            filepath, salt, iv, encrypted_data, original_extension
        )
        
        # Info hasil
        original_size = len(file_data)
        encrypted_size = os.path.getsize(output_path)
        
        print("\n" + "═" * 50)
        print("✅ ENKRIPSI BERHASIL!")
        print("═" * 50)
        print(f"📁 File asli     : {filepath}")
        print(f"🔒 File output   : {output_path}")
        print(f"📊 Ukuran asli   : {original_size:,} bytes")
        print(f"📊 Ukuran enkripsi: {encrypted_size:,} bytes")
        print("═" * 50)
        
        # Tanya apakah mau hapus file asli
        delete_original = input("\n🗑️  Hapus file asli? (y/n): ").strip().lower()
        if delete_original == 'y':
            os.remove(filepath)
            print("✅ File asli telah dihapus.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def decrypt_file_flow():
    """Alur untuk dekripsi file."""
    print("\n" + "─" * 50)
    print("              DEKRIPSI FILE")
    print("─" * 50)
    
    # Input file path
    filepath = input("Masukkan path file .locked: ").strip()
    
    # Validasi file
    if not os.path.exists(filepath):
        print(f"❌ Error: File tidak ditemukan: {filepath}")
        return
    
    if not filepath.endswith(ENCRYPTED_EXTENSION):
        print(f"❌ Error: File harus berekstensi {ENCRYPTED_EXTENSION}")
        return
    
    # Input password
    print("\n🔐 Masukkan password untuk membuka file:")
    password = get_password(confirm=False)
    
    try:
        # Baca file terenkripsi
        print("\n⏳ Membaca file terenkripsi...")
        salt, iv, encrypted_data, original_extension = read_encrypted_file(filepath)
        
        # Derive key dari password
        print("⏳ Deriving key dari password...")
        key = derive_key(password, salt)
        
        # Dekripsi
        print("⏳ Mendekripsi data...")
        decrypted_data = decrypt_data(encrypted_data, key, iv)
        
        # Tentukan path output
        output_path = get_output_path_for_decryption(filepath, original_extension)
        
        # Simpan file hasil dekripsi
        print("⏳ Menyimpan file...")
        write_file(output_path, decrypted_data)
        
        # Info hasil
        print("\n" + "═" * 50)
        print("✅ DEKRIPSI BERHASIL!")
        print("═" * 50)
        print(f"🔒 File terenkripsi: {filepath}")
        print(f"📁 File output     : {output_path}")
        print(f"📊 Ukuran file     : {len(decrypted_data):,} bytes")
        print("═" * 50)
        
        # Tanya apakah mau hapus file .locked
        delete_locked = input("\n🗑️  Hapus file .locked? (y/n): ").strip().lower()
        if delete_locked == 'y':
            os.remove(filepath)
            print("✅ File .locked telah dihapus.")
        
    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def show_about():
    """Menampilkan informasi tentang aplikasi."""
    about = """
╔═══════════════════════════════════════════════════════════╗
║                   TENTANG APLIKASI                        ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  File Locker v1.0                                         ║
║                                                           ║
║  Aplikasi untuk mengenkripsi dan mendekripsi file         ║
║  menggunakan algoritma AES-256-CBC.                       ║
║                                                           ║
║  ─────────────────────────────────────────────────────    ║
║                                                           ║
║  Teknologi yang Digunakan:                                ║
║  • Algoritma    : AES (Advanced Encryption Standard)      ║
║  • Mode         : CBC (Cipher Block Chaining)             ║
║  • Key Size     : 256 bits                                ║
║  • Key Derivation: PBKDF2 dengan SHA-256                  ║
║  • Padding      : PKCS7                                   ║
║                                                           ║
║  ─────────────────────────────────────────────────────    ║
║                                                           ║
║  Dibuat untuk Tugas Kuliah:                               ║
║  • Nama   : [Nama Anda]                                   ║
║  • NIM    : [NIM Anda]                                    ║
║  • Matkul : [Nama Mata Kuliah]                            ║
║  • Dosen  : [Nama Dosen]                                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(about)


def main():
    """Fungsi utama program."""
    print_banner()
    
    while True:
        print_menu()
        choice = input("\nPilih menu [0-3]: ").strip()
        
        if choice == '1':
            encrypt_file_flow()
        elif choice == '2':
            decrypt_file_flow()
        elif choice == '3':
            show_about()
        elif choice == '0':
            print("\n👋 Terima kasih telah menggunakan File Locker!")
            print("   Sampai jumpa!\n")
            sys.exit(0)
        else:
            print("\n⚠️  Pilihan tidak valid! Masukkan angka 0-3.")


if __name__ == "__main__":
    main()
