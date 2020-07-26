from ptrlib import padding_oracle_encrypt, Socket
from Crypto.Util.Padding import pad
from binascii import hexlify, unhexlify
from logging import getLogger, WARN

getLogger("ptrlib.pwn").setLevel(WARN + 1)

def decrypt(c):
    sock = Socket("youshallnotgetmycookies.3k.ctf.to", 13337)
    sock.sendlineafter("your cookie:", hexlify(c).upper())
    result = sock.recvline().decode()
    result = sock.recvline().decode()
    sock.close()
    if 'Nop' in result:
        return True
    elif "rude" in result:
        raise Exception("RUDE!!!")
    else:
        return False

plain = pad(b'Maple Oatmeal Biscuits', 16)
print(padding_oracle_encrypt(decrypt, plain, bs=16))

