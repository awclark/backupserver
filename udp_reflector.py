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

try:
	EchoServer.bind(ADDR)
	print "echo server started"
except Exception:
	print "Echo server failed"

while True:
	data, addr = EchoServer.recvfrom(BUFFER)
	print addr
	addlst = addr[0],REMOTE_PORT

	if REFLECT_SWITCH == 1:
		print 'sending to'
		print addlst
		EchoServer.sendto('%s' % (data), addr)
	splitdata = data.split(',')
	timecount = splitdata[0].strip("('")
	one_way_delay = (time.time() - float(timecount))
	packet_number = str(splitdata[1].strip("' '"))
	packet_number = packet_number.lstrip('0')

	print (time.ctime() + ',' + 'received , '+ packet_number + ' , ' + str(one_way_delay))
