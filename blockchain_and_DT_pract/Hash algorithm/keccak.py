import numpy as np
from bitarray import bitarray
from bitarray.util import ba2int

# r and c parameters for SHA-256
r = 1088
c = 512
w = 64

r_shifts = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
RC = np.zeros(24, dtype=object)


RC[0] = 0x0000000000000001
RC[1] = 0x0000000000008082
RC[2] = 0x800000000000808A
RC[3] = 0x8000000080008000
RC[4] = 0x000000000000808B
RC[5] = 0x0000000080000001
RC[6] = 0x8000000080008081
RC[7] = 0x8000000000008009
RC[8] = 0x000000000000008A
RC[9] = 0x0000000000000088
RC[10] = 0x0000000080008009
RC[11] = 0x000000008000000A
RC[12] = 0x000000008000808B
RC[13] = 0x800000000000008B
RC[14] = 0x8000000000008089
RC[15] = 0x8000000000008003
RC[16] = 0x8000000000008002
RC[17] = 0x8000000000000080
RC[18] = 0x000000000000800A
RC[19] = 0x800000008000000A
RC[20] = 0x8000000080008081
RC[20] = 0x8000000080008081
RC[21] = 0x8000000000008080
RC[22] = 0x0000000080000001
RC[23] = 0x8000000080008008


def right_rotate_bits(x, n):
    return (x >> n) | (x << (64 - n)) & bitarray(bin(0xFFFFFFFFFFFFFFFF)[2:])


def Round(A, RC_value):
    C = [bitarray("0"*64)] * 5
    D = [bitarray("0"*64)] * 5
    B = [[bitarray("0"*64)] * 5] * 5

    # θ step
    for x in range(5):
        C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]
        D[x] = C[(x - 1) % 5] ^ right_rotate_bits(C[(x + 1) % 5], 1)
    for x in range(5):
        for y in range(5):
            A[x][y] = A[x][y] ^ D[x]

    # ρ and π steps
    for x in range(5):
        for y in range(5):
            B[y][(2 * x + 3 * y) % 5] = right_rotate_bits(A[x][y], r_shifts[x][y])

    # χ step
    for x in range(5):
        for y in range(5):
            A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])

    # ι step
    ba_RC = bitarray("0" * (64-len(bin(RC_value)[2:]))) + bitarray(bin(RC_value)[2:])
    A[0][0] = A[0][0] ^ ba_RC
    return A


def keccak_f(A):
    for i in range(24):
        A = Round(A, RC[i])
    return A


def keccak(M):
    M_copy = M
    # encoding message to bits
    if isinstance(M, str):
        ba = bitarray()
        ba.frombytes(M.encode('utf-8'))
        ml = len(ba)
        M = ba
    else:
        M = bitarray(bin(M)[2:])
        ml = len(M)

    Mbytes = int(ml / 8)
    if Mbytes < r/8:
        M += bitarray("00000110") # 0x06
        while len(M) < r:
            M += bitarray("00000000")
    M = M ^ (bitarray("0" * (r-8)) + bitarray("10000000"))
    print(M)
    # Absorbing
    blocks = []
    for j in range(0, len(M), r):
        blocks.append(M[j: j+r])

    S = [[bitarray("0"*64)] * 5] * 5
    for block in blocks:
        block_arr = []
        for j in range(0, len(block), 64):
            block_arr.append(block[j:j+64])
        for x in range(5):
            for y in range(5):
                if x+5*y < r/w:
                    S[x][y] = S[x][y] ^ block_arr[x+5*y]
        print(S)
        S = keccak_f(S)

    # Squeezing
    Z = bitarray()
    while len(Z) < 256:
        for x in range(5):
            for y in range(5):
                if x+5*y < r/w:
                    Z += S[x][y]
                    S = keccak_f(S)
    Z = Z[:256]
    print(f"Keccak(SHA3-256) hash of \'{M_copy}\' = {hex(ba2int(Z))[2:]}")

keccak("")