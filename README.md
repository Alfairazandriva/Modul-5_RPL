# Sistem Manajemen Perpustakaan

Aplikasi desktop manajemen koleksi buku perpustakaan berbasis **Python**, dibangun dengan arsitektur **MVC (Model-View-Controller)**, antarmuka **CustomTkinter**, dan basis data **MySQL**. Aplikasi dilengkapi autentikasi pengguna (password di-hash SHA-256), otorisasi berbasis peran (Admin dan Anggota), pengujian otomatis dengan **pytest**, serta pipeline **CI GitHub Actions**.

## Fitur

- Login dengan verifikasi password ter-hash SHA-256 dan query berparameter (aman dari SQL Injection)
- Otorisasi berbasis peran (RBAC):
  - **Admin**: dapat menambah, memperbarui, dan menghapus data buku
  - **Anggota**: hanya dapat melihat daftar buku (read-only)
- CRUD data buku (judul, penulis, tahun terbit)
- Tombol Logout untuk kembali ke halaman login
- Unit test (pytest) dan linter (flake8) otomatis lewat GitHub Actions

## Struktur Direktori MVC

```
MODUL5_RPL/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml      # Konfigurasi CI GitHub Actions
├── config/
│   └── database.py              # Koneksi ke MySQL
├── models/                      # MODEL: akses data & logika bisnis
│   ├── buku_model.py            # CRUD tabel buku
│   └── user_model.py            # Hashing password, autentikasi, register user
├── views/                       # VIEW: antarmuka pengguna (CustomTkinter)
│   ├── login_view.py            # Jendela login
│   └── buku_view.py             # Jendela utama data buku
├── controllers/                 # CONTROLLER: penghubung Model dan View
│   ├── auth_controller.py       # Alur login
│   └── buku_controller.py       # CRUD buku, otorisasi role, logout
├── tests/                       # Pengujian otomatis (pytest)
│   ├── test_auth.py
│   └── test_buku.py
├── main.py                      # Titik masuk aplikasi
├── requirements.txt             # Daftar dependensi
└── README.md
```

| Komponen | Tanggung jawab |
|----------|----------------|
| Model | Query ke database, hashing password, verifikasi kredensial |
| View | Menampilkan antarmuka, tanpa logika bisnis |
| Controller | Menerima input dari View, memanggil Model, mengatur alur dan hak akses |

## Panduan Instalasi

### 1. Prasyarat

- Python 3.11 atau lebih baru
- [Laragon](https://laragon.org/) (atau server MySQL lain)
- Git
- Visual Studio Code (disarankan)

### 2. Clone repositori dan siapkan virtual environment

```bash
git clone https://github.com/Alfairazandriva/Modul-5_RPL.git
cd Modul-5_RPL

python -m venv env
./env/Scripts/activate        # Windows PowerShell
```

### 3. Instal dependensi

```bash
python -m pip install -r requirements.txt
```

## Konfigurasi Database MySQL

1. Jalankan **Laragon**, lalu klik **Start All** sampai MySQL aktif.
2. Buka terminal Laragon dan masuk ke MySQL:

   ```bash
   mysql -u root -p
   ```

3. Buat database dan tabel:

   ```sql
   CREATE DATABASE IF NOT EXISTS perpustakaan;
   USE perpustakaan;

   CREATE TABLE IF NOT EXISTS buku (
       id_buku INT PRIMARY KEY AUTO_INCREMENT,
       judul VARCHAR(150) NOT NULL,
       penulis VARCHAR(100) NOT NULL,
       tahun_terbit INT NOT NULL
   );

   CREATE TABLE IF NOT EXISTS users (
       id_user INT PRIMARY KEY AUTO_INCREMENT,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
   );
   ```

4. Masukkan akun uji coba (password disimpan dalam bentuk hash SHA-256):

   ```sql
   INSERT IGNORE INTO users (username, password, role) VALUES
   ('petugas', SHA2('admin123', 256), 'admin'),
   ('mahasiswa', SHA2('user123', 256), 'anggota');
   ```

5. Sesuaikan `host`, `user`, `password`, dan nama database di `config/database.py` dengan pengaturan MySQL di komputer Anda.

### Akun Uji Coba

| Username | Password | Role |
|----------|----------|------|
| petugas | admin123 | Admin |
| mahasiswa | user123 | Anggota |

## Cara Menjalankan Aplikasi

Pastikan MySQL di Laragon sudah menyala, lalu:

```bash
python main.py
```

1. Jendela login akan tampil. Masuk dengan salah satu akun uji coba.
2. Admin dapat menambah, memperbarui, dan menghapus buku. Anggota hanya dapat melihat daftar buku.
3. Tombol **Logout** mengembalikan pengguna ke halaman login.

### Menjalankan Pengujian

```bash
python -m pytest -v
```

### Pengecekan Kualitas Kode (Linter)

```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Membuat Berkas Eksekusi (.exe)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```

Hasilnya ada di folder `dist/AplikasiPerpustakaan.exe`. MySQL tetap harus menyala saat aplikasi dibuka.

## CI/CD

Setiap `push` atau `pull request` ke branch `main` memicu GitHub Actions (`.github/workflows/ci_pipeline.yml`) yang:

1. Mengambil kode dari repositori
2. Menyiapkan Python 3.11
3. Menginstal dependensi dari `requirements.txt`
4. Menjalankan linter flake8
5. Menjalankan unit test dengan pytest

## Teknologi

Python, CustomTkinter, MySQL (mysql-connector-python), pytest, flake8, PyInstaller, GitHub Actions.