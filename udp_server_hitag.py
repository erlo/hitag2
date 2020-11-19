#!/usr/bin/python
# -*- coding=utf-8 -*-

################################################################
#                                                              #
# Note: A lancer en meme temps que le programme GRC de capture #
#                                                              #
################################################################

import socket
import binascii
from Queue import Queue
from threading import Thread
import sys

localIP     = "127.0.0.1"
localPort   = 7878
bufferSize  = 1472

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

streamQueue = Queue()

def manchester(mcode):

    i = 0
    v = ""
    code = ""

    b = 0

    for s in mcode:

	if i == 0:
	    i = 1
	    v = "%s" % (s)
	else:

            b = b << 1 

	    i = 0
	    v = "%s%s" % (v,s)
	    if v == "01":
		code = "%s0" % (code)
	    elif v == "10":
		code = "%s1" % (code)
                b |= 1
	    elif v == "00": # Code invalide 00 => _
		code = "%s_" % (code)
	    elif v == "11": # Code invalide 11 => -
		code = "%s-" % (code)
	    else:
		print("erreur")
		return mcode

    return code



def processStream(q):

    messageFlag = False
    i = 0
    frame = ""
    rollcode = ""

    m = 0
    mcode = ""

    while True:

        data = q.get()

        for b in data:

            v = ord(b)

            if v == 1 and messageFlag == False:
                messageFlag = True
                i = 0

            if messageFlag == True:
                i += 1
                
                if i > 512 and i <= 512+228:
                    rollcode = "%s%s" % (rollcode,v)

                    # Permet d'aligner le debug du message
                    if rollcode[-20:] == "11111101010101010101":
                        rollcode = "01010101010101"

                if i >= 1300:
                    data = manchester(rollcode)

                    print("Raw decoded capture: %s" % (data))

                    data_sync = data[0:0+16]
                    data_uid = data[16:16+32]
                    data_btn = data[48:48+4]
                    data_counter = data[52:52+10]
                    data_ks = data[62:62+32]
                    data_pad = data[94:94+2]
                    data_chk = data[96:96+8]

                    # TODO: verif checksum?

                    try:
                        print("UID=%s BTN=%s COUNTER=%s KS=%s" % (hex(int(data_uid,2)), hex(int(data_btn,2)), hex(int(data_counter,2)), hex(int(data_ks,2))))
                    except: # Si pb de decodage des valeurs binaires
                        print("[Decode Error] SYNC=%s UID=%s BTN=%s COUNTER=%s KS=%s PAD=%s CHK=%s" % (data_sync, data_uid, data_btn, data_counter, data_ks, data_pad, data_chk))

                    frame = ""
                    rollcode = ""
                    messageFlag = False
                    i = 0

        sys.stdout.flush()
        q.task_done()

worker = Thread(target=processStream, args=(streamQueue,))
worker.setDaemon(True)
worker.start()

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    streamQueue.put(message)

