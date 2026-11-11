from controllers.auth_controller import AuthController
from controllers.buku_controller import BukuController

if __name__ == "__main__":
    while True:
        # 1. Tampilkan jendela login, tunggu sampai ditutup
        user = AuthController().run()

        # Login ditutup tanpa berhasil masuk -> keluar dari aplikasi
        if not user:
            break

        # 2. Buka jendela utama sesuai role
        logout = BukuController(user_role=user["role"]).run()

        # Jendela ditutup lewat tombol X -> keluar. Lewat Logout -> kembali ke login.
        if not logout:
            break