from ptrlib import *
from Crypto.Util.number import long_to_bytes

e = 65537

sock = Socket("34.82.101.212", 20001)
# sock = Socket("localhost", 3333)

sock.recvuntil("> ")
sock.sendline("1")
sock.recvuntil("c = ")
c = int(sock.recvline().strip())
sock.recvuntil("n = ")
n = int(sock.recvline().strip())

sock.recvuntil("> ")
sock.sendline(b"2")
sock.recvuntil("c = ")
sock.sendline(str(c).encode())
sock.recvuntil("m = ")
last = int(sock.recvline().strip())


def oracle(c):
    global last
    sock.recvuntil("> ")
    sock.sendline(b"2")
    sock.recvuntil("c = ")
    sock.sendline(str(c).encode())
    sock.recvuntil("m = ")
    m = int(sock.recvline().strip())
    if m != (last * 2) % 3:
        ret = 1
    else:
        ret = 0
    last = m
    return ret


m = lsb_leak_attack(oracle, n, e, c)
print(long_to_bytes(m))
