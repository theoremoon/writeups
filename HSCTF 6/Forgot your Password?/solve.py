from z3 import *


def chr2bin(s):
    data = 0
    for c in s:
        data <<= 8
        data += ord(c)
    return data


def next(x, y):
    xx = RotateLeft(x, 55) ^ ((x ^ y) ^ ((x ^ y) << 14))
    yy = RotateLeft(x ^ y, 36)
    return xx & 0xFFFFFFFFFFFFFFFF, yy & 0xFFFFFFFFFFFFFFFF


X, Y = BitVecs("x y", 64)

s = Solver()
s.add(X + Y == chr2bin("hsctfiss"[::-1]))
X2, Y2 = next(X, Y)
s.add(X2 + Y2 == chr2bin("ocoolwow"[::-1]))

r = s.check()
print(r)
if r != sat:
    exit()
m = s.model()
x = m[X].as_long()
y = m[Y].as_long()
print([x, y])

for i in range(6):
    X, Y = BitVecs("x y", 64)

    s = Solver()
    X2, Y2 = next(X, Y)
    s.add(X2 == x)
    s.add(Y2 == y)

    r = s.check()
    if r != sat:
        exit()
    m = s.model()
    x = m[X].as_long()
    y = m[Y].as_long()
    print([x, y])
