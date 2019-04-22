import random
import itertools

# from flag import flag

def decrypt(msg, perm):
    W = len(perm)
    res = [[None for _ in range(W) ] for _ in range(len(msg) // W)]

    for j in xrange(len(msg) // W):
        for k in range(W):
            res[j][perm[k]] = msg[0]
            msg = msg[1:]

    res = "".join([ "".join(c) for c in res ])
    a, b = res[-2:], res[:-2]
    for x, y in zip(b[:len(b)//2], b[len(b)//2:]):
        a += y + x
    return a


def encrypt(msg, perm):
	W = len(perm)
	while len(msg) % (2*W):
		msg += "."
	msg = msg[1:] + msg[:1]
	msg = msg[0::2] + msg[1::2]
	msg = msg[1:] + msg[:1]
	res = ""
	for j in xrange(0, len(msg), W):
		for k in xrange(W):
			res += msg[j:j+W][perm[k]]
	msg = res
	return msg

def encord(msg, perm, l):
	for _ in xrange(l):
		msg = encrypt(msg, perm)
	return msg

W, l = 7, random.randint(0, 1337)
perm = range(W)
for v in itertools.permutations(perm):
    flag = open("flag.enc", "r").read()

    for i in range(1337):
        flag = decrypt(flag, v)
        print(flag)
# f = open('flag.enc', 'w')
# f.write(enc)
# f.close()
