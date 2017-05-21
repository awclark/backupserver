# Created by Angus Clark on the 2/2/2017
# Final update by Angus Clark on the 21/5/2017

import socket
import time
import sys

REFLECTOR_HOST = ''
REFLECTOR_PORT = 5209
REMOTE_PORT = 54321
REFLECT_SWITCH = 1 # 1 for reflection enabled
BUFFER = 4096

ADDR = (REFLECTOR_HOST, REFLECTOR_PORT)

EchoServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the server to the client
try:
	EchoServer.bind(ADDR)
	print "echo server started"
except Exception:
	print "Echo server failed"

while True:
	data, addr = EchoServer.recvfrom(BUFFER)
	print addr
	addlst = addr[0],REMOTE_PORT
	# Return the packet to the sender
	if REFLECT_SWITCH == 1:
		print 'sending to'
		print addlst
		EchoServer.sendto('%s' % (data), addr)

