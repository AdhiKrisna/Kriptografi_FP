from PIL import Image

def encode_image(image_data, output_image_path, message):
    """Embed a message in an image."""
    img = Image.open(image_data)
    encoded = img.copy()

    width, height = img.size
    max_message_length = width * height * 3 // 8  # Maximum characters the image can hold

    # Check if the message is too long for the image
    if len(message) + 3 > max_message_length:  # +3 for the "###" end marker
        raise ValueError("Message is too long to be encoded in the image.")

    # Append end marker to message
    message += '###'

    # Convert message to binary
    binary_message = ''.join([format(ord(char), '08b') for char in message])
    message_length = len(binary_message)

    index = 0
    for y in range(height):
        for x in range(width):
            if index < message_length:
                r, g, b = img.getpixel((x, y))

                # Embed bits into R, G, and B channels
                r = (r & ~1) | int(binary_message[index]) if index < message_length else r
                g = (g & ~1) | int(binary_message[index + 1]) if index + 1 < message_length else g
                b = (b & ~1) | int(binary_message[index + 2]) if index + 2 < message_length else b

                # Update the pixel in the new image
                encoded.putpixel((x, y), (r, g, b))
                index += 3

            if index >= message_length:
                break
        if index >= message_length:
            break

    encoded.save(output_image_path)
    return output_image_path


def decode_image(input_image_path):
    """Extract a hidden message from an image."""
    img = Image.open(input_image_path)
    binary_message = ""

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    # Convert binary to characters
    chars = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join([chr(int(char, 2)) for char in chars if len(char) == 8])

    # Look for the end marker '###'
    end_index = decoded_message.find('###')
    if end_index != -1:
        return decoded_message[:end_index]
    return "Tidak ditemukan pesan yang tersembunyi"
