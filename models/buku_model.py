import sqlite3

class BukuModel:
    def __init__(self, db_name="perpustakaan.db"):
        self.db_name = db_name
        self.create_table()  # Membuat tabel otomatis saat objek dibuat

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Membuat tabel buku jika belum ada."""
        conn = self.connect()
        cursor = conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS buku (
                id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                penulis TEXT NOT NULL,
                tahun_terbit INTEGER NOT NULL
            )
        """
        cursor.execute(query)
        conn.commit()
        conn.close()

    def get_all_buku(self):
        """Mengambil seluruh data buku dari database."""
        conn = self.connect()
        # Menggunakan row_factory agar hasil query berupa dictionary/akses kolom lebih mudah
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buku")
        rows = cursor.fetchall()
        # Mengubah baris SQLite Row menjadi format dictionary standar
        result = [dict(row) for row in rows]
        conn.close()
        return result

    def create_buku(self, judul, penulis, tahun_terbit):
        """Menambahkan data buku baru ke database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            query = "INSERT INTO buku (judul, penulis, tahun_terbit) VALUES (?, ?, ?)"
            cursor.execute(query, (judul, penulis, tahun_terbit))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        """Memperbarui data buku berdasarkan id_buku."""
        conn = self.connect()
        cursor = conn.cursor()
        query = """
            UPDATE buku 
            SET judul = ?, penulis = ?, tahun_terbit = ?
            WHERE id_buku = ?
        """
        cursor.execute(query, (judul, penulis, tahun_terbit, id_buku))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected

    def delete_buku(self, id_buku):
        """Menghapus data buku berdasarkan id_buku."""
        conn = self.connect()
        cursor = conn.cursor()
        query = "DELETE FROM buku WHERE id_buku = ?"
        cursor.execute(query, (id_buku,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected