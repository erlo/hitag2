#!/usr/bin/python
# -*- coding=utf-8 -*-

###################################################################################################
# Ce programme permet de générer tous les symboles 0 et 1 a transmettre sur la sortie standard
# Usage: python %s <uid> <counter> <button> <keystream>
###################################################################################################

import sys

def manchester(code):

    mcode = ""

    for b in code:
        if b == "0":
            mcode = "%s%s" % (mcode, "01")
        elif b == "1":
            mcode = "%s%s" % (mcode, "10")
        else:
            return "ERREUR"

    return mcode

def checksum(data):
    # Calcul d'un XOR bit a bit sur les 10 octets
    checksum = ""
    for b in range(8):
        chk = 0
        for i in range(10):
            chk ^= int(data[i*8+b])
        checksum = "%s%s" % (checksum, chk)
    return(checksum)

if __name__ == "__main__":

    import sys

    if len(sys.argv) == 5:

	preambule_sync = "01"*256

	preambule_msg = "0"*12 + "1"*8

	sync = "{0:016b}".format(1)
	uid = "{0:032b}".format(int(sys.argv[1],16))
	btn = "{0:04b}".format(int(sys.argv[3],16))
	cnt = "{0:010b}".format(int(sys.argv[2],16))
	key = "{0:032b}".format(int(sys.argv[4],16))
	sep = "10"
	chk = checksum(uid+btn+cnt+key+sep)
	frame = manchester(sync+uid+btn+cnt+key+sep+chk)
	framefin = manchester(sync+cnt)

	print(preambule_sync+preambule_msg+frame+preambule_msg+frame+preambule_msg+frame+preambule_msg+framefin)
    else:
        print(("Usage: python %s <uid> <counter> <button> <keystream>") % sys.argv[0])


