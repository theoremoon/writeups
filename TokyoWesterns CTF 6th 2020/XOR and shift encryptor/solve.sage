N = 64
F = GF(2)

def L(n):
  m = [[0 for x in range(N)] for y in range(N)]

  for i in range(N - n):
    m[i + n][i] = 1

  return matrix(F, m)

def R(n):
  m = [[0 for x in range(N)] for y in range(N)]

  for i in range(N - n):
    m[i][i + n] = 1

  return matrix(F, m)


def I():
  m = [[0 for x in range(N)] for y in range(N)]

  for i in range(N):
    m[i][i] = 1

  return matrix(F, m)

def O():
  m = [[0 for x in range(N)] for y in range(N)]
  return matrix(F, m)

def genM():
  a = 3
  b = 13
  c = 37

  o = O()
  i = I()
  la = L(a)
  rb = R(b)
  rc = R(c)

  blocks = [
    [i + rc, i + la + rb + la*rb] + [o for _ in range(62)]
  ]
  for j in range(1, N):
    row = [o for _ in range(N)]
    row[(j+1) % N] = i
    blocks.append(row)

  M = block_matrix(F, [*zip(*blocks)])

  return M


def initial_state():
  s = "".join(["{:064b}".format(i) for i in range(N)])
  vec = []
  for c in s:
    vec.append(F(int(c)))
  return Matrix(F, vec)

def getvalue(row, index):
  v = 0
  for i in range(N):
    v = v*2 + int(row[0][index*N + i])
  return v


def dumpstate(a):
  xs = []
  for i in range(N):
    xs.append(getvalue(a, i))
  print(xs)

s = initial_state()
M = genM()

def init():
  global s, M
  s = initial_state()
  M = genM()

def randgen():
  global s, M
  res = (getvalue(s, 0) + getvalue(s, 1)) % ((1<<64)-1)
  s = s * M
  return res

def jump(n):
  global s,M
  s = s * (M^n)


def check_jump():
  init()
  jump(10000)
  assert randgen() == 7239098760540678124

  init()
  jump(100000)
  assert randgen() == 17366362210940280642

  init()
  jump(1000000)
  assert randgen() == 13353821705405689004

  init()
  jump(10000000)
  assert randgen() == 1441702120537313559

  init()
  for a in range(100):randgen()
  for a in range(200):randgen()
  buf = randgen()
  for a in range(300):randgen()
  buf2 = randgen()
  init()
  jump(100+200)
  print (buf == randgen())  
  jump(300)
  print (buf2 == randgen())

check_jump()

#init()
#jump(31337)
#for x in range(256):
#  buf = randgen()
#  sh = x//2
#  if sh > 64:sh = 64
#  mask = (1 << sh) - 1
#  buf &= mask
#  jump(buf)
#  print(randgen() & 0xff) 
