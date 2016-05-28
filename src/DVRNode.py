# This class represents a node in the Distance Vector Routing protocol

#!/usr/bin/python

from DistanceVectorTable import DistanceVectorTable

class DVRNode(object):

	# Attributes
	nodeID = ''		# (Character) ID of this node
	neighbours = {}		# Stores ID's of neighbour nodes, and their associated port numbers
				# Format: {'NeighbourID': <port>}
	dvt = None		# Stores distances to nodes via nodes
	
	# Constructor - given nodeID, and name of configuration file
	def __init__(self, nodeid, configFileName):
		self.nodeID = nodeid
	
		# Prepare the node's neighbour and dvt info from configuration file
		print "Initialising the neighbour table..."

		print "Initialising the dvt table..."		

	
	# Show the details of this node
	def showInfo(self):
		print "++ Node %s Neighbour Info ++" % self.nodeID
		self.dvt.show()
