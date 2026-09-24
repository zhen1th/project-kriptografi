# ============================================================
# super_cipher.py
# Implementasi Super Cipher — gabungan 4 algoritma berurutan
#
# Urutan Enkripsi:
#   Plaintext → Caesar → Rail Fence → Stream Cipher → Block Cipher → Ciphertext
#
# Urutan Dekripsi (terbalik):
#   Ciphertext → Block Decipher → Stream Decipher → Rail Fence Decipher → Caesar Decipher → Plaintext
#
# Semua menggunakan K = 8
# ============================================================

from algorithms.caesar import enkripsi_caesar, dekripsi_caesar
from algorithms.rail_fence import enkripsi_rail_fence, dekripsi_rail_fence
from algorithms.stream_cipher import enkripsi_stream_cipher, dekripsi_stream_cipher
from algorithms.block_cipher import enkripsi_block_cipher, dekripsi_block_cipher


def enkripsi_super_cipher(teks_asli: str) -> dict:
    """
    Mengenkripsi teks menggunakan Super Cipher (4 tahap berurutan).

    Urutan: Caesar → Rail Fence → Stream Cipher → Block Cipher

    Parameter:
        teks_asli (str): Teks yang akan dienkripsi.

    Mengembalikan:
        dict: Berisi input/output dan detail setiap tahap enkripsi.
    """
    hasil = {}

    # ── Tahap 1: Caesar Cipher ──────────────────────────────
    # Geser setiap huruf sebesar K = 8 posisi dalam alfabet
    hasil_caesar, langkah_caesar = enkripsi_caesar(teks_asli)
    hasil['tahap_1'] = {
        'nama': 'Caesar Cipher',
        'input': teks_asli,
        'output': hasil_caesar,
        'langkah': langkah_caesar,
    }

    # ── Tahap 2: Rail Fence Cipher ──────────────────────────
    # Susun karakter dalam pola zig-zag pada 8 rail, baca per rail
    hasil_rail_fence, matriks_rail, hasil_per_rail = enkripsi_rail_fence(hasil_caesar)
    hasil['tahap_2'] = {
        'nama': 'Rail Fence Cipher',
        'input': hasil_caesar,
        'output': hasil_rail_fence,
        'matriks_rail': matriks_rail,
        'hasil_per_rail': hasil_per_rail,
    }

    # ── Tahap 3: Stream Cipher ──────────────────────────────
    # Enkripsi per byte menggunakan XOR dengan keystream LFSR
    # Input: teks hasil Rail Fence (berupa karakter)
    # Output: format hexadecimal (string hex dipisah spasi)
    hasil_stream, langkah_stream, keystream_stream = enkripsi_stream_cipher(hasil_rail_fence)
    hasil['tahap_3'] = {
        'nama': 'Stream Cipher',
        'input': hasil_rail_fence,
        'output': hasil_stream,   # format: "XX XX XX ..."
        'langkah': langkah_stream,
        'keystream': keystream_stream,
    }

    # ── Tahap 4: Block Cipher ───────────────────────────────
    # Input: output Stream Cipher (string hex dipisah spasi)
    # Proses: parse hex → XOR setiap byte dengan K=8 → output hex baru
    # Ini adalah "double encryption" pada level byte
    hasil_block, langkah_block, jumlah_padding = enkripsi_block_cipher_dari_hex(hasil_stream)
    hasil['tahap_4'] = {
        'nama': 'Block Cipher',
        'input': hasil_stream,    # format: "XX XX XX ..."
        'output': hasil_block,    # format: "XX XX XX ..."
        'langkah': langkah_block,
        'jumlah_padding': jumlah_padding,
    }

    # Ciphertext akhir adalah output dari Block Cipher (format hexadecimal)
    hasil['ciphertext_akhir'] = hasil_block
    hasil['teks_asli'] = teks_asli

    return hasil


def dekripsi_super_cipher(teks_sandi_hex: str) -> dict:
    """
    Mendekripsi teks dari Super Cipher (4 tahap terbalik).

    Urutan: Block Decipher → Stream Decipher → Rail Fence Decipher → Caesar Decipher

    Parameter:
        teks_sandi_hex (str): Ciphertext dalam format hexadecimal (dipisah spasi).

    Mengembalikan:
        dict: Berisi input/output dan detail setiap tahap dekripsi.

    Raise:
        ValueError: Jika format hexadecimal tidak valid.
    """
    hasil = {}

    # ── Tahap 1: Block Decipher ─────────────────────────────
    # Balik XOR Block Cipher: P = C XOR K
    # Input: hex string dari ciphertext akhir
    # Output: hex string (hasil stream cipher sebelumnya)
    hasil_block_decipher, langkah_block = dekripsi_block_cipher_ke_hex(teks_sandi_hex)
    hasil['tahap_1'] = {
        'nama': 'Block Cipher Dekripsi',
        'input': teks_sandi_hex,
        'output': hasil_block_decipher,   # format: "XX XX XX ..."
        'langkah': langkah_block,
    }

    # ── Tahap 2: Stream Decipher ────────────────────────────
    # Balik XOR Stream Cipher: P = C XOR Keystream
    # Input: hex string (output block decipher = output stream cipher asli)
    # Output: teks karakter (hasil Rail Fence)
    hasil_stream_decipher, langkah_stream, keystream = dekripsi_stream_cipher(hasil_block_decipher)
    hasil['tahap_2'] = {
        'nama': 'Stream Cipher Dekripsi',
        'input': hasil_block_decipher,
        'output': hasil_stream_decipher,  # teks karakter
        'langkah': langkah_stream,
        'keystream': keystream,
    }

    # ── Tahap 3: Rail Fence Decipher ────────────────────────
    # Kembalikan posisi karakter dari pola zig-zag
    hasil_rail_fence_decipher, matriks_rail, hasil_per_rail = dekripsi_rail_fence(hasil_stream_decipher)
    hasil['tahap_3'] = {
        'nama': 'Rail Fence Cipher Dekripsi',
        'input': hasil_stream_decipher,
        'output': hasil_rail_fence_decipher,
        'matriks_rail': matriks_rail,
        'hasil_per_rail': hasil_per_rail,
    }

    # ── Tahap 4: Caesar Decipher ────────────────────────────
    # Kembalikan nilai karakter: P = (C - K) mod 26
    hasil_caesar_decipher, langkah_caesar = dekripsi_caesar(hasil_rail_fence_decipher)
    hasil['tahap_4'] = {
        'nama': 'Caesar Cipher Dekripsi',
        'input': hasil_rail_fence_decipher,
        'output': hasil_caesar_decipher,
        'langkah': langkah_caesar,
    }

    # Plaintext akhir adalah output dari Caesar Decipher
    hasil['plaintext_akhir'] = hasil_caesar_decipher
    hasil['ciphertext_awal'] = teks_sandi_hex

    return hasil


# ──────────────────────────────────────────────────────────────
# Fungsi bantuan internal Super Cipher
# Block Cipher yang bekerja pada data hex (output Stream Cipher)
# ──────────────────────────────────────────────────────────────

KUNCI = 8
NILAI_KUNCI_BINER = KUNCI & 0xFF  # = 00001000


def enkripsi_block_cipher_dari_hex(data_hex: str) -> tuple[str, list[dict], int]:
    """
    Mengenkripsi data dalam format hex menggunakan Block Cipher (XOR per byte).

    Input adalah string hex dipisah spasi (output Stream Cipher).
    Setiap byte XOR-kan dengan kunci K = 8.

    Parameter:
        data_hex (str): Data dalam format hexadecimal, misalnya "48 45 4C".

    Mengembalikan:
        tuple: (hasil_hex, langkah_enkripsi, jumlah_padding)
    """
    daftar_hex = data_hex.strip().split()
    data_byte = [int(nilai_hex, 16) for nilai_hex in daftar_hex]

    langkah_enkripsi = []
    data_sandi = []

    for nomor_blok, nilai_byte in enumerate(data_byte, start=1):
        hasil_xor = nilai_byte ^ NILAI_KUNCI_BINER
        data_sandi.append(hasil_xor)

        langkah_enkripsi.append({
            "Blok": nomor_blok,
            "Input Hex": format(nilai_byte, '02X'),
            "Biner Input": format(nilai_byte, '08b'),
            "Kunci (K=8)": format(NILAI_KUNCI_BINER, '08b'),
            "Operasi": "XOR",
            "Biner Output": format(hasil_xor, '08b'),
            "Output Hex": format(hasil_xor, '02X'),
        })

    hasil_hex = ' '.join(format(nilai, '02X') for nilai in data_sandi)
    return hasil_hex, langkah_enkripsi, 0


def dekripsi_block_cipher_ke_hex(data_hex: str) -> tuple[str, list[dict]]:
    """
    Mendekripsi data hex menggunakan Block Cipher (XOR per byte).

    Karena XOR bersifat simetris (A XOR K XOR K = A),
    proses dekripsi sama persis dengan enkripsi.

    Parameter:
        data_hex (str): Data dalam format hexadecimal.

    Mengembalikan:
        tuple: (hasil_hex, langkah_dekripsi)
            hasil_hex adalah hex string (output = input Stream Cipher asli)
    """
    daftar_hex = data_hex.strip().split()
    data_byte = [int(nilai_hex, 16) for nilai_hex in daftar_hex]

    langkah_dekripsi = []
    data_asli = []

    for nomor_blok, nilai_byte in enumerate(data_byte, start=1):
        hasil_xor = nilai_byte ^ NILAI_KUNCI_BINER
        data_asli.append(hasil_xor)

        langkah_dekripsi.append({
            "Blok": nomor_blok,
            "Input Hex (Sandi)": format(nilai_byte, '02X'),
            "Biner Sandi": format(nilai_byte, '08b'),
            "Kunci (K=8)": format(NILAI_KUNCI_BINER, '08b'),
            "Operasi": "XOR",
            "Biner Output": format(hasil_xor, '08b'),
            "Output Hex": format(hasil_xor, '02X'),
        })

    hasil_hex = ' '.join(format(nilai, '02X') for nilai in data_asli)
    return hasil_hex, langkah_dekripsi
