from PIL import Image

img = Image.open("flag.png")
w, h = img.size

prev = None
flag = []
for x in range(w):
    r, g, b = img.getpixel((x, 0))
    if (r, g, b) != prev:
        flag.extend([r, g, b])
        prev = (r, g, b)
print("".join(chr(c) for c in flag))
