from ptrlib import *

n = 136018504103450744973226909842302068548152091075992057924542109508619184755376768234431340139221594830546350990111376831021784447802637892581966979028826938086172778174904402131356050027973054268478615792292786398076726225353285978936466029682788745325588134172850614459269636474769858467022326624710771957129
e = 0x10001

sock = Socket("crypto.2020.chall.actf.co", 20600)
sock.recvuntil("flag:\n")
c = int(sock.recvline().decode())

last_bit = 1000000
def oracle(c):
	global last_bit
	sock.recvuntil("sign: ")
	sock.sendline(str(c))
	print(sock.recvline())
	current_bit = len(sock.recvline())
	oracle_v = 1 if current_bit <= last_bit else 0
	last_bit = current_bit
	return oracle_v

oracle(c)
print(lsb_leak_attack(oracle, n, e, c))
