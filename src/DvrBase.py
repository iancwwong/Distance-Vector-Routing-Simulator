# This script simulates a node in a network that utilises
# the Distance Vector Routing protocol
# Written by: Ian Wong
# Date: 20/05/16

#!usr/bin/python

from DVRNode import DVRNode
from AbstractDVT import AbstractDVT
from DVRSender import DVRSender
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
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.event = threading.Event()

		# Set buffer size
		self.BUFFER_SIZE = 1024

		# Assign the given socket
		self.sock = sock

	# Thread body - constantly listen for messages
	def run(self):
		global dvtProcessList		# The list that contains information to be parsed
		while not self.event.isSet():
			# Use select module to read from buffer
			msg = self.selectrecv()

			# Parse message type
			if msg != "":
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

	# Create udp socket with specified data port number
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', nodePort))

	# Prepare the list of dvt's to process
	global dvtProcessList
	dvtProcessList = []

	# Set the flag to send data to be false
	global sendFlag
	sendFlag = False
	
	# Create the listen thread, timerThread, and exchange class
	listenThread = ListenThread(sock)
	timerThread = TimerThread()
	dvrSender = DVRSender(sock, node)

	# Run the listen thread and timer thread
	listenThread.start()
	timerThread.start()

	# Flag for indicating whether the stable node has been printed
	stableNodePrinted = False

	print "Node up and running!"
	try:
		while True:

			# Check whether it is time to send out the DVT's
			if sendFlag == True:
				# Send the DVT's
				dvrSender.sendDVT()

				# Reset the flag
				sendFlag = False

			# Process all the dvt's
			# NOTE: all are in format as a tuple: (neighbourID, costs)
			#	 where costs is in the format: 	[ <NODETO>=<COST> ]
			while len(dvtProcessList) > 0:
				advtInfo = dvtProcessList.pop(0)
				abstractDVT = AbstractDVT(advtInfo[0], advtInfo[1])
				node.updateDVT(abstractDVT)

			# Only print node when it is both stable, and not yet printed
			if not node.stable:
				stableNodePrinted = False
			elif (node.stable) and (not stableNodePrinted):
				print "Node is stable!"
				node.showInfo()
				print ""
				stableNodePrinted = True

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
