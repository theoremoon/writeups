# gdb -n -q -x <self> <binary>
import gdb
import re

with open("input.txt", "w") as f:
    f.write("A" * 0x20)

alist = []
dlist = []

gdb.execute("b *0x401000", to_string=True)  # start
gdb.execute("run < input.txt", to_string=True)
gdb.execute("b *0x401128", to_string=True)  # cmp rax, rbx
gdb.execute("continue", to_string=True)
gdb.execute("set $rax = 0", to_string=True)  # ptrace = 0

gdb.execute("b *0x401024", to_string=True)  # mov    ah, byte ptr [rsi]
gdb.execute("b *0x401032", to_string=True)  # mov    dh, byte ptr [rcx]
gdb.execute("b *0x401075", to_string=True)  # je     0x401079

while True:
    gdb.execute("continue", to_string=True)
    gdb.execute("step", to_string=True)
    a = gdb.execute("print $ah", to_string=True).strip().split(" = ")[1]
    alist.append(int(a))

    gdb.execute("continue", to_string=True)
    gdb.execute("step", to_string=True)
    d = gdb.execute("print $dh", to_string=True).strip().split(" = ")[1]
    dlist.append(int(d))

    gdb.execute("continue", to_string=True)
    gdb.execute("set $eflags = $eflags | (1 << 6)", to_string=True)  # set ZF

    print("".join(chr(a ^ d) for a, d in zip(alist, dlist)))
