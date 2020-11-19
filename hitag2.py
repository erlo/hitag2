#!/usr/bin/env python
# -*- coding=utf-8 -*-

######################################################################################
# Implémentation de Hitag2: calcul du code authentifiant (KeyStream)
# à partir d'une clé, UID, compteur et code bouton
#
# Usage: python %s <key> <uid> <counter> <button>
######################################################################################


"""
HITAG2 cipher
Implemented by Aram Verstegen
Source: https://github.com/factoritbv/hitag2hell
"""

def i4(x, a, b, c, d):
    return (((x >> a) & 1)*8)+((x >> b) & 1)*4+((x >> c) & 1)*2+((x >> d) & 1)


def f20_4(state):
    return ((0x3c65 >> i4(state,34,43,44,46)) & 1)

def f20_3(state):
    return (( 0xee5 >> i4(state,28,29,31,33)) & 1)

def f20_2(state):
    return (( 0xee5 >> i4(state,17,21,23,26)) & 1)

def f20_1(state):
    return (( 0xee5 >> i4(state, 8,12,14,15)) & 1)

def f20_0(state):
    return ((0x3c65 >> i4(state, 2, 3, 5, 6)) & 1)

def f20_last(s0,s1,s2,s3,s4):
    return (0xdd3929b >> ((s0 * 16)
                        + (s1 *  8)
                        + (s2 *  4)
                        + (s3 *  2)
                        + (s4 *  1))) & 1

def f20(state):
    return f20_last(f20_0(state), f20_1(state), f20_2(state), f20_3(state), f20_4(state))

def lfsr_bs(state, i):
    return (state[i+ 0] ^ state[i+ 2] ^ state[i+ 3] ^ state[i+ 6] ^
            state[i+ 7] ^ state[i+ 8] ^ state[i+16] ^ state[i+22] ^
            state[i+23] ^ state[i+26] ^ state[i+30] ^ state[i+41] ^
            state[i+42] ^ state[i+43] ^ state[i+46] ^ state[i+47])

def f20a_bs(a,b,c,d):
    return (~(((a|b)&c)^(a|d)^b)) # 6 ops
def f20b_bs(a,b,c,d): 
    return (~(((d|c)&(a^b))^(d|a|b))) # 7 ops
def f20c_bs(a,b,c,d,e):
    return (~((((((c^e)|d)&a)^b)&(c^b))^(((d^e)|a)&((d^b)|c)))) # 13 ops

def filter_bs(state, i):
    return (f20c_bs( f20a_bs(state[i+ 2],state[i+ 3],state[i+ 5],state[i+ 6]),
                     f20b_bs(state[i+ 8],state[i+12],state[i+14],state[i+15]),
                     f20b_bs(state[i+17],state[i+21],state[i+23],state[i+26]),
                     f20b_bs(state[i+28],state[i+29],state[i+31],state[i+33]),
                     f20a_bs(state[i+34],state[i+43],state[i+44],state[i+46])))

def hitag2_init(key, uid, counter, button):

    nonce = counter << 4
    nonce |= button

    state = 0

    for i in range(32, 48):
        state = (state << 1) | ((key >> i) & 1)
    for i in range(0, 32):
        state = (state << 1) | ((uid >> i) & 1)
    for i in range(0, 32):
        nonce_bit = (f20(state) ^ ((nonce >> (31-i)) & 1))
        state = (state >> 1) | (((nonce_bit ^ (key >> (31-i))) & 1) << 47)

    return state

def lfsr_feedback(state):
    return (((state >>  0) ^ (state >>  2) ^ (state >>  3)
            ^ (state >>  6) ^ (state >>  7) ^ (state >>  8)
            ^ (state >> 16) ^ (state >> 22) ^ (state >> 23)
            ^ (state >> 26) ^ (state >> 30) ^ (state >> 41)
            ^ (state >> 42) ^ (state >> 43) ^ (state >> 46)
            ^ (state >> 47)) & 1)
def lfsr(state):
    return (state >>  1) + (lfsr_feedback(state) << 47)

def hitag2(state, length=48):
    c = 0
    for i in range(0, length):
        c = (c << 1) | f20(state)
        state = lfsr(state)
    return c

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 5:
        key = int(sys.argv[1], 16)
        uid = int(sys.argv[2], 16)
        counter = int(sys.argv[3], 16)
        button = int(sys.argv[4], 16)
        state = hitag2_init(key, uid, counter, button)
        print('KEYSTREAM = %08X' % (hitag2(state, 32)))
    else:
        print(("Usage: python %s <key> <uid> <counter> <button>") % sys.argv[0])
