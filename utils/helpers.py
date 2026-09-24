# ============================================================
# helpers.py
# Fungsi-fungsi pembantu yang digunakan di seluruh aplikasi
# ============================================================


def ubah_ke_biner(teks: str) -> list[str]:
    return [format(ord(karakter), '08b') for karakter in teks]


def ubah_ke_heksadesimal(teks: str) -> list[str]:
    return [format(ord(karakter), '02X') for karakter in teks]


def biner_ke_teks(daftar_biner: list[str]) -> str:
    return ''.join(chr(int(biner, 2)) for biner in daftar_biner)


def heksadesimal_ke_teks(daftar_hex: list[str]) -> str:
    return ''.join(chr(int(nilai_hex, 16)) for nilai_hex in daftar_hex)


def validasi_hex(teks_hex: str) -> bool:
    try:
        for nilai_hex in teks_hex.strip().split():
            int(nilai_hex, 16)
        return True
    except ValueError:
        return False


def format_tampilan_hex(data_byte: list[int]) -> str:
    return ' '.join(format(nilai, '02X') for nilai in data_byte)


def potong_teks(teks: str, panjang_maks: int = 50) -> str:
    if len(teks) > panjang_maks:
        return teks[:panjang_maks] + "..."
    return teks
