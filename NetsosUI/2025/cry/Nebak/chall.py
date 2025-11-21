import random
from random import Random

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

tebakjask = Random()
fakejask = Random()
ngasaljask = 0.8

kuota_efisiensi = 6767

if __name__ == "__main__":
    print(f"Can you guess the numbers? siiixxxx seveeeennnnn")
    ril = tebakjask.getrandbits(32)
    fek = fakejask.getrandbits(32)
    while True:
        print("1. Get random 32-bit number")
        print("2. Advance the generator state")
        print("3. Guess random number")
        choice = input("Choice: ")

        if choice == "1":
            if kuota_efisiensi <= 0:
                print("udah cukup wak")
                continue

            kuota_efisiensi -= 1
            print(ril if random.random() > ngasaljask else fek)

        elif choice == "2":
            print("Advancing...")
            ril = tebakjask.getrandbits(32)
            fek = fakejask.getrandbits(32)

        elif choice == "3":
            for _ in range(50):
                bits = random.randrange(32, 512)
                print(f"Number of bits: {bits}")
                guess = int(input("Your guess: "))
                num = tebakjask.getrandbits(bits)
                if guess != num:
                    print(f"Nope, this was the correct number: {num}")
                    exit()

            print("gg, goodluck ctfnya bang!")
            print(f"Here is your flag: {FLAG}")
            print("Bole share nich buat trophy: ")
            print(f"Total queries used: {6767 - kuota_efisiensi}")
        else:
            exit()
