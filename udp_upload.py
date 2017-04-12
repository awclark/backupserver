import socket
import numpy
import time
import json

BUFFER = 2048

handler_port = 5204
upload_port = 5205
incoming_host = ''

while True:

	handler_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket to be used to handle request and data
	upload_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket to be used to recieve test data
	upload_socket.settimeout(2) # set 2 second timeout on incoming packets
	handler_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	upload_addr = (incoming_host,upload_port)	
	handler_addr = (incoming_host,handler_port)
	handler_socket.bind(handler_addr)
	upload_socket.bind(upload_addr)
	handler_socket.listen(1)
	
	print 'Listening...'

	conn, addr = handler_socket.accept()

	print 'Connection Accepted:'
	print addr	

	#time.sleep(1)

	
	test_params = conn.recv(BUFFER)
	print test_params
	params = test_params.split(',') # split the expected paraments into sections.
	
	latency = []
	timing = []
	packets_rcvd = 0

	while True:
		try:
			data, addr = upload_socket.recvfrom(BUFFER)
		except Exception:
			break
		time_rcvd = time.time()
		latency.append(float((data.split(',')[1])) - time_rcvd)
		timing.append(time_rcvd)
		packets_rcvd = packets_rcvd + 1

	upload_socket.close()

	#print latency
	#print packets_rcvd
	#print timing
	
	lat = numpy.asarray(latency)
	RCV = numpy.asarray(timing)
	IAT = numpy.diff(RCV)

	tot_up_time = timing[packets_rcvd -1] - timing[1]
	mean_up_lat = numpy.mean(lat) # is not accurate due to unsync clocks (probably exclude)
	std_up_lat = numpy.std(lat)
	std_up_IAT = numpy.std(IAT)
	mean_up_IAT = numpy.mean(IAT)

	command = str(packets_rcvd) + ',' + str(tot_up_time) + ',' + str(mean_up_lat) + ',' + str(std_up_lat) + ',' + str(std_up_IAT) + ',' + str(mean_up_IAT)

	conn.send(command)
	handler_socket.close()
	
