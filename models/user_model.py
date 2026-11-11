import hashlib
import mysql.connector
from config.database import Database


class UserModel:
    ROLE_VALID = ("admin", "anggota")

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        # Mengubah plain text password menjadi hash SHA-256
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def autentikasi(self, username, password):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)

            # Parameterized Query untuk mencegah SQL Injection
            query = f"SELECT id_user, username, role FROM {self.table_name} WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return user
        return None

    def register_user(self, username, password, role="anggota"):
        """Mendaftarkan user baru dengan password otomatis di-hash SHA-256.

        Mengembalikan True jika berhasil, False jika gagal
        (input kosong, role tidak valid, username sudah dipakai, atau koneksi bermasalah).
        """
        username = (username or "").strip()
        if not username or not password:
            print("Error Register: username dan password wajib diisi")
            return False
        if role not in self.ROLE_VALID:
            print(f"Error Register: role harus salah satu dari {self.ROLE_VALID}")
            return False
        if not self.conn:
            return False

        password_hash = self.hash_password(password)
        cursor = self.conn.cursor()
        query = f"INSERT INTO {self.table_name} (username, password, role) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (username, password_hash, role))
            self.conn.commit()
            return True
        except mysql.connector.IntegrityError:
            # Kolom username bersifat UNIQUE, jadi username yang sama ditolak
            self.conn.rollback()
            print(f"Error Register: username '{username}' sudah digunakan")
            return False
        except Exception as e:
            self.conn.rollback()
            print(f"Error Register: {e}")
            return False
        finally:
            cursor.close()