from ptrlib import Socket

symbols = [
    [
        """
  #
 ##
# #
  #
  #
  #
#####
""",
        "1",
    ],
    [
        """
 #####
#     #
      #
 #####
#
#
#######
""",
        "2",
    ],
    [
        """
 #####
#     #
      #
 #####
      #
#     #
 #####
""",
        "3",
    ],
    [
        """
#
#    #
#    #
#    #
#######
     #
     #
""",
        "4",
    ],
    [
        """
#######
#
#
######
      #
#     #
 #####
""",
        "5",
    ],
    [
        """
 #####
#     #
#
######
#     #
#     #
 #####
""",
        "6",
    ],
    [
        """
#######
#    #
    #
   #
  #
  #
  #
""",
        "7",
    ],
    [
        """
 #####
#     #
#     #
 #####
#     #
#     #
 #####
""",
        "8",
    ],
    [
        """
 #####
#     #
#     #
 ######
      #
#     #
 #####
""",
        "9",
    ],
    [
        """
  ###
 #   #
#     #
#     #
#     #
 #   #
  ###
""",
        "0",
    ],
    [
        """

  #
  #
#####
  #
  #

""",
        "+",
    ],
    [
        """

 #   #
  # #
#######
  # #
 #   #

""",
        "*",
    ],
    [
        """



#####




""",
        "-",
    ],
]


def get_symbol(lines, p):
    for sym in symbols:
        is_this = True
        for i, symline in enumerate(sym[0].split("\n")):
            if i >= len(lines):
                break
            if not lines[i][p:].startswith(symline):
                is_this = False
                break
        if is_this:
            width = 0
            for symline in sym[0].split("\n"):
                width = max(width, len(symline))
            return (sym[1], width + p + 1)
    return ("=", p)


sock = Socket("104.154.120.223", 8083)

cnt = 0
while True:
    lines = []
    for _ in range(9):
        line = sock.recvline().decode().rstrip()
        print(line, flush=True)
        lines.append(line)
    sock.recvuntil(">>> ")

    expr = ""
    p = 0
    while True:
        sym, p = get_symbol(lines, p)
        if sym == "=":
            break
        expr += sym
    print("{}: {}".format(cnt, expr))
    sock.sendline(str(eval(expr)))
    cnt += 1

    if cnt == 100:
        break

sock.interactive()
