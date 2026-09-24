# ============================================================
# block_cipher.py
# Implementasi algoritma Block Cipher berbasis XOR
# Konsep: Enkripsi teks per blok 8 bit menggunakan XOR dengan kunci
# Ukuran blok: 8 bit (1 byte)
# Rumus Enkripsi : C = P XOR K
# Rumus Dekripsi : P = C XOR K
# K = 8 → representasi 8-bit: 00001000
# ============================================================

KUNCI = 8        # Kunci K = 8
UKURAN_BLOK = 8  # Ukuran blok dalam bit (1 byte = 8 bit)

# Nilai kunci dalam bentuk integer 8-bit
NILAI_KUNCI_BINER = KUNCI & 0xFF  # = 8 = 00001000


def enkripsi_block_cipher(teks_asli: str) -> tuple[str, list[dict], int]:
    """
    Mengenkripsi teks menggunakan Block Cipher (XOR per blok 8 bit).

    Parameter:
        teks_asli (str): Teks yang akan dienkripsi.

    Mengembalikan:
        tuple: (teks_sandi_hex, langkah_enkripsi, jumlah_padding)
            - teks_sandi_hex (str): Hasil enkripsi dalam format hexadecimal.
            - langkah_enkripsi (list[dict]): Detail proses setiap blok.
            - jumlah_padding (int): Jumlah byte padding yang ditambahkan.
    """
    # Konversi teks ke byte
    data_byte = [ord(karakter) for karakter in teks_asli]

    # Hitung padding yang dibutuhkan
    # Untuk blok 8 bit (1 byte), setiap karakter sudah 1 byte
    # Namun kita tampilkan proses padding untuk keperluan edukasi
    # Dalam implementasi ini, setiap byte = 1 blok (8 bit), sehingga tidak perlu padding
    jumlah_padding = 0  # Karena setiap byte ASCII sudah tepat 8 bit

    langkah_enkripsi = []
    data_sandi = []

    for nomor_blok, nilai_byte in enumerate(data_byte, start=1):
        # XOR antara plaintext byte dan kunci
        hasil_xor = nilai_byte ^ NILAI_KUNCI_BINER
        data_sandi.append(hasil_xor)

        langkah_enkripsi.append({
            "Blok": nomor_blok,
            "Karakter": teks_asli[nomor_blok - 1],
            "Biner Plaintext": format(nilai_byte, '08b'),
            "Kunci (K)": format(NILAI_KUNCI_BINER, '08b'),
            "Operasi": "XOR",
            "Biner Sandi": format(hasil_xor, '08b'),
            "Hex": format(hasil_xor, '02X'),
        })

    # Gabungkan hasil dalam format hexadecimal
    teks_sandi_hex = ' '.join(format(nilai, '02X') for nilai in data_sandi)

    return teks_sandi_hex, langkah_enkripsi, jumlah_padding


def dekripsi_block_cipher(teks_sandi_hex: str) -> tuple[str, list[dict]]:
    """
    Mendekripsi teks dari format hexadecimal menggunakan Block Cipher.

    Parameter:
        teks_sandi_hex (str): Ciphertext dalam format hexadecimal (dipisah spasi).

    Mengembalikan:
        tuple: (teks_asli, langkah_dekripsi)
            - teks_asli (str): Hasil dekripsi.
            - langkah_dekripsi (list[dict]): Detail proses setiap blok.

    Raise:
        ValueError: Jika format hexadecimal tidak valid.
    """
    # Parse hexadecimal menjadi daftar byte
    try:
        daftar_hex = teks_sandi_hex.strip().split()
        data_byte_sandi = [int(nilai_hex, 16) for nilai_hex in daftar_hex]
    except ValueError:
        raise ValueError("Format hexadecimal tidak valid. Gunakan format: 'XX XX XX ...'")

    langkah_dekripsi = []
    teks_asli = ""

    for nomor_blok, nilai_sandi in enumerate(data_byte_sandi, start=1):
        # XOR antara ciphertext byte dan kunci (dekripsi = enkripsi ulang dengan kunci sama)
        hasil_xor = nilai_sandi ^ NILAI_KUNCI_BINER
        karakter_asli = chr(hasil_xor)
        teks_asli += karakter_asli

        langkah_dekripsi.append({
            "Blok": nomor_blok,
            "Hex Sandi": format(nilai_sandi, '02X'),
            "Biner Sandi": format(nilai_sandi, '08b'),
            "Kunci (K)": format(NILAI_KUNCI_BINER, '08b'),
            "Operasi": "XOR",
            "Biner Plaintext": format(hasil_xor, '08b'),
            "Karakter": karakter_asli,
        })

    return teks_asli, langkah_dekripsi
