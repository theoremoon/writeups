from itertools import product
import string

table = string.printable


def weird_function_1(s):
    return sum([list(map(int,bin(ord(c))[2:].zfill(8))) for c in s], [])

def do_magic(OooO, B):
    return sum(m * b for m, b in zip(weird_function_1(OooO), B))

B = [4267101277, 4946769145, 6306104881, 7476346548, 7399638140, 1732169972, 1236242271, 5109093704, 2163850849, 6552199249, 3724603395, 3738679916, 5211460878, 642273320, 3810791811, 761851628, 1552737836, 4091151711, 1601520107, 3117875577, 2485422314, 1983900485, 6150993150, 2045278518]

cs = [
    34451302951,
    58407890177,
    49697577713,
    45443775595,
    38537028435,
    47069056666,
    49165602815,
    43338588490,
    32970122390,
]
rev = {}

for pat in product(table, repeat=3):
    s = "".join(pat)
    r = do_magic(s, B)
    if r in cs:
        rev[r] = s


for pat in product(table, repeat=2):
    s = "".join(pat)
    r = do_magic(s, B)
    if r in cs:
        rev[r] = s

for pat in product(table, repeat=1):
    s = "".join(pat)
    r = do_magic(s, B)
    if r in cs:
        rev[r] = s

for c in cs:
    print(rev[c], end="")
print()
