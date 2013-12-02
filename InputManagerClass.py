from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

class InputManager(DirectObject):
	def __init__(self):
		self.keyMap = {"up": False, "down": False, "left": False, "right": False}
		
		self.accept("w", self.setKey, ["up", True])
		self.accept("s", self.setKey, ["down", True])
		self.accept("a", self.setKey, ["left", True])
		self.accept("d", self.setKey, ["right", True])
		
		self.accept("w-up", self.setKey, ["up", False])
		self.accept("s-up", self.setKey, ["down", False])
		self.accept("a-up", self.setKey, ["left", False])
		self.accept("d-up", self.setKey, ["right", False])

	def setKey(self, key, value):
		self.keyMap[key] = value
		return
