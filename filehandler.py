#!/usr/bin/python

# created by Angus Clark on 8/01/2017
# last update 21/5/2017 **Improved readability and updated end-to-end implementation
import socket
import os
import json
import my_traceroute
import get_isp
import requests
import time

# Wait for connection from the client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '130.56.253.43'
max_tr_hop = 30
print host
port = 5208 # Port must be matched with client side
s.bind((host,port))
s.listen(5)
# Once connected being reading data into buffer
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
	# Add client IP address to datafield
	info["UserInfo"]["ip"] = addr[0]
	# Attempt to fetch the users ISP from whois directory
	try:
		info["UserInfo"]["ISP"] = get_isp.get_ip(addr[0])
	except:
		print 'need to update software'
	# Begin traceroute back to client
	last_addr = '0.0.0.0' #placeholder
	for hop in range(1,max_tr_hop):
		result = my_traceroute.traceroute(hop, info["UserInfo"]["ip"])
		#print result
		# If no result return
		if result  == -1:
			break
		if result[1] == last_addr:
			break

		
		# Add result to JSON folder in traceroute section
		info["TRACEROUTE"][str(result[0])] = {}
		info["TRACEROUTE"][str(result[0])].update({'node':result[1], 'rtt':result[2]})
		last_addr = result[1]
	# Decide on filenmae based upon MAC and timestamp
	id = info["UserInfo"]["user id"]
	timestamp = info["UserInfo"]["timestamp"]
	os.system('mkdir /home/ubuntu/data/'+str(id))
	path = "/home/ubuntu/data/" + str(id) + "/"
	filename = str(timestamp) + '.json'
	# Save the file to database
	savefile  = open(path + filename, 'w+')
	savefile.write(json.dumps(info))
	savefile.close()

	time.sleep(5)
	# Point the web server to the file that has just been added to the database so that it may include in mysql
	r = requests.post('http://130.56.253.43/nethealth_server/public/process_json.php', data = {'file':path+filename})
	#print r.status_code
