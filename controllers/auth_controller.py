import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.user = None  # diisi jika login berhasil
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user['username']} ({user['role']})!"
            )
            self.user = user
            # Cukup tutup jendela login. Jendela utama dibuka di main.py
            # setelah mainloop login selesai (lebih aman untuk CustomTkinter).
            self.view.destroy()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def run(self):
        """Menjalankan jendela login dan mengembalikan data user (atau None)."""
        self.view.mainloop()
        return self.user