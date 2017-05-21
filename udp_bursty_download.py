# Created by Angus Clark 4/11/2016 for TN2 
# Final update by Angus Clark 21/5/2017

# This module will send a stream of packets back to the sender in a bursty form
# For more details see the final report on TN2 'NetHealth' solution

import socket
import time
import numpy

BUFFER = 4096
HOST = ''
PORT = 5206

ADDR = (HOST, PORT)
# Set up socket for test
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# min backoff is the median (xm) in the pareto distribution for on/off backoff
backoff_min = 0.002
# Check to see if the socket is able to be bound to
try:
	sock.bind(ADDR)
	print "server started"
except Exception:
	print "ERROR"

while True:
	data, addr = sock.recvfrom(BUFFER)
	time.sleep(1)
	splitdata = data.split(',')
	# recieve parameters about the upcoming download stream
	packet_size =  int(splitdata[0])
	no_of_packets = int(splitdata[1])
	backoff = float(splitdata[2])
	burst_length = float(splitdata[3])
	snt_time = 0
	packets_sent = 0
	bursts_sent = 0
	l_padding = ''
	m_padding = ''
	s_padding = ''
	# setup three packet sizes to add to burstiness
	for j in range(78,packet_size):
		m_padding = m_padding + str(1)
	for j in range(78,packet_size - 200):
		s_padding = s_padding + str(1)
	for j in range(78,packet_size + 200):
		l_padding = l_padding + str(1)

	while packets_sent < no_of_packets:
		# find random backoff between bursts
		alpha = 1./(backoff - backoff_min)
		sleep_time = numpy.random.pareto(alpha) + backoff_min
		#print sleep_time
		time.sleep(sleep_time)
		this_burst = int(round(numpy.random.normal(burst_length,1)))
		burst = 0
		# decide what size packet will be sent in this burst
		if bursts_sent%30 < 10:
			padding = m_padding
		elif bursts_sent%30 > 20:
			padding = l_padding
		else:
			padding = s_padding
		bursts_sent = bursts_sent + 1
		# send the individual packets
		while burst < this_burst and packets_sent < no_of_packets:
			snt_time = time.time()
			sock.sendto(str((str('%08d' % packets_sent), snt_time, padding)), addr)
			packets_sent = packets_sent + 1
			burst = burst + 1	
