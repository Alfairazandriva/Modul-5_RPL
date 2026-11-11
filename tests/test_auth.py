from unittest.mock import MagicMock, patch
from models.user_model import UserModel


def test_hash_password_konsisten():
    password_asli = "admin123"
    hash_1 = UserModel.hash_password(password_asli)
    hash_2 = UserModel.hash_password(password_asli)

    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # Panjang karakter standar SHA-256


@patch("models.user_model.Database")
def test_autentikasi_pengguna_berhasil(mock_database):
    # Database palsu: tidak ada koneksi ke MySQL sungguhan
    mock_database.return_value.get_connection.return_value = MagicMock()

    model = UserModel()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "role": "admin",
    }
    model.conn = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    hasil = model.autentikasi("petugas", "admin123")

    assert hasil is not None
    assert hasil["username"] == "petugas"
    assert hasil["role"] == "admin"