from PIL import Image

img = Image.open("pic.png")
w, h = img.size

s = ''
c = ''
for y in range(3):
    for x in range(w):
        r, g, b = img.getpixel((x, y))
        c += str(r&1) + str(g&1) + str(b&1)
        if len(c) >= 8:
            s += chr(int(c[:8], 2))
            c = c[8:]
print(s.rstrip('\x00'))


