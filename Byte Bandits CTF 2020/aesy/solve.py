from ptrlib import *
from binascii import hexlify

sock = Socket("crypto.byteband.it", 7004)
sock.recvuntil("choice:\n")
sock.sendline("3")
sock.recvuntil(":\n")
ciphertext = bytes.fromhex(sock.recvline().decode())
iv, ciphertext = ciphertext[:16], ciphertext[16:]

def oracle(c):
    print(repr(c))
    sock.recvuntil(":\n")
    sock.sendline("2")
    sock.sendline(hexlify(c))
    sock.recvuntil("Alice: ")
    m = sock.recvline().decode()
    if "Got your message!!" in m:
        return True
    print(repr(m))
    return False

print(padding_oracle(oracle, ciphertext, bs=16, iv=iv))

