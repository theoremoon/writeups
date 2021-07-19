from itertools import combinations
# parameters of secp224r1
secp224r1_p = 0xffffffffffffffffffffffffffffffff000000000000000000000001
K = GF(secp224r1_p)
a = K(0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe)

used_mod = set()
modulus = 1
values = []

secp256r1_p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
secp256r1_K = GF(secp256r1_p)
secp256r1_a = secp256r1_K(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc)
secp256r1_b = secp256r1_K(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
secp256r1_E = EllipticCurve(secp256r1_K, (secp256r1_a, secp256r1_b))
secp256r1_G = secp256r1_E(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
secp256r1_E.set_order(0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 * 0x1)

while modulus < secp224r1_p:
    b = randint(0, secp224r1_p-1)
    EC = EllipticCurve(GF(secp224r1_p), [a, b])
    P = EC.random_point()
    try:
        alarm(10)

        order = int(P.order())
        factors = factor(order, limit=20000)
        cancel_alarm()
    except AlarmInterrupt:
        continue


    for f, _ in factors:
        if f in used_mod:
            continue
        if not 1000 < f < 10000:
            continue

        used_mod.add(f)

        Q = (order // f) * P
        qx, qy =  Q.xy()
        qx, qy = int(qx), int(qy)

        if qy == 0:
            continue

        px, py = secp256r1_E.random_point().xy()
        px, py = int(px), int(py)

        x = CRT_list([px, qx], [secp256r1_p, secp224r1_p])
        y = CRT_list([py, qy], [secp256r1_p, secp224r1_p])

        modulus *= f
        values.append((int(x),int(y), int(b), int(f)))
        print(f, len(values), modulus)

import json
with open("values.json", "w") as f:
    json.dump(values, f)
