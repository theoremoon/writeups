from base64 import b64decode
from ptrlib import chunks

def guess_state(xs, a, b, m):
    # s1 = a*s0 + b
    # s2 = a^2*s0 + ab + b
    # s3 = a^3*s0 + aab + ab + b
    # s4 = a^4*s0 + aaab + aab + ab + b

    n = len(xs)
    ks = [b]
    for i in range(1, n):
        ks.append(ks[i-1] + a^i * b)

    xxs = [(xs[i] << 48) - ks[i]  for i in range(n)]

    L = matrix(ZZ, n, 1, [m] + [a^i for i in range(1, n)])
    L = L.augment(matrix.identity(n)[:,1:] * -1)
    B = L.LLL()
    print(list(B))

    xB = B * vector(xxs)
    k = [round(x/m) for x in xB]
    yys = B.solve_right(vector(k) * m - xB)
    print(yys)

    s1 = (xs[0] << 48) + yys[0]
    s0 = (s1 - b) * inverse_mod(a, m) % m
    return s0

class LCG():
    def __init__(self, a, c, mod, seed):
        self.a = a
        self.c = c
        self.mod = mod
        self.seed = seed

    def next(self):
        self.seed = (self.seed * self.a + self.c) % self.mod
        return self.seed



discards = b64decode(b"GY2Usw+rJFXeslhLRO2QGnycljYrCNI/9d/pE4QvNzdu8aPXbFFup+wm6Ek2f0Ukno2DD2ojA/xNuuGdRyWSjgdY")
flag =  b64decode(b"jOjbAU0Bv7ErwBbR5zIIxYs9gL1rx+r4AVEvIgIZq6g5Kxyth6aH3pscIrA0PP6JD9hLeLLBjb0hngaW")
flag = [int.from_bytes(d, "little") for d in chunks(flag, 6)]

outputs = [int.from_bytes(d, "little") for d in chunks(discards, 6)]
a = 0xb65ecaa9cd047b44ad4bf6d4
p = 0xd95f16886f9b2c8d7bcdb96b
s = guess_state(outputs, a, 0, p)

lcg = LCG(a, 0, p, s)
outputs = []

plain = b""
for i in range(len(flag)):
    key = lcg.next() % (2**48)
    f = int(flag[i] ^^ key)
    plain += f.to_bytes(6, "little")

print(plain)
