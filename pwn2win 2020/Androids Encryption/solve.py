from ptrlib import *
from base64 import b64encode, b64decode
from Crypto.Util.Padding import *
from Crypto.Cipher import AES

BLOCK_SIZE = 16

def to_blocks(txt):
    return [txt[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(len(txt)//BLOCK_SIZE)]

def xor(b1, b2=None):
    if isinstance(b1, list) and b2 is None:
        assert len(set([len(b) for b in b1])) == 1, 'xor() - Invalid input size'
        assert all([isinstance(b, bytes) for b in b1]), 'xor() - Invalid input type'
        x = [len(b) for b in b1][0]*b'\x00'
        for b in b1:
            x = xor(x, b)
        return x
    assert isinstance(b1, bytes) and isinstance(b2, bytes), 'xor() - Invalid input type'
    return bytes([a ^ b for a, b in zip(b1, b2)])

plaintext = pad(b"the quick brown fox jumps over the lazy dog", AES.block_size)

sock = Socket("encryption.pwn2.win", 1337)
sock.sendlineafter("Choice: ", "1")
sock.sendlineafter("Plaintext: ", b64encode(plaintext))
c = b64decode(sock.recvline())
iv, c = c[:16], c[16:]

key = xor(to_blocks(c))

sock.sendlineafter("Choice: ", "2")
c = b64decode(sock.recvline())
iv, c = c[:16], c[16:]

blocks = to_blocks(c)
aes = AES.new(key=key, mode=AES.MODE_ECB)
curr = iv
ctxt = b''
for i in range(len(blocks)):
    ctxt += xor(aes.decrypt(blocks[i]), curr)
    curr = xor(blocks[i] , ctxt[-16:])

print(ctxt)
