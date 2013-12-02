import direct.directbase.DirectStart
from pandac.PandaModules import *

#from InputManagerClass_00 import InputManager

class BamWriter:
	def __init__(self):
		base.setBackgroundColor(0, 0, 0)
		# Sets the background color to black to make it easier to see things.
		
		base.disableMouse()
		# Turns off the default mouse camera controls.
		
		base.camera.setPos(0, 10, 0)
		base.camera.setH(180)
		# Moves the camera back so we can see the models we load.
		
		#self.inputManager = InputManager()
		# Creates an input manager so we can get user input.
		
		#taskMgr.add(self.inputTask, "Input Task")
		# Adds the input task that monitors for user input to the task manager so it will
		# run every frame.
		
		self.setupLight()
		# Calls the setupLight method to create out lighting environment.
		
		render.setShaderAuto()
		# Turns on Panda3D's automatic shader generation.
		
		self.modelRoot = render.attachNewNode("Model Root")
		# Creates a base NodePath for all the models to be children of.
		# This will be the NodePath we rotate to see the model from various angles.
				
		self.setupModels()
		# Calls the method that sets up the models.
		
		self.modelRoot.writeBamFile("YellowCycle.bam")
		# Writes out the modelRoot node and all its children into a bam file.
		
	def setupLight(self):
		primeL = DirectionalLight("prime")
		primeL.setColor(VBase4(.6,.6,.6,1))
		# Creates the primary directional light and sets it's color to 60%. 
		self.dirLight = render.attachNewNode(primeL)
		self.dirLight.setHpr(45,-60,0)
		# Assigns the light to a nodePath and rotates that nodePath to aim the light.
		
		render.setLight(self.dirLight)
		# Sets the directional light to illuminate everything attached to the render node.
		
		ambL = AmbientLight("amb")
		ambL.setColor(VBase4(.2,.2,.2,1))
		self.ambLight = render.attachNewNode(ambL)
		# Creates an ambient light to fill in the shadows and sets it's color to 20%.
		# also places it in a NodePath.
		
		render.setLight(self.ambLight)
		# Sets the ambient light to illuminate the scene.
		
	def inputTask(self, task):
		if(self.inputManager.keyMap["w"] == True):
			self.modelRoot.setP(self.modelRoot, .5)
		# Raises the model's pitch when w is pressed.
		
		elif(self.inputManager.keyMap["s"] == True):
			self.modelRoot.setP(self.modelRoot, -.5)
		# Lowers the model's pitch when s is pressed.
		
		if(self.inputManager.keyMap["a"] == True):
			self.modelRoot.setH(self.modelRoot, .5)
		# Raises the model's heading when a is pressed.
		
		elif(self.inputManager.keyMap["d"] == True):
			self.modelRoot.setH(self.modelRoot, -.5)
		# Lowers the model's heading when d is pressed.
		
		return task.again
		
	def setupModels(self):
		self.glossTS = TextureStage("glossTS")
		self.glossTS.setMode(TextureStage.MModulateGloss)
		# Creates a texture stage and changes it's mode to MModulateGloss, which will use the RGB
		# component of the texture for color, and the Alpha component for a gloss effect.
		
		self.normalTS = TextureStage("normalTS")
		self.normalTS.setMode(TextureStage.MNormal)
		# Creates a texture stage and changes its mode to MNormal, which will apply it as a 
		# normal map.
		
		self.glowTS = TextureStage("glowTS")
		self.glowTS.setMode(TextureStage.MModulateGlow)
		# Creates a texture stage and changes its mode to MModulateGlow, which will apply it as 
		# both a Modulate map and a Glow map.
		
		self.moulding =  loader.loadModel("../Models/Moulding.egg")
		self.moulding.reparentTo(self.modelRoot)
		# Loads the molding model and adds it to the scene.
		
		self.teamTex = loader.loadTexture("../Images/YellowTeamTex.png",
			"../Images/HighGloss.png")
		# Loads the image RedTeamTex.png as an RGB image, 
		# and stuffs HighGloss.png into it's Alpha component.
		
		self.moulding.setTexture(self.glossTS, self.teamTex)
		# Applies the texture we loaded to the molding using the glossTS TextureStage.
		
		self.normalTex = loader.loadTexture("../Images/Normal.png")
		# Loads a blank white image to use as a normal map.
		
		self.moulding.setTexture(self.normalTS, self.normalTex)
		# Applies another texture using the normalTS TextureStage.
		
		self.pp1 = loader.loadModel("../Models/PP1.egg")
		self.pp1.reparentTo(self.modelRoot)
		self.pp2 = loader.loadModel("../Models/PP2.egg")
		self.pp2.reparentTo(self.modelRoot)
		# Loads the two pieces of the power plant and connects them to the modelRoot.
		
		self.metalTex = loader.loadTexture("../Images/Metal.png", 
			"../Images/HighGloss.png")
		# Loads the image PlainMetal.png as an RGB image, 
		# and stuffs HighGloss.png into it's Alpha component.
		
		self.pp1.setTexture(self.glossTS, self.metalTex)
		# Assigns the plain metal texture to pp1 as an RGB-Gloss map.
		
		self.glowTex = loader.loadTexture("../Images/Blue.png",
			"../Images/HighGlow.png")
		# Loads the image PlainMetal.png as an RGB image, 
		# and stuffs HighGloss.png into it's Alpha component.
		
		self.pp2.setTexture(self.glowTS, self.glowTex)
		# Assigns the glow texture to pp2 as an RGB-Glow map.
		
		self.coffin = loader.loadModel("../Models/Coffin.egg")
		self.coffin.reparentTo(self.modelRoot)
		# Loads the coffin and connects it to the model root.
		
		self.coffinTex = loader.loadTexture("../Images/Coffin.png",
			"../Images/HighGloss.png")
		# Loads the texture for the coffin, with HighGloss.png in
		# the alpha channel.
		
		self.coffin.setTexture(self.glossTS, self.coffinTex)
		# Assigns the coffin texture to the coffin.
		
		self.frame = loader.loadModel("../Models/Frame.egg")
		self.frame.reparentTo(self.modelRoot)
		self.fuelTank = loader.loadModel("../Models/FuelTank.egg")
		self.fuelTank.reparentTo(self.modelRoot)
		self.sp1 = loader.loadModel("../Models/SP1.egg")
		self.sp1.reparentTo(self.modelRoot)
		self.sp2 = loader.loadModel("../Models/SP2.egg")
		self.sp2.reparentTo(self.modelRoot)
		# Loads the models for the frame, fuel tank, and shield projector
		# and connects the to the modelRoot.
		
		self.frame.setTexture(self.glossTS, self.metalTex)
		self.fuelTank.setTexture(self.glossTS, self.metalTex)
		self.sp1.setTexture(self.glossTS, self.metalTex)
		self.sp2.setTexture(self.glowTS, self.glowTex)
		# Assigns textures to the remaining pieces.

BW = BamWriter()
run()