exec(open("flag.enc").read())

K = 1 << 4095

kouhos = [[0, 0]]
count = 4095
while K > 0:
    next_kouho = set()
    for kouho in kouhos:
        P, Q = kouho
        p = P | K
        q = Q | K
        if X & K:
            if p * Q <= N:
                next_kouho.add((p, Q))
            if P * q <= N:
                next_kouho.add((P, q))
        else:
            if p * q <= N:
                next_kouho.add((p, q))
            else:
                next_kouho.add((P, Q))
    assert len(next_kouho) > 0

    kouhos = []
    for n in next_kouho:
        P, Q = n
        p = P | (K - 1)
        q = Q | (K - 1)
        if p * q >= N and P * Q <= N:
            kouhos.append(n)

    print(count, len(kouhos))
    count -= 1
    K >>= 1

print(kouhos)
