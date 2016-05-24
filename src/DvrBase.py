# This script simulates a node in a network that utilises
# the Distance Vector Routing protocol
# Written by: Ian Wong
# Date: 20/05/16

#!usr/bin/python

from sys import argv

# ----------------------------------------------------
# MAIN FUNCTIONS
# ----------------------------------------------------
def main():

	# Global variable: the Distance Vector Table that contains information about the costs
	# to travel to each node
	global myDVT
	
	# Check for proper usage
	if len(argv) < 4:
		print "Usage: python DvrBase.py <NODE_ID> <NODE_PORT> <config.txt> [-p] [-e]"
		exit()
	
	# Parse arguments
	nodeID = argv[1]
	nodePort = int(argv[2])
	configFilename = argv[3]

	# Obtain the data string for distance vector table
	dataStr = getDVTDataStr(nodeID, configFilename)

	# Create the Distance Vector Table object
	myDVT = DistanceVectorTable(dataStr)
	myDVT.show()
	exit()

	# Create the listen thread and exchange thread

	# Run exchange thread

	# Run listen thread

	# Wait for termination
	while True:
		pass

# Reads in a given file, and returns data for the DVT in the format:
# 	[NodeID]~[Neighbour node]=[cost],...
def getDVTDataStr(nodeID, configFilename):
	dataStr = nodeID + '~'
	
	# Read the file
	datafile = open(configFilename, 'r')
	lines = datafile.read()
	if len(lines) >= 2:
		for linenum in range(1, len(lines)):
			linedata = lines[linenum].split(' ')
			nodeToID = linedata[0]
			nodeToCost = float(linedata[1])
			nodeToPort = int(linedata[2])
			
		

	return dataStr

# ----------------------------------------------------
# RUNNING MAIN
# ----------------------------------------------------
if (__name__ == "__main__"):
	main()
