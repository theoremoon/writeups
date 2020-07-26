from libcst import *

with open('pyzzle', 'r') as f:
  program = f.read()

cst = eval(program)
with open('original.py', 'w') as f:
  f.write(cst.code)
