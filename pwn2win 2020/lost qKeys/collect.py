from ptrlib import *

bits = []
for _ in range(100):
    sock = Socket("quantum.pwn2.win", 1337)
    sock.sendlineafter("passwd:\n", "0")
    b = int(sock.recvline(), 16)
    bits.append(b)
    sock.close()
print(bits)
