#!/usr/bin/python
from ptrlib import *
import string
from Crypto.Cipher import AES
from binascii import hexlify

pt = "aaaaaaaaaaaaaaaa"
val = len(pt) % 16
if not val == 0:
    pt += '0'*(16 - val)

m = hexlify(pt.encode())
table = {}
print("[+] table1")
for p in brute_force_attack(3, table_len=len(string.printable)):
    s = brute_force_pattern(p, string.printable)
    k = '0' * 13 + s
    aes = AES.new(key=k.encode(), mode=AES.MODE_ECB)
    c = aes.encrypt(m)
    table[hexlify(c)] = k

print("[+] table2")
c = bytes.fromhex("ef92fab38516aa95fdc53c2eb7e8fe1d5e12288fdc9d026e30469f38ca87c305ef92fab38516aa95fdc53c2eb7e8fe1d5e12288fdc9d026e30469f38ca87c305")
for p in brute_force_attack(3, table_len=len(string.printable)):
    s = brute_force_pattern(p, string.printable)
    k =  s + '0' * 13
    aes = AES.new(key=k.encode(), mode=AES.MODE_ECB)
    m = aes.decrypt(c)
    if m in table:
        print("KEY1: {}".format(repr(table[m])))
        print("KEY2: {}".format(repr(k)))

