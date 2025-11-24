from pwn import xor

with open("keystream_leak.txt", "r") as f:
    lines = f.readlines()

with open("cipher.txt", "rb") as f:
    ciphertext = f.read()

leaked_states = [int(line.strip()) for line in lines]
keystream = [state & 0xFF for state in leaked_states]

flag = xor(ciphertext, bytes(keystream))
print(flag)