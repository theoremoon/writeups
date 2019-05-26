from flag import FLAG
from Crypto.Util.number import bytes_to_long, getRandomInteger, getPrime


def f(x, coeff):
    y = 0
    for i in range(len(coeff)):
        y += coeff[i] * pow(x, i)
    return y


N = 512
M = 3
secret = bytes_to_long(FLAG)
assert(secret < 2**N)

coeff = [secret] + [getRandomInteger(N) for i in range(M-1)]
party = [getRandomInteger(N) for i in range(M)]

val = map(lambda x: f(x, coeff), party)
output = list(zip(party, val))
print(output)
