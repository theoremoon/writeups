from PIL import Image
from Crypto.Util.number import *

img = Image.open("enc.png")
key = [41, 37, 23]
key = [inverse(k, 251) for k in key]

w, h = img.size
for x in range(w):
    for y in range(h):
        r,g,b, _ = img.getpixel((x, y))
        pixel = [r,g,b]
        for i in range(3):
            pixel[i] = pixel[i] * key[i] % 251
        img.putpixel((x, y), tuple(pixel))

img.save("flag.png")
