from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from UtilityFunctions import *

class ActorAI:
    def __init__(self, actor):
        self.actor = actor

        taskMgr.doMethodLater(getRandom(0, 1), self.runPilotAI, self.actor.name + " Run Pilot AI",
                              sort=int(self.actor.root.getY() + 100))

        if (self.actor.uc1 in self.actor.lanes[0]):
            self.lane = 0
        else:
            self.lane = 1

        self.riskRange = [10, 20]
        self.foresightRange = [3, 5]

        self.laneChangeChance = .5

        self.laneChangeAttempted = False

        self.riskMod = 0
        self.foresightMod = 0
        self.newTurnPrep()

        self.newTurn = False

        self.ucF = self.actor.lanes[self.lane][self.actor.uc3.index + self.foresightMod]

        self.detCN = CollisionNode(self.actor.name + "_DetCN")
        self.detCS = CollisionSphere(0, 0, 0, 50)
        self.detCN.addSolid(self.detCS)
        self.detCN.setIntoCollideMask(BitMask32.allOff())
        self.detCN.setFromCollideMask(BitMask32.bit(4))
        self.detCNP = self.actor.root.attachNewNode(self.detCN)

        self.dCTrav = CollisionTraverser()
        self.dCHan = CollisionHandlerQueue()
        self.dCTrav.addCollider(self.detCNP, self.dCHan)

    def runPilotAI(self, task):
        if (self.actor.actor == None):
            self.destroy()
            return task.done

        dt = globalClock.getDt()
        if (dt > .20):
            return task.cont

        if (self.actor.active == True):
            self.checkDistantTurn(dt)

            self.checkNearTurn(dt)

        self.actor.speedCheck(dt)

        self.actor.simDrift(dt)

        self.actor.groundCheck(dt)

        self.actor.move(dt)

        self.checkMarkers()

        self.actor.bumpCTrav.traverse(render)

        return task.cont

    def checkDistantTurn(self, dt):
        turnAngle = self.findAngle(self.ucF, self.actor.actor)

        if (turnAngle < 1 and turnAngle > -1):
            turnAngle = 0

        if (self.actor.speed == 0):
            turnRate = self.actor.handling
        else:
            turnRate = self.actor.handling * (2 - (self.actor.speed / self.actor.maxSpeed))

        if (self.actor.speed > 0):
            eta = trueDist(self.actor.actor.getPos(render), self.ucF.getPos(render)) / self.actor.speed
        else:
            eta = 0

        if (self.laneChangeAttempted == False):

            if (turnAngle < -15):
                if (self.lane != 1):
                    self.changeLanes()

                self.laneChangeAttempted = True

            elif (turnAngle > 15):
                if (self.lane != 0):
                    self.changeLanes()

                self.laneChangeAttempted = True

        if (turnAngle < 0):
            turnAngle *= -1

        if (turnAngle > (turnRate + self.riskMod) * eta and eta != 0):
            self.actor.adjustThrottle("down", dt)

        else:
            self.actor.adjustThrottle("up", dt)

        return


    def checkNearTurn(self, dt):
        turnAngle = self.findAngle(self.actor.uc3, self.actor.actor)

        if (turnAngle < 1 and turnAngle > -1):
            turnAngle = 0

        if (self.actor.speed == 0):
            turnRate = self.actor.handling
        else:
            turnRate = self.actor.handling * (2 - (self.actor.speed / self.actor.maxSpeed))

        if (turnAngle < 0):
            self.actor.turning = "r"
            turnRate *= -1

            if (turnAngle < turnRate * dt):
                self.actor.actor.setH(self.actor.actor, turnRate * dt)
            else:
                hardness = (turnRate * dt) / turnAngle
                turnRate *= hardness
                self.actor.actor.setH(self.actor.actor, turnRate * dt * hardness)

            if (self.newTurn == False):
                self.newTurn = True

        elif (turnAngle > 0):
            self.actor.turning = "l"
            if (turnAngle > turnRate * dt):
                self.actor.actor.setH(self.actor.actor, turnRate * dt)
            else:
                hardness = (turnRate * dt) / turnAngle
                turnRate *= hardness
                self.actor.actor.setH(self.actor.actor, turnRate * dt * hardness)

            if (self.newTurn == False):
                self.newTurn = True
        else:
            self.actor.turning = None

            if (self.newTurn == True):
                self.newTurnPrep()

                self.newTurn = False
        return

    def newTurnPrep(self):
        self.riskMod = getRandom(self.riskRange[0], self.riskRange[1])
        self.foresightMod = int(getRandom(self.foresightRange[0], self.foresightRange[1]))
        self.laneChangeAttempted = False

        return

    def findAngle(self, marker, nodePath):

        markPos = marker.getPos(nodePath)
        self.actor.dirVec.set(markPos.getX(), markPos.getY(), 0)
        self.actor.dirVec.normalize()

        self.actor.actorVec.set(0, 1, 0)

        self.actor.refVec.set(0, 0, 1)

        return (self.actor.actorVec.signedAngleDeg(self.actor.dirVec, self.actor.refVec))

    def changeLanes(self):
        randVal = getRandom(0, 1)
        if (randVal < self.laneChangeChance):
            if (self.lane == 0):
                self.lane = 1
                self.actor.uc1 = self.actor.lanes[1][self.actor.uc1.index]
                self.actor.uc2 = self.actor.lanes[1][self.actor.uc2.index]
                self.actor.uc3 = self.actor.lanes[1][self.actor.uc3.index]
            elif (self.lane == 1):
                self.lane = 0
                self.actor.uc1 = self.actor.lanes[0][self.actor.uc1.index]
                self.actor.uc2 = self.actor.lanes[0][self.actor.uc2.index]
                self.actor.uc3 = self.actor.lanes[0][self.actor.uc3.index]

        return

    def checkMarkers(self):
        uc1 = self.actor.uc1
        self.actor.checkMarkers()

        if (uc1 != self.actor.uc1):
            farIndex = self.actor.uc3.index + self.foresightMod
            if (farIndex >= len(self.actor.lanes[self.lane])):
                farIndex -= len(self.actor.lanes[self.lane])
            self.ucF = self.actor.lanes[self.lane][farIndex]
        return

    def checkInArc(self, actor):
        actorPos = actor.root.getPos(self.actor.actor)
        self.actor.actorVec.set(actorPos.getX(), actorPos.getY(), self.actor.actor.getZ())
        self.actor.actorVec.normalize()
        self.actor.dirVec.set(0, 1, 0)

        actorAngle = self.actor.dirVec.angleDeg(self.actor.actorVec)

        if (actorAngle > 45):
            return (False)
        else:
            return (True)

    def destroy(self):
        self.detCNP.removeNode()
        self.actor = None
        return