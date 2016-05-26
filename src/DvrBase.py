# This script simulates a node in a network that utilises
# the Distance Vector Routing protocol
# Written by: Ian Wong
# Date: 20/05/16

#!usr/bin/python

from DVRNode import DVRNode
from sys import argv

# ----------------------------------------------------
# MAIN FUNCTIONS
# ----------------------------------------------------
def main():

	# Global variables 
	global node		# the object representing this node

	# Check for proper usage
	if len(argv) < 4:
		print "Usage: python DvrBase.py <NODE_ID> <NODE_PORT> <config.txt> [-p] [-e]"
		exit()

	# Parse arguments
	nodeID = argv[1]
	nodePort = int(argv[2])
	configFilename = argv[3]

	# Create the node
	node = DVRNode(nodeID, configFilename)
	node.showInfo()
	exit()
	
	# Create the listen thread and exchange thread

	# Run exchange thread

	# Run listen thread

	# Wait for termination
	while True:
		pass

# ----------------------------------------------------
# RUNNING MAIN
# ----------------------------------------------------
if (__name__ == "__main__"):
	main()
