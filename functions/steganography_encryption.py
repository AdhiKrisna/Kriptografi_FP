from PIL import Image
import io

# Convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Modify pixels according to the 8-bit binary data
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                            imdata.__next__()[:3] +
                            imdata.__next__()[:3]]

        # Modify pixel values
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # Set the stopping condition
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

# Encode the data into the image
def encode_image(image_data, output_image_path, message):
    # Embed a message in an image
    img = Image.open(image_data)
    newimg = img.copy()

    # Ensure there is data to encode
    if len(message) == 0:
        raise ValueError("Data to be encoded is empty")
    x, y = 0, 0
    # Embed the data into the image
    for pixel in modPix(newimg.getdata(), message + '###'):  # Append delimiter
        newimg.putpixel((x, y), pixel)
        if (x == newimg.width - 1):
            x = 0
            y += 1
        else:
            x += 1

    # Save the new image with the embedded data
    newimg.save(output_image_path)
    return output_image_path

# Decode the hidden data from the image
def decode_image(input_image_path):
    """Extract the hidden message from an image."""
    img = Image.open(input_image_path)
    imgdata = iter(img.getdata())
    
    data = ''
    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
        
        # Binary data string
        binstr = ''
        for i in pixels[:8]:
            binstr += '0' if i % 2 == 0 else '1'

        # Convert binary string to character
        data += chr(int(binstr, 2))
        
        # Check if the delimiter is reached
        if pixels[-1] % 2 != 0:
            return data.rstrip('###')


# from PIL import Image
# import io

# # Mengonversi data (pesan) menjadi bentuk biner 8-bit menggunakan nilai ASCII dari karakter
# def genData(data):
#     newd = []
#     for i in data:
#         # Mengubah setiap karakter menjadi biner 8-bit
#         newd.append(format(ord(i), '08b'))
#     return newd

# # Memodifikasi piksel sesuai dengan data biner 8-bit
# def modPix(pix, data):
#     datalist = genData(data)  # Mengonversi data menjadi bentuk biner
#     lendata = len(datalist)   # Mendapatkan panjang data
#     imdata = iter(pix)        # Membuat iterator untuk piksel gambar

#     # Loop untuk setiap karakter dalam data
#     for i in range(lendata):
#         # Mengambil 3 piksel sekaligus
#         pix = [value for value in imdata.__next__()[:3] +
#                             imdata.__next__()[:3] +
#                             imdata.__next__()[:3]]

#         # Memodifikasi nilai piksel
#         for j in range(0, 8):
#             # Jika bit data adalah '0' dan nilai piksel ganjil, ubah menjadi genap
#             if (datalist[i][j] == '0' and pix[j] % 2 != 0):
#                 pix[j] -= 1
#             # Jika bit data adalah '1' dan nilai piksel genap, ubah menjadi ganjil
#             elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
#                 if pix[j] != 0:
#                     pix[j] -= 1
#                 else:
#                     pix[j] += 1

#         # Menetapkan kondisi akhir (delimiter)
#         if i == lendata - 1:
#             # Menandai akhir pesan dengan membuat bit terakhir ganjil
#             if pix[-1] % 2 == 0:
#                 if pix[-1] != 0:
#                     pix[-1] -= 1
#                 else:
#                     pix[-1] += 1
#         else:
#             # Jika belum akhir pesan, pastikan bit terakhir genap
#             if pix[-1] % 2 != 0:
#                 pix[-1] -= 1

#         pix = tuple(pix)
#         # Mengembalikan piksel yang telah dimodifikasi
#         yield pix[0:3]
#         yield pix[3:6]
#         yield pix[6:9]

# # Fungsi untuk menyisipkan pesan ke dalam gambar
# def encode_image(image_data, output_image_path, message):
#     """Menyisipkan pesan ke dalam gambar."""
#     img = Image.open(image_data)
#     newimg = img.copy()

#     # Memastikan ada data yang akan disisipkan
#     if len(message) == 0:
#         raise ValueError("Data yang akan disisipkan kosong")
    
#     x, y = 0, 0
#     # Menyisipkan data ke dalam gambar
#     for pixel in modPix(newimg.getdata(), message + '###'):  # Menambahkan delimiter '###'
#         newimg.putpixel((x, y), pixel)
#         if (x == newimg.width - 1):
#             x = 0
#             y += 1
#         else:
#             x += 1

#     # Menyimpan gambar baru yang telah dimodifikasi
#     newimg.save(output_image_path)
#     return output_image_path

# # Fungsi untuk mengekstrak data tersembunyi dari gambar
# def decode_image(input_image_path):
#     """Mengekstrak pesan tersembunyi dari gambar."""
#     img = Image.open(input_image_path)
#     imgdata = iter(img.getdata())
    
#     data = ''
#     while True:
#         # Mengambil 3 piksel sekaligus
#         pixels = [value for value in imgdata.__next__()[:3] +
#                                 imgdata.__next__()[:3] +
#                                 imgdata.__next__()[:3]]
        
#         # Membuat string biner
#         binstr = ''
#         for i in pixels[:8]:
#             # Jika bit terakhir adalah 0, tambahkan '0', jika ganjil tambahkan '1'
#             binstr += '0' if i % 2 == 0 else '1'

#         # Mengonversi string biner menjadi karakter
#         data += chr(int(binstr, 2))
        
#         # Memeriksa apakah sudah mencapai delimiter
#         if pixels[-1] % 2 != 0:
#             return data.rstrip('###')
