# ----------------------------------------------------
# Distance Vector Routing Table
# ----------------------------------------------------
# This class represents a Distance Vector Routing table

#!/usr/bin/python

class DistanceVectorTable(object):
	# Constants
	# For indexing
	COST = 0
	NODE_VIA = 1
	STABILITY = 2
	
	INVALID_COST = -1
	
	# Attributes
	nodeID = ''		# (Character) ID of node that this DVT belongs to
	distanceTo = {}		# Distances to different nodes
				# Stored in the format: { 'nodeTo': ( cost, nodeVia, stableCount ) }
				#	where stableCount indicates number of updates where the entry for 
				#	'nodeTo' has NOT changed
	stable = False		# Indicates whether the DVT has stablised

	# Constructor
	def __init__(self, nodeID):
		self.nodeID = nodeID
		self.distanceTo = {}

	# Show the distance vector table
	def show(self):
		print "++ Distance Vector Table ++"
		print "nodeTo	| (cost, nodeVia, stability count)"
		print "-------------------------------------------"
		for nodeTo in self.distanceTo.keys():
			print "%s	| %s" % \
				(nodeTo, str(self.distanceTo[nodeTo]))

	# Insert an entry into the distance vector table
	def insertDistanceEntry(self, nodeID, nodeCost, nodeVia):
		self.distanceTo[nodeID] = (nodeCost, nodeVia, 0)	# default: set stability count to 0

	# Remove all instances of entries that involve a given nodeID
	# ie the nodeTo and nodeVia fields in self.distanceTo]
	def removeAll(self, nodeID):
		for nodeTo in self.distanceTo.keys():
			# case when destination is the node to be removed:
			if nodeTo == nodeID:
				self.distanceTo.pop(nodeTo)
			# case when nodeVia involves the node to be removed: make the cost invalid
			elif self.distanceTo[nodeTo][self.NODE_VIA] == nodeID:
				_, nodeVia, stableCount = self.distanceTo[nodeTo]
				self.distanceTo[nodeTo] = (self.INVALID_COST, nodeVia, 0)
				self.stable = False

	# Increase the stability count of ALL entries by 1
	# NOTE: Reaches a threshold of 3. If any are changed, then dvt is not yet stable
	def incAllStabilityCount(self):
		self.stable = True
		for nodeTo in self.distanceTo.keys():
			cost, nodeVia, stabilityCount = self.distanceTo[nodeTo]
			if stabilityCount < 3:		# threshold
				stabilityCount += 1
				self.stable = False
			self.distanceTo[nodeTo] = (cost, nodeVia, stabilityCount)

	# Reset the stability count of each entry
	def resetStability(self):
		for nodeTo in self.distanceTo.keys():
			cost, nodeVia, stabilityCount = self.distanceTo[nodeTo]
			self.distanceTo[nodeTo] = (cost, nodeVia, 0)
		self.stable = False
			
