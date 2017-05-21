# Created by Angus Clark 11/10/2016

# This is a veraition of the variable bit rate download module, it instead send downstream packets with a CBR

import socket
import time

BUFFER = 4096
HOST = ''
PORT = 5203

ADDR = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	sock.bind(ADDR)
	print "server started"
except Exception:
	print "ERROR"

while True:
	data, addr = sock.recvfrom(BUFFER)
	time.sleep(1)
	splitdata = data.split(',')
	
	packet_size =  int(splitdata[0])
	no_of_packets = int(splitdata[1])
	packets_per_second = int(splitdata[2])
	
	IDT = 1./packets_per_second
	
	padding = ''
	for j in range(78,packet_size):
		padding = padding + str(1)
	for i in range(1, no_of_packets+1):
		time.sleep(IDT)
		snt_time = time.time()
		command = str(i) + ',' + str(snt_time) + ',' padding
		sock.sendto(command, addr)	
