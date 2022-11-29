from bitarray import bitarray
from bitarray.util import ba2int


def right_rotate_bits(x, n):
    return ((x >> n) | (x << (32 - n)) & 0xFFFFFFFF) & 0xffffffff


def get_last_64_bits(len):
    """This function is used to get 64 bits representing length of message"""
    last64 = bitarray()
    last64.frombytes((len).to_bytes(8, byteorder="big"))
    return last64


def sha2hash(msg):
    m_copy = msg
    h0 = 0x6A09E667
    h1 = 0xBB67AE85
    h2 = 0x3C6EF372
    h3 = 0xA54FF53A
    h4 = 0x510E527F
    h5 = 0x9B05688C
    h6 = 0x1F83D9AB
    h7 = 0x5BE0CD19

    # Constants
    k = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2]

    # This block of code is used for encoding message to bits
    if isinstance(msg, str):
        ba = bitarray()
        ba.frombytes(msg.encode('utf-8'))
        ml = len(ba)
        msg = ba
    else:
        msg = bitarray(bin(msg)[2:])
        ml = len(msg)

    blocks = []  # This variable is used to store 512-bit blocks of message

    # this block of code is used to separate message in 512-bit block and preprocessing message
    while True:
        if len(msg) >= 512:
            blocks.append(msg[:512])
            msg = msg[512:]
        if 447 < len(msg) < 512:
            block1 = msg
            block1 += bitarray("1")
            while len(block1) < 512:
                block1 += bitarray("0")
            blocks.append(block1)
            block2 = bitarray()
            while len(block2) != 448:
                block2 += bitarray("0")
            last64 = get_last_64_bits(ml)
            block2 += last64
            blocks.append(block2)
            break
        if 447 >= len(msg):
            msg += bitarray("1")
            while len(msg) < 448:
                msg += bitarray("0")
            last64 = get_last_64_bits(ml)
            msg += last64
            blocks.append(msg)
            break

    # Breaking each block in 16 32-bit chunks
    for block in blocks:
        chunks = []
        for j in range(0, 512, 32):
            chunks.append(ba2int(block[j: j + 32]))

        # Generating additional 48 words
        for j in range(16, 64):
            s0 = (right_rotate_bits(chunks[j-15], 7)) ^ (right_rotate_bits(chunks[j-15], 18)) ^ (chunks[j - 15] >> 3)
            s1 = (right_rotate_bits(chunks[j-2], 17)) ^ (right_rotate_bits(chunks[j-2], 19)) ^ (chunks[j-2] >> 10)
            chunks.append((chunks[j-16] + s0 + chunks[j-7] + s1) & 0xffffffff)

        # Main cycle
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        for i in range(64):
            e0 = right_rotate_bits(a, 2) ^ right_rotate_bits(a, 13) ^ right_rotate_bits(a, 22)
            Ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (e0 + Ma) & 0xffffffff
            e1 = right_rotate_bits(e, 6) ^ right_rotate_bits(e, 11) ^ right_rotate_bits(e, 25)
            ch = (e & f) ^ ((~e) & g)
            t1 = (h + e1 + ch + k[i] + chunks[i]) & 0xffffffff

            h = g
            g = f
            f = e
            e = (d + t1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xffffffff
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff

    hash = (h0 << 224) | (h1 << 192) | (h2 << 160) | (h3 << 128) | (h4 << 96) | (h5 << 64) |(h6 << 32) | h7
    print(f"SHA2-256 hash of \'{m_copy}\' = {hex(hash)[2:]}")

sha2hash("The quick brown fox jumps over the lazy dog")