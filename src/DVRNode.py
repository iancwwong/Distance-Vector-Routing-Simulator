# ----------------------------------------------------
# DISTANCE VECTOR ROUTING NODE
# ----------------------------------------------------
# This class represents a node in the Distance Vector Routing protocol

#!/usr/bin/python

from DistanceVectorTable import DistanceVectorTable
import AbstractDVT as ADVT

class DVRNode(object):

	# Attributes
	nodeID = ''		# (Character) ID of this node
	numNeighbours = 0
	neighbours = {}		# Stores ID's of neighbour nodes, and their associated port numbers
				# Format: {'NeighbourID': <port>}
	dvt = None		# Stores distances to nodes via nodes
	stable = False		# Indicates whether the DVT has stablised
	
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
			neighbourCost = float(lineParts[1])
			neighbourPort = int(lineParts[2])
			self.neighbours[neighbourID] = neighbourPort
			self.dvt.insertDistanceEntry(neighbourID, neighbourCost, neighbourID)	# nodeVia is the neighbour itself
		
	# Given an abstractDVT, update this DVT
	def updateDVT(self, abstractDVT):
		# Increase the stability count of ALL entries
		self.dvt.incAllStabilityCount()

		# Update the DVT based on info from abstract DVT
		for dest in abstractDVT.dvt.keys():
			costToDest = abstractDVT.dvt[dest] + self.dvt.distanceTo[abstractDVT.nodeID][0]
			if (dest not in self.dvt.distanceTo.keys()) or (self.dvt.distanceTo[dest][0] > costToDest):
				self.dvt.distanceTo[dest] = (costToDest, abstractDVT.nodeID, 0)

		# Change stability flag as accordingly
		self.stable = self.dvt.stable
	
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


