def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def ACAC(x):
    x ^= x >> 27
    x *= 0x2a636f7468616e2b
    x &= 0xffffffffffffffff
    x ^= x >> 34
    x *= 0x49534954445455c9
    x &= 0xffffffffffffffff
    x ^= x >> 23
    return x


# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?
#                        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO
# abcdefghijklmnopqrstuvwXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX <- x

# abcdefghijklmnopqrstuvwXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX <- x
# xor
#                        abcdefghijklmnopqrstuvwXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX <- x >> 23
# v
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTXXXXXXXXXXXXXXXXXX <- y

# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTXXXXXXXXXXXXXXXXXX <- y
# xor
#                        -----------------------xyzABCDEFGHIJKLMNOPQRSTXXXXXXXXXXXXXXXXXX <- y >> 23
# v
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?

# ---

# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?
#                                   abcdefghijklmnopqrstuvwxyzABCD
# abcdefghijklmnopqrstuvwxyzABCDEFGHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# abcdefghijklmnopqrstuvwxyzABCDEFGHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX <- x
#                                   abcdefghijklmnopqrstuvwxyzABCD <- x >> 34
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!? <


def rev(x, k, n):
    if k * 2 >= n:
        return x ^ (x >> k)
    else:
        y = x ^ (x >> (n - k) << (n - k * 2))
        return y ^ ((y >> k) & ((1<<(n-k * 2)) - 1))

from Crypto.Util.number import *
import random

def inv(x):
    MOD = 2**64
    x = rev(x, 23, 64)
    x = inverse(0x49534954445455c9, MOD) * x % MOD
    x = rev(x, 34, 64)
    x = inverse(0x2a636f7468616e2b, MOD) * x % MOD
    x = rev(x, 27, 64)
    return x


cipher = open("cipher.txt_f4c901996df2cc2a767f44dcdbf9b5f4").read().strip()


x = b""
for i in range(0, len(cipher), 16):
    c = int(cipher[i:i+16], 16)
    y = inv(c)
    x += y.to_bytes((y.bit_length() + 7) // 8, "little")

x = bytearray(x)
for i in range(len(x)):
    if x[i] > 0x7f:
        x[i] = 0x20

print(bytes(x))
