from Crypto.Util.number import *
from socket import socket, AF_INET, SOCK_STREAM

def read_data():
    return int(file.readline().decode().strip())

def send_data(x):
    file.write(str(x).encode() + b'\n')
    file.flush()

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('34.87.174.144', 9999))
file = sock.makefile('rwb')
n = read_data()
e = 65537
c = read_data()
M = 2020

def oracle(x):
    send_data(x)
    return read_data()

i = 1
z = oracle(c)
while True:
    inv = inverse(pow(M, i, n), n)
    c2 = (c * pow(inv, e, n)) % n

    ith_z = (oracle(c2) - (z * inv) % n) % M
    z = ith_z * (M ** i) + z
    i += 1
    print(f"[+] {i}")

    if pow(z, e, n) == c:
        break

while True:
    send_data(z)
    line = file.readline()
    print(line)
    if len(line) == 0:
        break
