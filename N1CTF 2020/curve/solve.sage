from ptrlib import Socket, brute_force_attack, brute_force_pattern
import hashlib, string
import re

# http://mslc.ctf.su/wp/polictf-2012-crypto-500/
def hensel_lift(curve, p, point):
    A, B = map(int, (E.a4(), E.a6()))
    x, y = map(int, point.xy())

    fr = y**2 - (x**3 + A*x + B)
    t = (- fr / p) % p
    t *= inverse_mod(2 * y, p)  # (y**2)' = 2 * y
    t %= p
    new_y = y + p * t
    return x, new_y

def sssa_attack(E, g, v, p):
    x1, y1 = g.xy()
    x2, y2 = v.xy()
    if 0:
        # Hensel lift can preserve the curve
        x1, y1 = hensel_lift(E, p, g)
        x2, y2 = hensel_lift(E, p, v)
    else:
        # we can calso lift by adding random multiple of p
        # just need to compute new curve
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)+p
        y2 = int(y2)+p

    # calculate new A, B (actually, they will be the same here)
    mod = p ** 2

    A2 = y2**2 - y1**2 - (x2**3 - x1**3)
    A2 = A2 * inverse_mod(x2 - x1, mod)
    A2 %= mod

    B2 = y1**2 - x1**3 - A2 * x1
    B2 %= mod

    # new curve
    E2 = EllipticCurve(IntegerModRing(p**2), [A2, B2])

    # calculate dlog
    g2s = (p - 1) * E2(x1, y1)
    v2s = (p - 1) * E2(x2, y2)

    x1s, y1s = map(int, g2s.xy())
    x2s, y2s = map(int, v2s.xy())

    dx1 = (x1s - x1) // p
    dx2 = (x2s - x2) // p
    dy1 = (y1s - y1)
    dy2 = (y2s - y2)

    m = (dy1 * inverse_mod(dx1, p) % p) * (dx2 * inverse_mod(dy2, p) % p) % p
    return m



P = 11093300438765357787693823122068501933326829181518693650897090781749379503427651954028543076247583697669597230934286751428880673539155279232304301123931419
A = 490963434153515882934487973185142842357175523008183292296815140698999054658777820556076794490414610737654365807063916602037816955706321036900113929329671
B = 7668542654793784988436499086739239442915170287346121645884096222948338279165302213440060079141960679678526016348025029558335977042712382611197995002316466

# F = FiniteField(P)
# EC = EllipticCurve(F, A, B)
F = GF(P)
EC = EllipticCurve(F, [A, B])
q = 11093300438765357787693823122068501933326829181518693650897090781749379503427651954028543076247583697669597230934286751428880673539155279232304301123931419
Gx, Gy = 3625919638993368116712722653537836360205467638660460537383904776747654152570720347805947618600786655716075512037422494054570126589477523390586846553421898, 8091311603673854111398603022147605529578092076570314705936204260089129024440183796062158051191844155110792343378466956735150763083256102150854507631124416
G = EC(Gx,Gy)


table = string.ascii_letters + string.digits

sock = Socket("47.242.140.57", 9998)
prefix, digest = sock.recvregex(r"sha256\(([^+]+)\+XXXX\) == ([0-9a-f]+)")
print(prefix, digest)
digest = digest.decode()
for p in brute_force_attack(4, table_len=len(table)):
    xxxx = brute_force_pattern(p, table=table).encode()

    if hashlib.sha256(prefix + xxxx).hexdigest() == digest:
        break

sock.sendline(xxxx)

print("[+] PoW done")

sock.sendlineafter("P: ", str(P))
sock.sendlineafter("A: ", str(A))
sock.sendlineafter("B: ", str(B))
sock.sendlineafter("X1: ", str(Gx))
sock.sendlineafter("Y1: ", str(Gy))
sock.sendlineafter("X2: ", str(Gx))
sock.sendlineafter("Y2: ", str(Gy))


print("[+] Parameter Sent")




for i in range(30):
    print("[+] ROUND {}".format(i + 1))
    g0x, g0y, g1x, g1y, cx, cy = map(int, sock.recvregex(r"\(([0-9]+) : ([0-9]+) : 1\) \(([0-9]+) : ([0-9]+) : 1\) \(([0-9]+) : ([0-9]+) : 1\)"))
    g0 = EC(g0x, g0y)
    g1 = EC(g1x, g1y)
    c = EC(cx, cy)

    a0 = sssa_attack(EC, G, g0, P)
    a1 = sssa_attack(EC, G, g1, P)
    c = sssa_attack(EC, G, c, P)
    # a0 = SSSA_Attack(F, EC, G, g0)
    # a1 = SSSA_Attack(F, EC, G, g1)
    # c = SSSA_Attack(F, EC, G, c)

    if (a0 * a1) % q == c:
        sock.sendline("0")
    else:
        sock.sendline("1")


sock.interactive()
