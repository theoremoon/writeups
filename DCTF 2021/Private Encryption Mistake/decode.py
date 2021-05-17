from base64 import b64decode

with open("hoge.txt") as f:
    lines = f.read().strip().split("\n")[1:-1]

parts = []
cur = ''
p = 0
while p < len(lines):
    if lines[p] != '':
        cur += lines[p]
    else:
        if cur == '':
            pass
        else:
            parts.append(cur)
            cur = ''
    p += 1

for part in parts:
    for i in range(3):
        try:
            data = b64decode((part[:-10] + "="*i).encode())
            print()
            h = data.hex()
            for l in h.split("0282"):
                print(l)
            print()
            break
        except:
            pass

