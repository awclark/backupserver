import time
import socket

def traceroute(ttl, dest_ip):
	port = 33434
	currentaddr = None
	timeout = 5.0 # set timeout in s
	
	icmp = socket.getprotobyname('icmp')
	udp = socket.getprotobyname('udp')

	recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
	recvsock.settimeout(timeout)
	sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
	sendsock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
	recvsock.bind(("",port))
	sendtime = time.time()
	sendsock.sendto("",(dest_ip,port))

	try:
		data, currentaddr  = recvsock.recvfrom(512)
		recvtime = time.time()

	except socket.error:
		return -1
	
	sendsock.close()
	recvsock.close()

	rtt = 1000 * (recvtime - sendtime)
	return (ttl, currentaddr[0], rtt)


		
