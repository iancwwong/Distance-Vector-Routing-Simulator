# This class represents a Distance Vector Routing table

#!/usr/bin/python

class DistanceVectorTable(object):
	# Constants
	# For indexing
	NODE_VIA = 0
	DISTANCE = 1
	
	# Attributes
	nodeID = ''		# (Character) ID of node that this DVT belongs to
	distanceTo = {}		# Distances to different nodes
				# Stored in the format: { 'nodeTo': ( cost, nodeVia ) }

	# Constructor
	def __init__(self, dataStr):
		dvtComponents = dataStr.split('~')
		self.nodeID = dvtComponents[0]
		costs = dvtComponents[1]
		for costData in costs.split(','):
			costInfo = costsData.split('=')
			nodeTo = costInfo[0]
			cost = float(costInfo[1])
			self.distanceTo[nodeTo] = (nodeTo, cost)

	# Show the distance vector table
	def show(self):
		print "++ Distance Vector Table ++" % self.nodeID
		print "nodeTo %t | nodeVia %t | cost"
		for nodeTo in self.distanceTo.keys():
			print "%s %t | %s %t | %s" % \
				(nodeTo, self.distanceTo[nodeTo][self.NODE_VIA], self.distanceTo[nodeTo][self.DISTANCE])
		print ""	# formatting
