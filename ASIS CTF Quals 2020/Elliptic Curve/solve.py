from sage.all import *
from ptrlib import *
import proofofwork


while True:
    sock = Socket("76.74.178.201", 9531)
    shax, h, l= sock.recvregex(r"that ([^ ]+?)\(X\)\[-6:\] = ([0-9a-f]{6}) and len\(X\) = (.+)")
    h = h.decode()
    print(shax, h, l)
    if shax == b'sha1':
        s = proofofwork.sha1('?' * (40 - 6) + h, text=b'?' * int(l))
    elif shax == b'md5':
        s = proofofwork.md5('?' * (32 - 6) + h, text=b'?' * int(l))
    elif shax == b'sha256':
        s = proofofwork.sha256('?' * (64 - 6) + h, text=b'?' * int(l))
    else:
        sock.close()
        continue
    break
sock.sendline(s)

x, y = [int(x) for x in sock.recvregex(r"P = \(([0-9]+), ([0-9]+)\)")]
s = int(sock.recvregex(r"Send the ([0-9]+) \* P")[0])

origx = x
print("x = {}, y = {}, s = {}".format(x, y, s))
# find p
if is_prime(x + 1):
    p = x + 1
elif is_prime(x):
    p = x
    x = x - 1
elif is_prime(x - 1):
    p = x - 1
    x = x - 2
else:
    assert False

# find a
_, a = PolynomialRing(GF(p), "a").objgen()
f = 3 * x**2 + 3*x + 1 + a
a = int(f.roots()[0][0])

# find b
_, b = PolynomialRing(GF(p), "b").objgen()
f = x**3 + a*x + b - y**2
b = int(f.roots()[0][0])


EC = EllipticCurve(GF(p), [a, b])
print("p = {}, a = {}, b = {}".format(p, a, b))

# check
P = EC((x, y))
P = EC((x+1, y))
P = EC((x+2, y))

P = EC((origx, y))
Q = (s * P).xy()

sock.sendline("({}, {})".format(*Q))
sock.interactive()
