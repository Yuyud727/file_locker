"""
file_handler.py - Handler Operasi File

Modul ini berisi fungsi-fungsi untuk:
- Membaca file dalam mode binary
- Menulis file terenkripsi dengan format khusus
- Membaca dan memparse file terenkripsi
- Menyimpan file hasil dekripsi
"""

import os
from utils import SALT_SIZE, IV_SIZE

# Ekstensi file terenkripsi
ENCRYPTED_EXTENSION = ".locked"

# Magic bytes untuk identifikasi file (opsional, untuk validasi)
MAGIC_BYTES = b"FLCK"  # File Locker
MAGIC_SIZE = 4


def read_file(filepath: str) -> bytes:
    """
    Membaca file dalam mode binary.
    
    Args:
        filepath: Path ke file yang akan dibaca
    
    Returns:
        bytes: Isi file dalam bentuk bytes
    
    Raises:
        FileNotFoundError: Jika file tidak ditemukan
        IOError: Jika gagal membaca file
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
    
    with open(filepath, 'rb') as f:
        return f.read()


def write_file(filepath: str, data: bytes) -> None:
    """
    Menulis data ke file dalam mode binary.
    
    Args:
        filepath: Path file tujuan
        data: Data yang akan ditulis (bytes)
    
    Raises:
        IOError: Jika gagal menulis file
    """
    # Buat direktori jika belum ada
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(filepath, 'wb') as f:
        f.write(data)


def write_encrypted_file(filepath: str, salt: bytes, iv: bytes, 
                         encrypted_data: bytes, original_extension: str) -> str:
    """
    Menulis file terenkripsi dengan format khusus.
    
    Format file terenkripsi:
    [MAGIC_BYTES (4)] [EXT_LEN (1)] [EXT (var)] [SALT (16)] [IV (16)] [DATA (var)]
    
    Args:
        filepath: Path dasar untuk file output
        salt: Salt yang digunakan untuk key derivation
        iv: Initialization Vector
        encrypted_data: Data yang sudah dienkripsi
        original_extension: Ekstensi file asli (untuk recovery)
    
    Returns:
        str: Path file terenkripsi yang dibuat
    """
    # Buat path output dengan ekstensi .locked
    output_path = filepath + ENCRYPTED_EXTENSION
    
    # Encode ekstensi asli (untuk recovery saat dekripsi)
    ext_bytes = original_extension.encode('utf-8')
    ext_len = len(ext_bytes)
    
    # Gabungkan semua komponen
    file_content = (
        MAGIC_BYTES +           # Magic bytes untuk identifikasi
        bytes([ext_len]) +      # Panjang ekstensi (1 byte, max 255)
        ext_bytes +             # Ekstensi asli
        salt +                  # Salt untuk key derivation
        iv +                    # IV untuk AES
        encrypted_data          # Data terenkripsi
    )
    
    write_file(output_path, file_content)
    return output_path


def read_encrypted_file(filepath: str) -> tuple:
    """
    Membaca dan memparse file terenkripsi.
    
    Args:
        filepath: Path ke file .locked
    
    Returns:
        tuple: (salt, iv, encrypted_data, original_extension)
    
    Raises:
        ValueError: Jika format file tidak valid
    """
    data = read_file(filepath)
    
    # Validasi magic bytes
    if data[:MAGIC_SIZE] != MAGIC_BYTES:
        raise ValueError("Format file tidak valid! Bukan file File Locker.")
    
    # Parse komponen
    pos = MAGIC_SIZE
    
    # Baca panjang ekstensi
    ext_len = data[pos]
    pos += 1
    
    # Baca ekstensi
    original_extension = data[pos:pos + ext_len].decode('utf-8')
    pos += ext_len
    
    # Baca salt
    salt = data[pos:pos + SALT_SIZE]
    pos += SALT_SIZE
    
    # Baca IV
    iv = data[pos:pos + IV_SIZE]
    pos += IV_SIZE
    
    # Sisa adalah encrypted data
    encrypted_data = data[pos:]
    
    return salt, iv, encrypted_data, original_extension


def get_output_path_for_decryption(encrypted_filepath: str, 
                                    original_extension: str,
                                    output_dir: str = None) -> str:
    """
    Membuat path untuk file hasil dekripsi.
    
    Args:
        encrypted_filepath: Path file .locked
        original_extension: Ekstensi file asli
        output_dir: Direktori output (opsional)
    
    Returns:
        str: Path untuk menyimpan file hasil dekripsi
    """
    # Hapus ekstensi .locked
    base_path = encrypted_filepath
    if base_path.endswith(ENCRYPTED_EXTENSION):
        base_path = base_path[:-len(ENCRYPTED_EXTENSION)]
    
    # Tambahkan ekstensi asli
    output_path = base_path + original_extension
    
    # Jika ada output directory, pindahkan ke sana
    if output_dir:
        filename = os.path.basename(output_path)
        output_path = os.path.join(output_dir, filename)
    
    # Hindari overwrite: tambahkan suffix jika file sudah ada
    if os.path.exists(output_path):
        base, ext = os.path.splitext(output_path)
        counter = 1
        while os.path.exists(f"{base}_decrypted_{counter}{ext}"):
            counter += 1
        output_path = f"{base}_decrypted_{counter}{ext}"
    
    return output_path
