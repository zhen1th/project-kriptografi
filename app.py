# ============================================================
# app.py
# Aplikasi Pembelajaran Kriptografi — Streamlit
# Kelompok Kriptografi | Kunci tetap: K = 8
#
# Jalankan dengan: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd

from algorithms.caesar import enkripsi_caesar, dekripsi_caesar
from algorithms.rail_fence import enkripsi_rail_fence, dekripsi_rail_fence, buat_pola_zigzag
from algorithms.stream_cipher import (
    enkripsi_stream_cipher,
    dekripsi_stream_cipher,
    buat_keystream,
    KUNCI as KUNCI_STREAM,
    POSISI_TAP,
    PANJANG_REGISTER,
)
from algorithms.block_cipher import (
    enkripsi_block_cipher,
    dekripsi_block_cipher,
    NILAI_KUNCI_BINER,
)
from algorithms.super_cipher import (
    enkripsi_super_cipher,
    dekripsi_super_cipher,
)

# ──────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Aplikasi Pembelajaran Kriptografi",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# KONSTANTA
# ──────────────────────────────────────────────
KUNCI_GLOBAL = 8  # Kunci tetap K = 8


# ============================================================
# FUNGSI TAMPILAN MATRIKS RAIL FENCE
# Menggunakan teks biasa tanpa HTML/CSS kustom
# ============================================================

def tampilkan_matriks_rail_fence_teks(matriks_rail: list, jumlah_rail: int, panjang_teks: int):
    """
    Menampilkan visualisasi matriks Rail Fence dalam bentuk teks biasa.
    Menggunakan st.code() agar terlihat rapi tanpa HTML/CSS.
    """
    baris_output = []
    for nomor_baris in range(jumlah_rail):
        # Buat representasi setiap baris/rail
        baris = f"Rail {nomor_baris + 1:2d}: "
        for kolom in range(panjang_teks):
            karakter = matriks_rail[nomor_baris][kolom]
            if karakter != '.':
                baris += f" {karakter} "
            else:
                baris += " . "
        baris_output.append(baris)
    st.code('\n'.join(baris_output), language=None)


# ============================================================
# HALAMAN: CAESAR CIPHER
# ============================================================

def tampilkan_caesar():
    st.header("Caesar Cipher")
    st.write(
        "Caesar Cipher adalah algoritma substitusi klasik. "
        "Setiap huruf digeser sebesar K posisi dalam alfabet (A=0, B=1, ..., Z=25)."
    )
    st.write(f"Kunci yang digunakan: K = {KUNCI_GLOBAL}")
    st.write("Rumus Enkripsi: C = (P + K) mod 26")
    st.write("Rumus Dekripsi: P = (C - K) mod 26")

    st.divider()

    mode = st.session_state.get("caesar_mode", None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enkripsi", key="caesar_pilih_enkripsi", use_container_width=True, type="primary" if mode == "Enkripsi" else "secondary"):
            st.session_state["caesar_mode"] = "Enkripsi"
            st.rerun()
    with col2:
        if st.button("Dekripsi", key="caesar_pilih_dekripsi", use_container_width=True, type="primary" if mode == "Dekripsi" else "secondary"):
            st.session_state["caesar_mode"] = "Dekripsi"
            st.rerun()

    if mode is None:
        st.info("Silakan klik tombol Enkripsi atau Dekripsi di atas untuk menampilkan formulir.")
        return

    if mode == "Enkripsi":
        st.subheader("Enkripsi Caesar Cipher")
        teks_input = st.text_area(
            "Plaintext:",
            placeholder="Masukkan teks yang akan dienkripsi. Contoh: HELLO WORLD",
            height=100,
            key="caesar_enkripsi_input"
        )

        if st.button("Proses Enkripsi", key="caesar_btn_enkripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong. Masukkan plaintext terlebih dahulu.")
            else:
                teks_asli = teks_input.upper()
                teks_sandi, langkah_enkripsi = enkripsi_caesar(teks_asli)

                with st.expander("Langkah 1 - Tabel Perhitungan Enkripsi", expanded=True):
                    st.write(f"Rumus: C = (P + {KUNCI_GLOBAL}) mod 26")
                    df_langkah = pd.DataFrame(langkah_enkripsi)
                    st.dataframe(df_langkah, use_container_width=True, hide_index=True)

                with st.expander("Langkah 2 - Referensi Alfabet"):
                    daftar_alfabet = "  ".join(
                        f"{chr(65 + indeks)}={indeks}" for indeks in range(26)
                    )
                    st.code(daftar_alfabet, language=None)

                with st.expander("Langkah 3 - Hasil Enkripsi"):
                    st.write(f"Plaintext  : {teks_asli}")
                    st.write(f"Kunci      : K = {KUNCI_GLOBAL}")
                    st.write(f"Ciphertext : {teks_sandi}")

                st.divider()
                st.subheader("Hasil Enkripsi")
                st.write(f"Plaintext  : {teks_asli}")
                st.write(f"Ciphertext : {teks_sandi}")
                st.success(f"Enkripsi selesai.")

    else:  # mode == "Dekripsi"
        st.subheader("Dekripsi Caesar Cipher")
        teks_input = st.text_area(
            "Ciphertext:",
            placeholder="Masukkan ciphertext yang akan didekripsi. Contoh: PMTTW EWZTL",
            height=100,
            key="caesar_dekripsi_input"
        )

        if st.button("Proses Dekripsi", key="caesar_btn_dekripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong. Masukkan ciphertext terlebih dahulu.")
            else:
                teks_sandi = teks_input.upper()
                teks_asli, langkah_dekripsi = dekripsi_caesar(teks_sandi)

                with st.expander("Langkah 1 - Tabel Perhitungan Dekripsi", expanded=True):
                    st.write(f"Rumus: P = (C - {KUNCI_GLOBAL}) mod 26")
                    df_langkah = pd.DataFrame(langkah_dekripsi)
                    st.dataframe(df_langkah, use_container_width=True, hide_index=True)

                with st.expander("Langkah 2 - Hasil Dekripsi"):
                    st.write(f"Ciphertext : {teks_sandi}")
                    st.write(f"Kunci      : K = {KUNCI_GLOBAL}")
                    st.write(f"Plaintext  : {teks_asli}")

                st.divider()
                st.subheader("Hasil Dekripsi")
                st.write(f"Ciphertext : {teks_sandi}")
                st.write(f"Plaintext  : {teks_asli}")
                st.success("Dekripsi selesai.")


# ============================================================
# HALAMAN: RAIL FENCE CIPHER
# ============================================================

def tampilkan_rail_fence():
    st.header("Rail Fence Cipher")
    st.write(
        "Rail Fence Cipher adalah algoritma transposisi klasik. "
        "Karakter disusun dalam pola zig-zag pada sejumlah rail (baris), "
        "lalu dibaca dari setiap rail secara berurutan."
    )
    st.write(f"Kunci yang digunakan: K = {KUNCI_GLOBAL} (jumlah rail = {KUNCI_GLOBAL})")

    st.divider()

    mode = st.session_state.get("rail_mode", None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enkripsi", key="rail_pilih_enkripsi", use_container_width=True, type="primary" if mode == "Enkripsi" else "secondary"):
            st.session_state["rail_mode"] = "Enkripsi"
            st.rerun()
    with col2:
        if st.button("Dekripsi", key="rail_pilih_dekripsi", use_container_width=True, type="primary" if mode == "Dekripsi" else "secondary"):
            st.session_state["rail_mode"] = "Dekripsi"
            st.rerun()

    if mode is None:
        st.info("Silakan klik tombol Enkripsi atau Dekripsi di atas untuk menampilkan formulir.")
        return

    if mode == "Enkripsi":
        st.subheader("Enkripsi Rail Fence Cipher")
        teks_input = st.text_area(
            "Plaintext:",
            placeholder="Masukkan teks yang akan dienkripsi. Contoh: HELLO WORLD",
            height=100,
            key="rail_enkripsi_input"
        )

        if st.button("Proses Enkripsi", key="rail_btn_enkripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                teks_asli = teks_input.upper()
                jumlah_rail_efektif = min(KUNCI_GLOBAL, len(teks_asli))
                teks_sandi, matriks_rail, hasil_per_rail = enkripsi_rail_fence(teks_asli)

                with st.expander("Langkah 1 - Pola Zig-Zag per Karakter", expanded=True):
                    st.write(f"Panjang teks : {len(teks_asli)} karakter")
                    st.write(f"Jumlah rail  : {jumlah_rail_efektif}")
                    pola_rail = buat_pola_zigzag(len(teks_asli), jumlah_rail_efektif)
                    df_pola = pd.DataFrame({
                        "Posisi": range(1, len(teks_asli) + 1),
                        "Karakter": list(teks_asli),
                        "Nomor Rail": [rail + 1 for rail in pola_rail],
                    })
                    st.dataframe(df_pola, use_container_width=True, hide_index=True)

                with st.expander("Langkah 2 - Visualisasi Matriks Rail", expanded=True):
                    st.write("Karakter ditempatkan pada rail sesuai pola zig-zag (titik = posisi kosong):")
                    tampilkan_matriks_rail_fence_teks(matriks_rail, jumlah_rail_efektif, len(teks_asli))

                with st.expander("Langkah 3 - Pembacaan per Rail"):
                    st.write("Baca karakter dari setiap rail dari kiri ke kanan:")
                    for nomor_baris, isi_rail in enumerate(hasil_per_rail, start=1):
                        if isi_rail:
                            st.write(f"Rail {nomor_baris}: {isi_rail}")

                with st.expander("Langkah 4 - Pembentukan Ciphertext"):
                    st.write("Gabungkan semua rail:")
                    for nomor_baris, isi_rail in enumerate(hasil_per_rail, start=1):
                        if isi_rail:
                            st.write(f"  Rail {nomor_baris}: {isi_rail}")
                    st.write(f"Ciphertext: {teks_sandi}")

                st.divider()
                st.subheader("Hasil Enkripsi")
                st.write(f"Plaintext  : {teks_asli}")
                st.write(f"Ciphertext : {teks_sandi}")
                st.success("Enkripsi selesai.")

    else:  # mode == "Dekripsi"
        st.subheader("Dekripsi Rail Fence Cipher")
        teks_input = st.text_area(
            "Ciphertext:",
            placeholder="Masukkan ciphertext Rail Fence yang akan didekripsi.",
            height=100,
            key="rail_dekripsi_input"
        )

        if st.button("Proses Dekripsi", key="rail_btn_dekripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                teks_sandi = teks_input.upper()
                jumlah_rail_efektif = min(KUNCI_GLOBAL, len(teks_sandi))
                teks_asli, matriks_rail, hasil_per_rail = dekripsi_rail_fence(teks_sandi)

                with st.expander("Langkah 1 - Hitung Jumlah Karakter per Rail", expanded=True):
                    pola_rail = buat_pola_zigzag(len(teks_sandi), jumlah_rail_efektif)
                    jumlah_per_rail = [0] * jumlah_rail_efektif
                    for nomor_rail in pola_rail:
                        jumlah_per_rail[nomor_rail] += 1
                    df_jumlah = pd.DataFrame({
                        "Rail": range(1, jumlah_rail_efektif + 1),
                        "Jumlah Karakter": jumlah_per_rail,
                    })
                    st.dataframe(df_jumlah, use_container_width=True, hide_index=True)

                with st.expander("Langkah 2 - Distribusi Ciphertext ke Rail"):
                    st.write("Isi setiap rail dari ciphertext:")
                    for nomor_baris, isi_rail in enumerate(hasil_per_rail, start=1):
                        if isi_rail:
                            st.write(f"Rail {nomor_baris}: {isi_rail}")

                with st.expander("Langkah 3 - Rekonstruksi Pola Zig-Zag"):
                    tampilkan_matriks_rail_fence_teks(matriks_rail, jumlah_rail_efektif, len(teks_sandi))

                with st.expander("Langkah 4 - Hasil Dekripsi"):
                    st.write(f"Plaintext: {teks_asli}")

                st.divider()
                st.subheader("Hasil Dekripsi")
                st.write(f"Ciphertext : {teks_sandi}")
                st.write(f"Plaintext  : {teks_asli}")
                st.success("Dekripsi selesai.")


# ============================================================
# HALAMAN: STREAM CIPHER
# ============================================================

def tampilkan_stream_cipher():
    st.header("Stream Cipher")
    st.write(
        "Stream Cipher adalah algoritma kriptografi modern yang mengenkripsi data per byte "
        "menggunakan operasi XOR dengan keystream. Keystream dihasilkan oleh LFSR "
        "(Linear Feedback Shift Register)."
    )
    st.write(f"Kunci yang digunakan: K = {KUNCI_GLOBAL} (seed awal LFSR)")
    st.write("Rumus Enkripsi: C = P XOR Keystream")
    st.write("Rumus Dekripsi: P = C XOR Keystream")

    st.divider()

    with st.expander("Informasi Keystream Generator (LFSR)"):
        st.write(f"Seed awal (K)      : {KUNCI_GLOBAL} = {format(KUNCI_GLOBAL, '08b')} (biner)")
        st.write(f"Panjang register   : {PANJANG_REGISTER} bit")
        st.write(f"Posisi tap         : bit {POSISI_TAP[0]+1} dan bit {POSISI_TAP[1]+1} (dari kiri)")
        st.write("Operasi feedback   : XOR antara posisi tap")
        st.write(
            "Karena parameter tetap, keystream yang sama selalu dihasilkan "
            "untuk seed yang sama sehingga dekripsi dapat dilakukan."
        )
        contoh_keystream, _ = buat_keystream(8)
        df_keystream_contoh = pd.DataFrame({
            "Byte ke-": range(1, 9),
            "Desimal": contoh_keystream,
            "Biner": [format(nilai, '08b') for nilai in contoh_keystream],
            "Hex": [format(nilai, '02X') for nilai in contoh_keystream],
        })
        st.write("8 byte pertama keystream:")
        st.dataframe(df_keystream_contoh, use_container_width=True, hide_index=True)

    mode = st.session_state.get("stream_mode", None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enkripsi", key="stream_pilih_enkripsi", use_container_width=True, type="primary" if mode == "Enkripsi" else "secondary"):
            st.session_state["stream_mode"] = "Enkripsi"
            st.rerun()
    with col2:
        if st.button("Dekripsi", key="stream_pilih_dekripsi", use_container_width=True, type="primary" if mode == "Dekripsi" else "secondary"):
            st.session_state["stream_mode"] = "Dekripsi"
            st.rerun()

    if mode is None:
        st.info("Silakan klik tombol Enkripsi atau Dekripsi di atas untuk menampilkan formulir.")
        return

    if mode == "Enkripsi":
        st.subheader("Enkripsi Stream Cipher")
        teks_input = st.text_area(
            "Plaintext:",
            placeholder="Masukkan teks yang akan dienkripsi. Contoh: HELLO",
            height=100,
            key="stream_enkripsi_input"
        )

        if st.button("Proses Enkripsi", key="stream_btn_enkripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                teks_asli = teks_input
                teks_sandi_hex, langkah_enkripsi, keystream = enkripsi_stream_cipher(teks_asli)

                with st.expander("Langkah 1 - Konversi Plaintext ke Biner", expanded=True):
                    df_konversi = pd.DataFrame({
                        "Karakter": list(teks_asli),
                        "ASCII (Desimal)": [ord(k) for k in teks_asli],
                        "Biner (8-bit)": [format(ord(k), '08b') for k in teks_asli],
                        "Hex": [format(ord(k), '02X') for k in teks_asli],
                    })
                    st.dataframe(df_konversi, use_container_width=True, hide_index=True)

                with st.expander("Langkah 2 - Keystream yang Digunakan"):
                    st.write(f"Seed LFSR: {KUNCI_GLOBAL} = {format(KUNCI_GLOBAL, '08b')} (biner)")
                    df_keystream = pd.DataFrame({
                        "Byte ke-": range(1, len(keystream) + 1),
                        "Keystream (Desimal)": keystream,
                        "Keystream (Biner)": [format(nilai, '08b') for nilai in keystream],
                        "Keystream (Hex)": [format(nilai, '02X') for nilai in keystream],
                    })
                    st.dataframe(df_keystream, use_container_width=True, hide_index=True)

                with st.expander("Langkah 3 - Operasi XOR per Byte", expanded=True):
                    st.write("Rumus: C = P XOR Keystream")
                    df_langkah = pd.DataFrame(langkah_enkripsi)
                    st.dataframe(df_langkah, use_container_width=True, hide_index=True)

                with st.expander("Langkah 4 - Hasil dalam Hexadecimal"):
                    st.write(f"Ciphertext (Hex): {teks_sandi_hex}")

                st.divider()
                st.subheader("Hasil Enkripsi")
                st.write(f"Plaintext        : {teks_asli}")
                st.write(f"Ciphertext (Hex) : {teks_sandi_hex}")
                st.info("Output Stream Cipher dalam format Hexadecimal. Gunakan format ini saat dekripsi.")
                st.success("Enkripsi selesai.")

    else:  # mode == "Dekripsi"
        st.subheader("Dekripsi Stream Cipher")
        st.info("Masukkan ciphertext dalam format hex dipisah spasi. Contoh: 40 6D 64 64 6F")
        teks_input = st.text_area(
            "Ciphertext (Hexadecimal):",
            placeholder="Contoh: 40 6D 64 64 6F",
            height=100,
            key="stream_dekripsi_input"
        )

        if st.button("Proses Dekripsi", key="stream_btn_dekripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                try:
                    teks_sandi = teks_input.strip()
                    # Validasi format hex
                    for nilai_hex in teks_sandi.split():
                        int(nilai_hex, 16)

                    teks_asli, langkah_dekripsi, keystream = dekripsi_stream_cipher(teks_sandi)

                    with st.expander("Langkah 1 - Keystream yang Digunakan", expanded=True):
                        st.write(f"Seed LFSR: {KUNCI_GLOBAL} = {format(KUNCI_GLOBAL, '08b')} (biner)")
                        df_keystream = pd.DataFrame({
                            "Byte ke-": range(1, len(keystream) + 1),
                            "Keystream (Biner)": [format(nilai, '08b') for nilai in keystream],
                            "Keystream (Hex)": [format(nilai, '02X') for nilai in keystream],
                        })
                        st.dataframe(df_keystream, use_container_width=True, hide_index=True)

                    with st.expander("Langkah 2 - Operasi XOR per Byte", expanded=True):
                        st.write("Rumus: P = C XOR Keystream")
                        df_langkah = pd.DataFrame(langkah_dekripsi)
                        st.dataframe(df_langkah, use_container_width=True, hide_index=True)

                    with st.expander("Langkah 3 - Hasil Plaintext"):
                        st.write(f"Plaintext: {teks_asli}")

                    st.divider()
                    st.subheader("Hasil Dekripsi")
                    st.write(f"Ciphertext (Hex) : {teks_sandi}")
                    st.write(f"Plaintext        : {teks_asli}")
                    st.success("Dekripsi selesai.")

                except ValueError:
                    st.error("Format hexadecimal tidak valid. Gunakan format: XX XX XX ... (dipisah spasi)")


# ============================================================
# HALAMAN: BLOCK CIPHER
# ============================================================

def tampilkan_block_cipher():
    st.header("Block Cipher")
    st.write(
        "Block Cipher adalah algoritma kriptografi modern yang mengenkripsi data "
        "dalam blok-blok berukuran tetap. Setiap blok dienkripsi secara terpisah "
        "menggunakan kunci yang sama."
    )
    st.write(f"Kunci yang digunakan: K = {KUNCI_GLOBAL}")
    st.write(f"Ukuran blok: 8 bit (1 byte per blok)")
    st.write(f"Kunci dalam biner: {format(NILAI_KUNCI_BINER, '08b')}")
    st.write("Rumus Enkripsi: C = P XOR K")
    st.write("Rumus Dekripsi: P = C XOR K  (XOR bersifat simetris)")

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ukuran Blok", "8 bit (1 byte)")
    with col2:
        st.metric("Kunci K", str(KUNCI_GLOBAL))
    with col3:
        st.metric("Kunci (Biner)", format(NILAI_KUNCI_BINER, '08b'))

    st.divider()

    mode = st.session_state.get("block_mode", None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enkripsi", key="block_pilih_enkripsi", use_container_width=True, type="primary" if mode == "Enkripsi" else "secondary"):
            st.session_state["block_mode"] = "Enkripsi"
            st.rerun()
    with col2:
        if st.button("Dekripsi", key="block_pilih_dekripsi", use_container_width=True, type="primary" if mode == "Dekripsi" else "secondary"):
            st.session_state["block_mode"] = "Dekripsi"
            st.rerun()

    if mode is None:
        st.info("Silakan klik tombol Enkripsi atau Dekripsi di atas untuk menampilkan formulir.")
        return

    if mode == "Enkripsi":
        st.subheader("Enkripsi Block Cipher")
        teks_input = st.text_area(
            "Plaintext:",
            placeholder="Masukkan teks yang akan dienkripsi. Contoh: HELLO",
            height=100,
            key="block_enkripsi_input"
        )

        if st.button("Proses Enkripsi", key="block_btn_enkripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                teks_asli = teks_input
                teks_sandi_hex, langkah_enkripsi, jumlah_padding = enkripsi_block_cipher(teks_asli)

                with st.expander("Langkah 1 - Konversi Plaintext ke Byte dan Biner", expanded=True):
                    st.write("Setiap karakter dikonversi ke nilai ASCII lalu ke biner 8-bit (1 blok = 1 byte):")
                    df_konversi = pd.DataFrame({
                        "Blok": range(1, len(teks_asli) + 1),
                        "Karakter": list(teks_asli),
                        "ASCII (Desimal)": [ord(k) for k in teks_asli],
                        "Biner (8-bit)": [format(ord(k), '08b') for k in teks_asli],
                    })
                    st.dataframe(df_konversi, use_container_width=True, hide_index=True)

                with st.expander("Langkah 2 - Persiapan Kunci 8-bit"):
                    st.write(f"Kunci K = {KUNCI_GLOBAL}")
                    st.write(f"Kunci dalam biner  : {format(NILAI_KUNCI_BINER, '08b')}")
                    st.write(f"Kunci dalam hex    : {format(NILAI_KUNCI_BINER, '02X')}")
                    st.write("Kunci yang sama digunakan untuk semua blok.")

                with st.expander("Langkah 3 - Operasi XOR Setiap Blok", expanded=True):
                    st.write(f"Rumus: C = P XOR K  (K = {format(NILAI_KUNCI_BINER, '08b')})")
                    df_langkah = pd.DataFrame(langkah_enkripsi)
                    st.dataframe(df_langkah, use_container_width=True, hide_index=True)

                with st.expander("Langkah 4 - Gabungkan Blok Menjadi Ciphertext"):
                    st.write(f"Ciphertext (Hex): {teks_sandi_hex}")
                    st.write("Setiap dua karakter hex = 1 blok (1 byte = 8 bit)")

                st.divider()
                st.subheader("Hasil Enkripsi")
                st.write(f"Plaintext        : {teks_asli}")
                st.write(f"Ciphertext (Hex) : {teks_sandi_hex}")
                st.info("Output Block Cipher dalam format Hexadecimal. Gunakan format ini saat dekripsi.")
                st.success("Enkripsi selesai.")

    else:  # mode == "Dekripsi"
        st.subheader("Dekripsi Block Cipher")
        st.info("Masukkan ciphertext dalam format hex dipisah spasi. Contoh: 40 4D 44 44 47")
        teks_input = st.text_area(
            "Ciphertext (Hexadecimal):",
            placeholder="Contoh: 40 4D 44 44 47",
            height=100,
            key="block_dekripsi_input"
        )

        if st.button("Proses Dekripsi", key="block_btn_dekripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                try:
                    teks_sandi = teks_input.strip()
                    for nilai_hex in teks_sandi.split():
                        int(nilai_hex, 16)

                    teks_asli, langkah_dekripsi = dekripsi_block_cipher(teks_sandi)

                    with st.expander("Langkah 1 - Kunci yang Digunakan", expanded=True):
                        st.write(f"Kunci K = {KUNCI_GLOBAL}")
                        st.write(f"Kunci dalam biner : {format(NILAI_KUNCI_BINER, '08b')}")

                    with st.expander("Langkah 2 - Operasi XOR per Blok", expanded=True):
                        st.write(f"Rumus: P = C XOR K  (K = {format(NILAI_KUNCI_BINER, '08b')})")
                        df_langkah = pd.DataFrame(langkah_dekripsi)
                        st.dataframe(df_langkah, use_container_width=True, hide_index=True)

                    with st.expander("Langkah 3 - Hasil Plaintext"):
                        st.write(f"Plaintext: {teks_asli}")

                    st.divider()
                    st.subheader("Hasil Dekripsi")
                    st.write(f"Ciphertext (Hex) : {teks_sandi}")
                    st.write(f"Plaintext        : {teks_asli}")
                    st.success("Dekripsi selesai.")

                except ValueError:
                    st.error("Format hexadecimal tidak valid. Gunakan format: XX XX XX ... (dipisah spasi)")


# ============================================================
# HALAMAN: SUPER CIPHER
# ============================================================

def tampilkan_super_cipher():
    st.header("Super Cipher")
    st.write(
        "Super Cipher menggabungkan keempat algoritma sebelumnya secara berlapis "
        "untuk menghasilkan enkripsi yang lebih kuat."
    )
    st.write(f"Kunci yang digunakan: K = {KUNCI_GLOBAL} pada semua tahap.")

    st.divider()

    mode = st.session_state.get("super_mode", None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enkripsi", key="super_pilih_enkripsi", use_container_width=True, type="primary" if mode == "Enkripsi" else "secondary"):
            st.session_state["super_mode"] = "Enkripsi"
            st.rerun()
    with col2:
        if st.button("Dekripsi", key="super_pilih_dekripsi", use_container_width=True, type="primary" if mode == "Dekripsi" else "secondary"):
            st.session_state["super_mode"] = "Dekripsi"
            st.rerun()

    if mode is None:
        st.info("Silakan klik tombol Enkripsi atau Dekripsi di atas untuk menampilkan formulir.")
        return

    if mode == "Enkripsi":
        st.subheader("Enkripsi Super Cipher")
        teks_input = st.text_area(
            "Plaintext:",
            placeholder="Masukkan teks yang akan dienkripsi. Contoh: HELLO WORLD",
            height=100,
            key="super_enkripsi_input"
        )

        if st.button("Proses Enkripsi", key="super_btn_enkripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                teks_asli = teks_input.upper()
                hasil = enkripsi_super_cipher(teks_asli)

                # ── Tahap 1: Caesar Cipher ──
                data_tahap_1 = hasil['tahap_1']
                with st.expander("Langkah 1 - Caesar Cipher", expanded=True):
                    st.write(f"Input   : {data_tahap_1['input']}")
                    st.write(f"Proses  : Geser setiap huruf sebesar K = {KUNCI_GLOBAL} posisi")
                    st.write(f"Rumus   : C = (P + {KUNCI_GLOBAL}) mod 26")
                    df_caesar = pd.DataFrame(data_tahap_1['langkah'])
                    st.dataframe(df_caesar, use_container_width=True, hide_index=True)
                    st.write(f"Output  : {data_tahap_1['output']}")

                # ── Tahap 2: Rail Fence Cipher ──
                data_tahap_2 = hasil['tahap_2']
                jumlah_rail_efektif = min(KUNCI_GLOBAL, len(data_tahap_2['input']))
                with st.expander("Langkah 2 - Rail Fence Cipher", expanded=True):
                    st.write(f"Input       : {data_tahap_2['input']}")
                    st.write(f"Proses      : Susun pola zig-zag pada {jumlah_rail_efektif} rail, baca per rail")
                    st.write("Visualisasi matriks rail:")
                    tampilkan_matriks_rail_fence_teks(
                        data_tahap_2['matriks_rail'],
                        jumlah_rail_efektif,
                        len(data_tahap_2['input'])
                    )
                    st.write("Pembacaan per rail:")
                    for nomor_baris, isi_rail in enumerate(data_tahap_2['hasil_per_rail'], start=1):
                        if isi_rail:
                            st.write(f"  Rail {nomor_baris}: {isi_rail}")
                    st.write(f"Output  : {data_tahap_2['output']}")

                # ── Tahap 3: Stream Cipher ──
                data_tahap_3 = hasil['tahap_3']
                with st.expander("Langkah 3 - Stream Cipher", expanded=True):
                    st.write(f"Input   : {data_tahap_3['input']}")
                    st.write(f"Proses  : XOR setiap byte dengan keystream LFSR (seed = {KUNCI_GLOBAL})")
                    st.write("Rumus   : C = Plaintext_byte XOR Keystream_byte")
                    keystream = data_tahap_3['keystream']
                    df_keystream = pd.DataFrame({
                        "Byte ke-": range(1, len(keystream) + 1),
                        "Keystream (Biner)": [format(nilai, '08b') for nilai in keystream],
                        "Keystream (Hex)": [format(nilai, '02X') for nilai in keystream],
                    })
                    st.write("Keystream yang digunakan:")
                    st.dataframe(df_keystream, use_container_width=True, hide_index=True)
                    df_stream = pd.DataFrame(data_tahap_3['langkah'])
                    st.write("Operasi XOR per byte:")
                    st.dataframe(df_stream, use_container_width=True, hide_index=True)
                    st.write(f"Output (Hex) : {data_tahap_3['output']}")

                # ── Tahap 4: Block Cipher ──
                data_tahap_4 = hasil['tahap_4']
                with st.expander("Langkah 4 - Block Cipher", expanded=True):
                    st.write(f"Input (Hex)  : {data_tahap_4['input']}")
                    st.write(
                        f"Proses       : XOR setiap byte dengan kunci K = {KUNCI_GLOBAL} "
                        f"= {format(NILAI_KUNCI_BINER, '08b')} (biner)"
                    )
                    st.write(f"Rumus        : C = Input_byte XOR {format(NILAI_KUNCI_BINER, '08b')}")
                    df_block = pd.DataFrame(data_tahap_4['langkah'])
                    st.dataframe(df_block, use_container_width=True, hide_index=True)
                    st.write(f"Output (Hex) : {data_tahap_4['output']}")

                # ── Hasil Akhir ──
                ciphertext_akhir = hasil['ciphertext_akhir']
                st.divider()
                st.subheader("Hasil Akhir Super Cipher")
                st.write(f"Plaintext        : {teks_asli}")
                st.write(f"Ciphertext (Hex) : {ciphertext_akhir}")
                st.info("Gunakan ciphertext hex di atas untuk proses dekripsi Super Cipher.")
                st.success("Super Enkripsi selesai.")

    else:  # mode == "Dekripsi"
        st.subheader("Dekripsi Super Cipher")
        st.info("Masukkan ciphertext hex dari hasil Super Enkripsi. Format: XX XX XX ...")
        teks_input = st.text_area(
            "Ciphertext (Hexadecimal):",
            placeholder="Contoh: 58 45 5C 5C 5F ...",
            height=100,
            key="super_dekripsi_input"
        )

        if st.button("Proses Dekripsi", key="super_btn_dekripsi"):
            if not teks_input.strip():
                st.warning("Input tidak boleh kosong.")
            else:
                try:
                    teks_sandi = teks_input.strip()
                    for nilai_hex in teks_sandi.split():
                        int(nilai_hex, 16)

                    hasil = dekripsi_super_cipher(teks_sandi)

                    # ── Tahap 1: Block Cipher Dekripsi ──
                    data_tahap_1 = hasil['tahap_1']
                    with st.expander("Langkah 1 - Block Cipher Dekripsi", expanded=True):
                        st.write(f"Input (Hex)  : {data_tahap_1['input']}")
                        st.write(
                            f"Proses       : XOR setiap byte dengan kunci K = {KUNCI_GLOBAL} "
                            f"= {format(NILAI_KUNCI_BINER, '08b')}"
                        )
                        st.write("Rumus        : P = C XOR K")
                        df_block = pd.DataFrame(data_tahap_1['langkah'])
                        st.dataframe(df_block, use_container_width=True, hide_index=True)
                        st.write(f"Output (Hex) : {data_tahap_1['output']}")

                    # ── Tahap 2: Stream Cipher Dekripsi ──
                    data_tahap_2 = hasil['tahap_2']
                    with st.expander("Langkah 2 - Stream Cipher Dekripsi", expanded=True):
                        st.write(f"Input (Hex)  : {data_tahap_2['input']}")
                        st.write(f"Proses       : XOR setiap byte dengan keystream LFSR (seed = {KUNCI_GLOBAL})")
                        st.write("Rumus        : P = C XOR Keystream")
                        keystream = data_tahap_2['keystream']
                        df_keystream = pd.DataFrame({
                            "Byte ke-": range(1, len(keystream) + 1),
                            "Keystream (Biner)": [format(nilai, '08b') for nilai in keystream],
                            "Keystream (Hex)": [format(nilai, '02X') for nilai in keystream],
                        })
                        st.write("Keystream yang digunakan:")
                        st.dataframe(df_keystream, use_container_width=True, hide_index=True)
                        df_stream = pd.DataFrame(data_tahap_2['langkah'])
                        st.write("Operasi XOR per byte:")
                        st.dataframe(df_stream, use_container_width=True, hide_index=True)
                        st.write(f"Output (Teks): {data_tahap_2['output']}")

                    # ── Tahap 3: Rail Fence Cipher Dekripsi ──
                    data_tahap_3 = hasil['tahap_3']
                    jumlah_rail_efektif = min(KUNCI_GLOBAL, len(data_tahap_3['input']))
                    with st.expander("Langkah 3 - Rail Fence Cipher Dekripsi", expanded=True):
                        st.write(f"Input        : {data_tahap_3['input']}")
                        st.write(f"Proses       : Rekonstruksi pola zig-zag pada {jumlah_rail_efektif} rail")
                        st.write("Visualisasi matriks rail:")
                        tampilkan_matriks_rail_fence_teks(
                            data_tahap_3['matriks_rail'],
                            jumlah_rail_efektif,
                            len(data_tahap_3['input'])
                        )
                        st.write("Isi per rail:")
                        for nomor_baris, isi_rail in enumerate(data_tahap_3['hasil_per_rail'], start=1):
                            if isi_rail:
                                st.write(f"  Rail {nomor_baris}: {isi_rail}")
                        st.write(f"Output  : {data_tahap_3['output']}")

                    # ── Tahap 4: Caesar Cipher Dekripsi ──
                    data_tahap_4 = hasil['tahap_4']
                    with st.expander("Langkah 4 - Caesar Cipher Dekripsi", expanded=True):
                        st.write(f"Input   : {data_tahap_4['input']}")
                        st.write(f"Proses  : Geser mundur setiap huruf sebesar K = {KUNCI_GLOBAL} posisi")
                        st.write(f"Rumus   : P = (C - {KUNCI_GLOBAL}) mod 26")
                        df_caesar = pd.DataFrame(data_tahap_4['langkah'])
                        st.dataframe(df_caesar, use_container_width=True, hide_index=True)
                        st.write(f"Output  : {data_tahap_4['output']}")

                    # ── Hasil Akhir ──
                    plaintext_akhir = hasil['plaintext_akhir']
                    st.divider()
                    st.subheader("Hasil Akhir Super Dekripsi")
                    st.write(f"Ciphertext (Hex) : {teks_sandi}")
                    st.write(f"Plaintext        : {plaintext_akhir}")
                    st.success("Super Dekripsi selesai.")

                except ValueError:
                    st.error("Format hexadecimal tidak valid. Gunakan format: XX XX XX ... (dipisah spasi)")


# ============================================================
# HALAMAN: ABOUT
# ============================================================

def tampilkan_about():
    st.title("About")

    st.header("Tentang Aplikasi")
    st.write(
        "Aplikasi ini dibuat untuk memenuhi tugas mata kuliah Kriptografi. "
        "Tujuan utama aplikasi adalah menjadi media pembelajaran interaktif "
        "yang membantu mahasiswa memahami cara kerja algoritma kriptografi "
        "melalui simulasi langkah demi langkah."
    )
    st.write(f"Kunci tetap: K = {KUNCI_GLOBAL} digunakan pada seluruh algoritma.")

    st.header("Anggota Kelompok")

    daftar_anggota = [
        {"nomor": 1, "nama": "Partawijaya Rihal Dariretci", "nim": "123240181"},
        {"nomor": 2, "nama": "Yohanes Herang Aji Dharma", "nim": "123240191"},
        {"nomor": 3, "nama": "Alvin Adhika Putra", "nim": "123240193"},
        {"nomor": 4, "nama": "Kafka Akmal Dani", "nim": "123240203"},
    ]

    df_anggota = pd.DataFrame(daftar_anggota)
    df_anggota.columns = ["No", "Nama", "NIM"]
    st.dataframe(df_anggota, use_container_width=True, hide_index=True)

    st.header("Algoritma yang Diimplementasikan")
    st.write("1. Caesar Cipher   — Kriptografi Klasik (Substitusi)")
    st.write("2. Rail Fence Cipher — Kriptografi Klasik (Transposisi)")
    st.write("3. Stream Cipher   — Kriptografi Modern (XOR + LFSR)")
    st.write("4. Block Cipher    — Kriptografi Modern (XOR per blok)")
    st.write("5. Super Cipher    — Gabungan keempat algoritma di atas")

    st.header("Catatan Teknis")
    st.write("- Semua algoritma diimplementasikan secara manual tanpa library enkripsi siap pakai.")
    st.write(f"- Kunci K = {KUNCI_GLOBAL} bersifat tetap dan tidak dapat diubah.")
    st.write("- Stream Cipher dan Block Cipher menghasilkan output dalam format Hexadecimal.")
    st.write("- Untuk mendekripsi, gunakan output hex dari proses enkripsi sebagai input.")
    st.write(
        "- Super Cipher menjalankan 4 lapisan enkripsi: "
        "Caesar → Rail Fence → Stream Cipher → Block Cipher."
    )


# ============================================================
# HALAMAN: PROGRAM (5 tab algoritma)
# ============================================================

def tampilkan_program():
    st.title("Program Kriptografi")
    st.write(f"Kunci tetap: K = {KUNCI_GLOBAL}")
    st.write("Pilih algoritma yang ingin digunakan pada tab di bawah ini.")

    st.divider()

    tab_caesar, tab_rail, tab_stream, tab_block, tab_super = st.tabs([
        "Caesar Cipher",
        "Rail Fence Cipher",
        "Stream Cipher",
        "Block Cipher",
        "Super Cipher",
    ])

    with tab_caesar:
        tampilkan_caesar()

    with tab_rail:
        tampilkan_rail_fence()

    with tab_stream:
        tampilkan_stream_cipher()

    with tab_block:
        tampilkan_block_cipher()

    with tab_super:
        tampilkan_super_cipher()


# ============================================================
# FUNGSI SIDEBAR
# ============================================================

def tampilkan_sidebar() -> str:
    """
    Menampilkan sidebar dengan dua menu: PROGRAM dan ABOUT.

    Mengembalikan:
        str: Menu yang dipilih pengguna ("PROGRAM" atau "ABOUT").
    """
    with st.sidebar:
        st.title("Aplikasi Kriptografi")
        st.write("Kelompok Kriptografi")
        st.write(f"Kunci tetap: K = {KUNCI_GLOBAL}")

        st.divider()

        menu_dipilih = st.radio(
            "Menu:",
            options=["PROGRAM", "ABOUT"],
            key="menu_sidebar"
        )

    return menu_dipilih


# ============================================================
# MAIN — TITIK MASUK APLIKASI
# ============================================================

def main():
    """Fungsi utama yang menjalankan aplikasi Streamlit."""
    menu_dipilih = tampilkan_sidebar()

    if menu_dipilih == "PROGRAM":
        tampilkan_program()
    elif menu_dipilih == "ABOUT":
        tampilkan_about()


# Streamlit memanggil modul secara langsung
main()
