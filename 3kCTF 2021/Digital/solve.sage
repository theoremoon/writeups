from Crypto.Util.number import *
from hashlib import sha256


# https://raw.githubusercontent.com/defund/coppersmith/master/coppersmith.sage
import itertools

def small_roots(f, bounds, m=1, d=None):
	if not d:
		d = f.degree()

	R = f.base_ring()
	N = R.cardinality()
	
	f /= f.coefficients().pop(0)
	f = f.change_ring(ZZ)

	G = Sequence([], f.parent())
	for i in range(m+1):
		base = N^(m-i) * f^i
		for shifts in itertools.product(range(d), repeat=f.nvariables()):
			g = base * prod(map(power, f.variables(), shifts))
			G.append(g)

	B, monomials = G.coefficient_matrix()
	monomials = vector(monomials)

	factors = [monomial(*bounds) for monomial in monomials]
	for i, factor in enumerate(factors):
		B.rescale_col(i, factor)

	B = B.dense_matrix().LLL()

	B = B.change_ring(QQ)
	for i, factor in enumerate(factors):
		B.rescale_col(i, 1/factor)

	H = Sequence([], f.parent().change_ring(QQ))
	for h in filter(None, B*monomials):
		H.append(h)
		I = H.ideal()
		if I.dimension() == -1:
			H.pop()
		elif I.dimension() == 0:
			roots = []
			for root in I.variety(ring=ZZ):
				root = tuple(R(root[var]) for var in f.variables())
				roots.append(root)
			return roots

	return []


p = 0x433fd29e6352ba4f433aaf05634348bf2fa7df007861ec24e1088b4105307a9af5645fff0bb561f31210b463346f6d2990a8395e51f0abf6f0affad2364a09ef3ab2cfa66497ebb9d6ac7ed98710634c5a39ddc9d423294911cfa787e28ac2943df345ed6b979ed9a383e1be05e35b305c797f826c9502280dd5b8af4ff532527eed2e91d290b145fac6d647c81127ed06eaa580d64bcf2740ee8ed2aa158cc297ca9315172df731f149927ba7b6e72adf88bde00d13cc7784c717ce1d042cbc3bd8db1549a75fb5c4d586ed1d67fe0129e522f394236b8053513905277b8e930101b0660807598039a4796e66018113fbf3f1703303bb3808779e3613995cb9
q = 0xc313d1a2bf3516a555c54875798a59a3d219ea76179b712886beec177263cec7
g = 0x21ac05c17f3cc476fa34ea77b5e2252e848f2ab35cf4e1f6cc53f15349af6e56f1c5ad36fe7cdf0a00c8162032b623d1271b4f586d26dba704706c32d0cefa01937e82d8af632596e9d27ff10a7cad23766ae97c07bb7dc3b2e24a482ab30c02435c8ce99b0cc356146c371bda04582ee1b40b2f29227ba8225aa490b4bd788662168929fdd2cfbce0e0dc59da3db76651ee91fbc654d36f277003f96ff6b045b2ab5187b0d4024a32281672c606206aebb1f3fe9b75877e38dcd38c73aa588ec01ae3fca344befbdf745a47f7a45b4d06643fea5e4e9b02f763cc5b2e7e8488945b0fe12b56b83a29cbe47ec9d276197d0245d11abc8833f88d114f3a897f81

y =  5624204323708883762857532177093000216929823277043458966645372679201025592769376026088466517180933057673841523705217308006821461505613041092599344214921758292705684588442147606413017270932589190682167865180010809895170865252326994825400330559172774619220024016595462686075240147992717554220738390033531322461011161893179173499597221230442911598574630392043521768535083211677909300720125573266145560294501586465872618003220096582182816143583907903491981432622413089428363003509954017358820731242558636829588468685964348899875705345969463735608144901602683917246879183938340727739626879210712728113625391485513623273477
r1 =  53670875511938152371853380079923244962420018116685861532166510031799178241334
s1 =  6408272343562387170976380346088007488778435579509591484022774936598892550745
r2 =  3869108664885100909066777013479452895407563047995298582999261416732594613401
s2 =  63203374922611188872786277873252648960215993219301469335034797776590362136211


MSG1 = b'Joe made the sugar cookies.'
MSG2 = b'Susan decorated them.'
h1 = int(sha256(MSG1).hexdigest(), 16)
h2 = int(sha256(MSG2).hexdigest(), 16)
r1inv = int(inverse_mod(r1, q))
r2inv = int(inverse_mod(r2, q))

s1inv = int(inverse_mod(s1, q))
s2inv = int(inverse_mod(s2, q))


PR.<k1u, k2l, k> = PolynomialRing(GF(q))

k1 = k1u*2^64 + k
k2 = k*2^64 + k2l

f = r1inv*(k1*s1 - h1) - r2inv*(k2*s2 - h2)
roots = small_roots(f, [2^64, 2^64, 2^64], m=2, d=2)
print(roots)
for root in roots:
	k1u, k2l, k = [int(r) for r in root]
	k1 = k1u*2^64 + k
	k2 = k*2^64 + k2l

	x1 = (r1inv*(k1*s1 - h1)) % q
	x2 = (r2inv*(k2*s2 - h2)) % q

	print(x1)
	print(int(x1).to_bytes(100, "big"))
	print(int(x2).to_bytes(100, "big"))
	print(pow(g, int(x1), p) == y)
	print(pow(g, int(x2), p) == y)

# PR.<k1, k2> = PolynomialRing(GF(q))
# 
# f = r1inv*(k1*s1 - h1) - r2inv*(k2*s2 - h2)
# roots = small_roots(f, [2^128, 2^128], m=2, d=2)
# print(roots)
# for root in roots:
# 	k1, k2 = roots[0]
# 
# 	k1 = int(k1)
# 	k2 = int(k2)
# 	x = (r1inv*(k1*s1 - h1)) % q
# 	x2 = (r2inv*(k2*s2 - h2)) % q
# 	print(x)
# 	print(int(x).to_bytes(100, "big"))
# 	print(int(x2).to_bytes(100, "big"))
# 
# 	print(pow(g, int(x), p) == y)
# # print(pow(g, int(x), q) == y1)
