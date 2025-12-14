HEADER_SIZE = 54
END_MARK = "###"

def text_to_binary(text):
    binary = ""
    for char in text:
        binary += format(ord(char), "08b")
    return binary

def binary_to_text(binary):
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        text += chr(int(byte, 2))
    return text

def file_exists(filename):
    try:
        open(filename, "rb").close()
        return True
    except:
        return False

def is_bmp(filename):
    try:
        file = open(filename, "rb")
        header = file.read(2)
        file.close()
        return header == b'BM'
    except:
        return False

def hide_message(input_image, output_image, secret):
    if not file_exists(input_image):
        print("Error: Image file does not exist.")
        return

    if not is_bmp(input_image):
        print("Error: Only BMP images are supported.")
        return

    try:
        file = open(input_image, "rb")
        image_bytes = bytearray(file.read())
        file.close()
    except:
        print("Error: Could not read image.")
        return

    secret = secret + END_MARK
    secret_binary = text_to_binary(secret)

    if len(secret_binary) > len(image_bytes) - HEADER_SIZE:
        print("Error: Message is too large for this image.")
        return

    index = 0
    for i in range(HEADER_SIZE, HEADER_SIZE + len(secret_binary)):
        image_bytes[i] = (image_bytes[i] & 254) | int(secret_binary[index])
        index += 1

    try:
        file = open(output_image, "wb")
        file.write(image_bytes)
        file.close()
        print("Success: Message hidden in image.")
    except:
        print("Error: Could not save output image.")