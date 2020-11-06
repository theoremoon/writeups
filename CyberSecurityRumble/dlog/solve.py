from ptrlib import Socket
from Crypto.Util.number import inverse

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f

sock = Socket("chal.cybersecurityrumble.de", 31782)
sock.sendlineafter("x: ", "1")
sock.sendlineafter("y: ", "1")
Q = list(map(int, sock.recvregex(r"Point\(([0-9]+),([0-9]+)\)")))

Fp = 1 * inverse(1, p) % p
Fq = Q[0] * inverse(Q[1], p)  %p

d = Fq  *inverse(Fp, p) % p
sock.sendlineafter("now gif secret: ", str(d))

print(sock.recv())
