import ast
with open("output.txt") as f:
  p = ast.literal_eval(f.readline().strip())
  key = ast.literal_eval(f.readline().strip())
  enc = ast.literal_eval(f.readline().strip())


SIZE = 8
MS = MatrixSpace(GF(p), SIZE)

key = MS(key)
enc = MS(enc)

M = key^(-1)  * enc * key^(-1)

flag = 0
for i in range(SIZE):
    for j in range(SIZE):
        n = i * SIZE + j
        if M[i,j] < 128:
          flag = flag*256 + int(M[i,j])

print(int(flag).to_bytes(100, "big"))
