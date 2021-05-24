import ast

with open("output.txt") as f:
    ciphers = ast.literal_eval(f.readline().strip().split(" = ")[1])

n = len(ciphers[0])
flag = [0 for i in range(n)]
for cipher in ciphers:
    for i in range(n):
        if cipher[i] == "1":
            flag[i] = 1

flag = "".join(str(v) for v in flag)
print(int(flag, 2).to_bytes(100, "big").strip(b"\0"))

