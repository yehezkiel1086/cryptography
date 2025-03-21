MAX_B_VALUE = 255
MAX_M_VALUE = 256


def is_value_right(m: int, b: int) -> bool:
    # equation of the known plain text
    if (((255 * m) + b) % 256) == 183:
        if (((216 * m) + b) % 256) == 50:
            return True

    return False


def main():
    for possible_m_value in range(1, 257):
        for possible_b_value in range(256):
            is_m_and_b_right = is_value_right(possible_m_value, possible_b_value)

            if is_m_and_b_right:
                print(f"m value: {possible_m_value}, b value: {possible_b_value}")

    return


if __name__ == "__main__":
    main()
