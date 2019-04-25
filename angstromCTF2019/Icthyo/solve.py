from PIL import Image

img = Image.open("out.png")
w, h = img.size

lines = []

for y in range(h):
    line = []
    for x in range(w):
        line.append(img.getpixel((x, y)))
    lines.append(line)

buf = ""
for l in lines:
    c = ""
    for x in range(8):
        r, g, b = l[x * 32]
        c += str((b & 1) ^ ((r ^ g) & 1))
    x = int(c[::-1], 2)
    if x == 0:
        break
    buf += chr(x)
print(buf)
