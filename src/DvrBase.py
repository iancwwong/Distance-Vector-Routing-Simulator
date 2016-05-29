# This script simulates a node in a network that utilises
# the Distance Vector Routing protocol
# Written by: Ian Wong
# Date: 20/05/16

#!usr/bin/python

from DVRNode import DVRNode
from TimerThread import TimerThread
from sys import argv

# ----------------------------------------------------
# MAIN FUNCTIONS
# ----------------------------------------------------
def main():
	global sendFlag

	# Check for proper usage
	if len(argv) < 4:
		print "Usage: python DvrBase.py <NODE_ID> <NODE_PORT> <config.txt> [-p] [-e]"
		exit()

	# Parse arguments
	nodeID = argv[1]
	nodePort = int(argv[2])
	configFilename = argv[3]

	# Create the node
	print "Initialising node..."
	node = DVRNode(nodeID, configFilename)
	node.showInfo()
	print ""	# formatting
	exit()

	# Prepare the list of dvt's to process
	dvtProcessList = []

	# Set the flag to send data to be false
	sendFlag = False
	
	# Create the listen thread, timerThread, and exchange class
	# listenThread = ListenThread(nodePort, dvtProcessList)
	timerThread = TimerThread()
	# dvtSender = DVTSender(nodePort, node)

	# Run the listen thread and timer thread
	#listenThread.run()
	timerThread.run()

	print "Starting to exchange node info..."

	# Quit when keyboardInterrupt (Ctrl+C)
	try:
		while True:

			# Check whether it is time to send out the DVT's
			if sendFlag:
				# Send the DVT's
				print "Sending the dvt's..."

				# Reset the flag
				sendFlag = False

			# Process all the dvt's
			while len(dvtProcessList) > 0:
				# procDVT = dvtProcessList.pop(0)
				# process procDVT
				print "Processing the first DVT in those received..."

			# Check whether the node is stable
			# if node.stable:
			#	node.dvt.show()
	
	except KeyboardInterrupt:
		exit()

# ----------------------------------------------------
# RUNNING MAIN
# ----------------------------------------------------
if (__name__ == "__main__"):
	# Global variables
	global sendFlag
	global timerThread
	main()
