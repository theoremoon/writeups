from ptrlib import Socket
import random
import string


def decrypt(mes):
    chars = mes.split(" ")
    plain = ""
    for char in chars:
        elements = char.split("/")
        if len(elements) == 5:
            plain += char[-1]
        elif len(elements) == 3:
            plain += char[0]
        elif elements[2][0] in "~`!@#$%^&*()_-+=<,>.?|":
            plain += elements[1][0]
        else:
            plain += elements[2][0]
    return plain

sock = Socket("104.154.120.223", 8085)
sock.recvuntil("Your cipher key: ")
line = sock.recvline().decode().rstrip()
key = decrypt(line)
sock.recvuntil("Your choice: ")
sock.sendline("2")
sock.recvuntil("Please enter the key to get flag: ")
sock.sendline(key)
sock.interactive()
