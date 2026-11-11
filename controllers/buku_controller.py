import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    # Role yang hanya boleh melihat data (tidak boleh tambah/ubah/hapus).
    ROLE_HANYA_LIHAT = ("anggota",)

    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.logout_requested = False
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan role pada judul jendela
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol View dengan fungsi Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.btn_logout.configure(command=self.logout)

        # Klik baris tabel -> isi form otomatis
        self.view.tabel.bind("<<TreeviewSelect>>", self.isi_form_dari_tabel)

        # OTORISASI: batasi tombol dan form sesuai role
        self.atur_hak_akses()

        self.muat_data_tabel()

    # ---------- Otorisasi ----------
    def boleh_ubah_data(self):
        return self.user_role not in self.ROLE_HANYA_LIHAT

    def atur_hak_akses(self):
        if not self.boleh_ubah_data():
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_delete.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            for entry in (self.view.entry_judul, self.view.entry_penulis, self.view.entry_tahun):
                entry.configure(state="disabled")

    def tolak_jika_tidak_berhak(self, aksi):
        """Proteksi ganda di level controller. True jika akses ditolak."""
        if not self.boleh_ubah_data():
            messagebox.showerror("Akses Ditolak", f"Anda tidak memiliki izin untuk {aksi} data!")
            return True
        return False

    # ---------- Helper ----------
    def kosongkan_form(self):
        for entry in (self.view.entry_judul, self.view.entry_penulis, self.view.entry_tahun):
            entry.delete(0, "end")

    def validasi_form(self):
        """Mengembalikan (judul, penulis, tahun) jika valid, selain itu None."""
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return None
        if not tahun.isdigit() or len(tahun) != 4:
            messagebox.showwarning("Peringatan", "Tahun harus berupa 4 digit angka!")
            return None
        return judul, penulis, tahun

    def ambil_id_terpilih(self, pesan):
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", pesan)
            return None
        return self.view.tabel.item(selected_item)["values"][0]

    # ---------- Tabel ----------
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for buku in self.model.get_all_buku():
            self.view.tabel.insert(
                "", "end",
                values=(buku["id_buku"], buku["judul"], buku["penulis"], buku["tahun_terbit"])
            )

    def isi_form_dari_tabel(self, event):
        """Mengisi form saat baris tabel diklik (hanya untuk role yang boleh mengubah)."""
        if not self.boleh_ubah_data():
            return
        selected_item = self.view.tabel.selection()
        if not selected_item:
            return
        values = self.view.tabel.item(selected_item)["values"]
        if values:
            self.kosongkan_form()
            self.view.entry_judul.insert(0, values[1])
            self.view.entry_penulis.insert(0, values[2])
            self.view.entry_tahun.insert(0, values[3])

    # ---------- CRUD ----------
    def simpan_data(self):
        if self.tolak_jika_tidak_berhak("menambah"):
            return
        data = self.validasi_form()
        if not data:
            return

        if self.model.create_buku(*data):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def perbarui_data(self):
        if self.tolak_jika_tidak_berhak("memperbarui"):
            return
        id_buku = self.ambil_id_terpilih("Pilih baris data yang ingin diperbarui terlebih dahulu!")
        if id_buku is None:
            return
        data = self.validasi_form()
        if not data:
            return

        self.model.update_buku(id_buku, *data)
        messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
        self.kosongkan_form()
        self.muat_data_tabel()

    def hapus_data(self):
        if self.tolak_jika_tidak_berhak("menghapus"):
            return
        id_buku = self.ambil_id_terpilih("Pilih baris data yang ingin dihapus terlebih dahulu!")
        if id_buku is None:
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?"):
            self.model.delete_buku(id_buku)
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.kosongkan_form()
            self.muat_data_tabel()

    # ---------- Logout ----------
    def logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin keluar dan kembali ke halaman login?"):
            self.logout_requested = True
            self.view.destroy()

    def run(self):
        """Menjalankan jendela utama. Mengembalikan True jika user menekan Logout."""
        self.view.mainloop()
        return self.logout_requested