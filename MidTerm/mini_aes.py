"""
Referensi:
- https://piazza.com/class_profile/get_resource/ixlc30gojpe5fs/iyv0273azwtz4
- https://sandilands.info/sgordon/teaching/reports/simplified-aes-example-v2.pdf
"""

class MiniAes:
    # constants
    __ROUND__ = 3
    __SBOX__ = [
        0xE, 0x4, 0xD, 0x1,  # 0x0  0x1  0x2  0x3
        0x2, 0xF, 0xB, 0x8,  # 0x4  0x5  0x6  0x7
        0x3, 0xA, 0x6, 0xC,  # 0x8  0x9  0xA  0xB
        0x5, 0x9, 0x0, 0x7,  # 0xC  0xD  0xE  0xF
    ]
    __INV_SBOX__ = [
        0xE, 0x3, 0x4, 0x8,
        0x1, 0xC, 0xA, 0xF,
        0x7, 0xD, 0x9, 0x6,
        0xB, 0x2, 0x0, 0x5
    ]

    def __init__(self):
        self.__plaintext = ""
        self.__keys = ""

    # Getter and Setter for __plaintext
    def set_plaintext(self, plaintext: str) -> None:
        self.__plaintext = plaintext.upper()

    def get_plaintext(self) -> str:
        return self.__plaintext

    # Getter and Setter for __keys
    def set_keys(self, keys: str) -> None:
        while len(keys) < 4:
            # append with "0"
            keys += "0"
        self.__keys = keys[:4].upper()

    def get_keys(self) -> str:
        return self.__keys

    def round_key_generator(self) -> None:
        # untuk key expansion sederhana (belum implementasi full)
        return

    def sub_nibbles(self, state: str):
        subs_list: list[list[int]] = []

        # defensive measure
        if len(state) == 0:
            print("plaintext is empty")
            exit(1)

        # check if plaintext is divisible by 2
        # if not, pad the plaintext with a '0' character
        if len(state) & 1:
            state += "0"

        for i in range(0, len(state), 2):
            this_char_list: list[int] = []
            two_chars = state[i : i + 2]

            for char in two_chars:
                # Convert char ke angka
                full_nibble = int(char, 16)

                # get first and last nibble
                first_nibble = (full_nibble & 240) >> 4
                last_nibble = full_nibble & 15

                # Ganti dari S-Box
                first_nibble_subs = self.__SBOX__[first_nibble]
                last_nibble_subs = self.__SBOX__[last_nibble]

                # add to list
                this_char_list.append(first_nibble_subs)
                this_char_list.append(last_nibble_subs)

            subs_list.append(this_char_list)

        return subs_list

    def shift_rows(self, state: list[list[int]]):
        for matrix in state:
            # swap the second and fourth element
            matrix[1], matrix[3] = matrix[3], matrix[1]
        return state

    def mix_columns(self, state):
        __CONSTANT_MATRIX = [
            0x3,
            0x4,
            0x4,
            0x3,
        ]

        result_list: list[list[int]] = []

        for matrix in state:
            this_matrix_result = []

            # index 0
            index_zero = (__CONSTANT_MATRIX[0] * matrix[0]) ^ (__CONSTANT_MATRIX[2] * matrix[1])
            this_matrix_result.append(index_zero)

            # index 1
            index_one = (__CONSTANT_MATRIX[1] * matrix[0]) ^ (__CONSTANT_MATRIX[3] * matrix[1])
            this_matrix_result.append(index_one)

            # index 2
            index_two = (__CONSTANT_MATRIX[0] * matrix[2]) ^ (__CONSTANT_MATRIX[2] * matrix[3])
            this_matrix_result.append(index_two)

            # index 3
            index_three = (__CONSTANT_MATRIX[1] * matrix[2]) ^ (__CONSTANT_MATRIX[3] * matrix[3])
            this_matrix_result.append(index_three)

            result_list.append(this_matrix_result)

        return result_list

    def add_round_keys(self, state: list[list[int]], round_key: list[int]) -> list[list[int]]:
        result: list[list[int]] = []

        for matrix in state:
            this_matrix_result: list[int] = []

            for s, k in zip(matrix, round_key):
                this_matrix_result.append(s ^ k)

            result.append(this_matrix_result)

        return result

    def encrypt(self) -> str:
        if not self.__plaintext or len(self.__plaintext) != 4:
            raise ValueError("Plaintext harus 4 karakter hex")

        if not self.__keys or len(self.__keys) != 4:
            raise ValueError("Key harus 4 karakter hex")

        state = self.sub_nibbles(self.__plaintext)
        key_matrix = self.sub_nibbles(self.__keys)

        state = self.add_round_keys(state, key_matrix[0])

        for current_round in range(self.__ROUND__ - 1):
            print(f"Running round: {current_round}")
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_keys(state, key_matrix[0])

        state = self.shift_rows(state)
        state = self.add_round_keys(state, key_matrix[0])

       # Convert the final state back to hex string
        result = ""
        matrix = state[0]  # take matrix one
        for i in range(0, len(matrix), 2):
            combined = (matrix[i] << 4) + matrix[i + 1]
            result += format(combined, "02X")  # always 2 digit hex

        return result