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
    """Embed a message in an image."""
    img = Image.open(image_data)
    newimg = img.copy()

    # Ensure there is data to encode
    if len(message) == 0:
        raise ValueError("Data to be encoded is empty")

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
