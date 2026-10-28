import customtkinter as ctk
from tkinter import ttk

class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Anggota Perpustakaan")
        self.geometry("800x450")
        
        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # FRAME KIRI: FORMULIR INPUT ANGGOTA
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_kiri, text="Form Data Anggota", font=("Arial", 16, "bold")).pack(pady=15)
        
        # Komponen Input (Nama Anggota dan Alamat)
        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Anggota")
        self.entry_nama.pack(pady=10, padx=15, fill="x")
        
        self.entry_alamat = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Alamat")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")
        
        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Anggota", fg_color="green")
        self.btn_simpan.pack(pady=15, padx=15, fill="x")
        
        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Anggota", fg_color="blue")
        self.btn_update.pack(pady=10, padx=15, fill="x")
        
        self.btn_delete = ctk.CTkButton(self.frame_kiri, text="Hapus Anggota", fg_color="red")
        self.btn_delete.pack(pady=10, padx=15, fill="x")
        
        # FRAME KANAN: TABEL DAFTAR ANGGOTA
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_kanan, text="Daftar Koleksi Anggota", font=("Arial", 16, "bold")).pack(pady=15)
        
        kolom = ("id", "nama", "alamat")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)
        
        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")
        
        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("nama", width=150)
        self.tabel.column("alamat", width=200)
        
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

# Blok eksekusi untuk menguji tampilan grafis Anggota
if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()