import socket
import time
import numpy

BUFFER = 4096
HOST = ''
PORT = 5206

ADDR = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
backoff_min = 0.002

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
	backoff = float(splitdata[2])
	burst_length = float(splitdata[3])
	snt_time = 0
	packets_sent = 0
	bursts_sent = 0
	l_padding = ''
	m_padding = ''
	s_padding = ''

	for j in range(78,packet_size):
		m_padding = m_padding + str(1)
	for j in range(78,packet_size - 200):
		s_padding = s_padding + str(1)
	for j in range(78,packet_size + 200):
		l_padding = l_padding + str(1)

	while packets_sent < no_of_packets:
		alpha = 1./(backoff - backoff_min)
		sleep_time = numpy.random.pareto(alpha) + backoff_min
		#print sleep_time
		time.sleep(sleep_time)
		this_burst = int(round(numpy.random.normal(burst_length,1)))
		burst = 0
		if bursts_sent%30 < 10:
			padding = m_padding
		elif bursts_sent%30 > 20:
			padding = l_padding
		else:
			padding = s_padding
		bursts_sent = bursts_sent + 1
		while burst < this_burst and packets_sent < no_of_packets:
			snt_time = time.time()
			sock.sendto(str((str('%08d' % packets_sent), snt_time, padding)), addr)
			packets_sent = packets_sent + 1
			burst = burst + 1
	
			

	print packets_sent
	#for i in range(1, no_of_packets+1):
	#	time.sleep(IDT)
	#	snt_time = time.time()
	#	sock.sendto(str((str('%08d' % i),snt_time, padding)), addr)	
