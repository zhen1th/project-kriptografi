# ============================================================
# helpers.py
# Fungsi-fungsi pembantu yang digunakan di seluruh aplikasi
# ============================================================


def ubah_ke_biner(teks: str) -> list[str]:
    """
    Mengubah setiap karakter dalam teks menjadi representasi biner 8-bit.

    Parameter:
        teks (str): Teks yang akan diubah.

    Mengembalikan:
        list[str]: Daftar string biner 8-bit untuk setiap karakter.
    """
    return [format(ord(karakter), '08b') for karakter in teks]


def ubah_ke_heksadesimal(teks: str) -> list[str]:
    """
    Mengubah setiap karakter dalam teks menjadi representasi hexadecimal.

    Parameter:
        teks (str): Teks yang akan diubah.

    Mengembalikan:
        list[str]: Daftar string hexadecimal untuk setiap karakter.
    """
    return [format(ord(karakter), '02X') for karakter in teks]


def biner_ke_teks(daftar_biner: list[str]) -> str:
    """
    Mengubah daftar string biner 8-bit menjadi teks.

    Parameter:
        daftar_biner (list[str]): Daftar string biner 8-bit.

    Mengembalikan:
        str: Teks hasil konversi.
    """
    return ''.join(chr(int(biner, 2)) for biner in daftar_biner)


def heksadesimal_ke_teks(daftar_hex: list[str]) -> str:
    """
    Mengubah daftar string hexadecimal menjadi teks.

    Parameter:
        daftar_hex (list[str]): Daftar string hexadecimal.

    Mengembalikan:
        str: Teks hasil konversi.
    """
    return ''.join(chr(int(nilai_hex, 16)) for nilai_hex in daftar_hex)


def validasi_hex(teks_hex: str) -> bool:
    """
    Memvalidasi apakah string merupakan hexadecimal yang valid.

    Parameter:
        teks_hex (str): String yang akan divalidasi.

    Mengembalikan:
        bool: True jika valid, False jika tidak.
    """
    try:
        for nilai_hex in teks_hex.strip().split():
            int(nilai_hex, 16)
        return True
    except ValueError:
        return False


def format_tampilan_hex(data_byte: list[int]) -> str:
    """
    Memformat daftar nilai byte menjadi string hexadecimal yang rapi.

    Parameter:
        data_byte (list[int]): Daftar nilai byte (integer).

    Mengembalikan:
        str: String hexadecimal dipisah spasi (contoh: '48 45 4C 4C 4F').
    """
    return ' '.join(format(nilai, '02X') for nilai in data_byte)


def potong_teks(teks: str, panjang_maks: int = 50) -> str:
    """
    Memotong teks panjang untuk keperluan tampilan.

    Parameter:
        teks (str): Teks yang akan dipotong.
        panjang_maks (int): Panjang maksimum karakter yang ditampilkan.

    Mengembalikan:
        str: Teks yang sudah dipotong dengan '...' jika diperlukan.
    """
    if len(teks) > panjang_maks:
        return teks[:panjang_maks] + "..."
    return teks
