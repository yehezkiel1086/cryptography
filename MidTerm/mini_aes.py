class MiniAes:
    # constants
    __ROUND__ = 3
    __SBOX__ = [
        [0xE, 0x4, 0xD, 0x1],  # 0x0  0x1  0x2  0x3
        [0x2, 0xF, 0xB, 0x8],  # 0x4  0x5  0x6  0x7
        [0x3, 0xA, 0x6, 0xC],  # 0x8  0x9  0xA  0xB
        [0x5, 0x9, 0x0, 0x7],  # 0xC  0xC  0xD  0xE
    ]

    def __init__(self):
        self.__plaintext = ""
        self.__keys = ""

    # Getter and Setter for __plaintext
    def set_plaintext(self, plaintext: str) -> None:
        self.__plaintext = plaintext

    def get_plaintext(self) -> str:
        return self.__plaintext

    # Getter and Setter for __keys
    def set_keys(self, keys: str) -> None:
        self.__keys = keys

    def get_keys(self) -> str:
        return self.__keys

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
                # result := 8 bit, 2^8 == 16 ^ 2 == 256
                full_nibble = int(char, 16)

                # get first and last nibble
                # using AND operator
                # nibble = 4 bit, full nibble = 8 bit
                # 1111 0000 = 240
                # 0000 1111 = 15
                first_nibble = full_nibble & 240 >> 4  # needs to be shifted
                last_nibble = full_nibble & 15

                # Ganti dari S-Box
                first_nibble_subs = self.__SBOX__[first_nibble // 4][first_nibble % 4]
                last_nibble_subs = self.__SBOX__[last_nibble // 4][last_nibble % 4]

                # add to list
                this_char_list.append(first_nibble_subs)
                this_char_list.append(last_nibble_subs)

            subs_list.append(this_char_list)

        return subs_list

    def shift_rows(self, state: list[list[int]]):
        for matrix in state:
            matrix[1] ^= matrix[3]
            matrix[3] ^= matrix[1]
            matrix[1] ^= matrix[3]

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
            index_zero = (__CONSTANT_MATRIX[0] * matrix[0]) ^ (
                __CONSTANT_MATRIX[2] * matrix[1]
            )
            this_matrix_result.append(index_zero)

            # index 1
            index_one = (__CONSTANT_MATRIX[1] * matrix[0]) ^ (
                __CONSTANT_MATRIX[3] * matrix[1]
            )
            this_matrix_result.append(index_one)

            # index 2
            index_two = (__CONSTANT_MATRIX[0] * matrix[2]) ^ (
                __CONSTANT_MATRIX[2] * matrix[3]
            )
            this_matrix_result.append(index_two)

            # index 3
            index_three = (__CONSTANT_MATRIX[1] * matrix[2]) ^ (
                __CONSTANT_MATRIX[3] * matrix[3]
            )
            this_matrix_result.append(index_three)

            result_list.append(this_matrix_result)

        # Placeholder: implement column mixing on state
        return result_list

    def add_round_keys(self, state: str, round_key: str) -> str:
        result = ""

        for s_char, k_char in zip(state, round_key):
            s_val = int(s_char, 16)
            k_val = int(k_char, 16)
            result += format(s_val ^ k_val, "X")

        return result
