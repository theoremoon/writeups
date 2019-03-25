import re


lines = open("dis.asm").read().splitlines()
i = 0
flagbuf = ['' for _ in range(0x1000)]
while i < len(lines):
    if lines[i] == 'mov    rax,QWORD PTR [rbp-0x20]':
        i += 3

        index = 0
        if lines[i].startswith('add'):
            r = re.findall(r',(.+)$', lines[i])
        else:
            r = re.findall(r'0x(.+)\]', lines[i])
        if len(r) == 1:
            index = int(r[0], 16)

        i += 1
        if lines[i].startswith('cmp'):
            pass
        else:
            i += 1
            if lines[i].startswith('cmp'):
                r = re.findall(r'0x(.+)$', lines[i])
                print(r[0], lines[i])
                flagbuf[index] = chr(int(r[0], 16))
            else:
                r = re.findall(r',0x(.+)$', lines[i])
                xor = r[0]
                i += 1
                r = re.findall(r',0x(.+)$', lines[i])
                c = r[0]
                flagbuf[index] = chr(int(xor, 16) ^ int(c, 16))
    else:
        i += 1
print(''.join(flagbuf))
