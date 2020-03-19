from ptrlib import *
from base64 import b64decode
import string
import random
import time


def otp(a, b):
    r = ""
    for i, j in zip(a, b):
        r += chr(ord(i) ^ ord(j))
    return r


def genSample():
    p = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for _ in range(random.randint(1, 30))])
    k = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for _ in range(len(p))])
    
    x = otp(p, k)
    
    return x.encode(), p, k


sock = Socket("misc.2020.chall.actf.co", 20301)
t = int(time.time()) - 50
random.seed(t)

sock.recvuntil("> ")
sock.sendline("2")
y = b64decode(sock.recvline())
x, p, k = genSample()
count = 0
while x != y:
    t += 1
    count += 1
    random.seed(t)
    x, p, k = genSample()
    if count > 100:
        print(":(")
        exit()
sock.recvuntil("answer: ")
sock.sendline(p)
print(sock.recvline())



