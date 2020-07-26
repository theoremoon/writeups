from PIL import Image, ImageDraw

lines = open("plaintext").read().strip().split("\n")
points = {}
for line in lines:
    if not line.startswith("DD"):
        continue
    _, idx, x, y = line.strip().split(" ")
    points[int(idx)] = (int(x), int(y))




img = Image.new("RGB", (2200, 200))
draw = ImageDraw.Draw(img)

for line in lines:
    if not line.startswith("E "):
        continue
    _, p1, p2, _ = line.strip().split(" ")
    p1 = points[int(p1)]
    p2 = points[int(p2)]

    draw.line([p1, p2], fill=(255, 255, 255), width=1)

img.save("flag.png")

