# gdb -n -q -x solve.py ./timeout
import gdb
import re

gdb.execute("set pagination off")
variables = gdb.execute("info var", to_string=True)
for v in variables.split("\n"):
    if not v.startswith("0x"):
        continue
    addr, name = v.split()
    if name == "can_continue":
        break
gdb.execute("break main")
gdb.execute("run")
gdb.execute("set {int}(" + addr + ") = 0x539")
gdb.execute("jump generate")
gdb.execute("quit")
