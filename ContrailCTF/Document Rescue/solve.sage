from Crypto.Util.number import bytes_to_long, long_to_bytes
data = open("flag.www", "rb").read()

m2 = bytes_to_long(b"-9.9")
mn_ = b"%EOF\0\0\0\0"

c1 = bytes_to_long(data[:4])
c2 = bytes_to_long(data[4:8])
cn_1 = bytes_to_long(data[-8:-4])
cn =   bytes_to_long(data[-4:])

x2 = m2 ^^ c2

m = 2 ^ 32

for i in range(0, len(mn_) - 3):
    mn = bytes_to_long(mn_[i : i + 4])
    xn = mn ^^ cn

    a, b = var('a', "b")
    solutions = solve_mod([ a*c1 + b == x2, a*cn_1 + b == xn ], m)

    for s in solutions:
        a, b = s
        print(a,b)
        name = "flag_{}_{}".format(a,b)
        # decrypt
        plain = b""
        for j in range(4, len(data), 4):
            c = bytes_to_long(data[j : j + 4])
            c_1 = bytes_to_long(data[j - 4 : j])
            m_j = int((a * c_1 + b) % m) ^^ c
            plain += long_to_bytes(m_j, blocksize=4)

        plain = bytearray(plain)
        plain[:4] = b"-1.5"
        plain = b"%PDF" + bytes(plain)

        with open(name, "wb") as f:
            f.write(plain)
