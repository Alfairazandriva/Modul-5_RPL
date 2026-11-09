from config.database import Database

class BukuModel:
    def __init__(self):
        self.db = Database()

    def get_all_buku(self):
        """Mengambil seluruh data buku dari database."""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM buku")
        result = cursor.fetchall()
        conn.close()
        return result

    def tambah_buku(self, judul, penulis, tahun_terbit):
        """Menambahkan data buku baru."""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            query = "INSERT INTO buku (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
            cursor.execute(query, (judul, penulis, tahun_terbit))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        """Memperbarui data buku berdasarkan id_buku."""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            query = "UPDATE buku SET judul = %s, penulis = %s, tahun_terbit = %s WHERE id_buku = %s"
            cursor.execute(query, (judul, penulis, tahun_terbit, id_buku))
            conn.commit()
            rows_affected = cursor.rowcount
            conn.close()
            return rows_affected > 0
        except Exception as e:
            print(f"Error: {e}")
            return False

    def delete_buku(self, id_buku):
        """Menghapus data buku berdasarkan id_buku."""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            query = "DELETE FROM buku WHERE id_buku = %s"
            cursor.execute(query, (id_buku,))
            conn.commit()
            rows_affected = cursor.rowcount
            conn.close()
            return rows_affected > 0
        except Exception as e:
            print(f"Error: {e}")
            return False