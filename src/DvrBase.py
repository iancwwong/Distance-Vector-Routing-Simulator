# This script simulates a node in a network that utilises
# the Distance Vector Routing protocol
# Written by: Ian Wong
# Date: DD/MM/YY

#!usr/bin/python

from sys import argv

# ----------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------
def main():
	
	# Check for proper usage
	if len(argv) < 4:
		print "Usage: python DvrBase.py <NODE_ID> <NODE_PORT> <config.txt> [-p] [-e]"
		exit()
	
	# Parse arguments
	nodeID = argv[1]
	nodePort = int(argv[2])
	configFilename = argv[3]

# ----------------------------------------------------
# RUNNING MAIN
# ----------------------------------------------------
if (__name__ == "__main__"):
	main()
