#!/usr/bin/python3
from Crypto.Random.random import getrandbits
from base64 import b64decode, b64encode
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import flag

BITS = 220

def shift(n,i):
    n1=(n<<i)%0x800
    n2=(n>>(11-i))
    return n1^n2


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

def challenge():
    goal = HashGenerate(getrandbits(BITS))
    print("Hash : %s [0/5]" % hex(goal))
    answer = []
    for i in range(1, 6):
        data = b64decode(input("data : "))
        value = bytes_to_long(data)
        result = HashGenerate(value)
        if (result!= goal) or (value in answer):
            exit(0)
        answer.append(value)
        print("Hash : %s [%d/5]" % (hex(goal), i))
    print("\nGood!\n")


if __name__ == '__main__':
    print("Can you make a hash like this?\n")
    stage = 1
    while stage <= 10:
        print("============================================")
        print("                  Stage %d" % stage)
        print("============================================")
        try: 
            challenge()
            stage+=1
        except:
            print("Nop")
            exit(0)
    print(flag)

