from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *


class Gui:
    def __init__(self, fonts):
	self.score = 0
        self.modTS = TextureStage("Modulate")
        self.modTS.setMode(TextureStage.MModulate)

        self.createLLGui(fonts)

        self.createURGui(fonts)

        self.createWarning(fonts)

        self.visible = False

        taskMgr.add(self.updateGui, "Update Gui")

    def setActor(self, actor):
        self.actor = actor
        return

    def createLLGui(self, fonts):
        self.llFrame = DirectFrame(
            frameSize=(0, 0.60, 0, .45),
            frameColor=(1, 1, 1, 0),
            parent=base.a2dBottomLeft
        )

        speedEgg = loader.loadModel("Models/SpeedBar.egg")
        self.speedBG = speedEgg.find("**/BackgroundBar")
        self.speedBar = speedEgg.find("**/SpeedBar")
        self.speedFrame = speedEgg.find("**/BarFrame")
        self.speedBG.reparentTo(self.llFrame)
        self.speedBar.reparentTo(self.speedBG)
        self.speedFrame.reparentTo(self.speedBG)
        self.speedBG.setPos(.175, 0, .225)

        alpha = loader.loadTexture("Images/BarAlpha.png")
        alpha.setFormat(Texture.FAlpha)
        alpha.setWrapV(Texture.WMClamp)

        self.speedBar.setTexture(self.modTS, alpha)

        self.throttleBar = speedEgg.find("**/ThrottleBar")
        self.throttleBar.reparentTo(self.speedBG)

        throtAlpha = loader.loadTexture("Images/ThrottleAlpha.png")
        throtAlpha.setFormat(Texture.FAlpha)
        self.throttleBar.setTexture(self.modTS, throtAlpha)

        self.speedText = DirectLabel(text="180 KPH",
                                     text_font=fonts["orange"], text_scale=.075,
                                     pos=(.5, 0, .15), text_fg=(1, 1, 1, 1),
                                     relief=None, text_align=TextNode.ARight,
                                     parent=self.llFrame)

        return

    def createURGui(self, fonts):
        self.urFrame = DirectFrame(frameSize=(-.6, 0, -.4, 0),
                                   frameColor=(1, 1, 1, 0),
                                   parent=base.a2dTopRight
        )

        self.energyText = DirectLabel(text="Score:0",
                                      text_font=fonts["orange"], text_scale=.05,
                                      pos=(-.65, 0, -.0525), text_fg=(1, 1, 1, 1),
                                      relief=None, text_align=TextNode.ARight,
                                      parent=self.urFrame)

        return

    def createWarning(self, fonts):
        self.warning = DirectLabel(
            text="*** Emergency Shut Down Active ***",
            text_font=fonts["orange"], text_scale=.1,
            text_fg=(1, 1, 1, 0), relief=None,
            text_align=TextNode.ACenter,
            parent=base.aspect2d)

        self.warningLerp = LerpFunc(self.fadeWarning,
                                    fromData=1,
                                    toData=0,
                                    duration=.5)

        self.warningSeq = Sequence(
            Func(self.showWarning),
            Wait(1),
            self.warningLerp,
            Wait(.5))

        return

    def updateLLGui(self):
        if (self.actor.throttle >= 0):
            self.throttleBar.setColor(0, 1, 0)
            throtRatio = 1 - self.actor.throttle
        else:
            self.throttleBar.setColor(1, 1, 1)
            throtRatio = 1 + self.actor.throttle

        self.throttleBar.setTexOffset(TextureStage.getDefault(),
                                      0, .925 * throtRatio)

        if (self.actor.speed >= 0):
            speedRatio = (self.actor.maxSpeed -
                          self.actor.speed) / self.actor.maxSpeed
        else:
            speedRatio = (self.actor.maxSpeed +
                          self.actor.speed) / self.actor.maxSpeed

        self.speedBar.setTexOffset(self.modTS, 0, .95 * speedRatio)

        self.speedText["text"] = str(int(self.actor.speed)) + " KPH"

        return

    def updateURGui(self):
	self.score = self.score + self.actor.speed/10
        self.energyText["text"] = "Score:"+str(int(self.score))
        return

    def updateGui(self, task):
        dt = globalClock.getDt()
        if (dt > .20):
            return task.cont

        if (self.visible == True):

            self.updateLLGui()
	    self.updateURGui()

            if (self.actor.shutDown == True and
                        self.warningSeq.isPlaying() == False):
                self.warningSeq.loop()

            if (self.actor.shutDown == False and
                        self.warningSeq.isPlaying() == True):
                self.warningSeq.finish()

        return task.cont

    def hide(self):
        self.llFrame.hide()
        self.urFrame.hide()
        self.visible = False
        return

    def show(self):
        self.llFrame.show()
        self.urFrame.show()
        self.visible = True
        return

    def showWarning(self):
        self.warning["text_fg"] = (1,1,1,1)
        return

    def fadeWarning(self, T):
        self.warning["text_fg"] = (1,1,1,T)
        return
