from ptrlib import Socket, crt

NUM_LOCKS = 5
NUM_TRIES = 250

sock = Socket("chal.uiuc.tf", 2004)
sock.sendlineafter("caught? ", "9")

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251][::-1]

for i in range(NUM_LOCKS):
    print(f"stage {i+1}")
    shares = eval(sock.recvlineafter("portions:\n").decode())

    for p in primes:
        flag = True
        for s in shares:
            if s[1] == p:
                flag = False
                break
        if flag:
            prime = p
            break

    for x in range(251):
        v, _ = crt(shares + [(x, prime)])
        sock.sendlineafter("key: ", str(v))
        if b"unlocked" in sock.recvline():
            break
sock.interactive()


