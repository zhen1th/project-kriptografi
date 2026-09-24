# ============================================================
# stream_cipher.py
# Implementasi algoritma Stream Cipher berbasis XOR
# Konsep: Enkripsi per byte menggunakan XOR dengan keystream
# Generator keystream: LFSR (Linear Feedback Shift Register)
# Rumus Enkripsi : C = P XOR K
# Rumus Dekripsi : P = C XOR K
# Kunci awal / seed: K = 8
# ============================================================

KUNCI = 8  # Seed awal untuk LFSR = K = 8

# Parameter LFSR yang digunakan:
# - Register awal : 8 bit (diisi dari nilai KUNCI = 8)
# - Panjang register: 8 bit
# - Tap (posisi feedback): bit ke-8 dan bit ke-4 (indeks 7 dan 3)
# Parameter ini tetap dan deterministik agar keystream selalu sama.
PANJANG_REGISTER = 8
POSISI_TAP = [7, 3]  # Posisi tap untuk feedback LFSR (0-indexed dari kiri)


def buat_keystream(panjang: int) -> tuple[list[int], list[list[int]]]:
    # Inisialisasi register LFSR dari nilai KUNCI dalam bentuk 8 bit
    register = [(KUNCI >> (PANJANG_REGISTER - 1 - bit)) & 1
                for bit in range(PANJANG_REGISTER)]

    # Pastikan register tidak semua nol (LFSR tidak boleh diinisialisasi dengan semua 0)
    if all(bit == 0 for bit in register):
        register[0] = 1

    keystream_byte = []
    riwayat_register = [register[:]]  # Simpan keadaan awal register

    for _ in range(panjang):
        byte_keystream = 0
        for posisi_bit in range(PANJANG_REGISTER):
            # Hitung bit feedback dari XOR posisi tap
            bit_feedback = 0
            for posisi_tap in POSISI_TAP:
                bit_feedback ^= register[posisi_tap]

            # Ambil bit output (bit paling kanan / LSB)
            bit_output = register[PANJANG_REGISTER - 1]

            # Geser register ke kanan, masukkan feedback di kiri
            register = [bit_feedback] + register[:PANJANG_REGISTER - 1]

            # Susun byte dari bit output
            byte_keystream = (byte_keystream << 1) | bit_output

        keystream_byte.append(byte_keystream)
        riwayat_register.append(register[:])

    return keystream_byte, riwayat_register


def enkripsi_stream_cipher(teks_asli: str) -> tuple[str, list[dict], list[int]]:
    # Konversi teks ke byte (ASCII)
    data_byte = [ord(karakter) for karakter in teks_asli]
    panjang = len(data_byte)

    # Generate keystream
    keystream, _ = buat_keystream(panjang)

    langkah_enkripsi = []
    data_sandi = []

    for nomor_byte, (nilai_plaintext, nilai_keystream) in enumerate(
            zip(data_byte, keystream), start=1):
        # XOR antara plaintext byte dan keystream byte
        hasil_xor = nilai_plaintext ^ nilai_keystream
        data_sandi.append(hasil_xor)

        langkah_enkripsi.append({
            "Byte": nomor_byte,
            "Karakter": teks_asli[nomor_byte - 1],
            "Biner Plaintext": format(nilai_plaintext, '08b'),
            "Biner Keystream": format(nilai_keystream, '08b'),
            "Hasil XOR (Biner)": format(hasil_xor, '08b'),
            "Hex": format(hasil_xor, '02X'),
        })

    # Gabungkan hasil dalam format hexadecimal
    teks_sandi_hex = ' '.join(format(nilai, '02X') for nilai in data_sandi)

    return teks_sandi_hex, langkah_enkripsi, keystream


def dekripsi_stream_cipher(teks_sandi_hex: str) -> tuple[str, list[dict], list[int]]:
    # Parse hexadecimal menjadi daftar byte
    try:
        daftar_hex = teks_sandi_hex.strip().split()
        data_byte_sandi = [int(nilai_hex, 16) for nilai_hex in daftar_hex]
    except ValueError:
        raise ValueError("Format hexadecimal tidak valid. Gunakan format: 'XX XX XX ...'")

    panjang = len(data_byte_sandi)

    # Generate keystream yang sama
    keystream, _ = buat_keystream(panjang)

    langkah_dekripsi = []
    teks_asli = ""

    for nomor_byte, (nilai_sandi, nilai_keystream) in enumerate(
            zip(data_byte_sandi, keystream), start=1):
        # XOR antara ciphertext byte dan keystream byte
        hasil_xor = nilai_sandi ^ nilai_keystream
        karakter_asli = chr(hasil_xor)
        teks_asli += karakter_asli

        langkah_dekripsi.append({
            "Byte": nomor_byte,
            "Hex Sandi": format(nilai_sandi, '02X'),
            "Biner Sandi": format(nilai_sandi, '08b'),
            "Biner Keystream": format(nilai_keystream, '08b'),
            "Hasil XOR (Biner)": format(hasil_xor, '08b'),
            "Karakter": karakter_asli,
        })

    return teks_asli, langkah_dekripsi, keystream
