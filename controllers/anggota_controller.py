import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Binding tombol
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_anggota = self.model.get_all_anggota() # Sesuaikan nama method di model Anda
        for anggota in data_anggota:
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['email']))

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        email = self.view.entry_email.get()

        if not nama or not email:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return

        berhasil = self.model.create_anggota(nama, email)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.muat_data_tabel()

    def run(self):
        self.view.mainloop()