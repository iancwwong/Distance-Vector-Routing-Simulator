#!usr/bin/python

import socket
import time

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

i = 0
while (i < 5):
	sock.sendto("Fck this assignment.", ("127.0.0.1", 2000))
	print "Message %d sent." % i
	i += 1
	time.sleep(2)
