p = 43753
PR.<y> = PolynomialRing(GF(p))

_, N, C = open("polynomial_rsa.txt").read().split("\n")

N = sage_eval(N.split(":")[1], locals=vars())

(P, _), ( Q, _ ) = N.factor()
n, m = P.degree(), Q.degree()
e = 65537
s = (p^n - 1)*(p^m - 1)
d = inverse_mod(e, s)

S.<x> = PR.quotient(N)
C = sage_eval(C.split(":")[1], locals=vars())

M = C^d
print("".join([chr(c) for c in M.list()]))

