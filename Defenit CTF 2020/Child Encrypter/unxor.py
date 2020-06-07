from ptrlib import xor
import string


def check(bs):
    for b in bs:
        if chr(b) not in string.printable:
            return False
    return True


ciphertext = open("ciphertext.txt", "rb").read()
blocks = []

for i in range(0, len(ciphertext), 16):
    blocks.append(ciphertext[i:i+16])

# k = 54
# xorkey = xor(b"5_", blocks[k][:2])
# for j in range(len(blocks)):
#     s = xor(xorkey, blocks[j][:2])
#     if check(s):
#         print("({}, {}),".format(j, s))

plains =[
(15, b'eat for '),
(19, b' is the '),
(33, b'risk." H'),
(54, b'5_g00d!}'),
]
keyn = 15
for i, p in enumerate(plains):
    if keyn == p[0]:
        keyi = i
        keylen = len(p[1])

key = xor(plains[keyi][1], blocks[keyn][:keylen])
for i in range(len(plains)):
    print("({}, {}), ".format(plains[i][0], xor(key, blocks[ plains[i][0] ][:keylen])))

Defenit{AES_CTR_m0de_i5_g00d!}
# plains = [
# (0, b'Like OFB, Counte'), 
# (5, b'he next keystrea'), 
# (7, b'pting successive'), 
# (24, b'ction used to be'), 
# (26, b'critics argued t'), 
# (38, b'd a weakness of '), 
# (44, b'ic bias in its i'), 
# (53, b't{AES_CTR_m0de_i'), 
# ]
# 
# keyn = 0
# for i, p in enumerate(plains):
#     if keyn == p[0]:
#         keyi = i
#         keylen = len(p[1])
# 
# key = xor(plains[keyi][1], blocks[keyn][:keylen])
# for i in range(len(plains)):
#     print("({}, {}), ".format(plains[i][0], xor(key, blocks[ plains[i][0] ][:keylen])))

# plains = [
#     (1,  b'r mode turns a b'),
#     (16, b'ime, although an'),
#     (20, b' and most popula'),
#     (30, b'nown systematic '),
#     (45, b'nput. Along with'),
#     (47, b's one of two blo'),
#     (52, b'. FLAG is Defeni'),
# ]
# 
# keyn = 20
# for i, p in enumerate(plains):
#     if keyn == p[0]:
#         keyi = i
#         keylen = len(p[1])
# 
# key = xor(plains[keyi][1], blocks[keyn][-keylen:])
# for i in range(len(plains)):
#     print(xor(key, blocks[ plains[i][0] ][-keylen:]))
