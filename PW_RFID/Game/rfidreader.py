import os
import time
import re
import clr 
clr.AddReferenceToFileAndPath(os.path.join('lib','ASCHFProtLib.dll'))
import ASCHFProtLib
from threading import Thread

class RFIDReader(Thread):

	"""
	The RF ID reader runs in a seperate thread.
	It simply runs in an infinite loop, sending serial
	messages to the RFID reader. An event handler handles
	the returned data.
	"""

	def __init__(self, com_port, baud_rate):
	
		"""
		Do some setup
		"""
		
		Thread.__init__(self)
		
		self.running=True
		self.TAGPATTERN=re.compile(r"E0040100[0-9A-F]{8}")
		self.current_tags = []
		self.reader = ASCHFProtLib.HFProt()
		self.reader.OnRS232AscMsg += self.onRS232MsgReceived
		if self.reader.OpenRSCom(baud_rate, com_port):
			print ">>>Successfully connected to RFID reader."
		else:
			print ">>> Connection to RFID reader failed."
			# Kill thread
			self.running=False

	
	def run(self):
	
		"""
		Overloaded Thread method.
		"""
		
		while self.running:
			try:
				self.reader.SendRS232("M01")
				time.sleep(1)
				#print self.current_tags
			except KeyboardInterrupt:
				self.running=False
		print ">>> Closing serial, killing thread."
		self.reader.CloseRSCom()
	
	
	def onRS232MsgReceived(self, sender, event):
	
		"""
		This event handler parses responses coming from the
		RFID reader and populates a list with tag IDs that 
		are currently on the reader.
		"""
	
		self.current_tags = []
		for m in re.finditer(self.TAGPATTERN, event):
			self.current_tags.append(m.group(0))