from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

def encrypt_file(input_data, key):
    # Mengenkripsi konten file menggunakan algoritma stream cipher ChaCha20.
    # Buat cipher ChaCha20 dengan kunci dan nonce (12 bytes)
    nonce = get_random_bytes(12)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    
    # Enkripsi konten
    ciphertext = cipher.encrypt(input_data)
    
    # Gabungkan nonce dengan ciphertext
    return nonce + ciphertext

def decrypt_file(input_data, key):
    # Mendekripsi konten file yang terenkripsi menggunakan algoritma stream cipher ChaCha20.
    # Pisahkan nonce dari ciphertext
    nonce = input_data[:12]
    ciphertext = input_data[12:]
    
    # Buat cipher ChaCha20 dengan kunci dan nonce yang sama
    cipher = ChaCha20.new(key=key, nonce=nonce)
    
    # Dekripsi konten
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# def fix_base64_padding(b64_string):
#     """Memperbaiki padding Base64 jika tidak sesuai."""
#     return b64_string + '=' * (-len(b64_string) % 4)