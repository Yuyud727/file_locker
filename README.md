# 🔒 File Locker - AES-256 Encryption

Aplikasi untuk mengenkripsi dan mendekripsi file menggunakan algoritma **AES-256-CBC**.

---

## 📋 Daftar Isi

1. [Tentang Aplikasi](#tentang-aplikasi)
2. [Teknologi yang Digunakan](#teknologi-yang-digunakan)
3. [Struktur Proyek](#struktur-proyek)
4. [Instalasi](#instalasi)
5. [Cara Penggunaan](#cara-penggunaan)
6. [Penjelasan Algoritma](#penjelasan-algoritma)
7. [Format File Terenkripsi](#format-file-terenkripsi)
8. [Screenshot](#screenshot)
9. [Referensi](#referensi)

---

## 📖 Tentang Aplikasi

**File Locker** adalah aplikasi keamanan yang memungkinkan pengguna untuk:

- 🔐 **Mengenkripsi** file apapun (gambar, dokumen, video, dll.) dengan password
- 🔓 **Mendekripsi** file yang sudah dienkripsi dengan password yang benar
- 🛡️ Melindungi file sensitif dari akses yang tidak sah

### Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| Enkripsi AES-256 | Menggunakan standar enkripsi yang digunakan oleh pemerintah AS |
| Password-based | Key dihasilkan dari password menggunakan PBKDF2 |
| Cross-platform | Berjalan di Windows, macOS, dan Linux |
| GUI & CLI | Tersedia versi command line dan graphical interface |

---

## 🔧 Teknologi yang Digunakan

### Algoritma Kriptografi

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| **Algoritma Enkripsi** | AES (Advanced Encryption Standard) | Standar enkripsi simetris yang paling banyak digunakan |
| **Mode Operasi** | CBC (Cipher Block Chaining) | Setiap block ciphertext bergantung pada block sebelumnya |
| **Ukuran Key** | 256 bits | Tingkat keamanan tertinggi AES |
| **Key Derivation** | PBKDF2 dengan SHA-256 | Mengubah password menjadi cryptographic key |
| **Padding** | PKCS7 | Standar padding untuk block cipher |
| **Iterasi PBKDF2** | 100,000 | Mencegah brute-force attack |

### Library Python

```
pycryptodome==3.20.0
```

**PyCryptodome** adalah library kriptografi Python yang menyediakan implementasi algoritma kriptografi yang aman dan teroptimasi.

---

## 📁 Struktur Proyek

```
file-locker/
│
├── main.py              # Program utama (versi CLI)
├── gui.py               # Program dengan tampilan GUI
├── aes_handler.py       # Modul enkripsi & dekripsi AES
├── file_handler.py      # Modul operasi file
├── utils.py             # Fungsi utility (key derivation, dll.)
│
├── test_files/          # Folder untuk file testing
├── output/              # Folder output hasil enkripsi/dekripsi
│
├── requirements.txt     # Dependency Python
└── README.md            # Dokumentasi (file ini)
```

### Penjelasan File

| File | Fungsi |
|------|--------|
| `main.py` | Entry point program CLI dengan menu interaktif |
| `gui.py` | Entry point program GUI menggunakan Tkinter |
| `aes_handler.py` | Implementasi enkripsi dan dekripsi AES-256-CBC |
| `file_handler.py` | Fungsi untuk membaca, menulis, dan memformat file |
| `utils.py` | Fungsi pendukung seperti key derivation dan generate random bytes |

---

## 🚀 Instalasi

### Prasyarat

- Python 3.7 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download proyek ini**

2. **Buka terminal/command prompt di folder proyek**

3. **Install dependency**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi**
   
   Versi CLI:
   ```bash
   python main.py
   ```
   
   Versi GUI:
   ```bash
   python gui.py
   ```

---

## 💻 Cara Penggunaan

### Versi CLI (Command Line Interface)

#### Enkripsi File

```
1. Jalankan: python main.py
2. Pilih menu [1] Enkripsi File
3. Masukkan path file yang ingin dienkripsi
4. Buat password (minimal 4 karakter)
5. Konfirmasi password
6. File terenkripsi akan tersimpan dengan ekstensi .locked
```

#### Dekripsi File

```
1. Jalankan: python main.py
2. Pilih menu [2] Dekripsi File
3. Masukkan path file .locked
4. Masukkan password
5. File asli akan dipulihkan
```

### Versi GUI (Graphical User Interface)

1. Jalankan `python gui.py`
2. Klik **Browse** untuk memilih file
3. Masukkan password
4. Untuk enkripsi: isi konfirmasi password, klik **ENKRIPSI**
5. Untuk dekripsi: pilih file .locked, klik **DEKRIPSI**

---

## 🔬 Penjelasan Algoritma

### 1. AES (Advanced Encryption Standard)

AES adalah algoritma enkripsi simetris yang ditetapkan oleh NIST sebagai standar enkripsi pada tahun 2001. AES bekerja dengan:

- **Block size**: 128 bits (16 bytes)
- **Key size**: 128, 192, atau 256 bits (aplikasi ini menggunakan 256 bits)
- **Rounds**: 14 rounds untuk AES-256

```
Plaintext ──► [AES Encryption + Key] ──► Ciphertext
Ciphertext ──► [AES Decryption + Key] ──► Plaintext
```

### 2. Mode CBC (Cipher Block Chaining)

CBC adalah mode operasi dimana setiap block plaintext di-XOR dengan ciphertext block sebelumnya sebelum dienkripsi.

```
     P1          P2          P3
      │           │           │
      ▼           ▼           ▼
IV ──►⊕    ┌────►⊕    ┌────►⊕
      │    │     │    │     │
      ▼    │     ▼    │     ▼
   [AES]   │  [AES]   │  [AES]
      │    │     │    │     │
      ▼    │     ▼    │     ▼
     C1 ───┘    C2 ───┘    C3

P = Plaintext block
C = Ciphertext block
IV = Initialization Vector
⊕ = XOR operation
```

**Keuntungan CBC:**
- Plaintext yang sama menghasilkan ciphertext berbeda (karena IV random)
- Lebih aman dari mode ECB

### 3. PBKDF2 (Password-Based Key Derivation Function 2)

PBKDF2 mengubah password menjadi cryptographic key yang aman:

```
Password + Salt ──► [PBKDF2 + 100,000 iterations] ──► 256-bit Key
```

**Komponen:**
- **Password**: Input dari user
- **Salt**: Random 16 bytes (mencegah rainbow table attack)
- **Iterations**: 100,000 (mencegah brute-force)
- **Hash**: SHA-256

### 4. Padding PKCS7

Karena AES bekerja per block 16 bytes, data perlu di-padding:

```
Data: "Hello" (5 bytes)
Padding: 11 bytes dengan nilai 0x0B
Hasil: "Hello" + [0x0B × 11] = 16 bytes
```

---

## 📦 Format File Terenkripsi

File .locked memiliki struktur:

```
┌────────────┬───────────┬──────────────┬──────────┬──────────┬─────────────────┐
│   MAGIC    │  EXT_LEN  │     EXT      │   SALT   │    IV    │ ENCRYPTED DATA  │
│  4 bytes   │  1 byte   │   variable   │ 16 bytes │ 16 bytes │    variable     │
│  "FLCK"    │   0-255   │  extension   │  random  │  random  │   ciphertext    │
└────────────┴───────────┴──────────────┴──────────┴──────────┴─────────────────┘
```

| Field | Ukuran | Deskripsi |
|-------|--------|-----------|
| MAGIC | 4 bytes | Identifier file ("FLCK") |
| EXT_LEN | 1 byte | Panjang ekstensi asli |
| EXT | variable | Ekstensi file asli (untuk recovery) |
| SALT | 16 bytes | Random salt untuk PBKDF2 |
| IV | 16 bytes | Random IV untuk AES-CBC |
| DATA | variable | Data terenkripsi |

---

## 📸 Screenshot

### Versi CLI
```
╔═══════════════════════════════════════════════════════════╗
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
╚═══════════════════════════════════════════════════════════╝

==================================================
                 MENU UTAMA
==================================================
  [1] Enkripsi File
  [2] Dekripsi File
  [3] Tentang Aplikasi
  [0] Keluar
==================================================
```

---

## 🧪 Testing

### Test Case 1: Enkripsi dan Dekripsi File Teks
```bash
# 1. Buat file test
echo "Hello, World! Ini adalah test enkripsi." > test_files/sample.txt

# 2. Jalankan aplikasi dan enkripsi file
python main.py
# Pilih [1], masukkan path: test_files/sample.txt
# Buat password: test1234

# 3. Dekripsi file
# Pilih [2], masukkan path: test_files/sample.txt.locked
# Masukkan password: test1234
```

### Test Case 2: Password Salah
```bash
# Coba dekripsi dengan password salah
# Expected: Error "Password salah atau file corrupt!"
```

### Test Case 3: File Berbagai Tipe
```bash
# Test dengan file gambar (.jpg, .png)
# Test dengan file dokumen (.pdf, .docx)
# Test dengan file video (.mp4)
```

---

## 🔒 Keamanan

### Kekuatan
- AES-256 dianggap tidak bisa di-crack dengan teknologi saat ini
- PBKDF2 dengan 100,000 iterasi mencegah brute-force
- Random salt mencegah rainbow table attack
- Random IV memastikan ciphertext berbeda setiap enkripsi

### Keterbatasan
- Keamanan bergantung pada kekuatan password
- Tidak ada mekanisme recovery jika password hilang
- Metadata file (nama, ukuran) masih terlihat

### Rekomendasi
- Gunakan password minimal 8 karakter
- Kombinasikan huruf besar, kecil, angka, dan simbol
- Jangan gunakan password yang mudah ditebak

---

## 📚 Referensi

1. **NIST FIPS 197** - Advanced Encryption Standard (AES)
   - https://csrc.nist.gov/publications/detail/fips/197/final

2. **RFC 2898** - PKCS #5: Password-Based Cryptography Specification
   - https://tools.ietf.org/html/rfc2898

3. **PyCryptodome Documentation**
   - https://pycryptodome.readthedocs.io/

4. **Block Cipher Mode of Operation**
   - https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation

---

## 👤 Informasi Pengembang

```
Nama        : [Nama Anda]
NIM         : [NIM Anda]
Mata Kuliah : [Nama Mata Kuliah]
Dosen       : [Nama Dosen]
Universitas : [Nama Universitas]
```

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan tugas kuliah.

---

*Dibuat dengan ❤️ untuk tugas kuliah*
# file_locker
