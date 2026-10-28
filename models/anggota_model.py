import sqlite3

class AnggotaModel:
    def __init__(self, db_name="perpustakaan.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Membuat tabel anggota jika belum ada."""
        conn = self.connect()
        cursor = conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS anggota (
                id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                alamat TEXT NOT NULL
            )
        """
        cursor.execute(query)
        conn.commit()
        conn.close()

    def create_anggota(self, nama, alamat):
        """Menambahkan anggota baru (Create)."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "INSERT INTO anggota (nama, alamat) VALUES (?, ?)"
        cursor.execute(query, (nama, alamat))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    def read_all_anggota(self):
        """Mengambil seluruh data anggota (Read)."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT id_anggota, nama, alamat FROM anggota"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data

    def read_anggota_by_id(self, id_anggota):
        """Mengambil satu data anggota berdasarkan ID (Read)."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT id_anggota, nama, alamat FROM anggota WHERE id_anggota = ?"
        cursor.execute(query, (id_anggota,))
        data = cursor.fetchone()
        conn.close()
        return data