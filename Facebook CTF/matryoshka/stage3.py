r15 = [0x19, 0x02, 0xea, 0x87][::-1]
correct = [0xe5, 0x89, 0x48, 0x55]
ans = []

for i in range(4):
    ans.append(chr(r15[i] ^ correct[i]))

ans = "".join(ans)[::-1] + "uOQJ"
print(ans)
