from base64 import b64decode
from zlib import decompress

data = open("encrypted.txt", "rb").read()

i = 0
while True:
    try:
        if i % 2 == 0:
            data = b64decode(data)
        else:
            data = decompress(data)
        i += 1
    except:
        print(data)
        break
