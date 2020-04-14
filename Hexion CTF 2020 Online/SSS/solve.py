from sage.all import *
from ptrlib import *
from Crypto.Util.number import *

P = 2**521 - 1

sock = Socket("challenges1.hexionteam.com", 5001)
xs = []
ys = []
for i in range(0x42):
    sock.recvuntil(">>> ")
    x = bytes_to_long(str(i).encode())
    sock.sendline(str(i))
    y = int(sock.recvline().decode())
    xs.append(x)
    ys.append(y)
    print((x, y))

F = GF(P)
PR = PolynomialRing(F, name="x")
shares = [(F(x), F(y))for x, y in zip(xs, ys)]
for size in range(0x30, 0x41):
    secret = list(PR.lagrange_polynomial(shares[:size]))[0]
    h = hex(secret)
    if len(h) % 2 != 0:
        continue
    print(bytes.fromhex(h[2:]))
