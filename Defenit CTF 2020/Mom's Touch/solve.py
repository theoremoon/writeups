import gdb

gdb.execute("b main")
gdb.execute("b *0x8048800")
gdb.execute("run < piyo2")

flag = ''
for _ in range(0x49):
    # ecx1 = int(gdb.execute("print $ecx", to_string=True).split(" ")[2])
    # ecx2 = int(gdb.execute("print $ecx", to_string=True).split(" ")[2])
    # ecx3 = int(gdb.execute("print $ecx", to_string=True).split(" ")[2])
    mask1 = int(gdb.execute("x/w $bp*4 + 0x80492AC", to_string=True).split("\t")[1])
    mask2 = int(gdb.execute("x/w $eax*4 + 0x80492AC", to_string=True).split("\t")[1])
    cmpto = int(gdb.execute("x/w $esi*4 + 0x8049144", to_string=True).split("\t")[1])
    gdb.execute("step")
    gdb.execute("step")
    gdb.execute("step")
    gdb.execute("step")

    gdb.execute("set $ZF = 6")
    gdb.execute("set $eflags |= (1 << $ZF)")

    flag += chr(mask1 ^ mask2 ^ cmpto)
    print(flag)

    gdb.execute("continue")
gdb.execute("quit")

