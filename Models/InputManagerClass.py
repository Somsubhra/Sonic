from direct.showbase.DirectObject import DirectObject

class InputManager(DirectObject):
	def __init__(self):
		self.keyMap = {"w" : False,
						"s" : False,
						"a" : False,
						"d" : False,
						"mouse1" : False,
						"mouse3" : False}
		self.accept("w", self.setKey, ["w", True])
		self.accept("s", self.setKey, ["s", True])
		self.accept("a", self.setKey, ["a", True])
		self.accept("d", self.setKey, ["d", True])
		self.accept("mouse1", self.setKey, ["mouse1", True])
		self.accept("mouse3", self.setKey, ["mouse3", True])
		self.accept("w-up", self.setKey, ["w", False])
		self.accept("s-up", self.setKey, ["s", False])
		self.accept("a-up", self.setKey, ["a", False])
		self.accept("d-up", self.setKey, ["d", False])
		self.accept("mouse1-up", self.setKey, ["mouse1", False])
		self.accept("mouse3-up", self.setKey, ["mouse3", False])
	def setKey(self, key, value):
		self.keyMap[key] = value