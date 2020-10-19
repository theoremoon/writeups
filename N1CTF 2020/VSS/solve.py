from PIL import Image
from mt19937predictor import MT19937Predictor


img = Image.open("share2.png")

predict_bits = []
w, h = img.size
for y in range(0, 96, 2):
    for x in range(0, w, 2):
        p = img.getpixel((w - x - 1, h - y - 1))
        if p == 0:
            predict_bits.append(0)
        else:
            predict_bits.append(1)

bits = []
for i in range(624):
    x = "".join(str(b) for b in predict_bits[i*32:(i+1)*32][::-1])
    bits.append(int(x, 2))

predictor = MT19937Predictor()
for b in bits:
    predictor.setrandbits(b, 32)

bs = []
for b in bits:
    bs = [int(b) for b in bin(b)[2:].zfill(32)] + bs

while len(bs) < (w * h // 4):
    bs = [int(b) for b in bin(predictor.getrandbits(32))[2:].zfill(32)] + bs

flipped_coins = bs[-(w * h // 4):]

print(flipped_coins)

w, h = w // 2, h // 2
qr = Image.new("L", (w, h))
for i in range(len(flipped_coins)):
    x, y = i % w, i // h
    p = img.getpixel((2*x, 2*y))
    color0 = 0 if flipped_coins[i] else 255
    if p == color0:
        qr.putpixel((x, y), 255)
    else:
        qr.putpixel((x, y), 0)

qr.save("qr.png")
