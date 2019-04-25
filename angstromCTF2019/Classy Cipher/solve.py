# from secret import flag, shift
# 
def encrypt(d, s):
	e = ''
	for c in d:
		e += chr((ord(c)+s) % 0xff)
	return e

# assert encrypt(flag, shift) == ':<M?TLH8<A:KFBG@V'

a = ':<M?TLH8<A:KFBG@V'
for i in range(256):
    print(encrypt(a, i))

