from params import K1, K2, L3, R3
from Crypto.Util.number import *


def exor(a, b):
    temp = ""
    for i in range(n):
        if (a[i] == b[i]):
            temp += "0"
        else:
            temp += "1"
    return temp

n = 26936

# L3 = R2 = f1 ^ L1 = R1 ^ K1 ^ L1
# R1 = f2 ^ L2 = (R2 ^ K2) ^ (R1) = (f1 ^ L1) ^ K2 ^ R1 = (R^1 ^ K1) ^ L1 ^ K2 ^ R1 = K1 ^ K2 ^ L1
L1 = exor(exor(R3, K1), K2)
R1 = exor(exor(L3, K1), L1)

plaintext = long_to_bytes(int(L1 + R1, 2))
with open("plaintext", "wb") as f:
    f.write(bytes.fromhex(plaintext.decode()))
