offset = 0x137
size = 0x678

data = open("code2", "rb").read()[offset : offset + size]
key = [ord(c) for c in "r00t"]

new_opecodes = []

for i in range(0, size):
    new_opecodes.append((data[i] - key[i % 4] + 256) % 256)
open("stage3_code", "wb").write(bytearray(new_opecodes))
