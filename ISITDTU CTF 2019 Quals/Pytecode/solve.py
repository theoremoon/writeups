from z3 import *

flag = [Int("x%d" % i) for i in range(30)]
solver = Solver()

for f in flag:
    solver.add(0x20 <= f, f <= 0x7F)

solver.add(flag[0] + 52 == flag[-1])
solver.add(flag[-1] - 2 == flag[7])
for i, c in enumerate("ISITDTU"):
    solver.add(flag[i] == ord(c))

solver.add(flag[9] == flag[14])
solver.add(flag[19] == flag[14])
solver.add(flag[19] == flag[24])
solver.add(flag[8] == 49)
solver.add(flag[8] == flag[16])

for i, c in enumerate("d0nT"):
    solver.add(flag[i + 10] == ord(c))

# solver.add(ord("0") <= flag[18], flag[18] <= ord("9"))
# solver.add(ord("0") <= flag[23], flag[23] <= ord("9"))
# solver.add(ord("0") <= flag[28], flag[28] <= ord("9"))
# solver.add(flag[18] - ord("0") + flag[23] - ord("0") + flag[28] - ord("0") == 9)
# solver.add(flag[18] == flag[28])
solver.add(flag[18] == ord("3"))
solver.add(flag[23] == ord("3"))
solver.add(flag[28] == ord("3"))

solver.add(flag[15] == ord("L"))
# solver.add(Xor(flag[17], -10) == -99)
solver.add(flag[17] == 107)
solver.add(flag[20] + 2 == flag[27])
solver.add(flag[27] == 100)
solver.add(flag[20] >= 97)
solver.add(flag[27] % 100 == 0)
solver.add(flag[25] == ord("C"))
solver.add(
    ord("0") <= flag[26],
    flag[26] <= ord("9"),
    flag[26] % 2 == 0,
    flag[26] % 3 == 0,
    flag[26] % 4 == 0,
)
solver.add(ord("0") <= flag[23], flag[23] <= ord("9"), flag[23] == ord("3"))
solver.add(flag[22] == flag[13] + 0x20)

solver.add(sum(flag) == 2441)
solver.add(flag[7] == ord("{"))
solver.add(flag[9] == ord("_"))
# solver.add(flag[21] == ord("y"))


if solver.check() != sat:
    print("unsat")
    exit()

model = solver.model()
flag_str = ""
for f in flag:
    flag_str += chr(model[f].as_long())
print(flag_str)
