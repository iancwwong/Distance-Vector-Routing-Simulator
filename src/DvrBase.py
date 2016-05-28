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

	# Prepare the list of dvt's to process
	dvtProcessList = []

	# Set the flag to send data to be false
	sendFlag = False
	IDLE_DURATION = 5
	
	# Create the listen thread, timerThread, and exchange class
	# listenThread = ListenThread(nodePort, dvtProcessList)
	# timerThread = TimerThread(IDLE_DURATION, sendFlag)
	# dvtSender = DVTSender(nodePort, node)

	# Run the listen thread and timer thread
	#listenThread.run()
	#timerThread.run()

	# Wait for termination
	while True:
		# Process all the dvt's
		while len(dvtProcessList) > 0:
			# procDVT = dvtProcessList.pop(0)
			# process procDVT
			print "Processing the first DVT in those received..."

		# Check whether it is time to send out the DVT's
		if sendFlag:
			# Send the DVT's
			print "Sending the dvt's..."

			# Reset the flag
			sendFlag = False
		
# ----------------------------------------------------
# RUNNING MAIN
# ----------------------------------------------------
if (__name__ == "__main__"):
	main()
