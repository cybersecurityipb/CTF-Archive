# --- 1. DATA DARI SOAL ---
# Ciphertext diambil dari xxd yang kamu kasih
hex_cipher = "6caad8c8a40848f200009de6c7344c7b9c03f5bebca962193aef4a84ad397a99ff04f4"
ciphertext = bytes.fromhex(hex_cipher)

# Leaked states dari file (copy paste semua angka tadi)
leaked_states = [
    2694419740, 2430555337, 3055882924, 228605358, 4055459295, 
    676741477, 1030306057, 1320993926, 2317712498, 3680836913, 
    1922319333, 1836782265, 1490734773, 218490631, 4065897775, 
    3125259028, 189241330, 1710684784, 2355890305, 95797196, 
    813001417, 1021781706, 3522243094, 1603928614, 1122416469, 
    4125638785, 2423341845, 3666529189, 61609182, 2391267942, 
    148130332, 4246509548, 3552866507, 1487751530, 1895017353, 
    3277260507, 4251037246, 22647618, 3958787364, 227107204
]

# --- 2. DECRYPT ---
# Aturan: Keystream = Lowest byte (8 bit terakhir) dari State
keystream = [state & 0xFF for state in leaked_states]

flag = ""
# Kita zip ciphertext dengan keystream. 
# Kalau keystream lebih panjang, dia otomatis berhenti pas cipher abis.
for c, k in zip(ciphertext, keystream):
    flag += chr(c ^ k)

print(f"FLAG: {flag}")