#!usr/bin/python

import socket
import time
import random

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 2001))

i = 0
while True:
	msg, addr = sock.recvfrom(1024)
	print "Message received! %s" % msg
