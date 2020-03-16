
from hashlib import sha256
seed = b'secret_sauce_#9'   
def keygen(s):
   keys = []
   for i in range(2020):
      s = sha256(s).digest()
      keys.append(s)
   return keys

keys = keygen(seed)
with open("key.bin", "wb") as f:
   for k in keys:
      f.write(k)
