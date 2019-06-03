r13 = [0x59, 0xb9, 0x78, 0xc7]
correct = [0xe5, 0x89, 0x48, 0x55]
ans = [[] for _ in range(4)]

for p in range(4):
    for c in range(256):
        if (r13[p] - c + 256) % 256 == correct[p]:
            ans[p].append(chr(c))
print(ans)
