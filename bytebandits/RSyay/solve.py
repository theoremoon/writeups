from ptrlib import *
from base64 import *
from binascii import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

sock = Socket("crypto.byteband.it", 7002)
cnt = 0
while True:
    cnt += 1
    if cnt >= 33:
        break

    print(cnt)
    sock.recvuntil("(b64encoded) :")
    m = b64decode(sock.recvline().strip())
    print("[+]m:", repr(m))

    sock.recvline()
    x = int(sock.recvline().strip().decode(), 16)
    n = (x - 1) // 4
    print("[+]n:", n)
    key = RSA.construct((n, 65537))
    cipher = PKCS1_OAEP.new(key)
    c = cipher.encrypt(m)
    sock.recvuntil("(b64encoded) :")
    sock.sendline(b64encode(c))
    print(sock.recvline())

sock.interactive()
