data = eval(open("data").read())
size = max(*[d.bit_length() for d in data])

bits = [[0, 0] for _ in range(size)]

for d in data:
    for i in range(size):
        b = (d >> i) & 1
        bits[i][b] += 1

aggr = [
    0 if b[0] > b[1] else 1
    for b in bits
]

x = int("".join(str(a) for a in aggr), 2)
print(bytes.fromhex(hex(x)[2:]))
