from PIL import Image

def encode_image(image_data, output_image_path, message):
    """Menyisipkan pesan ke dalam gambar."""
    # Membuka gambar dari BytesIO
    img = Image.open(image_data)
    encoded = img.copy()

    width, height = img.size
    index = 0

    # Tambahkan karakter pembatas di akhir pesan untuk menandai akhir pesan
    message += '###'
    
    # Konversi pesan ke dalam bentuk biner
    binary_message = ''.join([format(ord(char), '08b') for char in message])
    message_length = len(binary_message)
    
    for y in range(height):
        for x in range(width):
            # Ambil nilai RGB dari pixel
            r, g, b = img.getpixel((x, y))

            # Modifikasi bit paling tidak signifikan dari warna merah (R)
            if index < message_length:
                r = (r & ~1) | int(binary_message[index])
                index += 1

            # Modifikasi bit paling tidak signifikan dari warna hijau (G)
            if index < message_length:
                g = (g & ~1) | int(binary_message[index])
                index += 1

            # Modifikasi bit paling tidak signifikan dari warna biru (B)
            if index < message_length:
                b = (b & ~1) | int(binary_message[index])
                index += 1

            # Update pixel dengan nilai RGB baru
            encoded.putpixel((x, y), (r, g, b))

            # Jika pesan sudah selesai disisipkan, keluar dari loop
            if index >= message_length:
                break
        if index >= message_length:
            break

    # Simpan gambar yang telah disisipi pesan
    encoded.save(output_image_path)
    return output_image_path


# Fungsi untuk mengekstrak data dari gambar
def decode_image(input_image_path):
    """Ekstrak pesan dari gambar."""
    img = Image.open(input_image_path)
    binary_message = ""
    
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            # Ambil bit paling tidak signifikan dari setiap warna (RGB)
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    # Konversi biner menjadi teks
    chars = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join([chr(int(char, 2)) for char in chars])

    # Cari pembatas '###' untuk menandai akhir pesan
    end_index = decoded_message.find('###')
    if end_index != -1:
        return decoded_message[:end_index]
    return "Tidak ditemukan pesan yang tersembunyi"