from ptrlib import xor


cipher = open("enc.dat", "rb").read()
keys = bytes([int(x) for x in open("keys").read().strip().split()])

print(xor(keys, cipher))
