from TrackLanesClass import TrackLanes
from pandac.PandaModules import *

class Track:
	def __init__(self):
		self.track = loader.loadModel("Models/Track.egg")
		self.track.reparentTo(render)
		self.planet = loader.loadModel("Models/Planet.egg")
		self.planet.reparentTo(render)
		self.trackLanes = TrackLanes()
		self.gravity = 1
		self.groundCol = loader.loadModel("Models/Ground.egg")
		self.groundCol.reparentTo(render)
		mask = BitMask32.range(1,3)
		mask.clearRange(2,1)
		self.groundCol.setCollideMask(mask)
		self.setupLight()
		
	def setupLight(self):
		primeL = DirectionalLight("prime")
		primeL.setColor(VBase4(.6,.6,.6,1))
		self.dirLight = render.attachNewNode(primeL)
		self.dirLight.setHpr(45,-60,0)
		render.setLight(self.dirLight)		
		ambL = AmbientLight("amb")
		ambL.setColor(VBase4(.2,.2,.2,1))
		self.ambLight = render.attachNewNode(ambL)		
		render.setLight(self.ambLight)
		return

	def destroy(self):
		self.track.removeNode()
		self.planet.removeNode()
		self.groundCol.removeNode()
		self.dirLight.removeNode()
		self.ambLight.removeNode()
		self.trackLanes.destroy()
		self.trackLanes = None
		self.skySphere = None
		render.setLightOff()		
		return	
