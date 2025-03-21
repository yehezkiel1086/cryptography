B_VALUE = 42
N_VALUE = 256
X_VALUE = 187


def main():
    # search the inverse of m
    encrypted_hex_values = read_image("affinecipher.jpeg")

    if encrypted_hex_values is not None:
        decrypted_hex = get_decrypted_array(encrypted_hex_values)
        bytearray_plain = array_of_hex_to_bytearray(decrypted_hex)
        write_to_file("decrypted.jpeg", bytearray_plain)

    return


def get_decrypted_array(array: list[str]):
    cipher_hex = []

    for i in range(len(array)):
        C = hex(get_plaintext(int(array[i], 16)))
        cipher_hex.append(C)

    return cipher_hex


def get_plaintext(ciphertext) -> int:
    return (X_VALUE * (ciphertext - B_VALUE)) % N_VALUE


def read_image(image_path: str):
    try:
        with open(image_path, "rb") as image:
            f = image.read()
            b = bytearray(f)
            array_of_hex = [hex(byte) for byte in b]

            return array_of_hex
    except FileNotFoundError:
        print("Error: file not found")

        return None
    except ValueError as e:
        print("Error:", e)

        return None


def array_of_hex_to_bytearray(array_of_hex: list[str]):
    bytearray_data = bytearray()

    for hex_value in array_of_hex:
        if hex_value.startswith("0x"):
            hex_value = hex_value[2:]
        byte_value = int(hex_value, 16)
        bytearray_data.append(byte_value)

    return bytearray_data


def write_to_file(image_name: str, bytes_data):
    try:
        with open(image_name, "wb") as file:
            file.write(bytes_data)
            print("Berhasil membuat gambar")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
