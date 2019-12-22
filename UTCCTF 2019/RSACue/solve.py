from Crypto.PublicKey import RSA
from Crypto.Util.number import *
from crypto_commons.generic import fermat_factors
from base64 import b64decode

rsa = RSA.importKey(open("publickey.pem").read())
p, q = fermat_factors(rsa.n)
e = rsa.e
d = inverse(e, (p - 1) * (q - 1))

c = b64decode(open("ciphertext").read().replace("\n", ""))
c = bytes_to_long(c)

m = pow(c, d, rsa.n)
print(long_to_bytes(m))
