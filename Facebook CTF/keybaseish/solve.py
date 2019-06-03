from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime
from Crypto import Random

RSAkey = RSA.generate(1024)
key_params = RSAkey.__getstate__()
sign = 43522081190908620239526125376626925272670879862906206214798620592212761409287968319160030205818706732092664958217053982767385296720310547463903001181881966554081621263332073144333148831108871059921677679366681345909190184917461295644569942753755984548017839561073991169528773602380297241266112083733072690367

pin = int(input().strip())
n = getPrime(pin.bit_length() + 1)
for i in range(2, n):
    x = pow(sign, i, n)
    if x == pin:
        print(x)
        print("{}:{}".format(i, n))
        exit()
