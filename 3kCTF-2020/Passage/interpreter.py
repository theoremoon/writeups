import string

table = set([ord(c) for c in string.ascii_letters + string.digits + ' -{}_'])

pc = 0
ptr = 0
mem = [0 for _ in range(65536)]

jumplist = {}
code = open("code.bf").read().strip()
while pc < len(code):
    if code[pc] == '+':
        mem[ptr] = (mem[ptr] + 1) % 256

    elif code[pc] == '-':
        mem[ptr] = (mem[ptr] - 1) % 256

    elif code[pc] == '>':
        ptr = (ptr + 1) % 65536

    elif code[pc] == '<':
        ptr = (ptr - 1) % 65536

    elif code[pc] == '[':
        cnt = 0
        if pc not in jumplist:
            pc2 = pc + 1
            while True:
                if code[pc2] == ']':
                    if cnt == 0:
                        jumplist[pc2] = pc-1
                        jumplist[pc] = pc2
                        break
                    else:
                        cnt -= 1
                elif code[pc2] == '[':
                    cnt += 1
                pc2 += 1

        if mem[ptr] == 0:
            pc = jumplist[pc]
            print([chr(v) for v in mem if v in table])

    elif code[pc] == ']':
        pc = jumplist[pc]

    elif code[pc] == '.':
        pass
        # print(mem[ptr], ",", end="")

    
    pc += 1

import code
code.interact(local=locals())
