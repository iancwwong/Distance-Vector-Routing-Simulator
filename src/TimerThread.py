# This class represents the timing thread that sleeps for a specified idle_duration
# When the sleep is completed, it signals Main to exchange dvt with neighbours

#!usr/bin/python

import threading
import time

class TimerThread(threading.Thread):
	IDLE_DURATION = 2		# how long is period between exchanging dvt's
	
	# Constructor
	def __init__(self):
		threading.Thread.__init__(self)
		self.event = threading.Event()		# for terminating thread

	# run the thread
	def run(self):
		global sendFlag		# Reference of the boolean variable in main
		try:
			while not self.event.isSet():
				time.sleep(self.IDLE_DURATION)
				sendFlag = True
		except KeyboardInterrupt:
			exit()
