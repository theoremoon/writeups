package main

import (
	"crypto/cipher"
	"crypto/des"
	"crypto/sha256"
	"encoding/hex"
	"log"
)

const seed = "secret_sauce_#9"

func keygen(s []byte) [][]byte {
	keys := make([][]byte, 2020)
	for i := 0; i < len(keys); i++ {
		s2 := sha256.Sum256(s)
		keys[i] = s2[:]
		s = s2[:]
	}
	return keys
}

func scramble(src int) []int {
	stream := make([]int, 10)
	for i := 0; i < 10; i++ {
		stream[i] = src & 3
		src = src / 4
	}
	stream2 := make([]int, 0)
	for i := 0; i < 101; i++ {
		for _, j := range stream {
			stream2 = append(stream2, j)
		}
	}
	return stream2
}

func encrypt(keys [][]byte, src int, m []byte) []byte {
	dk := scramble(src)
	encrypted := make([]byte, len(m))
	msg := m[:]
	for i, key := range keys {
		idx := dk[i]
		k := key[idx*8 : (idx+1)*8]
		b, err := des.NewCipher(k)
		if err != nil {
			panic(err)
		}
		encrypter := cipher.NewCBCEncrypter(b, make([]byte, 8))
		encrypter.CryptBlocks(encrypted, msg)
		msg = encrypted[:]
	}
	return msg
}

func decrypt(keys [][]byte, src int, c []byte) []byte {
	dk := scramble(src)
	rev_keys := make([][]byte, 0)
	for i, key := range keys {
		idx := dk[i]
		k := key[idx*8 : (idx+1)*8]
		rev_keys = append(rev_keys, k)
	}

	decrypted := make([]byte, len(c))
	msg := c
	for i := len(rev_keys) - 1; i >= 0; i-- {
		k := rev_keys[i]
		b, err := des.NewCipher(k)
		if err != nil {
			panic(err)
		}
		decrypter := cipher.NewCBCDecrypter(b, make([]byte, 8))
		decrypter.CryptBlocks(decrypted, msg)
		msg = decrypted[:]
	}
	return msg
}

func main() {
	keys := keygen([]byte(seed))

	m := []byte("Attack at DAWN!!")
	c := []byte("\x15\x08\x54\xff\x3c\xf4\xc4\xc0\xd2\x3b\xd6\x8a\x82\x34\x83\xbe")

	table := make(map[string]int)
	for a := 0; a < 65536; a++ {
		s := a*16 + 0xe
		encrypted := encrypt(keys[:len(keys)/2], s, m)
		table[hex.EncodeToString(encrypted)] = s
		if a%256 == 0 {
			log.Printf("Progress1: %d/255\n", a/256)
		}
	}

	for a := 0; a < 65536; a++ {
		s := 0xa*65536 + a
		decrypted := decrypt(keys[len(keys)/2:len(keys)], s, c)
		if s1, exists := table[hex.EncodeToString(decrypted)]; exists {
			log.Printf("Found: %d %d\n", s1, s)
		}
		if a%256 == 0 {
			log.Printf("Progress2: %d/255\n", a/256)
		}
	}

}
