def func(bits):
    keys = gen_rsa_key(bits, e=65537)
    p = keys.p
    q = keys.q
    m = getPrime(bits+1)
    # x = pow(p, m, m)*pow(q, m, m) + p*pow(q, m, m) + q*pow(p, m, m) + p*q + pow(p, m-1, m)*pow(q, m-1, m)
    # x = p * q + p * q + p * q + p * q + 1 * 1
    x = 4*n + 1
    text = os.urandom(32)
    print('Plaintext (b64encoded) : ', b64encode(text).decode())
    print()
    print(hex(x)[2:])
    print(hex(m)[2:])
    # print(b64encode(encrypt(keys, text)))
    print()
    ciphertext = input('Ciphertext (b64encoded) : ')
    check()


def encrypt(keys, plaintext):
    from Crypto.Cipher import PKCS1_OAEP
    encryptor = PKCS1_OAEP.new(keys)
    return encryptor.encrypt(plaintext)
