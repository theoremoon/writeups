from ptrlib import *
from binascii import hexlify, unhexlify

iv_len = 16
hash_len = 20
salt_len = 16

username = b"takoyaki"
password = b"hogepiyo"

sock = Socket("207.148.68.109", 20000)
# sock = Socket("localhost", 8765)
sock.recvuntil("Input username:\n")
sock.sendline(username)

sock.recvuntil("Input password:\n")
sock.sendline(password)


sock.recvuntil("Your cookie:\n")
hex_cookie = sock.recvline().decode().strip()
data = unhexlify(hex_cookie)
iv, cookie, checksum = data[:iv_len], data[iv_len:-hash_len], data[-hash_len:]
print("[+]cookie, checksum = {}, {}".format(cookie, checksum))


def oracle(x):
    sock.recvuntil("Input your cookie:\n")
    my_cookie = hexlify(x + checksum).decode()
    sock.sendline(my_cookie)
    result = sock.recvline().decode().strip()
    if "padding" in result:
        return False
    if "hash" in result:
        return True
    raise Exception(result)


def pad(x):
    l = (16 - len(x)) % 16
    return x + bytes([l] * l)


known_msg = b"admin:0;username:%s;password:%s" % (username, password)
append_msg = b";admin:1"

new_checksum, new_data = lenext(SHA1, salt_len, checksum, known_msg, append_msg)
attack_data = padding_oracle_encrypt(oracle, plain=pad(new_data), bs=16, unknown=b"A")

print("[+]new_cookie, new_checksum = {}, {}".format(repr(new_data), repr(new_checksum)))
print("[+]attack data = {}".format(hexlify(new_data)))

sock.recvuntil("Input your cookie:\n")
attack_cookie = hexlify(attack_data).decode() + new_checksum
sock.sendline(attack_cookie)

print(new_checksum)
print(sock.recvline())
print(sock.recvline())
print(sock.recvline())
print(sock.recvline())
