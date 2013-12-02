import direct.directbase.DirectStart
from direct.filter.CommonFilters import CommonFilters

from GuiClass import Gui
from RaceClass import Race
from InputManagerClass import InputManager
from MenuClass import Menu

class World:
	def __init__(self):
		base.disableMouse()
		base.setBackgroundColor(0, 0, 0)
		self.inputManager = InputManager()
		self.filters = CommonFilters(base.win, base.cam)
		filterok = self.filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, intensity=3.0, size=2)
		render.setShaderAuto()
		
		self.menuGraphics = loader.loadModel("Models/MenuGraphics.egg")

		self.fonts = {
			"silver": loader.loadFont("Fonts/LuconSilver.egg"),
			"blue": loader.loadFont("Fonts/LuconBlue.egg"),
			"orange": loader.loadFont("Fonts/LuconOrange.egg")
		}
		
		gui = Gui(self.fonts)
		self.race = Race(self.inputMaager, gui)
		self.race.createDemoRace()
		self.createStartMenu()

		musicMgr = base.musicManager
		self.music = musicMgr.getSound("Sound/music_1.wav")
		self.music.setLoop(True)
		self.music.setVolume(.5)
		self.music.play()

	def createStartMenu(self):
		menu = Menu(self.menuGraphics, self.fonts, self.inputManager)
		menu.initMenu([0, None, ["New Game", "Quit Game"], [[self.race.createRace, self.createReadyDialogue], [base.userExit]], [[None, None], [None]]])

	def createReadyDialogue(self):
		menu = Menu(self.menuGraphics, self.fonts, self.inputManager)
		menu.initMenu([3, "Ready?", ["Yes", "Exit"], [[self.race.startRace], [self.race.createDemoRace]], [[3], [None]]])

	def debugTask(self, task):
		print(taskMgr)
		return task.again

w = World()
run()
