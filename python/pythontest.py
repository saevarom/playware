import clr
import pyevent
import re
import time
import sys
import ironclad

DEBUG=True
TAGPATTERN=re.compile(r"E0040100[0-9A-F]{8}")


tag_mapping = {
	'numerals': {
		'E00401001CCE8F48': '1',
		'E00401001CCE952C': '2',
	},
	'operators': {
		'E00401001CCE9CF2': '+',
		'E00401001CCE77ED': '=',
	},
}

input_tags = []
input_tags_temp = []

def onRS232MsgReceived(sender, event):
	global input_tags, input_tags_temp
	#if DEBUG: print "Tags on plate:"
	for m in re.finditer(TAGPATTERN, event):
		#if DEBUG: print "\t%s" % m.group(0)
		if m.group(0) in tag_mapping['numerals'].keys():
			if len(input_tags_temp) == 1:
				if input_tags_temp[0] in tag_mapping['operators'].values():
					input_tags.append(input_tags_temp)
					input_tags_temp = []
			if tag_mapping['numerals'][m.group(0)] not in input_tags_temp:
				input_tags_temp.append(tag_mapping['numerals'][m.group(0)])
		if m.group(0) in tag_mapping['operators'].keys():
			if len(input_tags_temp) == 0:
				print "You must put a number on the plate!"
			else:
				if tag_mapping['operators'][m.group(0)] not in input_tags_temp:
					input_tags.append(input_tags_temp)
					input_tags_temp = [tag_mapping['operators'][m.group(0)]]
					if tag_mapping['operators'][m.group(0)] == '=':
						print input_tags
		print input_tags_temp

	
running=True
clr.AddReference('ASCHFProtLib.dll')
import ASCHFProtLib
a = ASCHFProtLib.HFProt()
a.OnRS232AscMsg += onRS232MsgReceived
if a.OpenRSCom(19200, "COM2"):
	while running:
		try:
			a.SendRS232("M01")
			time.sleep(1)
		except KeyboardInterrupt:
			running=False

a.CloseRSCom()