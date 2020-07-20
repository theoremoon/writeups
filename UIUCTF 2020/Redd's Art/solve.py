key = sum(ord(c) for c in "uiuctf{v3Ry_r341_@rTT}")
xs = [ord(c) for c in "hthzgubI>*ww7>z+Ha,m>W,7z+hmG`"]

for k in range(256):
    ys = "".join(chr((((k+x) % 256) ^ key) & 0xff) for x in xs)
    print(repr(ys))
