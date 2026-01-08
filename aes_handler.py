"""
aes_handler.py - Handler Enkripsi dan Dekripsi AES

Modul ini berisi implementasi enkripsi dan dekripsi menggunakan:
- Algoritma: AES (Advanced Encryption Standard)
- Mode: CBC (Cipher Block Chaining)
- Padding: PKCS7
- Key Size: 256 bits
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_data(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Mengenkripsi data menggunakan AES-256-CBC.
    
    Proses enkripsi:
    1. Buat cipher AES dengan key dan IV
    2. Tambahkan padding ke data (agar kelipatan 16 bytes)
    3. Enkripsi data yang sudah di-padding
    
    Args:
        data: Data yang akan dienkripsi (bytes)
        key: Kunci enkripsi 256-bit (bytes)
        iv: Initialization Vector 128-bit (bytes)
    
    Returns:
        bytes: Data terenkripsi (ciphertext)
    """
    # Buat cipher AES mode CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Tambahkan padding PKCS7 dan enkripsi
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data


def decrypt_data(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Mendekripsi data menggunakan AES-256-CBC.
    
    Proses dekripsi:
    1. Buat cipher AES dengan key dan IV yang sama
    2. Dekripsi ciphertext
    3. Hapus padding untuk mendapatkan data asli
    
    Args:
        encrypted_data: Data terenkripsi (bytes)
        key: Kunci dekripsi 256-bit (bytes)
        iv: Initialization Vector 128-bit (bytes)
    
    Returns:
        bytes: Data asli (plaintext)
    
    Raises:
        ValueError: Jika password salah atau data corrupt
    """
    # Buat cipher AES mode CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Dekripsi dan hapus padding
    decrypted_padded = cipher.decrypt(encrypted_data)
    
    try:
        decrypted_data = unpad(decrypted_padded, AES.block_size)
    except ValueError:
        raise ValueError("Password salah atau file corrupt!")
    
    return decrypted_data
