from ptrlib import xor


add_spice = lambda b: 0xff & ((b << 1) | (b >> 7))
plaintext = bytes(add_spice(b) for b in b"Isabelle")

ciphertext = open("blackmail_encrypted", "rb").read()
for i in range(0, len(ciphertext) - 8):
    key = xor(plaintext, ciphertext[i:])
    try:
        if key.decode().isalpha():
            print(repr(key))
    except UnicodeDecodeError:
        pass


