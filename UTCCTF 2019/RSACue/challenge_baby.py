from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import gmpy2
from flag import m

p = getPrime(1024)
while True:
	p1 = gmpy2.next_prime(p)
	if p1-p == 2:
		q = p1
		break
	else:
		p = p1

n = p*q
e = 65537
pub = RSA.construct((long(n), long(e)))
f = open('publickey.pem', 'w')
f.write(pub.exportKey())
f.close()
key = PKCS1_v1_5.new(pub)
ct = key.encrypt(m).encode('base64')
f1 = open('ciphertext', 'w')
f1.write(ct)
f1.close()

