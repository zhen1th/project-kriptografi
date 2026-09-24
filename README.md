# 🔐 Cryptography Educational App

Aplikasi pembelajaran kriptografi interaktif berbasis **Python + Streamlit** untuk mata kuliah Kriptografi.

---

## 📋 Deskripsi

Aplikasi ini dirancang sebagai media pembelajaran yang membantu mahasiswa memahami cara kerja algoritma kriptografi melalui **simulasi langkah demi langkah**. Setiap proses enkripsi dan dekripsi ditampilkan secara rinci sehingga mudah dipahami dan dipresentasikan.

**Kunci tetap: `K = 8`** digunakan pada seluruh algoritma.

---

## 🚀 Cara Instalasi dan Menjalankan

### 1. Pastikan Python sudah terinstal
```bash
python --version
# Harus Python 3.8 atau lebih baru
```

### 2. Clone atau unduh project ini
```bash
# Pastikan berada di direktori project
cd kriptografi-app
```

### 3. Instal dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi
```bash
streamlit run app.py
```

### 5. Buka di browser
Secara otomatis akan terbuka di `http://localhost:8501`

---

## 📁 Struktur Project

```text
kriptografi-app/
│
├── app.py                  ← File utama aplikasi Streamlit
├── requirements.txt        ← Daftar dependensi Python
├── README.md               ← Dokumentasi project (file ini)
│
├── algorithms/             ← Modul implementasi algoritma
│   ├── __init__.py
│   ├── caesar.py           ← Caesar Cipher
│   ├── rail_fence.py       ← Rail Fence Cipher
│   ├── stream_cipher.py    ← Stream Cipher (LFSR)
│   ├── block_cipher.py     ← Block Cipher (XOR)
│   └── super_cipher.py     ← Super Cipher (gabungan)
│
└── utils/                  ← Modul utilitas
    ├── __init__.py
    └── helpers.py          ← Fungsi konversi dan validasi
```

---

## 🔐 Penjelasan Algoritma

### 1. Caesar Cipher (Kriptografi Klasik)

**Jenis:** Substitusi monoalfabetik

**Konsep:** Setiap huruf dalam plaintext digeser sebesar K posisi dalam alfabet (A=0, B=1, ..., Z=25).

| Operasi | Rumus |
|---------|-------|
| Enkripsi | `C = (P + K) mod 26` |
| Dekripsi | `P = (C - K) mod 26` |

**Contoh** dengan K=8:
- `H (7) → (7+8) mod 26 = 15 → P`
- `E (4) → (4+8) mod 26 = 12 → M`
- `HELLO → PMTTW`

---

### 2. Rail Fence Cipher (Kriptografi Klasik)

**Jenis:** Transposisi

**Konsep:** Karakter disusun dalam pola zig-zag pada K rail (baris), kemudian dibaca dari atas ke bawah per rail.

**Enkripsi:**
1. Tuliskan karakter mengikuti pola zig-zag pada K rail
2. Baca setiap rail dari kiri ke kanan
3. Gabungkan hasil bacaan semua rail → Ciphertext

**Dekripsi:**
1. Hitung jumlah karakter per rail
2. Distribusikan ciphertext ke setiap rail
3. Baca kembali mengikuti pola zig-zag → Plaintext

---

### 3. Stream Cipher (Kriptografi Modern)

**Jenis:** Stream

**Konsep:** Enkripsi dilakukan per byte menggunakan operasi XOR dengan keystream yang dihasilkan oleh LFSR (Linear Feedback Shift Register).

| Operasi | Rumus |
|---------|-------|
| Enkripsi | `C = P ⊕ Keystream` |
| Dekripsi | `P = C ⊕ Keystream` |

**Parameter LFSR:**
- Seed awal: K = 8 = `00001000`
- Panjang register: 8 bit
- Posisi tap: bit 8 dan bit 4

**Output:** Format Hexadecimal

---

### 4. Block Cipher (Kriptografi Modern)

**Jenis:** Block

**Konsep:** Plaintext dibagi menjadi blok-blok 8 bit (1 byte per blok). Setiap blok dienkripsi secara terpisah menggunakan XOR dengan kunci 8-bit.

| Operasi | Rumus |
|---------|-------|
| Enkripsi | `C = P ⊕ K` |
| Dekripsi | `P = C ⊕ K` |

**Parameter:**
- Ukuran blok: 8 bit (1 byte)
- Kunci K = 8 = `00001000`

**Output:** Format Hexadecimal

---

### 5. Super Cipher (Gabungan)

**Jenis:** Hybrid (gabungan 4 algoritma)

**Konsep:** Menggabungkan keempat algoritma secara berlapis untuk meningkatkan keamanan.

**Urutan Enkripsi:**
```
PLAINTEXT
   ↓
Caesar Cipher (K=8)      ← Substitusi karakter
   ↓
Rail Fence Cipher (Rail=8) ← Transposisi karakter
   ↓
Block Cipher (K=8)       ← Enkripsi per byte ke Hex
   ↓
CIPHERTEXT (Hexadecimal)
```

**Urutan Dekripsi (terbalik):**
```
CIPHERTEXT (Hexadecimal)
   ↓
Block Decipher           ← Konversi Hex ke teks
   ↓
Rail Fence Decipher      ← Kembalikan posisi karakter
   ↓
Caesar Decipher          ← Kembalikan nilai karakter
   ↓
PLAINTEXT
```

---

## 👥 Anggota Kelompok

| No | Nama | NIM |
|----|------|-----|
| 1 | Partawijaya Rihal Dariretci | 123240181 |
| 2 | Yohanes Herang Aji Dharma | 123240191 |
| 3 | Alvin Adhika Putra | 123240193 |
| 4 | Kafka Akmal Dani | 123240203 |

---

## 📝 Catatan Penting

- Semua algoritma dibuat **secara manual** tanpa menggunakan library enkripsi siap pakai
- Kunci `K = 8` **bersifat tetap** dan tidak dapat diubah oleh pengguna
- Stream Cipher dan Block Cipher menghasilkan output dalam format **Hexadecimal**
- Untuk mendekripsi Stream Cipher/Block Cipher, gunakan output hex dari proses enkripsi
- Super Cipher menggunakan 3 lapisan: Caesar + Rail Fence + Block Cipher

---

## 💡 Contoh Input/Output

### Caesar Cipher
- **Input:** `HELLO WORLD`
- **Output:** `PMTTW EWZTL`

### Rail Fence Cipher (8 rail, teks pendek)
- **Input:** `HELLO`
- **Output:** Bergantung pada distribusi karakter per rail

### Stream Cipher
- **Input:** `HELLO`
- **Output:** `40 6D 64 64 6F` *(contoh — nilai bergantung keystream LFSR)*

### Block Cipher
- **Input:** `HELLO`
- **Output:** `40 4D 44 44 47` *(H=72 XOR 8=64=0x40, dst.)*

### Super Cipher
- **Input:** `HELLO WORLD`
- **Output:** Ciphertext hexadecimal berlapis
