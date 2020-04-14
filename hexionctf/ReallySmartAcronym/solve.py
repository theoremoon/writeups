from ptrlib import *

e = 65537

sock = Socket("challenges1.hexionteam.com", 5000)
sock.recvuntil(":")
c = int(sock.recvline().decode())

sock.recvuntil("=> ")
sock.sendline("-1")
n = int(sock.recvline().decode()) + 1

def lsb_oracle(c):
    sock.recvuntil("> ")
    sock.sendline(str(c))
    return int(sock.recvline().decode()) == 1

print(lsb_leak_attack(lsb_oracle, n, e, c))

