# Created by Angus Clark 1/2/2017 for TN2 Project

import time
import socket

def traceroute(ttl, dest_ip):
	port = 33434 # standard port for sending icmp packets
	currentaddr = None
	timeout = 5.0 # set timeout in s were traceroute will be stopped
	
	icmp = socket.getprotobyname('icmp')
	udp = socket.getprotobyname('udp')

	# set recv socket to recieve ICMP packets from server once ttl has expired
	recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
	recvsock.settimeout(timeout)
	# set send socket to send udp packets with variable ttl
	sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
	sendsock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
	# allow recv socket to recieve from any IP
	recvsock.bind(("",port))
	# record the send time and sned a packet to the destintion IP
	sendtime = time.time()
	sendsock.sendto("",(dest_ip,port))
	# Wait to recieve response
	try:
		data, currentaddr  = recvsock.recvfrom(512)
		recvtime = time.time()

	except socket.error:
		return -1
	
	sendsock.close()
	recvsock.close()

	rtt = 1000 * (recvtime - sendtime)
	return (ttl, currentaddr[0], rtt)


		
