from ecdsa import VerifyingKey
from Crypto.Cipher import AES
from hashlib import sha256
from Crypto.Util.number import long_to_bytes
import sys
from pwn import xor

r  = 0x288b415d6703ba7a2487681b10da092d991a2ef7d10de016daea4444523dc792
s1 = 0xfc00f6d1c8e93beb4c983104f1991e6d1951aa729004b7a1e841f29d12797f4
z1 = 0x9f9b697baa97445b19c6552e13b3a796ec9b76d6d95190a0c7fab01cce59b7fd

s2 = 0x693ee365dd7307a44fddbdd81c0059b5b5f7ef419beee7aaada3c37798e270c5
z2 = 0x465e2cf6b15b701b2d40cac239ab4d50388cd3e0ca54621cff58308f7c9a226b

with open('pub.pem', 'rb') as f:
    vk = VerifyingKey.from_pem(f.read())
    n = vk.curve.order

k = ((z1 - z2) * pow(s1 - s2, -1, n)) % n
d = (((s1 * k) - z1) * pow(r, -1, n)) % n

with open("secret_blob.bin", "rb") as f:
    secret_blob = f.read()

seed = long_to_bytes(d, 32)
keystream = b""
counter = 0
while len(keystream) < len(secret_blob):
    keystream += sha256(seed + counter.to_bytes(4, 'big')).digest()
    counter += 1
flag = xor(secret_blob, keystream)
print(flag)
