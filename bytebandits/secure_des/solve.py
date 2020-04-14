from ptrlib import *
from base64 import *
from Crypto.Util.number import *
from Crypto.Cipher import DES

# Source: https://codereview.stackexchange.com/q/43210
def legendre_symbol(a, p):
	"""
	Legendre symbol
	Define if a is a quadratic residue modulo odd prime
	http://en.wikipedia.org/wiki/Legendre_symbol
	"""
	ls = pow(a, (p - 1)//2, p)
	if ls == p - 1:
		return -1
	return ls


# Source: https://codereview.stackexchange.com/q/43210
def prime_mod_sqrt(a, p):
	"""
	Square root modulo prime number
	Solve the equation
		x^2 = a mod p
	and return list of x solution
	http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
	"""
	a %= p

	# Simple case
	if a == 0:
		return [0]
	if p == 2:
		return [a]

	# Simple case
	if p % 4 == 3:
		x = pow(a, (p + 1)//4, p)
		return [x, p-x]


def unpow(a, p):
	for _ in range(15):
		a = prime_mod_sqrt(a, p)
		a = a[0]
	return [int(x) for x in prime_mod_sqrt(a, p)]

def decrypt(key, l, ciphertext):
	keys = []
	for i in range(128):
		keys.append(key[l[i]:l[i]+8])


	keys = list(reversed(keys))
	for i in range(128):
		cipher = DES.new(keys[i], DES.MODE_ECB)
		ciphertext = cipher.decrypt(ciphertext)

	return ciphertext

def main():
	sock = Socket("crypto.byteband.it", 7001)
	sock.recvuntil("> ")
	sock.sendline("2")
	p = int(sock.recvline()[2:], 16)
	l2 = eval(sock.recvline().decode())
	l1 = []
	key = b""
	for l in l2:
		x = unpow(int(l[2:], 16), p)
		x = min(*x)
		x = long_to_bytes(x)
		l1.append(bytes_to_long(x[8:]))
		key += x[:8]
	sock.recvuntil("> ")
	sock.sendline("3")
	cipher = b64decode(sock.recvline())
	print(decrypt(key, l1, cipher))
main()


