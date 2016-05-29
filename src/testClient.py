#!usr/bin/python

import socket
import time
import random

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

i = 0
while (i < 1):
	print "Sending sample abstract dvt"
	sock.sendto("#NeighbourDVT#B#A=2,C=3,D=2", ("127.0.0.1", 2000))
	sock.sendto("#NeighbourDVT#D#A=2,C=4,B=1", ("127.0.0.1", 2000))
	print "Message %d sent." % i
	i += 1
	time.sleep(2)
