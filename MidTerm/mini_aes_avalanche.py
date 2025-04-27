import copy

from mini_aes import MiniAes

def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

def bin_to_hex(bin_string):
    return hex(int(bin_string, 2))[2:].upper().zfill(len(bin_string) // 4)

def flip_bit(hex_string, bit_position):
    bin_string = hex_to_bin(hex_string)
    bit_list = list(bin_string)
    bit_list[bit_position] = '1' if bit_list[bit_position] == '0' else '0'
    flipped_bin_string = ''.join(bit_list)
    return bin_to_hex(flipped_bin_string)

def count_bit_difference(a, b):
    a_bin = hex_to_bin(a)
    b_bin = hex_to_bin(b)
    count = sum(c1 != c2 for c1, c2 in zip(a_bin, b_bin))
    return count

def avalanche_effect_plaintext(plaintext, key):
    print("=== Avalanche Test: Uji sensitivitas terhadap perubahan 1-bit di plaintext ===")
    aes = MiniAes()
    aes.set_plaintext(plaintext)
    aes.set_keys(key)
    original_state = aes.encrypt()
    original_cipher = aes.state_to_hex(original_state)

    bin_len = len(hex_to_bin(plaintext))
    total_bits_changed = 0

    for i in range(bin_len):
        flipped_plaintext = flip_bit(plaintext, i)
        aes_flipped = MiniAes()
        aes_flipped.set_plaintext(flipped_plaintext)
        aes_flipped.set_keys(key)
        flipped_state = aes_flipped.encrypt()
        flipped_cipher = aes_flipped.state_to_hex(flipped_state)

        bits_changed = count_bit_difference(original_cipher, flipped_cipher)
        total_bits_changed += bits_changed

        print(f"Flipping bit {i}:")
        print(f"  Plaintext: {plaintext} -> {flipped_plaintext}")
        print(f"  Ciphertext: {original_cipher} -> {flipped_cipher}")
        print(f"  Bits yang diganti: {bits_changed}")

    average_change = total_bits_changed / bin_len
    print(f"\nRerata Avalanche Effect (perubahan plaintext 1-bit): {average_change:.2f} bits berubah\n")

def avalanche_effect_key(plaintext, key):
    print("=== Avalanche Test: Uji sensitivitas terhadap perubahan 1-bit di key ===")
    aes = MiniAes()
    aes.set_plaintext(plaintext)
    aes.set_keys(key)
    original_state = aes.encrypt()
    original_cipher = aes.state_to_hex(original_state)

    bin_len = len(hex_to_bin(key))
    total_bits_changed = 0

    for i in range(bin_len):
        flipped_key = flip_bit(key, i)
        aes_flipped = MiniAes()
        aes_flipped.set_plaintext(plaintext)
        aes_flipped.set_keys(flipped_key)
        flipped_state = aes_flipped.encrypt()
        flipped_cipher = aes_flipped.state_to_hex(flipped_state)

        bits_changed = count_bit_difference(original_cipher, flipped_cipher)
        total_bits_changed += bits_changed

        print(f"Flipping bit {i}:")
        print(f"  Key: {key} -> {flipped_key}")
        print(f"  Ciphertext: {original_cipher} -> {flipped_cipher}")
        print(f"  Bits berubah: {bits_changed}")

    average_change = total_bits_changed / bin_len
    print(f"\nRerata Avalanche Effect (perubahan key 1-bit): {average_change:.2f} bits berubah\n")

if __name__ == "__main__":
  # Contoh penggunaan
  plaintext = input("Masukkan plaintext: ") # "C3C3"
  key = input("Masukkan key: ") # "A1A1"

  avalanche_effect_plaintext(plaintext, key)
  avalanche_effect_key(plaintext, key)
