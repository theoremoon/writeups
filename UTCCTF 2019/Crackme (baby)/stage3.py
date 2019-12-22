s = "L33TC0dE"
want = "x\001\022\vw\002E\032x\001\022\vw\002Edm\002\002ub\001E"
code = ""

for i in range(len(want)):
    code += chr(ord(want[i]) ^ ord(s[i % len(s)]))
print(code)

