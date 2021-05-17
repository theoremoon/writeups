from Crypto.Util.number import getPrime, bytes_to_long
from math import prod

primes = [getPrime(1024 // 128) for i in range(128)]
N = prod(primes)
phi = prod(p - 1 for p in primes)
e = 0x10001
d = pow(e, -1, phi)

with open('flag.txt', 'rb') as f:
    flag = bytes_to_long(f.read())

c = pow(flag, e, N)
print(f'N = {N}')
print(f'e = {e}')
print(f'c = {c}')

assert(pow(c, d, N) == flag)
