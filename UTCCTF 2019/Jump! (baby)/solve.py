import gdb

gdb.execute("b main")
gdb.execute("run")
data = gdb.execute("info addr selfish", to_string=True).split()
for d in data:
    if d.startswith("0x"):
        break
gdb.execute("set {{int}}{}=0".format(d))
gdb.execute("jump gimme_flag")
