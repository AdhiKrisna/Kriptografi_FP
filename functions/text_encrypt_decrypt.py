from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
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

def ecc_encrypt(message, public_key, private_key):
    if isinstance(message, str):
        message = message.encode()  # Convert to bytes if it's a string
    
    # Generate a random shared secret using ECDH (Elliptic Curve Diffie-Hellman)
    shared_secret = private_key.exchange(ec.ECDH(), public_key)
    
    # Derive a symmetric key from the shared secret using PBKDF2
    salt = os.urandom(16)  # Salt for PBKDF2
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    symmetric_key = kdf.derive(shared_secret)
    
    # Generate a random IV (Initialization Vector) for AES encryption
    iv = os.urandom(16)
    
    # Encrypt the message using AES in CBC mode
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Make sure the message is padded to be a multiple of 16 bytes (PKCS7 padding)
    padder = padding.PKCS7(128).padder()  # PKCS7 padding with 128-bit block size
    padded_message = padder.update(message) + padder.finalize()
    
    # Encrypt the padded message
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    encrypted_message = iv + salt + encrypted_message
    encrypted_message = base64.b64encode(encrypted_message).decode('utf-8')
    
    # Return IV, Salt, and encrypted message (so we can use the same salt during decryption)
    return encrypted_message

def ecc_decrypt(encrypted_message, private_key, public_key):
    encrypted_message = base64.b64decode(encrypted_message)
    # Extract the IV (first 16 bytes), salt (next 16 bytes), and encrypted data
    iv = encrypted_message[:16]
    salt = encrypted_message[16:32]
    encrypted_data = encrypted_message[32:]

    # Generate the shared secret using the private key and the public key of the sender
    shared_secret = private_key.exchange(ec.ECDH(), public_key)
    
    # Derive the symmetric key from the shared secret using PBKDF2 and the same salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    symmetric_key = kdf.derive(shared_secret)

    # Decrypt the message using AES in CBC mode
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding from the decrypted message (PKCS7 unpadding)
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
    decrypted_message_str = unpadded_message.decode('utf-8')  # Decoding to string

    return decrypted_message_str  # Return the original decrypted message (without padding)


# Super Encryption Function
def super_encrypt(message, rail_key):
    # Step 1: Encrypt with Rail Fence Cipher
    rail_encrypted, space_positions = rail_fence_encrypt(message, rail_key)
    print(f"Space Positions: {space_positions}")
    
    # Step 2: Encrypt with ECC (Elliptic Curve Cryptography)
    private_key, public_key = generate_ecc_keys()
    ecc_encrypted = ecc_encrypt(rail_encrypted, public_key, private_key)
    private_key_content, public_key_content = get_key_base64(private_key, public_key)
    
    query = "INSERT INTO messages (encrypted_text, rail_fence_key, space_position, private_key_content, public_key_content) VALUES (%s, %s, %s, %s, %s)"
    params = (ecc_encrypted, rail_key, str(space_positions), private_key_content, public_key_content)
    cn.run_query(query, params, fetch=False)
    return ecc_encrypted, space_positions

# Super Decryption Function
def super_decrypt(encrypted_message, rail_key, space_positions):
    # Step 1: Decrypt with ECC (Elliptic Curve Cryptography)
    query = "SELECT private_key_content, public_key_content FROM messages WHERE encrypted_text = %s"
    result = cn.run_query(query, (encrypted_message,), True)
    private_key_content, public_key_content = result[0], result[1]
    ecc_private_key = load_key_from_base64(private_key_content, is_private=True)    
    ecc_public_key = load_key_from_base64(public_key_content, is_private=False)
    ecc_decrypted = ecc_decrypt(encrypted_message, ecc_private_key, ecc_public_key)
    print(f"ECC Decrypted: {ecc_decrypted}")

    # Step 2: Decrypt with Rail Fence Cipher
    space_positions = [int(pos.strip()) for pos in space_positions.strip('[]').split(',')]
    rail_decrypted = rail_fence_decrypt(ecc_decrypted, rail_key, space_positions)
    print(f"Rail Fence Decrypted: {rail_decrypted}")
    return rail_decrypted

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

# print("Private Key:", private_key)
# print("Public Key:", public_key)
# private_key_base64, public_key_base64 = get_key_base64(private_key, public_key)
# print("Private Key Base64:", private_key_base64)
# print("Public Key Base64:", public_key_base64)

# Contoh penggunaan untuk memuat kunci dari Base64
# private_key_reloaded = load_key_from_base64(private_key_base64, is_private=True)
# public_key_reloaded = load_key_from_base64(public_key_base64, is_private=False)

# print("Private Key Loaded:", private_key_reloaded)
# print("Public Key Loaded:", public_key_reloaded)

# message = "Hello, World! This is a test message. Let's see if the encryption and decryption work correctly. This is a very long message that will be encrypted and decrypted using ECC."
# encrypyted_message = ecc_encrypt(message, public_key_reloaded, private_key_reloaded)
# print("Encrypted Message:", encrypyted_message)

# decrypted_message = ecc_decrypt(encrypyted_message, private_key_reloaded, public_key_reloaded)
# print("Decrypted Message:", decrypted_message)

