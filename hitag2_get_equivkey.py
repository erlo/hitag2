#!/usr/bin/env python
# -*- coding=utf-8 -*-

######################################################################################
# Recherche de la clé équivalente pour un UID, compteur, bouton et LFSR définis
# Usage: python %s <uid> <counter> <button> <initstate>
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
    return (0xdd3929b >> ((s0 * 16) + (s1 *  8) + (s2 *  4) + (s3 *  2) + (s4 *  1))) & 1

def f20(state):
    return f20_last(f20_0(state), f20_1(state), f20_2(state), f20_3(state), f20_4(state))

###############################################################################################

def hitag2_get_equivkey(uid, counter, button, lfsr_initstate):

    state = 0
    equivKey = 0

    # Initialisation des 16 bits connus de la clé a partir du cipher d'init
    for i in range(0, 16):
        state = (state << 1) | ((lfsr_initstate >> (32+i)) & 1)
        equivKey = (equivKey << 1) | ((lfsr_initstate >> (47-i)) & 1)

    for i in range(0, 32):
        state = (state << 1) | ((uid >> i) & 1)

    # Boucle sur les 18 bits de l'IV qui contiennent le COUNTER_HIGH qui n'est pas transmis:
    for i in range(0, 18):

        # Retour de la fonction F
        f = f20(state) & 1

        # CipherState
        c = lfsr_initstate >> (31-i) & 1 

        # Calcul du nonce (IV^KEY) n:
        n = f ^ c

        equivKey = (equivKey << 1) | (n & 1)

        state = (state >> 1) | ((lfsr_initstate >> (31-i) & 1) << 47)

    # Boucle sur les 10 de COUNTER_LOW et les 4 bits du code bouton
    for i in range(0, 14):

        nonce = counter << 4
        nonce |= button

        # Retour de la fonction F
        f = f20(state) & 1

        # CipherState
        c = lfsr_initstate >> (13-i) & 1 

        # Calcul de la cle (IV^KEY) n:
        n = f ^ c

        # Calcul de la cle final:
        k = n ^ ((nonce >> (13-i)) & 1)

        equivKey = (equivKey << 1) | (k & 1)

        state = (state >> 1) | ((lfsr_initstate >> (13-i) & 1) << 47)

    return equivKey

if __name__ == "__main__":

    import sys

    if len(sys.argv) == 5:

        uid = int(sys.argv[1], 16)
        counter = int(sys.argv[2], 16)
        button = int(sys.argv[3], 16)
        initstate = int(sys.argv[4], 16)

        equivKey = hitag2_get_equivkey(uid, counter, button, initstate)

        print 'KEY => %012X' % (int("{0:048b}".format(equivKey),2))

    else:
        print("Usage: python %s <uid> <counter> <button> <initstate>" % sys.argv[0])
