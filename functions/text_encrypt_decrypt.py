from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import base64
import connection as cn


# Algoritma Rail Fence Cipher dengan penanganan spasi
def rail_fence_encrypt(text, key):
    """Encrypt text using Rail Fence Cipher while removing spaces."""
    # Simpan posisi spasi dalam teks
    space_positions = [i for i, char in enumerate(text) if char == ' ']
    
    # Hilangkan spasi dari teks
    text = text.replace(' ', '')
    
    # Rail Fence Encryption
    rail = [''] * key
    direction_down = False
    row = 0
    for char in text:
        rail[row] += char
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    
    encrypted_text = ''.join(rail)
    return encrypted_text, space_positions

def rail_fence_decrypt(cipher, key, space_positions):
    """Decrypt text using Rail Fence Cipher and restore spaces."""
    # Rail Fence Decryption
    rail = [[''] * len(cipher) for _ in range(key)]
    idx, direction_down, row = 0, None, 0
    
    # Tandai posisi karakter di rail
    for i in range(len(cipher)):
        rail[row][i] = '*'
        if row == 0:
            direction_down = True
        elif row == key - 1:
            direction_down = False
        row += 1 if direction_down else -1
    
    # Isi karakter dari cipher ke rail
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and idx < len(cipher):
                rail[i][j] = cipher[idx]
                idx += 1
    
    # Baca teks terenkripsi dari rail
    result = []
    row, direction_down = 0, None
    for i in range(len(cipher)):
        result.append(rail[row][i])
        if row == 0:
            direction_down = True
        elif row == key - 1:
            direction_down = False
        row += 1 if direction_down else -1
    
    decrypted_text = ''.join(result)
    
    # Kembalikan spasi pada posisi yang benar
    decrypted_text_with_spaces = list(decrypted_text)
    for pos in space_positions:
        decrypted_text_with_spaces.insert(pos, ' ')
    
    return ''.join(decrypted_text_with_spaces)

# Algoritma Elliptic Curve Cryptography (ECC)
def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

# Fungsi untuk enkripsi menggunakan ECC (Elliptic Curve Cryptography)
def ecc_encrypt(message, fernet_public_key):
    if isinstance(message, str):
        message = message.encode()  # Ubah pesan menjadi bytes jika berupa string

    # Generate ephemeral private key untuk enkripsi
    # Ephemeral key adalah kunci sementara yang digunakan untuk enkripsi
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ephemeral_public_key = ephemeral_private_key.public_key()

    # Menghasilkan shared secret menggunakan kunci publik penerima
    shared_secret = ephemeral_private_key.exchange(ec.ECDH(), fernet_public_key)

    # Gunakan HKDF untuk memperluas shared secret agar sesuai dengan panjang pesan
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=len(message),  # Sesuaikan panjang key dengan panjang pesan
        salt=None,
        info=b'ecc-algorithm'
    ).derive(shared_secret)
    
    # XOR pesan dengan derived key atau kunci yang sudah diperluas
    encrypted_message = bytes([m ^ k for m, k in zip(message, derived_key)])
    
    # Kembalikan kunci publik ephemeral dan pesan terenkripsi
    ephemeral_public_key_bytes = ephemeral_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return encode_to_base64(ephemeral_public_key_bytes + encrypted_message) # Encode ke Base64

# Fungsi untuk dekripsi menggunakan ECC (Elliptic Curve Cryptography)
def ecc_decrypt(encrypted_message, fernet_private_key):
    # Decode dari Base64
    encrypted_message_bytes = base64.b64decode(encrypted_message)

    # Ambil kunci publik ephemeral dan pesan terenkripsi
    ephemeral_public_key_bytes = encrypted_message_bytes[:91]  # Panjang DER untuk SECP256R1 adalah 91 byte
    encrypted_data = encrypted_message_bytes[91:]

    # Muat kunci publik ephemeral
    ephemeral_public_key = serialization.load_der_public_key(
        ephemeral_public_key_bytes, backend=default_backend()
    )

    # Menghasilkan shared secret menggunakan kunci privat penerima dan kunci publik ephemeral
    shared_secret = fernet_private_key.exchange(ec.ECDH(), ephemeral_public_key)

    # Gunakan HKDF untuk memperluas shared secret menjadi kunci yang cukup panjang
    # HKDF adalah Key Derivation Function yang menghasilkan kunci yang lebih aman dan sesuai dengan panjang teks
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=len(encrypted_data),  # Sesuaikan panjang key dengan panjang pesan terenkripsi
        salt=None,
        info=b'ecc-algorithm'
    ).derive(shared_secret)

    # XOR pesan terenkripsi dengan derived key untuk dekripsi
    decrypted_message = bytes([c ^ k for c, k in zip(encrypted_data, derived_key)])
    
    return decrypted_message.decode('utf-8') # ini untuk mengbuat pesan kembali dari bite ke bentuk string

def encode_to_base64(data):
    """Encode data (bytes) to Base64."""
    return base64.b64encode(data).decode('utf-8')

def get_key_base64(private_key, public_key):
    # Mendapatkan private key dalam bentuk DER (bytes)
    private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Mendapatkan public key dalam bentuk DER (bytes)
    public_key_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Encode ke Base64
    private_key_base64 = encode_to_base64(private_key_der)
    public_key_base64 = encode_to_base64(public_key_der)

    return private_key_base64, public_key_base64

def load_key_from_base64(base64_key, is_private=True):
    # Decode Base64 kembali ke DER (biner)
    key_der = base64.b64decode(base64_key)

    if is_private:
        # Memuat private key dari DER format
        return serialization.load_der_private_key(key_der, password=None)
    else:
        # Memuat public key dari DER format
        return serialization.load_der_public_key(key_der)

# Super Encryption Function
def super_encrypt(message, rail_key):
    # Step 1: Encrypt with Rail Fence Cipher
    rail_encrypted, space_positions = rail_fence_encrypt(message, rail_key)
    print(f"Space Positions: {space_positions}")
    
    # Step 2: Encrypt with ECC (Elliptic Curve Cryptography)
    private_key, public_key = generate_ecc_keys()
    ecc_encrypted = ecc_encrypt(rail_encrypted, public_key, private_key)
    private_key_content, public_key_content = get_key_base64(private_key, public_key)
    
    query = "INSERT INTO messages (encrypted_text, rail_fence_key, space_position, private_key_content) VALUES (%s, %s, %s, %s)"
    params = (ecc_encrypted, rail_key, str(space_positions), private_key_content)
    cn.run_query(query, params, fetch=False)
    return ecc_encrypted, space_positions

# Super Decryption Function
def super_decrypt(encrypted_message, rail_key, space_positions):
    # Step 1: Decrypt with ECC (Elliptic Curve Cryptography)
    query = "SELECT private_key_content FROM messages WHERE encrypted_text = %s"
    result = cn.run_query(query, (encrypted_message,), True)
    if result is None or len(result) == 0:
        print("No data found.")
        return None
    private_key_content = result['private_key_content'][0]
    ecc_private_key = load_key_from_base64(private_key_content, is_private=True)    
    ecc_decrypted = ecc_decrypt(encrypted_message, ecc_private_key)
    print(f"ECC Decrypted: {ecc_decrypted}")

    # Step 2: Decrypt with Rail Fence Cipher
    space_positions = [int(pos.strip()) for pos in space_positions.strip('[]').split(',')]
    rail_decrypted = rail_fence_decrypt(ecc_decrypted, rail_key, space_positions)
    print(f"Rail Fence Decrypted: {rail_decrypted}")
    return rail_decrypted


# Contoh penggunaan
private_key, public_key = generate_ecc_keys()
print("Private Key:", private_key)
print("Public Key:", public_key)

# # Enkripsi
# message = "Hello, ECC World!"
# encrypted_message = ecc_encrypt(message, public_key)
# print("Encrypted Message:", encrypted_message)

# # Dekripsi
# decrypted_message = ecc_decrypt(encrypted_message, private_key)
# print("Decrypted Message:", decrypted_message)

private_key_base64, public_key_base64 = get_key_base64(private_key, public_key)
print("Private Key Base64:", private_key_base64)
print("Public Key Base64:", public_key_base64)

# Contoh penggunaan untuk memuat kunci dari Base64
private_key_reloaded = load_key_from_base64(private_key_base64, is_private=True)
public_key_reloaded = load_key_from_base64(public_key_base64, is_private=False)

print("Private Key Loaded:", private_key_reloaded)
print("Public Key Loaded:", public_key_reloaded)

message = "Hello, World! This is a test message. Let's see if the encryption and decryption work correctly. This is a very long message that will be encrypted and decrypted using ECC."
encrypyted_message = ecc_encrypt(message, public_key_reloaded)
print("Encrypted Message:", encrypyted_message)

decrypted_message = ecc_decrypt(encrypyted_message, private_key_reloaded)
print("Decrypted Message:", decrypted_message)

