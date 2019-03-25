from Crypto.PublicKey import RSA
from base64 import b64decode
from factordb.factordb import FactorDB
import fractions

keys = []
for i in range(101):
    lines = open("pub{}.pem".format(i)).read().splitlines()
    der = b64decode(''.join(lines[1:-1]))
    rsa = RSA.importKey(der)
    keys.append(rsa)

for x in keys:
    for y in keys:
        if x.n != y.n and fractions.gcd(x.n, y.n) != 1:
            print(x.n, y.n, fractions.gcd(x.n, y.n))
