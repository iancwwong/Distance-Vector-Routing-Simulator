# ----------------------------------------------------
# SENDER CLASS
# ----------------------------------------------------
# This object will represent the object that sends
# the node's DVT information (as an abstract dvt) to neighbours
import socket
import AbstractDVT as AVDT

class DVRSender(object):

	# Attributes
	UDP_IP = "127.0.0.1"	# the machine to send to
	
	# Constructor
	def __init__(self, sock, node):

		# Assign the sock
		self.sock = sock

		# Assign the node object
		self.node = node

	# Send out the dvt of the node to all its neighbours
	def sendDVT(self):

		# Iterate through all neighbours, getting the port number
		for neighbour in self.node.neighbours.keys():
			port = self.node.neighbours[neighbour]
			dataStr = "#NeighbourDVT" + AVDT.getAbstractDVTString(self.node)
			self.sock.sendto(dataStr, (self.UDP_IP, port))

	# Send a message to neighbour nodes
	def sendReset(self):
		for neighbour in self.node.neighbours.keys():
			port = self.node.neighbours[neighbour]
			dataStr = "#Reset"
			self.sock.sendto(dataStr, (self.UDP_IP, port))
		

