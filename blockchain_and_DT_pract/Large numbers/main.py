from random import randint
from datetime import datetime

n = 8
key_num = {}  # this variable is used to store data in format {N: number of possible keys of N bits}
for i in range(10):
    key_num[n] = 2 ** n
    print(f"Number of {n}-bit keys:", key_num[n])
    n *= 2
print()


def gen_random_key(bits):
    """This function generates random key of {bits} bits"""
    return hex(randint(0, key_num[bits] - 1))


n = 8
random_keys = {}  # this variable is used to store data in format {N: random generated N-bit key}
for j in range(10):
    random_keys[n] = gen_random_key(n)
    print(f"Randomly generated {n}-bit key:", random_keys[n])
    n *= 2


def bruteforce(key):
    """This function is used to brute force key value and measure time for brute force in milliseconds"""
    start_value = 0
    start_time = datetime.now()
    while hex(start_value) != key:
        start_value += 1
    end_time = datetime.now()
    delta = end_time - start_time
    print("\nTime needed to brute force in milliseconds:", delta.total_seconds() * 1000, "\nThe key is:",
          hex(start_value))


n = 8
for i in range(10):
    bruteforce(random_keys[n])
    n *= 2

