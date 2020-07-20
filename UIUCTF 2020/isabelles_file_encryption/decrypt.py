def super_secret_decryption(file_name, password):
    with open(file_name, "rb") as f:
        ciphertext = f.read()
  
    remove_spice = lambda b: 0xff & ((b >> 1) | (b << 7))
    plaintext = bytearray(remove_spice(c ^ password[i % len(password)]) for i, c in enumerate(ciphertext))

    with open(file_name + password.decode(), "wb") as f:
        f.write(plaintext)

super_secret_decryption("blackmail_encrypted", b'iSaBelLE')
