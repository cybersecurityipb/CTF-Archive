# Nonce Twice, Pay the Price

**Category:** Cryptography  
**Author:** DJ Strigel  
**Solved by:** Ji4xuu

## Description
Someone didn’t follow proper cryptography hygiene!

You intercepted two signatures from the same service, and it looks like they reused the same ECDSA nonce. The signatures are on different messages, but that repeated nonce might just be your golden ticket.

Your mission: recover the private key from the reused nonce and decrypt the flag.

Tip: ECDSA nonce reuse leaks the private key… if you know how to exploit it.

Challenge author: DJ Strigel

## Attachment
- [secret_blob.bin](secret_blob.bin)
- [sig1.txt](sig1.txt)
- [sig2.txt](sig2.txt)
- [pub.pem](pub.pem)

## Solver
[solver](solve.py)

## POC/ Writeup

Solved by Ji4xuu

Step 1, dapetin private key

Karena di deskripsi sudah dimention ECDSA, nonce reuse, maka kita bisa dengan mudah dapetin $k$ sama $d$ nya.

di ECDSA, Signature ($s$) digenerate dengan $s \equiv k^{-1}(z + r \cdot d) \pmod n$ dimana $r = (k \cdot G).x \pmod n$ dengan $G$ adalah generator, $d$ adalah private key, $z=Hash(m)$ dan $n$ adalah order dari kurvanya.

Karena nonce reuse, dari sig1 dan sig2 diperoleh :
1. $s_1 \cdot k \equiv z_1 + r \cdot d \pmod n$
2. $s_2 \cdot k \equiv z_2 + r \cdot d \pmod n$
Kurangkan (1) dan (2) diperoleh :

$$k \equiv (s_1 - s_2)^{-1} (z_1 - z_2) \pmod n$$

Selanjutnya dari (1) diperoleh $d \equiv r^{-1}(s_1 \cdot k - z_1) \pmod n$

Step 2, dukun gimana cara decrypt flagnya
Singkat cerita, curiga yg belum kita pakai adalah secret_blob.bin kemungkinan ini encrypted flag, tapi gimana cara decrypt nya pakai d? singkat cerita dukun, let gemini cook, dan gemini menebak ini adalah xor with keystream, beliau menebak XOR-SHA256-CTR, dimana 
$$K_s = SHA256(d||0) + SHA256(d||0) + ...$$

dan flag = K_s ^ enc. Maka solve

``flag : pctf{ecdsa_n0nc3_r3us7e_get!s_y0u8_0wn1ed}``