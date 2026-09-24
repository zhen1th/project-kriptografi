"""
test_algorithms.py
Script pengujian semua algoritma kriptografi
"""
from algorithms.caesar import enkripsi_caesar, dekripsi_caesar
from algorithms.rail_fence import enkripsi_rail_fence, dekripsi_rail_fence
from algorithms.stream_cipher import enkripsi_stream_cipher, dekripsi_stream_cipher
from algorithms.block_cipher import enkripsi_block_cipher, dekripsi_block_cipher
from algorithms.super_cipher import enkripsi_super_cipher, dekripsi_super_cipher

teks_asli = "HELLO WORLD"
print("=" * 60)
print("TEST SEMUA ALGORITMA KRIPTOGRAFI")
print(f"Teks asli: {teks_asli}")
print("=" * 60)

# Test Caesar
sandi, langkah = enkripsi_caesar(teks_asli)
balik, _ = dekripsi_caesar(sandi)
print(f"\n[1] Caesar Cipher")
print(f"  Enkripsi : {teks_asli} -> {sandi}")
print(f"  Dekripsi : {sandi} -> {balik}")
print(f"  Reversible: {balik == teks_asli}")

# Test Rail Fence
sandi_rf, matriks, per_rail = enkripsi_rail_fence(teks_asli)
balik_rf, _, _ = dekripsi_rail_fence(sandi_rf)
print(f"\n[2] Rail Fence Cipher")
print(f"  Enkripsi : {teks_asli} -> {sandi_rf}")
print(f"  Dekripsi : {sandi_rf} -> {balik_rf}")
print(f"  Reversible: {balik_rf == teks_asli.replace(' ', '')} (spasi dihilangkan)")

# Test Stream Cipher
sandi_stream, _, _ = enkripsi_stream_cipher(teks_asli)
balik_stream, _, _ = dekripsi_stream_cipher(sandi_stream)
print(f"\n[3] Stream Cipher")
print(f"  Enkripsi : {teks_asli} -> {sandi_stream}")
print(f"  Dekripsi : {sandi_stream} -> {balik_stream}")
print(f"  Reversible: {balik_stream == teks_asli}")

# Test Block Cipher
sandi_block, langkah_b, _ = enkripsi_block_cipher(teks_asli)
balik_block, _ = dekripsi_block_cipher(sandi_block)
print(f"\n[4] Block Cipher")
print(f"  Enkripsi : {teks_asli} -> {sandi_block}")
print(f"  Dekripsi : {sandi_block} -> {balik_block}")
print(f"  Reversible: {balik_block == teks_asli}")

# Test Super Cipher (4 tahap penuh)
print(f"\n[5] Super Cipher (4 tahap: Caesar -> Rail Fence -> Stream -> Block)")
hasil_super = enkripsi_super_cipher(teks_asli)
print(f"  Tahap 1 Caesar      : {teks_asli} -> {hasil_super['tahap_1']['output']}")
print(f"  Tahap 2 Rail Fence  : {hasil_super['tahap_1']['output']} -> {hasil_super['tahap_2']['output']}")
print(f"  Tahap 3 Stream      : {hasil_super['tahap_2']['output']} -> {hasil_super['tahap_3']['output']}")
print(f"  Tahap 4 Block       : {hasil_super['tahap_3']['output']} -> {hasil_super['tahap_4']['output']}")
ciphertext_super = hasil_super['ciphertext_akhir']
print(f"  Ciphertext Akhir    : {ciphertext_super}")

hasil_de_super = dekripsi_super_cipher(ciphertext_super)
print(f"\n  Dekripsi (4 tahap: Block -> Stream -> Rail Fence -> Caesar)")
print(f"  Tahap 1 Block Dec   : {ciphertext_super} -> {hasil_de_super['tahap_1']['output']}")
print(f"  Tahap 2 Stream Dec  : {hasil_de_super['tahap_1']['output']} -> {hasil_de_super['tahap_2']['output']}")
print(f"  Tahap 3 RailFen Dec : {hasil_de_super['tahap_2']['output']} -> {hasil_de_super['tahap_3']['output']}")
print(f"  Tahap 4 Caesar Dec  : {hasil_de_super['tahap_3']['output']} -> {hasil_de_super['tahap_4']['output']}")
plaintext_kembali = hasil_de_super['plaintext_akhir']
print(f"  Plaintext Akhir     : {plaintext_kembali}")
print(f"  Reversible          : {plaintext_kembali == teks_asli.replace(' ', '')} (spasi dihilangkan pada Rail Fence)")

print("\n" + "=" * 60)
print("SEMUA TEST SELESAI")
print("=" * 60)
