from fastecdsa.curve import P224
from fastecdsa.point import Point
from ptrlib import crt
from tqdm import tqdm
from Crypto.Util.number import inverse

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

from itertools import product

CHANNEL_CIPHER_KDF_INFO = b"Channel Cipher v1.0"
CHANNEL_MAC_KDF_INFO = b"Channel MAC v1.0"
flagCipherKdfInfo = b"Flag Cipher v1.0"
flagMacKdfInfo = b"Flag MAC v1.0"
flagFixedIV = bytes([0x73, 0x40, 0x76, 0xd5, 0x67, 0xe0, 0x9, 0x2a, 0xbc, 0xe1, 0x9, 0x15, 0x82, 0x55, 0x43, 0x7d])
d = 70660979691982122950200127958675461805766058089618993620860247487201

IV = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff'

class AuthCipher(object):
    def __init__(self, secret, cipher_info, mac_info):
        self.cipher_key = self.derive_key(secret, cipher_info)
        self.mac_key = self.derive_key(secret, mac_info)

    def derive_key(self, secret, info):
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=16,
            salt=None,
            info=info,
            backend=default_backend(),
        )
        return hkdf.derive(secret)

    def encrypt(self, iv, plaintext):
        cipher = Cipher(algorithms.AES(self.cipher_key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(plaintext) + encryptor.finalize()

        h = hmac.HMAC(self.mac_key, hashes.SHA256(), backend=default_backend())
        h.update(iv)
        h.update(ct)
        mac = h.finalize()

        return (iv, ct, mac)

    def decrypt(self, iv, ciphertext):
        cipher = Cipher(algorithms.AES(self.cipher_key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        pt = decryptor.update(ciphertext) + decryptor.finalize()
        return pt


# cipher = AuthCipher(b"hello", flagCipherKdfInfo, flagMacKdfInfo)
# iv, ct, mac = cipher.encrypt(flagFixedIV, b"hogehoge")
# print(cipher.decrypt(iv, ct))

P = Point(16172896427079531402065391174021745391759293127844103141392333432900, 3771244459121791372570158792354692313003593392921088306467285612598, curve=P224)
G = Point(P224.gx, P224.gy, curve=P224)

pairs = [(60, 1181), (177, 1811), (327, 6571), (455, 2399), (550, 1607), (476, 1061), (123, 3797), (1481, 6871), (991, 3389), (564, 1907), (1612, 6343), (502, 5431), (497, 1283), (319, 3109), (2161, 4931), (262, 1361), (121, 2969), (878, 4513), (1470, 6599), (1735, 4289)]

data = b">}\"B\352\"WgA\234*\014p\326b\\O6\374\250\217K\343\334U\374\252~\267\026\325\212J\3178M\354{q\231\201\310\351yyj`3_\224^\313\204P\200\323\233="


for pat in tqdm(product([0, 1], repeat=len(pairs))):
    pairs2 = pairs[:]
    for i in range(len(pat)):
        if pat[i] == 1:
            pairs2[i] = (-pairs2[i][0] % pairs2[i][1], pairs2[i][1])

    d, _ = crt(pairs2)
    # print(d)
    # P_ = d*G
    # if P_.x == P.x and P_.y == P.y:
    #     print(d)

    try:
        key = d.to_bytes(224 // 8, "big")

        cipher = AuthCipher(key, flagCipherKdfInfo, flagMacKdfInfo)
        m = cipher.decrypt(flagFixedIV, data)
        if b"CTF" in m:
            print(m)
    except OverflowError:
        pass
