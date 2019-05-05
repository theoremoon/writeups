exec(open("primes").read())
exec(open("flag.enc").read())

from Crypto.Util.number import *

print(len(primes))
for prime in primes:
    p, q = prime
    phi = (p - 1) * (q - 1)
    d = inverse(E, phi)
    m = pow(C, d, N)
    print(long_to_bytes(m))
