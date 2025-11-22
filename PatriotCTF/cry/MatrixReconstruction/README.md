# Matrix Reconstruction

**Category:** Cryptography  
**Author:** DJ Strigel  
**Solved by:** Ji4xuu

## Description
Someone’s been messing with your secure communication channel… and they’ve left traces!

You’ve intercepted a mysterious ciphertext and a series of leaked internal states from a rogue pseudorandom generator. It seems the generator is powered by a secret 32×32 matrix A and an unknown 32-bit vector B.

Your mission: reverse-engineer the system! Use the leaked states to reconstruct the hidden matrix, uncover the XOR constant, and decrypt the message. Only then will the true flag reveal itself.

Remember: the keystream bytes come from the lowest byte of each internal state. Pay attention to the details.

Challenge author: DJ Strigel

## Attachment
- [cipher.txt](cipher.txt)
- [keystream_leak.txt](keystream_leak.txt)
- [README.txt](README.txt)

## Solver
[solver](solve.py)

## POC/ Writeup

Solved by Ji4xuu

Karena dari deskripsi kita dikasih tahu bahwa "he keystream bytes come from the lowest byte of each internal state. Pay attention to the details.", dan kita dapat 40 internal states, dan ketika kita coba reconstruct keystreamnya dari leaked_keystream ini cukup dan diperoleh format flag, maka here we go, ga pelru diapa-apain, tinggal xor aja.

``flag : pctf{mAtr1x_r3construct?on_!s_fu4n}``