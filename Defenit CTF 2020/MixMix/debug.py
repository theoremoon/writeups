import gdb


gdb.execute("file ./mixmix")
gdb.execute("start < input")
piebase  = int(gdb.execute("piebase", to_string=True).strip().split(" = ")[1], 16)
data = 'mogutakomogumogutakomogudefenitc'
print(data)


gdb.execute("b *0x{:0x}".format(piebase+ 0xECA))
offsets = []
bits = []
for _ in range(256):
    gdb.execute("continue")
    offset = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    offsets.append(offset)
    bit = int(gdb.execute("print $rcx", to_string=True).strip().split(" = ")[1])
    bits.append(bit)

gdb.execute("b *0x{:0x}".format(piebase+ 0x102A))
gdb.execute("b *0x{:0x}".format(piebase+ 0x105B))
swapindex = []
bitvalues = []
for _ in range(256):
    gdb.execute("continue")
    offset = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    swapindex.append(offset)

    gdb.execute("continue")
    offset = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    bitvalues.append(offset)


gdb.execute("b *0x{:0x}".format(piebase+ 0x1123))
mogo_offsets = []
vs = []
for _ in range(256):
    gdb.execute("continue")
    offset = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    mogo_offsets.append(offset)

    gdb.execute("step")
    v = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    vs.append(v)


gdb.execute("b *0x{:0x}".format(piebase+0x0F64))
mogo_read_offsets = []
read_vs = []
for _ in range(256):
    gdb.execute("continue")
    offset = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    mogo_read_offsets.append(offset)

    gdb.execute("step")
    v = int(gdb.execute("print $rdx", to_string=True).strip().split(" = ")[1])
    read_vs.append(v)

gdb.execute("b *0x{:0x}".format(piebase+0x0D8b))
mini_values = []
vx = []
for _ in range(len(data)):
    gdb.execute("continue")
    v = int(gdb.execute("print $rsi", to_string=True).strip().split(" = ")[1])
    mini_values.append(v)

    v2 = int(gdb.execute("print $rcx", to_string=True).strip().split(" = ")[1])
    vx.append(v2)

print(offsets)
print(bits)
print(swapindex)
print(bitvalues)
print(mogo_offsets)
print(vs)
print(mogo_read_offsets)
print(read_vs)
print(mini_values)
print(vx)
