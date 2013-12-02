from pandac.PandaModules import *
from direct.showbase import Audio3DManager
from TrackClass import Track
from ActorClass import Actor

class Race:
	def __init__(self, inputManager, gui)
		self.inputManager = inputManager
		self.actors = []
		self.track = None
		self.gui = gui
		self.amList = []
		self.a3DList = []

		for N in range(4):
			self.amList.append(AudioManager.createAudioManager())
			base.addSfxManager(self.amLost[N])
			self.a3DList.append(Audio3DManager.Audio3DManager(base.sfxManagerList[N+1], camera))
			self.a3DList[N].setDropOffFactor(.1)

	def createDemoRace(self):
		self.gui.hide()
		self.destroyRace()
		self.track = Track()
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[0], 1, "A", ai=True))
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[1], 2, "B", ai=True))
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[2], 3, "C", ai=True))
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[3], 4, "D", ai=True))

		self.setCameraHigh(self.actors[0])
		self.startRace(1)
		return

	def createRace(self):
		self.gui.hide()
		self.destroyRace()
		self.track = Track()
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[0], 1, "A"))
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[1], 2, "B", ai=True))
		self.actors.append(Actor(self.inputManager, self.track, self.a3DList[3], 3, "C", ai=True))
		self.actors.append(Actor(self.inputManager, self.track, self.a3DLIst[4], 4, "D", ai=True))

		self.gui.setActor(self.actors[0])
		self.gui.show()

		self.setCameraFollow(self.actors[0])
		return

	def setCameraFollow(self, actor):
		base.camera.reparentTo(actor.dirNP)
		base.camera.setPos(0, -15, 3)
		base.camera.setHpr(0, 0, 0)
		return

	def setCameraHigh(self, actor):
		base.camera.reparentTo(actor.dirNP)
		base.camera.setPos(0, 30, 30)
		base.camera.lookAt(actor.root)
		return

	def startRace(self, delay):
		taskMgr.doMethodLater(delay, self.startActors, "Start Actors")
		return

	def startActors(self, task):
		for A in self.actors:
			A.active = True
		return task.done

	def destroyRace(self):
		if(self.track != None):
			self.track.destroy()
		for A in self.actors:
		 	A.destroy()
		del self.actors[0:4]
		return
