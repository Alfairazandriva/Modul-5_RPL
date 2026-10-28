from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()
    
    # Melakukan eksekusi fungsi tambah buku
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)
    
    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

def test_get_all_buku():
    # Menginisialisasi Model
    model = BukuModel()
    
    # Memanggil fungsi get_all_buku
    hasil = model.get_all_buku()
    
    # Memverifikasi bahwa hasil yang dikembalikan berupa list (daftar buku)
    assert isinstance(hasil, list)