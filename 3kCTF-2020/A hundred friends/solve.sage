# https://raw.githubusercontent.com/pwang00/Cryptographic-Attacks/master/Public%20Key/RSA/hastad.sage
"""
Sage implementation of Hastad's broadcast attack for small public exponent and multiple message/ciphertext pairs
"""

import binascii
import random


def linear_padding(ciphertexts, moduli, pad_array, const_array=(), e=3, eps=1/8):
#     if not(len(ciphertexts) == len(moduli) == len(pad_array) == len(const_array) == e):
#         raise RuntimeError("Moduli and ciphertext arrays have to be equal in length, and contain at least as many elements as e")
 
    '''
    Initialization with placeholders
    ciphertexts: ciphertext array
    T_array: Chinese Remainder Theorem coefficients
    moduli: Modulus array
    pad_array: Linear coefficient of padding applied to the message during encryption
    const_array: constant pad added to message during encryption (optional)
    '''

    n = len(ciphertexts)

    T_array = [Integer(0)]*n
    crt_array = [Integer(0)]*n
    polynomial_array = []

    for i in range(n):
        crt_array = [0]*n
        crt_array[i] = 1
        T_array[i] = Integer(crt(crt_array,moduli))

    G.<x> = PolynomialRing(Zmod(prod(moduli)))
    for i in range(n):
        polynomial_array += [T_array[i]*((pad_array[i]*x+const_array[i])^e - Integer(ciphertexts[i]))] #Representation of polynomial f(x) = (A*x + b) ^ e - C where (A*x + b) is the padding polynomial

    g = sum(polynomial_array).monic()  #Creates a monic polynomial from the sum of the individual polynomials
    roots = g.small_roots(epsilon=eps)
    return roots[0] if len(roots) >= 1 else -1



# def test_linear_padding():
#     moduli = []
#     ciphertexts = []
#     pad_array = []
#     const_array = []
#     e = 3
#     pad_bound = 2^512
#     prime_bound = 2^1024
#     m = int.from_bytes(b"p00rth0_th3_p00r", "big")
# 
#     for i in range(e):
#         pad = 1 # random.randint(0,pad_bound)
#         constant = random.randint(0,pad_bound)
#         pad_array += [pad]
#         const_array += [constant]
#         p = random_prime(prime_bound,proof=false)
#         q = random_prime(prime_bound,proof=false)
#         n = p*q
#         moduli += [n]
#         ciphertexts.append(pow(pad * m + constant,e,n))
# 
#     print(linear_padding(ciphertexts, moduli, pad_array, const_array))
#     return 0

import json
from random import sample

with open("params.json", "r") as f:
    params = json.load(f)

for i in range(1000):
    ns = []
    cs = []
    alist = []
    blist = []
    es = []
    e = 3
    paramlist = sample(params, k=5)
    for param in paramlist:
        ns.append(param["n"])
        cs.append(param["c"])
        alist.append(1)
        blist.append(param["pad"])

    res = linear_padding(cs,ns,alist,blist,e=e)
    if res == -1:
        print("NOT FOUND ({})".format(i),es)
    else:
        print(res)
        break
