#!/usr/bin/python

# created by Angus Clark on 8/01/2017
#ToDO incorperate the saving program into this one
import socket
import os
import json
import my_traceroute
import get_isp
import requests
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '130.56.253.43'
print host
port = 5208 # change when port is decided
s.bind((host,port))
#f = open('temp.json','wb')
s.listen(5)
while True:
	c, addr = s.accept()
	f = open('temp.json','wb')
	print addr[0]
	l = c.recv(1024)
	while(l):
		f.write(l)
		l = c.recv(1024)
	f.close()
	c.close()
	tempfile = open('temp.json','rb')
	info = json.load(tempfile)
	info["UserInfo"]["ip"] = addr[0]
	
	try:
		info["UserInfo"]["ISP"] = get_isp.get_ip(addr[0])
	except:
		print 'need to update software'

	last_addr = '0.0.0.0' #placeholder for first iteration
	for hop in range(1,30):
		result = my_traceroute.traceroute(hop, info["UserInfo"]["ip"])
		print result
		if result  == -1:
			break
		if result[1] == last_addr:
			break

		
		#info["TRACEROUTE"].update({'hop':result[0], 'node':result[1], 'rtt':result[2]})
		info["TRACEROUTE"][str(result[0])] = {}
		info["TRACEROUTE"][str(result[0])].update({'node':result[1], 'rtt':result[2]})
		last_addr = result[1]

	id = info["UserInfo"]["user id"]
	timestamp = info["UserInfo"]["timestamp"]
	os.system('mkdir /home/ubuntu/data/'+str(id))
	path = "/home/ubuntu/data/" + str(id) + "/"
	filename = str(timestamp) + '.json'

	savefile  = open(path + filename, 'w+')
	savefile.write(json.dumps(info))
	savefile.close()

	time.sleep(5)
	print path+filename
	r = requests.post('http://130.56.253.43/nethealth_server/public/process_json.php', data = {'file':path+filename})
	print r.status_code
