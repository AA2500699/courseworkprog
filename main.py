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
    
def read_message_file(filename):
    if not file_exists(filename):
        print("Error: Message file does not exist.")
        return None

    try:
        f = open(filename, "r")
        content = f.read()
        f.close()
    except:
        print("Error: Cannot read message file.")
        return None

    if content == "":
        print("Warning: Message file is empty.")
        return ""

    return content

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

def extract_message(image):
    if not file_exists(image):
        print("Error: Image file does not exist.")
        return

    if not is_bmp(image):
        print("Error: Only BMP images are supported.")
        return

    try:
        f = open(image, "rb")
        data = f.read()
        f.close()
    except:
        print("Error: Could not read image.")
        return

    binary = ""
    for i in range(HEADER_SIZE, len(data)):
        binary += str(data[i] & 1)

    message = binary_to_text(binary)

    if END_MARK in message:
        print("Hidden message:")
        print(message.split(END_MARK)[0])
    else:
        print("Warning: No hidden message found.")

def get_input(prompt):
    value = ""
    while value == "":
        value = input(prompt).strip()
        if value == "":
            print("Input cannot be empty.")
    return value

def main():
    while True:
        print("\n--- Steganography ---")
        print("1. Hide message you write")
        print("2. Hide message from text file")
        print("3. Extract message")
        print("4. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            img = get_input("Enter BMP image name: ")
            out = get_input("Enter output image name: ")
            msg = input("Enter secret message: ")
            hide_message(img, out, msg)

        elif choice == "2":
            img = get_input("Enter BMP image name: ")
            out = get_input("Enter output image name: ")
            file_name = get_input("Enter message file name: ")
            message = read_message_file(file_name)
            if message is not None:
                hide_message(img, out, message)

        elif choice == "3":
            img = get_input("Enter stego image name: ")
            extract_message(img)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose 1, 2, 3 or 4.")
main()