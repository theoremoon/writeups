from Crypto.Cipher import AES
from binascii import unhexlify, hexlify

key1 = b'0000000000000t\r['
key2 = b'}=v0000000000000'

c = bytes.fromhex("fa364f11360cef2550bd9426948af22919f8bdf4903ee561ba3d9b9c7daba4e759268b5b5b4ea2589af3cf4abe6f9ae7e33c84e73a9c1630a25752ad2a984abfbbfaca24f7c0b4313e87e396f2bf5ae56ee99bb03c2ffdf67072e1dc98f9ef691db700d73f85f57ebd84f5c1711a28d1a50787d6e1b5e726bc50db5a3694f576")
aes = AES.new(key2, AES.MODE_ECB)
middle = aes.decrypt(c)

aes = AES.new(key1, AES.MODE_ECB)
m = aes.decrypt(unhexlify(middle))
print(m)
print(unhexlify(m))
