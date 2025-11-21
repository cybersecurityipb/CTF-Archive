from pwn import *
from randcrack import RandCrack

#r = process(["python3", "chall.py"])
r = remote("ctf.netsos.id", 7102)
def send_1():
    r.recvline()
    r.recvline()
    r.recvline()
    r.sendlineafter(b'Choice: ', b'1')
    num = r.recvline().strip().decode()
    return int(num)

def send_2():
    r.recvline()
    r.recvline()
    r.recvline()
    r.sendlineafter(b'Choice: ', b'2')
    r.recvline()


rc = RandCrack()

print("[*] Here we go...")

rill = []
def solve():
    r.recvline()
    query_used =  0
    for i in range(640):
        rc_data = []
        rc_count = [0, 0]
        count = 0
        while True:
            val = send_1()
            query_used += 1
            if val not in rc_data:
                count += 1
                rc_data.append(val)
            rc_count[rc_data.index(val)] += 1
            if count == 2 and abs(rc_count[0] - rc_count[1]) >= 5:
                break
        ril_val = rc_data[0] if rc_count[0] < rc_count[1] else rc_data[1]
        if i < 624:
            rc.submit(ril_val)
        rill.append(ril_val)
        if i < 623:
            send_2()
        print(f"[*] Collected {i+1}/624 states. {query_used}/6767 query used")

solve()

r.sendline(b'3')

for i in range(50):
    r.recvuntil(b'Number of bits: ')
    bits = int(r.recvline().strip())

    guess = rc.predict_getrandbits(bits)
    
    print(f"[Guess {i+1}/50] Bits: {bits} -> {guess}")
    r.sendlineafter(b'Your guess: ', str(guess).encode())

r.interactive()

