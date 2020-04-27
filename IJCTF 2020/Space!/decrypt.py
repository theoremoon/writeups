from Crypto.Cipher import AES
from hashlib import md5
from base64 import *
import string

k1, k2 =  (b'kh\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'7w\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
k3, k4 =  (b'Y5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'aX\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
keys = [k1, k2, k4, k3]

cipher = b64decode(b"N2YxBndWO0qd8EwVeZYDVNYTaCzcI7jq7Zc3wRzrlyUdBEzbAx997zAOZi/bLinVj3bKfOniRzmjPgLsygzVzA==")
# cipher = b64decode(b"NeNpX4+pu2elWP+R2VK78Dp0gbCZPeROsfsuWY1Knm85/4BPwpBNmClPjc3xA284")
iv = md5(b"ignis").digest()

for k in keys[::-1]:
    aes = AES.new(key=k, mode=AES.MODE_CBC, IV=iv)
    cipher = aes.decrypt(cipher)
    print(repr(cipher))
