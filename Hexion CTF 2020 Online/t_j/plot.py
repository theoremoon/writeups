import struct
from PIL import Image

INIT_X, INIT_Y = 0, 0

picture = Image.new("RGB", (2000, 500), "white")
pixels = picture.load() 
lines = open("data").read().strip().split("\n")
x, y = INIT_X, INIT_Y
for l in lines:
    b, dx, dy = [struct.unpack("b", int(a, 16).to_bytes(1, "little"))[0] for a in l.split(":")[:3]]

    x = x + dx
    y = y + dy
    if b:
        try:
            pixels[x, y] = (0,0,0,0)
        except:
            pass
picture.save("flag.png", "PNG")
