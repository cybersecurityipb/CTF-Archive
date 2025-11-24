#!/usr/bin/env python3
from pwn import *
import string
import base64
import bcrypt
import concurrent.futures
import multiprocessing

context.log_level = 'error'

# Konfigurasi Target
HOST = '18.212.136.134'
PORT = 6666
_STATIC_SALT = b"$2b$12$C8YQMlqDyz3vGN9VOGBeGu"

# --- FUNGSI WORKER (Jalan di tiap Core CPU) ---
def check_candidate(args):
    candidate, target_hash = args
    payload = candidate.encode('utf-8')
    portion = payload[: len(payload) % 256]
    digest = bcrypt.hashpw(portion, _STATIC_SALT)
    generated_hash = f"vb$1${base64.b64encode(digest).decode()}"
    
    if generated_hash == target_hash:
        return candidate
    return None

def solve_level_1_parallel(io):
    print(f"[1] Level 1: Recovering via Parallel Bruteforce (Using {multiprocessing.cpu_count()} Cores)...")
    
    io.recvuntil(b"Leaked Note: ")
    leak = io.recvline().strip().decode()
    io.recvuntil(b"Target Hash: ")
    target_hash = io.recvline().strip().decode()
    
    charset = string.ascii_letters + string.digits
    
    candidates = []
    print("    [*] Generating candidate list...", end="\r")
    for c1 in charset:
        for c2 in charset:
            candidates.append((leak + c1 + c2, target_hash))
            
    print(f"    [*] Cracking {len(candidates)} hashes. Please wait...")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(check_candidate, candidates, chunksize=50)
        
        for res in results:
            if res:
                print(f"    [+] FOUND SECRET: {res[-2:]} (Full: {res[:20]}...)")
                io.sendlineafter(b"Enter password: ", res.encode())
                return True

    print("    [-] Failed to recover.")
    return False

def main():
    print(f"[*] Target: {HOST}:{PORT}")
    
    # Loop Retry untuk Level 5 RNG
    while True:
        try:
            io = process(["python3", "vibe_vault.py"])
            #io = remote(HOST, PORT) # Ganti ke process() kalau mau test lokal
        except:
            print("[-] Connection error. Retrying...")
            continue

        try:
            # LEVEL 1 (PARALLEL)
            import time
            start_time = time.time()
            if not solve_level_1_parallel(io):
                io.close()
                continue
            
            end_time = time.time()
            print(f"    [*] Level 1 solved in {end_time - start_time:.2f} seconds.")
            # LEVEL 2
            print("[2] Level 2: Empty Hash Collision...")
            io.recvuntil(b"prefix: '")
            prefix = io.recvuntil(b"'").strip(b"'").decode()
            p1 = prefix + "A" * (256 - len(prefix))
            p2 = prefix + "B" * (512 - len(prefix))
            io.sendlineafter(b"Format: string1,string2", f"{p1},{p2}".encode())
            if b"ACCESS DENIED" in io.recvline(): raise ValueError("L2 Failed")

            # LEVEL 3
            print("[3] Level 3: Modulo Truncation...")
            io.recvuntil(b"very long (")
            target_len = int(io.recvuntil(b" ").strip())
            io.sendlineafter(b"equivalent password: ", ("B" * (target_len % 256)).encode())
            if b"ACCESS DENIED" in io.recvline(): raise ValueError("L3 Failed")

            # LEVEL 4
            print("[4] Level 4: Smart Truncation...")
            io.recvuntil(b"The target password is: ", timeout=3)
            line = io.recvline().decode()
            pad_len = int(line.split("'C'")[0].strip())
            emoji_count = int(line.split("+")[1].strip().split("'")[0])
            full_target = ("C" * pad_len) + ("🔥" * emoji_count)
            io.sendlineafter(b"Enter password: ", full_target.encode()[:72])
            
            # LEVEL 5 (RNG Check)
            print("[5] Level 5: Prefix Attack...")
            check_l4 = io.recvline()
            if b"ACCESS DENIED" in check_l4: raise ValueError("L4 Failed")
            
            io.recvuntil(b'ID: "')
            prefix_l5 = io.recvuntil(b'"').strip(b'"').decode()
            io.recvuntil(b"SecretPassword: ")
            admin_len = int(io.recvuntil(b" ").strip())
            
            if (len(prefix_l5) + admin_len) % 256 > len(prefix_l5):
                print("    [-] Bad RNG for Level 5. Retrying connection...")
                io.close()
                continue
                
            io.sendlineafter(b"Input your password:", ("A" * admin_len).encode())
            
            # FINAL
            res = io.recvall(timeout=3).decode()
            if "CONGRATULATIONS" in res:
                print("\n" + "="*50)
                print("🔥 FLAG: " + res.split("reward: ")[1].split("\n")[0])
                print("="*50)
                break
                
        except Exception as e:
            # print(f"Err: {e}")
            io.close()
            continue

if __name__ == "__main__":
    # Multiprocessing support for Windows/macOS safety
    multiprocessing.freeze_support()
    main()