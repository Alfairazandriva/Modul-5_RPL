import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()
        
        # Binding tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        
        # Binding event klik pada tabel agar data otomatis masuk ke form
        self.view.tabel.bind("<<TreeviewSelect>>", self.isi_form_dari_tabel)
        
        # Memuat data ke tabel saat pertama kali aplikasi dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
            
        # Mengambil data dari Model (Database)
        data_buku = self.model.get_all_buku()
        
        # Memasukkan data ke dalam tabel View
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def isi_form_dari_tabel(self, event):
        """Mengisi otomatis kolom input form saat baris tabel diklik"""
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_data = self.view.tabel.item(selected_item)
            values = item_data['values']
            
            if values:
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_judul.insert(0, values[1])
                
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_penulis.insert(0, values[2])
                
                self.view.entry_tahun.delete(0, 'end')
                self.view.entry_tahun.insert(0, values[3])

    def simpan_data(self):
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        berhasil = self.model.create_buku(judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()

    def hapus_data(self):
        # 1. Pastikan pengguna sudah memilih baris pada tabel
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih baris data yang ingin dihapus terlebih dahulu!")
            return
        
        # 2. Ambil id_buku dari kolom pertama (index 0) baris yang dipilih
        item_data = self.view.tabel.item(selected_item)
        id_buku = item_data['values'][0]
        
        # 3. Konfirmasi dan eksekusi penghapusan via model
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?"):
            self.model.delete_buku(id_buku)
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            
            # Bersihkan form dan muat ulang tabel
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()

    def perbarui_data(self):
        # 1. Pastikan pengguna sudah memilih baris pada tabel
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih baris data yang ingin diperbarui terlebih dahulu!")
            return
            
        # 2. Ambil id_buku dari baris yang diklik
        item_data = self.view.tabel.item(selected_item)
        id_buku = item_data['values'][0]
        
        # 3. Ambil data baru dari form input
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        # 4. Eksekusi pembaruan via model
        self.model.update_buku(id_buku, judul, penulis, tahun)
        messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
        
        # 5. Bersihkan form dan muat ulang tabel
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.muat_data_tabel()

    def run(self):
        self.view.mainloop()