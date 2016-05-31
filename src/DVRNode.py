# ----------------------------------------------------
# DISTANCE VECTOR ROUTING NODE
# ----------------------------------------------------
# This class represents a node in the Distance Vector Routing protocol

#!/usr/bin/python

from DistanceVectorTable import DistanceVectorTable
import AbstractDVT as ADVT
from copy import deepcopy

class DVRNode(object):

	# Attributes
	nodeID = ''		# (Character) ID of this node
	numNeighbours = 0
	neighbours = {}		# Stores ID's of neighbour nodes, and their associated port numbers
				# Format: {'NeighbourID': <port>}
	deadNeighbours = []	# stores ID's of dead neighbours
	dvt = None		# Stores distances to nodes via nodes
	originalDVT = None	# Stores the original dvt upon intialisation

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
		self.originalDVT = None

		self.originalDVT = deepcopy(self.dvt.distanceTo)
		
	# Given an abstractDVT, update this DVT
	def updateDVT(self, abstractDVT):

		# Increase the stability count of ALL entries
		self.dvt.incAllStabilityCount()

		# Update the DVT based on info from abstract DVT
		for dest in abstractDVT.dvt.keys():
			# Only consider the destinations which are:
			#	* NOT this node 
			# 	* NOT a dead neighbour
			if (dest != self.nodeID) and (not dest in self.deadNeighbours):
				
				costToDest = abstractDVT.dvt[dest] + self.dvt.distanceTo[abstractDVT.nodeID][0]
				# Rewrite the original entry if:
				#	*destination doesn't exist in DVT
				#	*cost is invalid
				#	*oldCost > newCost
				if (not dest in self.dvt.distanceTo.keys()) \
				or (self.dvt.distanceTo[dest][0] == DistanceVectorTable.INVALID_COST) \
				or (self.dvt.distanceTo[dest][0] > costToDest):
					viaNode = self.dvt.distanceTo[abstractDVT.nodeID][1]	#node via to abstractDVT.nodeID
					self.dvt.insertDistanceEntry(dest, costToDest, viaNode)	

		# Check for any destinations that have been removed
		# ie those that are in node's DVT, but NOT in abstract dvt and NOT a neighbour
		for nodeTo in self.dvt.distanceTo.keys():
			if (not nodeTo in abstractDVT.dvt.keys()) and (not nodeTo in self.neighbours.keys()):
				self.dvt.distanceTo.pop(nodeTo)
				self.dvt.resetStability()

	# Given the id of a dead neighbour, manage it's dicts appropriately
	# NOTE: Assumes deadNeighbourID exists in neighbours
	def considerDead(self, deadNeighbourID):

		# Add dead neighbour id
		self.deadNeighbours.append(deadNeighbourID)

		# Remove all instances of destination, and nodeVia in dvt
		# corresponding to ID of deadNeighbourID
		#self.dvt.removeAll(deadNeighbourID)
			
		# Remove the entry in neighbours
		#self.neighbours.pop(deadNeighbourID)

		# Restore the entries of alive neighbours
		self.restoreAliveNeighbourEntries()
			
		# Reset the stability
		self.dvt.resetStability()

	def restoreAliveNeighbourEntries(self):
		for nodeID in self.originalDVT.keys():
			if not nodeID in self.deadNeighbours:
				self.dvt.distanceTo[nodeID] = self.originalDVT[nodeID]

	# Check for stablity of node's dvt
	def isStable(self):
		return self.dvt.stable

	# For all neighbours, return a mapping from neighbour port to neighbour id
	def getPortToNeighbourMapping(self):
		newMapping = dict((v,k) for k,v in self.neighbours.iteritems())
		return newMapping
	
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


