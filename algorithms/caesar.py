# ============================================================
# caesar.py
# Implementasi algoritma Caesar Cipher
# Konsep: substitusi karakter dengan pergeseran sebesar K
# Rumus Enkripsi : C = (P + K) mod 26
# Rumus Dekripsi : P = (C - K) mod 26
# ============================================================

KUNCI = 8  # Kunci tetap K = 8


def enkripsi_caesar(teks_asli: str) -> tuple[str, list[dict]]:
    """
    Mengenkripsi teks menggunakan Caesar Cipher.

    Parameter:
        teks_asli (str): Teks yang akan dienkripsi.

    Mengembalikan:
        tuple: (teks_sandi, langkah_enkripsi)
            - teks_sandi (str): Hasil enkripsi.
            - langkah_enkripsi (list[dict]): Daftar langkah per karakter.
    """
    teks_sandi = ""
    langkah_enkripsi = []

    for nomor, karakter in enumerate(teks_asli, start=1):
        if karakter.isalpha():
            # Konversi ke huruf kapital untuk keseragaman
            karakter_kapital = karakter.upper()
            # Hitung nilai P (posisi dalam alfabet, A=0)
            nilai_plaintext = ord(karakter_kapital) - ord('A')
            # Rumus enkripsi: C = (P + K) mod 26
            nilai_ciphertext = (nilai_plaintext + KUNCI) % 26
            # Konversi kembali ke karakter
            karakter_sandi = chr(nilai_ciphertext + ord('A'))
            teks_sandi += karakter_sandi

            langkah_enkripsi.append({
                "No": nomor,
                "Plaintext": karakter_kapital,
                "Nilai P": nilai_plaintext,
                "Rumus": f"({nilai_plaintext} + {KUNCI}) mod 26",
                "Nilai C": nilai_ciphertext,
                "Ciphertext": karakter_sandi,
            })
        else:
            # Karakter bukan huruf (spasi, tanda baca) dipertahankan
            teks_sandi += karakter
            langkah_enkripsi.append({
                "No": nomor,
                "Plaintext": karakter,
                "Nilai P": "-",
                "Rumus": "Bukan huruf, dipertahankan",
                "Nilai C": "-",
                "Ciphertext": karakter,
            })

    return teks_sandi, langkah_enkripsi


def dekripsi_caesar(teks_sandi: str) -> tuple[str, list[dict]]:
    """
    Mendekripsi teks menggunakan Caesar Cipher.

    Parameter:
        teks_sandi (str): Teks yang akan didekripsi.

    Mengembalikan:
        tuple: (teks_asli, langkah_dekripsi)
            - teks_asli (str): Hasil dekripsi.
            - langkah_dekripsi (list[dict]): Daftar langkah per karakter.
    """
    teks_asli = ""
    langkah_dekripsi = []

    for nomor, karakter in enumerate(teks_sandi, start=1):
        if karakter.isalpha():
            karakter_kapital = karakter.upper()
            # Hitung nilai C (posisi dalam alfabet)
            nilai_ciphertext = ord(karakter_kapital) - ord('A')
            # Rumus dekripsi: P = (C - K) mod 26
            nilai_plaintext = (nilai_ciphertext - KUNCI) % 26
            karakter_asli = chr(nilai_plaintext + ord('A'))
            teks_asli += karakter_asli

            langkah_dekripsi.append({
                "No": nomor,
                "Ciphertext": karakter_kapital,
                "Nilai C": nilai_ciphertext,
                "Rumus": f"({nilai_ciphertext} - {KUNCI}) mod 26",
                "Nilai P": nilai_plaintext,
                "Plaintext": karakter_asli,
            })
        else:
            teks_asli += karakter
            langkah_dekripsi.append({
                "No": nomor,
                "Ciphertext": karakter,
                "Nilai C": "-",
                "Rumus": "Bukan huruf, dipertahankan",
                "Nilai P": "-",
                "Plaintext": karakter,
            })

    return teks_asli, langkah_dekripsi
