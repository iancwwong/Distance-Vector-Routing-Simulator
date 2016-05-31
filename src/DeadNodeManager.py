# This class manages nodes by controlling which nodes are dead and alive

from DVRSender import DVRSender

class DeadNodeManager(object):

	# Attributes
	node = None		# ref to node
	neighbours = {}		# Mapping of port numbers to neighbours and alive count
				# Format: { 'portnum': ( <neighbourID>, <aliveCount> ) }
				# 	where alive count is number of times a port can be non-existent before being considered to be dead
	dvrSender = None	# The sender class

	def __init__(self, node, dvrSender):

		self.node = node
		
		# Obtain the neighbours and alive count mapping
		self.neighbours = self.node.getPortToNeighbourMapping()
		for portNum in self.neighbours.keys():
			neighbourID = self.neighbours[portNum]
			self.neighbours[portNum] = (neighbourID, 3)

		# Assign sender
		self.dvrSender = dvrSender

	# Given a list of ports where messages have originated from,
	# check whether there are any dead neighbours that should now
	# be considered for the node
	def manageDeadNodes(self, alivePorts):
		# Reduce alive count of all neighbours
		self.reduceAllAliveCount()
		
		# Iterate through ports from which messages have been received, and
		# inc alive count appropriately
		for port in alivePorts:
			if not port in self.neighbours.keys():
				continue
			neighbourID, aliveCount = self.neighbours[port]
			aliveCount = 3
			self.neighbours[port] = (neighbourID, aliveCount)
		
		# Check which ports have an alive count of 0 - ie dead
		for portnum in self.neighbours.keys():
			neighbourID, aliveCount = self.neighbours[portnum]
			if aliveCount == 0:
				# node dead - remove from the node's neighbours
				print "Death of %s is detected." % neighbourID
				self.node.considerDead(neighbourID)

				# Send reset message to neighbours
				self.dvrSender.sendReset()
				
				# remove port number from neighbours
				self.neighbours.pop(portnum)

				# reset node's dvt
				self.node.resetDVT()

	# Reduce the alive count of all neighbours
	def reduceAllAliveCount(self):
		for portNum in self.neighbours.keys():
			neighbourID, aliveCount = self.neighbours[portNum]
			if aliveCount > 0:
				aliveCount -= 1
			self.neighbours[portNum] = (neighbourID, aliveCount)

	# Show info about node's neighbours
	def showInfo(self):
		print "++ Neighbour info about node %s ++" % self.node.nodeID
		print "portNum	| (neighbourID, aliveCount)"
		for portNum in self.neighbours.keys():
			print "%d	|%s" % (portNum, str(self.neighbours[portNum]))
			
