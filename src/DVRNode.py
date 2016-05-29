# ----------------------------------------------------
# Distance Vector Routing Node
# ----------------------------------------------------
# This class represents a node in the Distance Vector Routing protocol

#!/usr/bin/python

from DistanceVectorTable import DistanceVectorTable

class DVRNode(object):

	# Attributes
	nodeID = ''		# (Character) ID of this node
	numNeighbours = 0
	neighbours = {}		# Stores ID's of neighbour nodes, and their associated port numbers
				# Format: {'NeighbourID': <port>}
	dvt = None		# Stores distances to nodes via nodes
	
	# Constructor - given nodeID, and name of configuration file
	def __init__(self, nodeid, configFileName):
		self.nodeID = nodeid
		self.dvt = DistanceVectorTable(self.nodeID)
	
		# Prepare the node's neighbour and dvt info from configuration file
		# Assumes the config file is not empty
		configFile = open(configFileName, 'r')
		self.numNeighbours = int(configFile.readline())

		# Parse each line in the file
		# Specified in the format:
		#	<NODE ID> <COST> <NODE PORT>
		for i in range(0, self.numNeighbours):
			lineParts = configFile.readline().split(' ')
			neighbourID = lineParts[0]
			neighbourCost = int(lineParts[1])
			neighbourPort = int(lineParts[2])
			self.neighbours[neighbourID] = neighbourPort
			self.dvt.insertDistanceEntry(neighbourID, neighbourCost, neighbourID)	# nodeVia is the neighbour itself
			
	# Show the details of this node
	def showInfo(self):
		print "== Info for node with id '%s' ==" % self.nodeID
		self.showNeighboursInfo()
		self.dvt.show()

	# Show the neighbours info of this node
	def showNeighboursInfo(self):
		print "++ Neighbour Info ++"
		print "Neighbour	| Port"
		print "-----------------------"
		for neighbour in self.neighbours.keys():
			print "%s 		| %s" % (neighbour, self.neighbours[neighbour])


