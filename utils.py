"""
utils.py - Fungsi Utility untuk File Locker

Modul ini berisi fungsi-fungsi pendukung seperti:
- Key derivation dari password menggunakan PBKDF2
- Generate random salt dan IV
"""

import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

# Konstanta
SALT_SIZE = 16      # 16 bytes = 128 bits
IV_SIZE = 16        # 16 bytes = 128 bits (sesuai block size AES)
KEY_SIZE = 32       # 32 bytes = 256 bits (untuk AES-256)
ITERATIONS = 100000 # Jumlah iterasi PBKDF2 (semakin tinggi semakin aman)


def generate_salt() -> bytes:
    """
    Generate random salt untuk key derivation.
    Salt memastikan password yang sama menghasilkan key berbeda.
    
    Returns:
        bytes: Random salt sepanjang SALT_SIZE bytes
    """
    return os.urandom(SALT_SIZE)


def generate_iv() -> bytes:
    """
    Generate random Initialization Vector (IV) untuk enkripsi AES-CBC.
    IV memastikan plaintext yang sama menghasilkan ciphertext berbeda.
    
    Returns:
        bytes: Random IV sepanjang IV_SIZE bytes
    """
    return os.urandom(IV_SIZE)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Menghasilkan key dari password menggunakan PBKDF2.
    
    PBKDF2 (Password-Based Key Derivation Function 2) adalah standar
    untuk mengubah password menjadi cryptographic key yang aman.
    
    Args:
        password: Password dari user (string)
        salt: Random salt (bytes)
    
    Returns:
        bytes: Key sepanjang KEY_SIZE bytes untuk AES
    """
    key = PBKDF2(
        password=password.encode('utf-8'),
        salt=salt,
        dkLen=KEY_SIZE,         # Panjang key output
        count=ITERATIONS,        # Jumlah iterasi
        hmac_hash_module=SHA256  # Hash algorithm
    )
    return key


def get_file_extension(filepath: str) -> str:
    """
    Mendapatkan ekstensi file dari path.
    
    Args:
        filepath: Path ke file
    
    Returns:
        str: Ekstensi file (termasuk titik) atau string kosong
    """
    if '.' in os.path.basename(filepath):
        return '.' + filepath.rsplit('.', 1)[1]
    return ''


def get_filename_without_ext(filepath: str) -> str:
    """
    Mendapatkan nama file tanpa ekstensi.
    
    Args:
        filepath: Path ke file
    
    Returns:
        str: Nama file tanpa ekstensi
    """
    basename = os.path.basename(filepath)
    if '.' in basename:
        return basename.rsplit('.', 1)[0]
    return basename
