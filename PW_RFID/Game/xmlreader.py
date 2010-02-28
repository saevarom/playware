import clr
clr.AddReference('System.Xml')
from System.Xml import XmlDocument, XmlNodeList
from System.IO import File

# This class takes care of reading the XML file and create the items needed for the game

class XmlSettings(object):
	def __init__(self):
		self.Document = XmlDocument()
	
	# Loads the XML data into a Document
	def load(self, filepath):
		self.rawXML = File.ReadAllText(filepath)
		self.Document.LoadXml(self.rawXML)
		
	# Selects the node called settings and returns a list of items there under
	def getSettings(self):
		ns = self.Document.SelectNodes("//settings")
		Item = {}
		for n in ns:
			for on in n.ChildNodes:
				Item[on.Name] = on.InnerText
		return Item
	
	# Selects the node called gameobjects and creates a list of all sprites to be used in the game
	def getGameData(self):
		ns = self.Document.SelectNodes("//gameobject")
		SettingList = []
		for n in ns:
			Item = {}
			for on in n.ChildNodes:
				if on.Name == 'images':
					Images = []
					for im in on.ChildNodes:
						Images.append(im.InnerText)
					Item[on.Name] = Images
				else:
					Item[on.Name] = on.InnerText
			if len(Item.items()) > 0:
				SettingList.append(Item)
		return SettingList