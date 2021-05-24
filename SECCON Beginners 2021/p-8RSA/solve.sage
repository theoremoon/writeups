from Crypto.Util.number import long_to_bytes


def isqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def fermat(n):
    x = isqrt(n) + 1
    y = isqrt(x * x - n)

    while True:
        w = x * x - n - y * y
        if w == 0:
            break
        elif w > 0:
            y += 1
        else:
            x += 1
    return x + y, x - y


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = egcd(b % a, a)
        return gcd, x - (b // a) * y, y

import random

def eth_root(x, e, p):
    """
    Adleman-Manders-Miller e-th root extraction algorithm in Fp
    x: e-th residue in Fq
    e: exponent (e | p-1)
    p: prime
    """
    assert is_prime(p)
    assert (p - 1) % e == 0
    assert (p - 1) % (e**2) != 0

    l = (p - 1) % (e**2) // e
    a = -inverse_mod(l, e) % e
    return pow(c, (1 + a * (p - 1) // e) // e, p)


def all_roots(known_root, e, p):
    """
    Find all e-th roots in Fp
    known_root: one of e-th root of something
    e: exponent size
    p: prime
    """

    # primitive e-th roots
    proots = set()
    while len(proots) < e:
        proots.add(pow(randint(2, p-1), (p - 1) // e, p))

    # all e-th roots
    roots = set()
    for root in proots:
        roots.add(known_root * root % p)

    return roots




n = 169221770188000341507764005330769042705223611712308424479120192596136318818708135716157255550936563268500310852894489839470320516645317338473018150885997977008925839939560590924435380239519554475266121835753044660177349444503693993991253475530436734034224314165897550185719665717183285653938232013807360458249
e = 17
c = 100233131931360278332734341652304555814094487252151131735286074616555402795190797647001889669472290770925839013131356212574455274690422113278015571750653365512998669453161955302008599029919101244702933443124944274359143831492874463245444294673660944786888148517110942002726017336219552279179125115273728023902

p, q = fermat(n)


cp, cq = c % p, c % q
mqs = all_roots(eth_root(cq, e, q), e, q)
mp = pow(cp, inverse_mod(e, p-1), p)

for mq in mqs:
    m = CRT_list([int(mp), int(mq)], [p, q])
    try:
        mstr = bytes.fromhex(hex(int(m))[2:])
        if b"ctf4b" in mstr:
            print(mstr)
    except:
        pass


