# ----------------------------------------------------
# ABSTRACT DISTANCE VECTOR TABLE
# ----------------------------------------------------
# This class represents a DVT that is obtained from a neighbour
# ie a simpler version of 'DistanceVectorTable'

class AbstractDVT(object):
	
	# Attributes
	nodeID = ''
	dvt = {}

	# Constructor - given a nodeID, and a list of costs
	# NOTE: The list of costs is in the format:
	# 	[ <NODETO>=<COST> ]
	def __init__(self, nodeID, costs):
		self.nodeID = nodeID
		for costInfo in costs:
			nodeTo = costInfo.split('=')[0]
			cost = float(costInfo.split('=')[1])
			self.dvt[nodeTo] = cost

	# Show the distance vector table
	def show(self):
		print "++ Abstract Distance Vector Table ++"
		print "nodeTo	| cost"
		print "-------------------------------------------"
		for nodeTo in self.dvt.keys():
			print "%s	| %s" % \
				(nodeTo, str(self.dvt[nodeTo]))

# Construct a string version of this object, given a node
# in the format:
# 	#<NODEID>#<NODETO>=<COST>,<NODETO>=<COST>...
# NOTE: Assumes the node has entries in its dvt
def getAbstractDVTString(node):
	nodeID = node.nodeID
	abstractDVTStr = '#' + node.nodeID + '#'
	nodesTo = node.dvt.distanceTo.keys()
	for i in range(0, len(nodesTo)):
		abstractDVTStr += nodesTo[i] + '=' + str(node.dvt.distanceTo[nodesTo[i]][0])	# cost is the first entry in tuple
		if (i < len(nodesTo) - 1):
			abstractDVTStr += ','
	return abstractDVTStr		
		
