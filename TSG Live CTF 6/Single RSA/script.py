from Crypto.Util.number import getStrongPrime, bytes_to_long

p = getStrongPrime(1024)
N = p
phi = p - 1
e = 0x10001
d = pow(e, -1, phi)

with open('flag.txt', 'rb') as f:
    flag = bytes_to_long(f.read())

c = pow(flag, e, N)
print(f'N = {N}')
print(f'e = {e}')
print(f'c = {c}')

