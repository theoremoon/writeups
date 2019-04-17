# '*' in FLAGs are eaten by worm
# THE CORRECT FLAG DOESN'T INCLUDE THE CHARACTER '*'s

require "openssl"

p1 = OpenSSL::BN::generate_prime(512)
q1 = OpenSSL::BN::generate_prime(512)
n = p1 * q1
e = OpenSSL::BN.new("3")
d = e.mod_inverse((p1-1) * (q1-1))
puts n
puts e
puts

# flag 1
FLAG1 = "FLAG_300{***0513a1db877145db49b38f80f8fe7a6c6c9912b67d6a9a6d2c8dada7e15e}"
plain1 = OpenSSL::BN.new(FLAG1.unpack("H*")[0].to_i(16))
cipher1 = plain1.mod_exp(e,n)
puts cipher1.to_s(16).downcase
puts FLAG1 == [cipher1.mod_exp(d,n).to_s(16)].pack("H*")
puts

# flag 2
FLAG2 = "FLAG_500{Copper is ****************************** Cu (from Latin: cuprum) and atomic number 29.}"
plain2 = OpenSSL::BN.new(FLAG2.unpack("H*")[0].to_i(16))
cipher2 = plain2.mod_exp(e,n)
puts cipher2.to_s(16).downcase
puts FLAG2 == [cipher2.mod_exp(d,n).to_s(16)].pack("H*")
puts
