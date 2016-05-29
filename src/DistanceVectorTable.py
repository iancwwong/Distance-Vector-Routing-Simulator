# This class represents a Distance Vector Routing table

#!/usr/bin/python

class DistanceVectorTable(object):
	# Constants
	# For indexing
	COST = 0
	NODE_VIA = 1
	STABILITY = 2
	
	# Attributes
	nodeID = ''		# (Character) ID of node that this DVT belongs to
	distanceTo = {}		# Distances to different nodes
				# Stored in the format: { 'nodeTo': ( cost, nodeVia, stableCount ) }
				#	where stableCount indicates number of updates where the entry for 
				#	'nodeTo' has NOT changed
	numDistanceEntries = 0	# Number of distance entries in the table (essentially len(distanceTo.keys()))
	stable = False		# Indicates whether the DVT has stablised

	# Constructor
	def __init__(self, nodeID):
		self.nodeID = nodeID
		self.distanceTo = {}
		self.numDistanceEntries = 0

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
