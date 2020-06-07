from z3 import *

def PIE(i, A, B, C):
    if i<16:
        return (A&B)|((~A)&C)
    return (A&B)|(B&C)|(C&A)

def pie(j):
    if(j<16): return j
    elif(j==16): return 0
    elif(j==17): return 4
    elif(j==18): return 8
    elif(j==19): return 12
    elif(j==20): return 1
    elif(j==21): return 5
    elif(j==22): return 9
    elif(j==23): return 13
    elif(j==24): return 2
    elif(j==25): return 6
    elif(j==26): return 10
    elif(j==27): return 14
    elif(j==28): return 3
    elif(j==29): return 7
    elif(j==30): return 11
    else: return 15

def shift(n,i):
    n1=(n<<i)%0x800
    n2=(n>>(11-i))
    return n1^n2


def HashGenerate(value):
    n = 3
    s = [3]*16 + [7]*16
    Q = [0]*36
    m = [0]*16
    X = []
    for i in range(0,20):
        X.insert(0, value&0x7ff)
        value >>=11
        
    for i in range(-3, 1, 1):
        Q[n+i]=X[i+3]
    for i in range(0,16):
        m[i]=X[i+4]
    for i in range(0, 32):
        Q[n+i+1]=shift(( (Q[n+i-3] + PIE(i,Q[n+i],Q[n+i-1],Q[n+i-2]) + m[pie(i)])%0x800 ), s[i]) 

    Y = []
    for i in range(0,4):
        Y.append((Q[n+i-3] + Q[32+i])%0x800)

    Y[1]=(Y[0]<<33)^(Y[1]<<22)
    Y[0]=Y[2]<<11
    Y[1]^=Y[0]^Y[3]

    return Y[1]

def crack(h):
    n = 3
    for t in range(1 << 11):
        tt = (t << 33) | (h & ((1 << 33) - 1))
        value = tt  << (220 - 44)

        x = value
        Q = [0]*36
        m = [0]*16

        X = []
        for i in range(0,20):
            X.insert(0, value&0x7ff)
            value >>=11
        for i in range(-3, 1, 1):
            Q[n+i]=X[i+3]
        for i in range(0,16):
            m[i]=X[i+4]

        for i in range(0, 4):
            P = PIE(i, Q[n+i], Q[n+i-1], Q[n+i-2])
            m[i] = 0x800 - P - Q[n+i-3]
            while m[i] < 0:
                m[i] += 0x800
            x |= (m[i] << (165 - 11 * i))

        h2 = HashGenerate(x)
        if h2 == h:
            return x


from ptrlib import *
from Crypto.Random.random import getrandbits
from base64 import b64decode, b64encode
from Crypto.Util.number import long_to_bytes, bytes_to_long

sock = Socket("hash-chungdol.ctf.defenit.kr", 8960)
for _ in range(10):
    h = int(sock.recvlineafter("Hash : ").split(b" ")[0], 16)
    r = crack(h)
    for i in range(1, 6):
        exploit = r | (i << 220)
        sock.sendlineafter("data : ", b64encode(long_to_bytes(exploit)))
        print(sock.recvline())
    print(sock.recvline())
sock.interactive()

