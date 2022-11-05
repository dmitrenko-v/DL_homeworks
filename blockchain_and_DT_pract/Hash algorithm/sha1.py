from bitarray import bitarray
from bitarray.util import ba2int


def get_last_64_bits(len):
    """This function is used to get 64 bits representing length of message"""
    last64 = bitarray()
    last64.frombytes((len).to_bytes(8, byteorder="big"))
    return last64


def leftrotate(x, n):
    """This function is used for left rotate bits operation"""
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def sha1hash(msg):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    msg_copy = msg
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
            chunks.append(ba2int(block[j: j+32]))

        # adding more chunks(up to 80)
        for j in range(16, 80):
            chunks.append(leftrotate(chunks[j - 3] ^ chunks[j - 8] ^ chunks[j - 14] ^ chunks[j - 16], 1))

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # Main loop(Rounds)
        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            tmp = (leftrotate(a, 5) + f + e + k + chunks[i]) & 0xffffffff
            e = d
            d = c
            c = leftrotate(b, 30)
            b = a
            a = tmp
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    hash = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    print(f"SHA-1 hash of {msg_copy} = {hex(hash)[2:]}")






