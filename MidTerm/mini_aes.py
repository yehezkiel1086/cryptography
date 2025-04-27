"""
references:
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
        0x5, 0x9, 0x0, 0x7,  # 0xC  0xC  0xD  0xE
    ]
    __INV_SBOX__ = [
        0xE, 0x3, 0x4, 0x8,
        0x1, 0xC, 0xA, 0xF,
        0x7, 0xD, 0x9, 0x6,
        0xD, 0x2, 0x0, 0x5,
    ]
    __MULTIPLICATION_TABLE__ = [
        # 0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0], # 0
        [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF], # 1
        [0x0, 0x2, 0x4, 0x6, 0x8, 0xA, 0xC, 0xE, 0x3, 0x1, 0x7, 0x5, 0xB, 0x9, 0xF, 0xD], # 2
        [0x0, 0x3, 0x6, 0x5, 0xC, 0xF, 0xA, 0x9, 0xB, 0x8, 0xD, 0xE, 0x7, 0x4, 0x1, 0x2], # 3
        [0x0, 0x4, 0x8, 0xC, 0x3, 0x7, 0xB, 0xF, 0x6, 0x2, 0xE, 0xA, 0x5, 0x1, 0xD, 0x9], # 4
        [0x0, 0x5, 0xA, 0xF, 0x7, 0x2, 0xD, 0x8, 0xE, 0xB, 0x4, 0x1, 0x9, 0xC, 0x3, 0x6], # 5
        [0x0, 0x6, 0xC, 0xA, 0xB, 0xD, 0x7, 0x1, 0x5, 0x3, 0x9, 0xF, 0xE, 0x8, 0x2, 0x4], # 6
        [0x0, 0x7, 0xE, 0x9, 0xF, 0x8, 0x1, 0x6, 0xD, 0xA, 0x3, 0x4, 0x2, 0x5, 0xC, 0xB], # 7
        [0x0, 0x8, 0x3, 0xB, 0x6, 0xE, 0x5, 0xD, 0xC, 0x4, 0xF, 0x7, 0xA, 0x2, 0x9, 0x1], # 8
        [0x0, 0x9, 0x1, 0x8, 0x2, 0xB, 0x3, 0xA, 0x4, 0xD, 0x5, 0xC, 0x6, 0xF, 0x7, 0xE], # 9
        [0x0, 0xA, 0x7, 0xD, 0xE, 0x4, 0x9, 0x3, 0xF, 0x5, 0x8, 0x2, 0x1, 0xB, 0x6, 0xC], # A
        [0x0, 0xB, 0x5, 0xE, 0xA, 0x1, 0xF, 0x4, 0x7, 0xC, 0x2, 0x9, 0xD, 0x6, 0x8, 0x3], # B
        [0x0, 0xC, 0xB, 0x7, 0x5, 0x9, 0xE, 0x2, 0xA, 0x6, 0x1, 0xD, 0xF, 0x3, 0x4, 0x8], # C
        [0x0, 0xD, 0x9, 0x4, 0x1, 0xC, 0x8, 0x5, 0x2, 0xF, 0xB, 0x6, 0x3, 0xE, 0xA, 0x7], # D
        [0x0, 0xE, 0xF, 0x1, 0xD, 0x3, 0x2, 0xC, 0x9, 0x7, 0x6, 0x8, 0x4, 0xA, 0xB, 0x5], # E
        [0x0, 0xF, 0xD, 0x2, 0x9, 0x6, 0x4, 0x8, 0x1, 0xE, 0xC, 0x3, 0x8, 0x7, 0x5, 0xA], # F
    ]

    def __init__(self, plaintext: str = "", keys: str = ""):
        self.__plaintext = plaintext
        self.__keys = keys
        self.__round_keys: list[list[int]] = []
        self.__ciphertext = ""

    # Getter and Setter for __ciphertext
    def set_ciphertext(self, ciphertext: str) -> None:
        self.__ciphertext = ciphertext

    def get_ciphertext(self) -> str:
        return self.__ciphertext

    # Getter and Setter for __plaintext
    def set_plaintext(self, plaintext: str) -> None:
        self.__plaintext = plaintext

    def get_plaintext(self) -> str:
        return self.__plaintext

    # Getter and Setter for __keys
    def set_keys(self, keys: str) -> None:
        # make at least the length of the keys is 2
        while len(keys) < 2:
            # append with "0"
            keys += "0"

        self.__keys = keys[:2]

    def get_keys(self) -> str:
        return self.__keys

    # Getter and Setter for __round_keys
    def set_round_keys(self, keys: list[list[int]]) -> None:
        self.__round_keys = keys

    def get_round_keys(self) -> list[list[int]]:
        return self.__round_keys

    def convert_to_nibble(self, text: str) -> list[list[int]]:
        res: list[list[int]] = []
        copy_of_text = text

        # defensive measure
        if len(text) == 0:
            raise ValueError("plaintext must not be empty")

        # check if plaintext is divisible by 2
        # if not, pad the plaintext with a '0' character
        if len(text) & 1:
            copy_of_text += "0"

        for i in range(0, len(copy_of_text), 2):
            this_char_list: list[int] = []
            two_chars = text[i : i + 2]

            this_char_list.append((int(two_chars[0], 16) & 240) >> 4)
            this_char_list.append(int(two_chars[0], 16) & 15)
            this_char_list.append((int(two_chars[1], 16) & 240) >> 4)
            this_char_list.append(int(two_chars[1], 16) & 15)

            res.append(this_char_list)

        return res

    def round_key_generator(self) -> None:
        round_keys: list[list[int]] = []

        # keys
        if self.get_keys() == "":
            self.set_keys("00")

        keys = self.get_keys()

        # round 0
        round_0_keys: list[int] = []
        round_0_keys.append((int(keys[0], 16) & 240) >> 4)
        round_0_keys.append(int(keys[0], 16) & 15)
        round_0_keys.append((int(keys[1], 16) & 240) >> 4)
        round_0_keys.append(int(keys[1], 16) & 15)

        round_keys.append(round_0_keys)

        # round = 3
        # but needed more for round 0 (plus 1) and the last one (plus 1)
        for i in range(self.__ROUND__):
            this_round_keys: list[int] = []

            this_round_keys.append(round_keys[i][0] ^ self.__SBOX__[round_keys[i][3]] ^ i)
            this_round_keys.append(round_keys[i][1] ^ this_round_keys[0])
            this_round_keys.append(round_keys[i][2] ^ this_round_keys[1])
            this_round_keys.append(round_keys[i][3] ^ this_round_keys[2])

            round_keys.append(this_round_keys)

        self.set_round_keys(round_keys)

        return

    def sub_nibbles(self, state: list[list[int]]):
        subs_list: list[list[int]] = []

        for matrix in state:
            nibble_subs: list[int] = []

            for nibble in matrix:
                nibble_subs.append(self.__SBOX__[nibble])

            subs_list.append(nibble_subs)

        return subs_list

    def shift_rows(self, state: list[list[int]]) -> list[list[int]]:
        return [[matrix[0], matrix[3], matrix[2], matrix[1]] for matrix in state]

    def mix_columns(self, state: list[list[int]]) -> list[list[int]]:
        __CONSTANT_MATRIX = [
            0x1, 0x4, 0x4, 0x1,
        ]

        result_list: list[list[int]] = []

        for matrix in state:
            this_matrix_result = []

            # index 0
            index_zero = (
                self.__MULTIPLICATION_TABLE__[matrix[0]][__CONSTANT_MATRIX[0]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[1]][__CONSTANT_MATRIX[2]]
            )

            this_matrix_result.append(index_zero)

            # index 1
            index_one = (
                self.__MULTIPLICATION_TABLE__[matrix[0]][__CONSTANT_MATRIX[1]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[1]][__CONSTANT_MATRIX[3]]
            )
            this_matrix_result.append(index_one)

            # index 2
            index_two = (
                self.__MULTIPLICATION_TABLE__[matrix[2]][__CONSTANT_MATRIX[0]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[3]][__CONSTANT_MATRIX[2]]
            )
            this_matrix_result.append(index_two)

            # index 3
            index_three = (
                self.__MULTIPLICATION_TABLE__[matrix[2]][__CONSTANT_MATRIX[1]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[3]][__CONSTANT_MATRIX[3]]
            )
            this_matrix_result.append(index_three)

            result_list.append(this_matrix_result)

        return result_list

    def add_round_keys(
        self, state: list[list[int]], round: int
    ) -> list[list[int]]:
        result: list[list[int]] = []

        round_keys = self.get_round_keys()

        for matrix in state:
            this_matrix_result: list[int] = []

            for s, k in zip(matrix, round_keys[round]):
                this_matrix_result.append(s ^ k)

            result.append(this_matrix_result)

        return result

    def state_to_hex(self, state: list[list[int]]) -> str:
        # Converts the first block of encryption state into a hex string (for output)
        result = ""
        matrix = state[0]  # take ONLY the first matrix, hapus jika ingin outputnya lebih dari 4 digit
        for i in range(0, len(matrix), 2):
            combined = (matrix[i] << 4) | matrix[i + 1]
            result += format(combined, "02X")
        return result

    def encrypt(self) -> list[list[int]]:
        self.round_key_generator()

        state = self.convert_to_nibble(self.get_plaintext())
        state = self.add_round_keys(state, 0)

        for current_round in range(1, self.__ROUND__):
            print(f"ROUND {current_round}")

            state = self.sub_nibbles(state)
            print(f"After SubNibbles: {self.state_to_hex(state)}")

            state = self.shift_rows(state)
            print(f"After ShiftRows : {self.state_to_hex(state)}")

            state = self.mix_columns(state)
            print(f"After MixColumns: {self.state_to_hex(state)}")

            state = self.add_round_keys(state, current_round)
            print(f"After AddRoundKey: {self.state_to_hex(state)}")

        print("FINAL ROUND")
        state = self.sub_nibbles(state)
        print(f"After SubNibbles: {self.state_to_hex(state)}")

        state = self.shift_rows(state)
        print(f"After ShiftRows : {self.state_to_hex(state)}")

        state = self.add_round_keys(state, 3)
        print(f"After AddRoundKey: {self.state_to_hex(state)}")

        print("Encrypt COMPLETE")

        print(f"Ciphertext: {self.state_to_hex(state)}")

        return state

    def inv_sub_nibbles(self, state: list[list[int]]):
        inv_subs_list: list[list[int]] = []

        for matrix in state:
            nibble_subs: list[int] = []

            for nibble in matrix:
                nibble_subs.append(self.__INV_SBOX__[nibble])

            inv_subs_list.append(nibble_subs)

        return inv_subs_list

    def inv_shift_rows(self, state: list[list[int]]):
        return [[matrix[0], matrix[3], matrix[2], matrix[1]] for matrix in state]

    def inv_mix_columns(self, state: list[list[int]]) -> list[list[int]]:
        __CONSTANT_MATRIX = [
            0x9, 0x2, 0x2, 0x9,
        ]

        result_list: list[list[int]] = []

        for matrix in state:
            this_matrix_result = []

            # index 0
            index_zero = (
              self.__MULTIPLICATION_TABLE__[matrix[0]][__CONSTANT_MATRIX[0]] ^
              self.__MULTIPLICATION_TABLE__[matrix[1]][__CONSTANT_MATRIX[2]]
            )
            this_matrix_result.append(index_zero)

            # index 1
            index_one = (
              self.__MULTIPLICATION_TABLE__[matrix[0]][__CONSTANT_MATRIX[1]] ^
              self.__MULTIPLICATION_TABLE__[matrix[1]][__CONSTANT_MATRIX[3]]
            )
            this_matrix_result.append(index_one)

            # index 2
            index_two = (
              self.__MULTIPLICATION_TABLE__[matrix[2]][__CONSTANT_MATRIX[0]] ^
              self.__MULTIPLICATION_TABLE__[matrix[3]][__CONSTANT_MATRIX[2]]
            )
            this_matrix_result.append(index_two)

            # index 3
            index_three = (
              self.__MULTIPLICATION_TABLE__[matrix[2]][__CONSTANT_MATRIX[1]] ^
              self.__MULTIPLICATION_TABLE__[matrix[3]][__CONSTANT_MATRIX[3]]
            )
            this_matrix_result.append(index_three)

            result_list.append(this_matrix_result)

        return result_list

    def decrypt(self) -> list[list[int]]:
        self.round_key_generator()

        print("Decrypting from final round...")

        state = self.convert_to_nibble(self.get_plaintext())
        state = self.add_round_keys(state, 3)
        state = self.inv_shift_rows(state)
        state = self.inv_sub_nibbles(state)

        for current_round in range(2, 0):
            print(f"ROUND {current_round}")

            state = self.add_round_keys(state, current_round)
            print(f"After InvRoundKeys: {self.state_to_hex(state)}")

            state = self.inv_mix_columns(state)
            print(f"After InvMixColumns: {self.state_to_hex(state)}")

            state = self.inv_shift_rows(state)
            print(f"After InvShiftRows : {self.state_to_hex(state)}")

            state = self.inv_sub_nibbles(state)
            print(f"After InvSubNibbles : {self.state_to_hex(state)}")

        print("FINAL INVERSE ROUND")

        state = self.add_round_keys(state, 0)
        print(f"After InvRoundKeys: {self.state_to_hex(state)}")

        print("Decrypt COMPLETE")
        print(f"Plaintext: {self.state_to_hex(state)}")

        return state
