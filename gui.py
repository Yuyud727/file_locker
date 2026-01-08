#!/usr/bin/env python3
"""
gui.py - GUI Version File Locker menggunakan Tkinter

Tampilan grafis untuk aplikasi File Locker.
Lebih user-friendly untuk presentasi dan demo.

Author: [Nama Anda]
Mata Kuliah: [Nama Mata Kuliah]
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

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


class FileLockerGUI:
    """Kelas utama untuk GUI File Locker."""
    
    def __init__(self, root):
        """Inisialisasi GUI."""
        self.root = root
        self.root.title("🔒 File Locker - AES-256 Encryption")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variabel
        self.filepath = tk.StringVar()
        self.password = tk.StringVar()
        self.password_confirm = tk.StringVar()
        self.status = tk.StringVar(value="Siap")
        
        # Setup UI
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Setup style untuk tampilan."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'))
        style.configure('Subtitle.TLabel', font=('Helvetica', 10))
        style.configure('Status.TLabel', font=('Helvetica', 9))
        style.configure('Big.TButton', font=('Helvetica', 11), padding=10)
    
    def create_widgets(self):
        """Membuat semua widget GUI."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === HEADER ===
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame, 
            text="🔒 File Locker",
            style='Title.TLabel'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Enkripsi file dengan AES-256-CBC",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack()
        
        # === FILE SELECTION ===
        file_frame = ttk.LabelFrame(main_frame, text="Pilih File", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_entry = ttk.Entry(file_frame, textvariable=self.filepath, width=50)
        file_entry.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        
        browse_btn = ttk.Button(
            file_frame, 
            text="Browse...",
            command=self.browse_file
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # === PASSWORD ===
        pass_frame = ttk.LabelFrame(main_frame, text="Password", padding="10")
        pass_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Password entry
        pass_row1 = ttk.Frame(pass_frame)
        pass_row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(pass_row1, text="Password:", width=15).pack(side=tk.LEFT)
        pass_entry = ttk.Entry(pass_row1, textvariable=self.password, show="•", width=35)
        pass_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Confirm password entry
        pass_row2 = ttk.Frame(pass_frame)
        pass_row2.pack(fill=tk.X)
        
        ttk.Label(pass_row2, text="Konfirmasi:", width=15).pack(side=tk.LEFT)
        pass_confirm_entry = ttk.Entry(
            pass_row2, 
            textvariable=self.password_confirm, 
            show="•", 
            width=35
        )
        pass_confirm_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Note untuk konfirmasi
        note_label = ttk.Label(
            pass_frame,
            text="* Konfirmasi hanya diperlukan untuk enkripsi",
            font=('Helvetica', 8),
            foreground='gray'
        )
        note_label.pack(anchor=tk.W, pady=(5, 0))
        
        # === ACTION BUTTONS ===
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=20)
        
        encrypt_btn = ttk.Button(
            action_frame,
            text="🔐 ENKRIPSI",
            style='Big.TButton',
            command=self.encrypt_file
        )
        encrypt_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        decrypt_btn = ttk.Button(
            action_frame,
            text="🔓 DEKRIPSI",
            style='Big.TButton',
            command=self.decrypt_file
        )
        decrypt_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # === PROGRESS ===
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # === STATUS ===
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status,
            style='Status.TLabel'
        )
        status_label.pack(side=tk.LEFT)
        
        # === INFO ===
        info_frame = ttk.LabelFrame(main_frame, text="Informasi", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        info_text = """
Cara Penggunaan:
1. Klik 'Browse...' untuk memilih file
2. Masukkan password (minimal 4 karakter)
3. Untuk ENKRIPSI: Isi konfirmasi password, lalu klik 'ENKRIPSI'
4. Untuk DEKRIPSI: Pilih file .locked, masukkan password, klik 'DEKRIPSI'

File terenkripsi akan disimpan dengan ekstensi .locked
        """
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
    
    def browse_file(self):
        """Membuka dialog untuk memilih file."""
        filetypes = [
            ("All Files", "*.*"),
            ("Locked Files", "*.locked"),
            ("Text Files", "*.txt"),
            ("Images", "*.jpg *.jpeg *.png *.gif"),
            ("Documents", "*.pdf *.doc *.docx"),
        ]
        
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.filepath.set(filepath)
            
            # Auto-detect mode berdasarkan ekstensi
            if filepath.endswith(ENCRYPTED_EXTENSION):
                self.status.set("Mode: Dekripsi (file .locked terdeteksi)")
            else:
                self.status.set("Mode: Enkripsi")
    
    def validate_inputs(self, for_encryption: bool = True) -> bool:
        """
        Validasi input user.
        
        Args:
            for_encryption: True jika validasi untuk enkripsi
        
        Returns:
            bool: True jika valid
        """
        # Cek file
        filepath = self.filepath.get().strip()
        if not filepath:
            messagebox.showerror("Error", "Pilih file terlebih dahulu!")
            return False
        
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File tidak ditemukan:\n{filepath}")
            return False
        
        # Cek password
        password = self.password.get()
        if len(password) < 4:
            messagebox.showerror("Error", "Password minimal 4 karakter!")
            return False
        
        # Cek konfirmasi password (hanya untuk enkripsi)
        if for_encryption:
            if password != self.password_confirm.get():
                messagebox.showerror("Error", "Password dan konfirmasi tidak cocok!")
                return False
            
            # Cek jika file sudah terenkripsi
            if filepath.endswith(ENCRYPTED_EXTENSION):
                messagebox.showerror("Error", "File sudah terenkripsi!")
                return False
        else:
            # Untuk dekripsi, cek ekstensi
            if not filepath.endswith(ENCRYPTED_EXTENSION):
                messagebox.showerror(
                    "Error", 
                    f"File harus berekstensi {ENCRYPTED_EXTENSION}"
                )
                return False
        
        return True
    
    def encrypt_file(self):
        """Handler untuk tombol enkripsi."""
        if not self.validate_inputs(for_encryption=True):
            return
        
        # Jalankan di thread terpisah agar UI tidak freeze
        thread = threading.Thread(target=self._do_encrypt)
        thread.start()
    
    def _do_encrypt(self):
        """Proses enkripsi di background thread."""
        self.progress.start()
        self.status.set("Mengenkripsi...")
        
        try:
            filepath = self.filepath.get().strip()
            password = self.password.get()
            
            # Baca file
            self.status.set("Membaca file...")
            file_data = read_file(filepath)
            original_extension = get_file_extension(filepath)
            
            # Generate salt dan IV
            self.status.set("Generating salt dan IV...")
            salt = generate_salt()
            iv = generate_iv()
            
            # Derive key
            self.status.set("Deriving key...")
            key = derive_key(password, salt)
            
            # Enkripsi
            self.status.set("Mengenkripsi data...")
            encrypted_data = encrypt_data(file_data, key, iv)
            
            # Simpan
            self.status.set("Menyimpan file...")
            output_path = write_encrypted_file(
                filepath, salt, iv, encrypted_data, original_extension
            )
            
            self.progress.stop()
            self.status.set("Selesai!")
            
            # Tampilkan hasil
            result = messagebox.askyesno(
                "Sukses! ✅",
                f"File berhasil dienkripsi!\n\n"
                f"Output: {output_path}\n\n"
                f"Hapus file asli?",
                icon='info'
            )
            
            if result:
                os.remove(filepath)
                self.filepath.set("")
            
            self.clear_passwords()
            
        except Exception as e:
            self.progress.stop()
            self.status.set("Error!")
            messagebox.showerror("Error", str(e))
    
    def decrypt_file(self):
        """Handler untuk tombol dekripsi."""
        if not self.validate_inputs(for_encryption=False):
            return
        
        # Jalankan di thread terpisah
        thread = threading.Thread(target=self._do_decrypt)
        thread.start()
    
    def _do_decrypt(self):
        """Proses dekripsi di background thread."""
        self.progress.start()
        self.status.set("Mendekripsi...")
        
        try:
            filepath = self.filepath.get().strip()
            password = self.password.get()
            
            # Baca file terenkripsi
            self.status.set("Membaca file...")
            salt, iv, encrypted_data, original_extension = read_encrypted_file(filepath)
            
            # Derive key
            self.status.set("Deriving key...")
            key = derive_key(password, salt)
            
            # Dekripsi
            self.status.set("Mendekripsi data...")
            decrypted_data = decrypt_data(encrypted_data, key, iv)
            
            # Simpan
            self.status.set("Menyimpan file...")
            output_path = get_output_path_for_decryption(filepath, original_extension)
            write_file(output_path, decrypted_data)
            
            self.progress.stop()
            self.status.set("Selesai!")
            
            # Tampilkan hasil
            result = messagebox.askyesno(
                "Sukses! ✅",
                f"File berhasil didekripsi!\n\n"
                f"Output: {output_path}\n\n"
                f"Hapus file .locked?",
                icon='info'
            )
            
            if result:
                os.remove(filepath)
                self.filepath.set("")
            
            self.clear_passwords()
            
        except ValueError as e:
            self.progress.stop()
            self.status.set("Error!")
            messagebox.showerror("Error", "Password salah atau file corrupt!")
        except Exception as e:
            self.progress.stop()
            self.status.set("Error!")
            messagebox.showerror("Error", str(e))
    
    def clear_passwords(self):
        """Bersihkan field password."""
        self.password.set("")
        self.password_confirm.set("")


def main():
    """Fungsi utama untuk menjalankan GUI."""
    root = tk.Tk()
    app = FileLockerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
