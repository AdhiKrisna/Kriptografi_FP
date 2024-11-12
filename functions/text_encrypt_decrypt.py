from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
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

def ecc_encrypt(message, public_key):
    encoded_message = message.encode()
    encrypted_message = base64.b64encode(encoded_message).decode()
    return encrypted_message

def ecc_decrypt(encrypted_message, private_key):
    decoded_message = base64.b64decode(encrypted_message.encode())
    return decoded_message.decode()

# Super Encryption Function
def super_encrypt(message, rail_key, ecc_public_key, ecc_private_key):
    # Step 1: Encrypt with Rail Fence Cipher
    rail_encrypted, space_positions = rail_fence_encrypt(message, rail_key)
    print(f"Space Positions: {space_positions}")
    print(f"Rail Fence Encrypted: {rail_encrypted}")
    
    # Step 2: Encrypt with ECC (Elliptic Curve Cryptography)
    private_key_content = extract_key_content(ecc_private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
    ecc_encrypted = ecc_encrypt(rail_encrypted, ecc_public_key)
    cn.run_query("INSERT INTO messages (encrypted_text, private_key) VALUES (%s, %s);", (ecc_encrypted, private_key_content), fetch=False)
    return ecc_encrypted, space_positions

# Super Decryption Function
def super_decrypt(encrypted_message, rail_key, space_positions, private_key_content):
    # Step 1: Decrypt with ECC (Elliptic Curve Cryptography)
    # private_key_content = extract_key_content(ecc_private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
    print("\nPrivate Key Content:", private_key_content)
    ecc_private_key = add_key_markers(private_key_content, "PRIVATE")
    ecc_decrypted = ecc_decrypt(encrypted_message, ecc_private_key)
    print(f"ECC Decrypted: {ecc_decrypted}")

    # Step 2: Decrypt with Rail Fence Cipher
    # Display the Private Key
    space_positions = [int(pos.strip()) for pos in space_positions.strip('[]').split(',')]
    
    rail_decrypted = rail_fence_decrypt(ecc_decrypted, rail_key, space_positions)
    print(f"Rail Fence Decrypted: {rail_decrypted}")
    return rail_decrypted

def extract_key_content(key_bytes):
    key_str = key_bytes.decode()
    key_lines = key_str.splitlines()
    return ''.join(line for line in key_lines if "BEGIN" not in line and "END" not in line)

def add_key_markers(key_content, key_type="PRIVATE"):
    if key_type == "PRIVATE":
        return f"-----BEGIN PRIVATE KEY-----\n{key_content}\n-----END PRIVATE KEY-----"
    elif key_type == "PUBLIC":
        return f"-----BEGIN PUBLIC KEY-----\n{key_content}\n-----END PUBLIC KEY-----"
    else:
        raise ValueError("Invalid key type. Use 'PRIVATE' or 'PUBLIC'.")



# Contoh penggunaan
private_key, public_key = generate_ecc_keys()
private_key_content = extract_key_content(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))

# encrypted_text, space_positions = super_encrypt("BELAJAR KRIPTOGRAFI UNTUK INDONESIA MERDEKA SUPAYA MENJADI BANGSA YANG ADIL MAKMUR DAN SEJAHTERA MENUJU INDONESIA EMAS", 18, public_key, private_key)
# super_decrypt(encrypted_text, 18, space_positions, private_key_content)
