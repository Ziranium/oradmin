#! /usr/bin/python
# Python Version: 2.6 - Platform: RedHat Enterprise Linux 5.10 64bits
# Created by Jonathan LAMBERT - contact@jonathanlambert.info

import threading
import time


class Thread (threading.Thread):

	def __init__(self, threadID, inputQueue, outputQueue, queueLock, req):
		threading.Thread.__init__(self)
		self.exitFlag = False
		self.threadID = threadID
		self.inputQueue = inputQueue
		self.outputQueue = outputQueue
		self.queueLock = queueLock
		self.otool = None
		self.req = req

	def run(self):
		while not self.exitFlag:
			self.queueLock.acquire()
			if not self.inputQueue.empty():
				self.otool = self.inputQueue.get()
				self.queueLock.release()
				dictSingleElem = {self.otool.instance : self.otool.execSelect(self.req, True)}
				self.outputQueue.put(dictSingleElem)
				#print "thread "+str(self.threadID)+" termine : "+self.otool.base
			else:
				self.queueLock.release()
			time.sleep(0.2)
