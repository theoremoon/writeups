from binascii import hexlify, unhexlify

f = open("cipher", "rb")

cnt = 0
while True:
    o = open("c{}".format(cnt), "w")
    for _ in range(16):
        bs = f.read(16)
        o.write(hexlify(bs).decode() + "\n")
        if len(bs) < 16:
            quit()

    o.close()
    cnt += 1
