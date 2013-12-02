import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject


class BamWriter(DirectObject):
	def __init__(self):
		
		self.model1 = loader.loadModel("Explosions/Laserburst3.egg")
		self.model1.setLightOff()
		self.model1.setBillboardAxis()	
		
		self.model1.reparentTo(render)
		result = self.model1.writeBamFile("Explosions/Laserburst3.bam")

		print(result)

BM = BamWriter()
run()
		