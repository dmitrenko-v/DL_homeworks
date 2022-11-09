def key_addition(key, l):
    i = 0
    while len(key) != l:
        key += key[i]
        i += 1
    return key


def vigenere_encode(M, key):
    ciphertext = ""
    m = len(M)
    if m != len(key):
        key = key_addition(key, m)
    for j in range(m):
        ciphertext += chr(((ord(M[j]) + ord(key[j])) % 26) + ord('A'))
    return ciphertext


def vigenere_decode(C, key):
    plaintext = ""
    m = len(C)
    if m != len(key):
        key = key_addition(key, m)
    for j in range(m):
        plaintext += chr(((ord(C[j]) - ord(key[j])) % 26) + ord('A'))
    return plaintext

