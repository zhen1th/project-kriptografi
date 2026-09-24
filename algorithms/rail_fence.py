# ============================================================
# rail_fence.py
# Implementasi algoritma Rail Fence Cipher
# Konsep: Transposisi karakter menggunakan pola zig-zag
# Jumlah rail = K = 8
# ============================================================

KUNCI = 8  # Jumlah rail = K = 8


def buat_pola_zigzag(panjang_teks: int, jumlah_rail: int) -> list[int]:
    """
    Membuat pola zig-zag berupa daftar nomor rail untuk setiap posisi karakter.

    Parameter:
        panjang_teks (int): Jumlah karakter dalam teks.
        jumlah_rail (int): Jumlah rail yang digunakan.

    Mengembalikan:
        list[int]: Daftar nomor rail (0 s.d. jumlah_rail-1) untuk setiap posisi.
    """
    pola_rail = []
    nomor_rail_saat_ini = 0
    arah = 1  # 1 = ke bawah, -1 = ke atas

    for _ in range(panjang_teks):
        pola_rail.append(nomor_rail_saat_ini)
        # Balik arah jika sudah di ujung rail
        if nomor_rail_saat_ini == 0:
            arah = 1
        elif nomor_rail_saat_ini == jumlah_rail - 1:
            arah = -1
        nomor_rail_saat_ini += arah

    return pola_rail


def enkripsi_rail_fence(teks_asli: str) -> tuple[str, list, list[str]]:
    """
    Mengenkripsi teks menggunakan Rail Fence Cipher.

    Parameter:
        teks_asli (str): Teks yang akan dienkripsi (spasi dipertahankan).

    Mengembalikan:
        tuple: (teks_sandi, matriks_rail, hasil_per_rail)
            - teks_sandi (str): Hasil enkripsi.
            - matriks_rail (list): Visualisasi pola zig-zag.
            - hasil_per_rail (list[str]): Isi karakter setiap rail.
    """
    jumlah_rail = KUNCI

    # Jika rail lebih banyak dari panjang teks, sesuaikan
    if jumlah_rail > len(teks_asli):
        jumlah_rail = len(teks_asli)

    # Buat pola zig-zag
    pola_rail = buat_pola_zigzag(len(teks_asli), jumlah_rail)

    # Buat matriks untuk visualisasi
    # matriks_rail[baris][kolom] = karakter atau '.'
    matriks_rail = [['.' for _ in range(len(teks_asli))] for _ in range(jumlah_rail)]

    for posisi, karakter in enumerate(teks_asli):
        nomor_baris = pola_rail[posisi]
        matriks_rail[nomor_baris][posisi] = karakter

    # Baca setiap rail dari kiri ke kanan untuk membentuk ciphertext
    hasil_per_rail = []
    teks_sandi = ""
    for baris in range(jumlah_rail):
        isi_rail = ""
        for kolom in range(len(teks_asli)):
            if matriks_rail[baris][kolom] != '.':
                isi_rail += matriks_rail[baris][kolom]
        hasil_per_rail.append(isi_rail)
        teks_sandi += isi_rail

    return teks_sandi, matriks_rail, hasil_per_rail


def dekripsi_rail_fence(teks_sandi: str) -> tuple[str, list, list[str]]:
    """
    Mendekripsi teks menggunakan Rail Fence Cipher.

    Parameter:
        teks_sandi (str): Teks yang akan didekripsi.

    Mengembalikan:
        tuple: (teks_asli, matriks_rail, hasil_per_rail)
            - teks_asli (str): Hasil dekripsi.
            - matriks_rail (list): Visualisasi pola zig-zag.
            - hasil_per_rail (list[str]): Karakter per rail.
    """
    jumlah_rail = KUNCI
    panjang = len(teks_sandi)

    if jumlah_rail > panjang:
        jumlah_rail = panjang

    # Buat pola zig-zag untuk mengetahui posisi setiap rail
    pola_rail = buat_pola_zigzag(panjang, jumlah_rail)

    # Hitung jumlah karakter per rail
    jumlah_karakter_per_rail = [0] * jumlah_rail
    for nomor_rail in pola_rail:
        jumlah_karakter_per_rail[nomor_rail] += 1

    # Distribusikan karakter ciphertext ke setiap rail
    hasil_per_rail = []
    posisi_awal = 0
    for baris in range(jumlah_rail):
        posisi_akhir = posisi_awal + jumlah_karakter_per_rail[baris]
        hasil_per_rail.append(teks_sandi[posisi_awal:posisi_akhir])
        posisi_awal = posisi_akhir

    # Rekonstruksi teks dengan membaca ulang mengikuti pola zig-zag
    indeks_per_rail = [0] * jumlah_rail
    teks_asli = ""

    # Buat matriks untuk visualisasi
    matriks_rail = [['.' for _ in range(panjang)] for _ in range(jumlah_rail)]

    for posisi in range(panjang):
        nomor_baris = pola_rail[posisi]
        indeks_dalam_rail = indeks_per_rail[nomor_baris]
        karakter = hasil_per_rail[nomor_baris][indeks_dalam_rail]
        teks_asli += karakter
        matriks_rail[nomor_baris][posisi] = karakter
        indeks_per_rail[nomor_baris] += 1

    return teks_asli, matriks_rail, hasil_per_rail
