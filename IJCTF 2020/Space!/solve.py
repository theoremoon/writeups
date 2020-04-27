from Crypto.Cipher import AES
from hashlib import md5
from base64 import *
import string

message = b"Its dangerous to solve alone, take this" + b"\x00"*9 
cipher = b64decode(b"NeNpX4+pu2elWP+R2VK78Dp0gbCZPeROsfsuWY1Knm85/4BPwpBNmClPjc3xA284")

iv = md5(b"ignis").digest()
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits

table = {}

for i, c1 in enumerate(alphabet):
    print(f"[+] {i+1}/{len(alphabet)}")
    for c2 in alphabet:
        k1 = (c1 + c2).encode() + b"\0" * 14
        aes1 = AES.new(key=k1, mode=AES.MODE_CBC, IV=iv)
        cipher1 = aes1.encrypt(message)
        for c3 in alphabet:
            for c4 in alphabet:
                k2 = (c3 + c4).encode() + b"\0" * 14
                aes2 = AES.new(key=k2, mode=AES.MODE_CBC, IV=iv)
                cipher2 = aes2.encrypt(cipher1)

                table[cipher2] = (k1, k2)


for i, c1 in enumerate(alphabet):
    print(f"[+] {i+1}/{len(alphabet)}")
    for c2 in alphabet:
        k1 = (c1 + c2).encode() + b"\0" * 14
        aes1 = AES.new(key=k1, mode=AES.MODE_CBC, IV=iv)
        message1 = aes1.decrypt(cipher)
        for c3 in alphabet:
            for c4 in alphabet:
                k2 = (c3 + c4).encode() + b"\0" * 14
                aes2 = AES.new(key=k2, mode=AES.MODE_CBC, IV=iv)
                message2 = aes2.decrypt(message1)

                if message2 in table:
                    print("k1, k2: ", table[message2])
                    print("k3, k4: ", (k1, k2))

