#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pwnlib.tubes import remote
from ptrlib import crt
import sys
import challenge_pb2
import struct
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastecdsa import curve
from fastecdsa.point import Point

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

CHANNEL_CIPHER_KDF_INFO = b"Channel Cipher v1.0"
CHANNEL_MAC_KDF_INFO = b"Channel MAC v1.0"

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

        out = challenge_pb2.Ciphertext()
        out.iv = iv
        out.data = ct
        out.mac = mac
        return out


def handle_pow(tube):
    raise NotImplemented()

def read_message(tube, typ):
    n = struct.unpack('<L', tube.recvnb(4))[0]
    buf = tube.recvnb(n)
    msg = typ()
    msg.ParseFromString(buf)
    return msg

def write_message(tube, msg):
    buf = msg.SerializeToString()
    tube.send(struct.pack('<L', len(buf)))
    tube.send(buf)

def curve2proto(c):
    return challenge_pb2.EcdhKey.CurveID.SECP256R1

def key2proto(key):
    assert(isinstance(key, ec.EllipticCurvePublicKey))
    out = challenge_pb2.EcdhKey()
    out.curve = curve2proto(key.curve)
    x, y = key.public_numbers().x, key.public_numbers().y
    out.public.x = x.to_bytes((x.bit_length() + 7) // 8, 'big')
    out.public.y = y.to_bytes((y.bit_length() + 7) // 8, 'big')
    return out

def proto2key(key):
    assert(isinstance(key, challenge_pb2.EcdhKey))
    assert(key.curve == challenge_pb2.EcdhKey.CurveID.SECP224R1)
    curve = ec.SECP224R1()
    x = int.from_bytes(key.public.x, 'big')
    y = int.from_bytes(key.public.y, 'big')
    public = ec.EllipticCurvePublicNumbers(x, y, curve)
    return ec.EllipticCurvePublicKey.from_encoded_point(curve, public.encode_point())

def run_session(x, y, b, guess_d, mod):
    tube = remote.remote('tiramisu.2021.ctfcompetition.com', 1337)
    # tube = pwnlib.tubes.remote.remote('127.0.0.1', port)
    # print(tube.recvuntil('== proof-of-work: '))
    if tube.recvline().startswith(b'enabled'):
        handle_pow()

    server_hello = read_message(tube, challenge_pb2.ServerHello)
    server_key = proto2key(server_hello.key)
    # print(server_hello)

    # private_key = ec.generate_private_key(ec.SECP224R1())
    out = challenge_pb2.EcdhKey()
    out.curve = challenge_pb2.EcdhKey.CurveID.SECP256R1
    out.public.x = x.to_bytes((x.bit_length() + 7) // 8, 'big')
    out.public.y = y.to_bytes((y.bit_length() + 7) // 8, 'big')

    client_hello = challenge_pb2.ClientHello()
    client_hello.key.CopyFrom(out)
    # print(client_hello)

    write_message(tube, client_hello)

    c = curve.P224
    c.b = b
    p = c.p
    try:
        guessed_shared_x = (guess_d * Point(x % p, y % p, curve=curve.P224)).x
    except ValueError:
        return False
    shared_key = guessed_shared_x.to_bytes(224 // 8, "big")
    # shared_key = private_key.exchange(ec.ECDH(), server_key)
    # print(shared_key)

    channel = AuthCipher(shared_key, CHANNEL_CIPHER_KDF_INFO, CHANNEL_MAC_KDF_INFO)
    msg = challenge_pb2.SessionMessage()
    msg.encrypted_data.CopyFrom(channel.encrypt(IV, b'hello'))
    write_message(tube, msg)
    # print('msg:', msg)

    reply = read_message(tube, challenge_pb2.SessionMessage)
    # print("d: {}, mod: {}".format(guess_d, mod))
    # print('reply:', repr(reply))
    # import code
    # code.interact(local=locals())
    tube.close()
    if len(repr(reply)):
        return True
    return False

def try_guess(x, y, b, mod):
    for guess_d in range(mod):
        if run_session(x, y, b, guess_d, mod):
            return (guess_d, mod)
    return None

def main():
    with open("values.json") as f:
        values = json.load(f)
    sorted(values, key=lambda x: x[3])

    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    pairs = []
    # for x, y, b, mod in values[start:]:
    #     try_guess(x, y, b, mod)
    #     input("[pause]")
    with ThreadPoolExecutor() as ex:
        futures = []
        for x, y, b, mod in values[start:]:
            futures.append(ex.submit(try_guess, x, y, b, mod))

        for f in as_completed(futures):
            pair = f.result()
            if pair is None:
                continue
            print("{}/{}".format(len(pairs) + 1, len(values)), pair)
            pairs.append(pair)
    print(pairs)
    print(crt(pairs))

main()

