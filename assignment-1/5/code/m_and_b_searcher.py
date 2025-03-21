N_SIZE = 256
RES = 133
VAR = 39
VALUE = 183


def main():
    # check m value
    possible_m = [num for num in range(256) if num % 2]
    m_value = 0

    for num in possible_m:
        temp = VAR * num

        if temp % N_SIZE == RES:
            print("We got the m result:", num)
            m_value = num

    # check b value
    temp_value = m_value * 255
    b_value = 1

    while True:
        tmp = temp_value + b_value

        if tmp % N_SIZE == VALUE:
            print("We got the b result:", b_value)
            break

        b_value += 1

    # find x value for decrypting
    x_value = 1

    while True:
        tmp = m_value * x_value

        if tmp % N_SIZE == 1:
            print("We got the x result:", x_value)
            break

        x_value += 1

    return


if __name__ == "__main__":
    main()
