import ast
with open("output.txt") as f:
    pubkey = ast.literal_eval(f.readline().strip().split(" = ")[1])
    cipher = ast.literal_eval(f.readline().strip().split(" = ")[1])


b = pubkey
c = cipher

# check the density
n = len(b)
d = float(n / log(max(b), 2))
print(d)
# assert(d < 0.9048)

# low-density attack, CLOS method
# prepare a basis
MULTIPLIER = 100
B = matrix(ZZ, n + 1, n + 1)
B.set_block(0, 0, MULTIPLIER * matrix(n, 1, b))
B.set_block(n, 0, MULTIPLIER * matrix([-c]))
B.set_block(0, 1, 2 * identity_matrix(n))
B.set_block(n, 1, matrix([-1] * n))

# LLL algorithm
for x in B.LLL():
    # print(x)
    if x[0] == 0 and all((x_i in [-1, +1]) for x_i in x[1:]):
        print('x={}'.format(x))

        # decode x
        m = 0
        for x_i in x:
            m *= 2
            m += int(x_i == +1)
        print(bytes.fromhex(hex(m)[2:]))

