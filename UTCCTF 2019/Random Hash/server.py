import sys
import random

for trial in range(20):
	mask = (1<<64)-1
	seed = random.getrandbits(64)
	base = random.getrandbits(64)|1
	def xhash(x):
		h = seed
		for b in x:
			h = ((h+b)*base)&mask
		return h

	a = input('string 1> ')
	b = input('string 2> ')
	if a == b:
		sys.exit(0)
	if xhash(a.encode()) != xhash(b.encode()):
		sys.exit(0)

with open('flag.txt') as f:
	print(f.read().strip())
