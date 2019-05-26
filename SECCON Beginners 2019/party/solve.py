from z3 import *

M = 3


def f(x, coeff):
    y = 0
    for i in range(len(coeff)):
        y += coeff[i] * pow(x, i)
    return y


s = Solver()
coeff = [Int("x:{}".format(i)) for i in range(M)]
for c in coeff:
    s.add(0 < c)
    s.add(c < (1 << 512))

encrypted = eval(open("encrypted", "r").read())
for x in encrypted:
    s.add(f(x[0], coeff) == x[1])

r = s.check()
if r == sat:
    m = s.model()
    print(m)
else:
    print(r)
    exit()
