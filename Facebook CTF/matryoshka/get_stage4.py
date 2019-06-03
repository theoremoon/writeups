offset = 0x12c
size = 0x44a

data = open("stage3_code", "rb").read()[offset : offset + size]
key = [ord(c) for c in "LJcbuOQJ"]

new_opecodes = []

for i in range(0, size):
    new_opecodes.append(data[i] ^ key[i % 8])
open("stage4_code", "wb").write(bytearray(new_opecodes))
