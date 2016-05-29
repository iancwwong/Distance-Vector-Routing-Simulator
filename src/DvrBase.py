# This script simulates a node in a network that utilises
# the Distance Vector Routing protocol
# Written by: Ian Wong
# Date: 20/05/16

#!usr/bin/python

from DVRNode import DVRNode
from AbstractDVT import AbstractDVT
from sys import argv
import threading
import time
import socket
import select

# Global variables
sendFlag = False
dvtProcessList = []

# ----------------------------------------------------
# SCHEDULER THREAD
# ----------------------------------------------------
# This class represents the timing thread that sleeps for a specified idle_duration
# When the sleep is completed, it signals Main to exchange dvt with neighbours

class TimerThread(threading.Thread):

	# Attributes
	IDLE_DURATION = 1		# how long is period between exchanging dvt's

	# Constructor
	def __init__(self):
		threading.Thread.__init__(self)
		self.event = threading.Event()		# for terminating thread

	# Thread body
	def run(self):
		global sendFlag
		while not self.event.isSet():
			time.sleep(self.IDLE_DURATION)
			if (self.event.isSet()):	# early check
				break
			time.sleep(self.IDLE_DURATION)
			sendFlag = True
		print "Exiting timer timer thread..."

	# Stop the thread
	def stop(self):
		self.event.set()

# ----------------------------------------------------
# LISTENING THREAD
# ----------------------------------------------------
# This class represents the listener thread that listens to messages from the specified
# port number
# NOTE: Uses the 'select' module for listening
class ListenThread(threading.Thread):
	
	# Constructor
	def __init__(self, portNum):
		threading.Thread.__init__(self)
		self.event = threading.Event()
		
		# Create udp socket with specified data port number
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('', portNum))

		# Set buffer size
		self.BUFFER_SIZE = 1024

	# Thread body - constantly listen for messages
	def run(self):
		global dvtProcessList		# The list that contains information to be parsed
		while not self.event.isSet():
			# Use select module to read from buffer
			msg = self.selectrecv()

			# Parse message type
			if msg != "":
				print "Message received: %s" % msg
				msgComponents = msg.split('#')
				msgType = msgComponents[1]

				# Case when DVT from neighbour is received in the format
				# Parse into ID and costs, append to the dvtProcessList
				# #NeighbourDVT#B#A=2,C=3,D=2
				if msgType == "NeighbourDVT":
					neighbourID = msgComponents[2]
					costs = msgComponents[3].split(',')
					dvtProcessList.append((neighbourID, costs))		

		print "Exiting listen module thread.."

	# Read data from buffer using select module
	def selectrecv(self):
		read_sockets, write_sockets, error_sockets = select.select([self.sock], [], [])
		for rs in read_sockets:
			if (rs == self.sock):
				msg, addr = rs.recvfrom(self.BUFFER_SIZE)
				return msg

	# Stop the listener by sending an empty message to itself
	def stop(self):
		self.event.set()
		time.sleep(1)
		self.sock.sendto("", ("127.0.0.1", self.sock.getsockname()[1]))

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
	print "Initialising node..."
	node = DVRNode(nodeID, configFilename)
	node.showInfo()
	print ""	# formatting

	# Prepare the list of dvt's to process
	global dvtProcessList
	dvtProcessList = []

	# Set the flag to send data to be false
	global sendFlag
	sendFlag = False
	
	# Create the listen thread, timerThread, and exchange class
	listenThread = ListenThread(nodePort)
	timerThread = TimerThread()
	# dvrSender = DVRSender(node)

	# Run the listen thread and timer thread
	listenThread.start()
	timerThread.start()

	print "Starting to exchange node info..."
	try:
		while True:

			# Check whether it is time to send out the DVT's
			if sendFlag == True:
				# Send the DVT's
				print "Sending node's dvt to neighbours..."

				#dvrSender.sendDVT()

				# Reset the flag
				sendFlag = False

			# Process all the dvt's
			# NOTE: all are in format as a tuple: (neighbourID, costs)
			#	 where costs is in the format: 	[ <NODETO>=<COST> ]
			while len(dvtProcessList) > 0:
				print "Processing the first DVT in those received..."
				advtInfo = dvtProcessList.pop(0)
				abstractDVT = AbstractDVT(advtInfo[0], advtInfo[1])
				abstractDVT.show()
				node.updateDVT(abstractDVT)

				print "Updated node:"
				node.showInfo()
				print ""

			# Check whether the node is stable
			if node.stable:
				print "Node is stable!"
				node.showInfo()
				print ""

	# Quit when keyboardInterrupt (Ctrl+C)	
	except KeyboardInterrupt:
		print "Exiting..."
		listenThread.stop()
		timerThread.stop()
		exit()

# ----------------------------------------------------
# RUNNING MAIN
# ----------------------------------------------------
if (__name__ == "__main__"):
	main()
