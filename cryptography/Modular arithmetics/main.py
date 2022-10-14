import random


def nsd(a, b):
    if a == 0:
        return b
    while b != 0:
        if a > b:
            a -= b
        else:
            b -= a
    return a


def is_prime(x):
    for i in range(2, x):
        if x % i == 0:
            return False
    return True


def euler_func(a):
    res = 0
    for i in range(1, a + 1):
        if nsd(a, i) == 1:
            res += 1
    return res


def mod(a, m):
    return a % m


def mod_with_exp(a, b, m):
    return (a**b) % m


def find_reverse(a, b, m):
    d = nsd(a, m)
    if b % d != 0:
        print("Нема рішень")
        return
    if d == 1:
        return (b * a**(euler_func(m) - 1)) % m
    else:
        m1 = int(m / d)
        x = (b * a**(euler_func(m1) - 1)) % m1
        return [x, x + m1]


def generate_random_prime(A, B):
    primes = [x for x in range(A, B+1) if is_prime(x)]
    return random.choice(primes)


while True:
    m = int(input("Введіть модуль m: "))
    print("1.Розв`язати рівняння a mod m = x\n2.Розв`язати рівняння виду a^b mod m = x\n3.Розв`язати рівняння a*х"
          " = b mod m\n4.Сгенерувати просте число у діапазоні від А до В")
    choice = input("Оберіть бажану операцію(1-4):")
    if choice == "1":
        a = int(input("Введіть параметр a: "))
        print(f"{a} mod {m} = {mod(a, m)}")
    if choice == "2":
        a = int(input("Введіть параметр a: "))
        b = int(input("Введіть параметр b: "))
        print(f"{a}^{b} mod {m} = {mod_with_exp(a, b, m)}")
    if choice == "3":
        a = int(input("Введіть параметр a: "))
        b = int(input("Введіть параметр b: "))
        x = find_reverse(a, b, m)
        print(f"x = {x}")
    if choice == "4":
        a = int(input("Введіть параметр A: "))
        b = int(input("Введіть параметр B: "))
        print(f"Просте число у діапазоні від А до В: {generate_random_prime(a, b)}")