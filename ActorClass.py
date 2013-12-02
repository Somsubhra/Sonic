from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from ActorAIClass import ActorAI


class Actor(DirectObject):
    def __init__(self, inputManager, track, audio3D, startPos,
                 name, ai=None):
        self.inputManager = inputManager

        self.setupVarsNPs(audio3D, startPos, name)
        self.setupCollisions()

        self.track = track

        self.lanes = self.track.trackLanes.lanes

        startingLane = self.track.trackLanes.getNearestMarker(self).lane

        self.uc1 = self.lanes[startingLane][0]
        self.uc2 = self.lanes[startingLane][1]
        self.uc3 = self.lanes[startingLane][2]

        if (ai == True):
            self.ai = ActorAI(self)
        elif (ai == None):
            self.ai = None
            taskMgr.add(self.actorControl, "Actor Control", sort=int(self.root.getY() + 100))

        self.setupLight()

    def setupVarsNPs(self, audio3D, startPos, name):
        self.name = name

        self.audio3D = audio3D

        self.root = render.attachNewNode("Root")

        self.actor = self.root.attachNewNode("Actor")

        if (startPos == 1):
            self.root.setPos(5, 0, 0)
            self.model = loader.loadModel("Models/sonic.egg")
            self.model.setScale(0.1,0.1,0.1)
            self.model.setHpr(180,0,0)
        elif (startPos == 2):
            self.root.setPos(-5, -5, 0)
            self.model = loader.loadModel("Models/BlueActor.bam")
        elif (startPos == 3):
            self.root.setPos(5, -10, 0)
            self.model = loader.loadModel("Models/GreenActor.bam")
        elif (startPos == 4):
            self.root.setPos(-5, -15, 0)
            self.model = loader.loadModel("Models/YellowActor.bam")

        #self.mounts = Actor("Models/Mounts.egg")

        self.model.reparentTo(self.actor)
        #self.mounts.reparentTo(self.model)

        self.fd = loader.loadModel("Models/Disc.bam")
        self.rd = loader.loadModel("Models/Disc.bam")

        self.engineSfx = self.audio3D.loadSfx("Sound/Engine.wav")
        self.audio3D.attachSoundToObject(self.engineSfx, self.root)
        self.engineSfx.setPlayRate(.5)
        self.engineSfx.setLoop(True)
        self.engineSfx.setVolume(2)
        self.engineSfx.play()

        self.dirNP = self.root.attachNewNode("DirNP")
        self.refNP = self.root.attachNewNode("RefNP")

        self.dirVec = Vec3(0, 0, 0)
        self.actorVec = Vec3(0, 0, 0)
        self.refVec = Vec3(0, 0, 0)

        self.speed = 0
        self.throttle = 0
        self.maxSpeed = 500
        self.maxShield = 500
        self.shield = self.maxShield
        self.accel = 25
        self.handling = 25
        self.maxEnergy = 100
        self.energy = self.maxEnergy
        self.stability = 25
        self.shieldRchrg = 10
        self.energyRchrg = 5
        self.shutDown = False

        self.turning = None
        self.lean = 0

        self.markerCount = 0
        self.currentLap = 0

        self.freeFall = False
        self.fallSpeed = 0
        self.trackNP = render.attachNewNode(self.name + "_TrackNode")

        self.active = False

        return

    def setupCollisions(self):
        self.shieldCN = CollisionNode(self.name + "_ShieldCN")

        self.shieldCN.setPythonTag("owner", self)

        CS1 = CollisionSphere(0, -.025, .75, .785)
        CS2 = CollisionSphere(0, -1.075, .85, .835)
        CS3 = CollisionSphere(0, 1.125, .6, .61)
        self.shieldCN.addSolid(CS1)
        self.shieldCN.addSolid(CS2)
        self.shieldCN.addSolid(CS3)

        self.shieldCN.setIntoCollideMask(BitMask32.range(2, 3))
        self.shieldCN.setFromCollideMask(BitMask32.bit(2))

        self.shieldCNP = self.model.attachNewNode(self.shieldCN)

        self.bumpCTrav = CollisionTraverser()
        self.bumpHan = CollisionHandlerPusher()

        self.bumpHan.addCollider(self.shieldCNP, self.root)

        self.bumpHan.addAgainPattern("%fn-again")

        self.bumpCTrav.addCollider(self.shieldCNP, self.bumpHan)

        self.accept(self.name + "_ShieldCN-again", self.bump)

        self.gRayCN = CollisionNode(self.name + "_GRayCN")

        self.fRay = CollisionRay(0, .5, 10, 0, 0, -1)
        self.bRay = CollisionRay(0, -.5, 10, 0, 0, -1)

        self.gRayCN.addSolid(self.fRay)
        self.gRayCN.addSolid(self.bRay)

        self.gRayCN.setFromCollideMask(BitMask32.bit(1))
        self.gRayCN.setIntoCollideMask(BitMask32.allOff())

        self.gRayCNP = self.actor.attachNewNode(self.gRayCN)

        self.gCTrav = CollisionTraverser()
        self.gHan = CollisionHandlerQueue()
        self.gCTrav.addCollider(self.gRayCNP, self.gHan)

        self.trgtrCN = CollisionNode(self.name + "_TargeterCN")
        self.trgtrRay = CollisionRay(0, 0, 0, 0, 1, 0)
        self.trgtrCN.addSolid(self.trgtrRay)
        self.trgtrCN.setFromCollideMask(BitMask32.bit(3))
        self.trgtrCN.setIntoCollideMask(BitMask32.allOff())
        #self.trgtrCNP = self.trgtrMount.attachNewNode(self.trgtrCN)

        self.trgtrCTrav = CollisionTraverser()
        self.trgtrCHan = CollisionHandlerQueue()
        #self.trgtrCTrav.addCollider(self.trgtrCNP, self.trgtrCHan)

        return

    def setupLight(self):
        self.glow = self.actor.attachNewNode(
            PointLight(self.name + "Glow"))
        self.glow.node().setColor(Vec4(.2, .6, 1, 1))

        self.glow.node().setAttenuation(Vec3(0, 0, .75))

        self.actor.setLight(self.glow)
        self.track.track.setLight(self.glow)
        return

    def actorControl(self, task):
        if (self.actor == None):
            return task.done

        dt = globalClock.getDt()
        if ( dt > .20):
            return task.cont

        if (self.active == True and self.shutDown == False):
            if (self.inputManager.keyMap["up"] == True):
                self.adjustThrottle("up", dt)
            elif (self.inputManager.keyMap["down"] == True):
                self.adjustThrottle("down", dt)

            if (self.inputManager.keyMap["right"] == True):
                self.turn("r", dt)
                self.turning = "r"
            elif (self.inputManager.keyMap["left"] == True):
                self.turn("l", dt)
                self.turning = "l"
            else:
                self.turning = None

        self.speedCheck(dt)
        self.simDrift(dt)
        self.groundCheck(dt)
        self.move(dt)
        self.checkMarkers()
        self.recharge(dt)

        self.bumpCTrav.traverse(render)

        return task.cont

    def cameraZoom(self, dir, dt):
        if (dir == "in"):
            base.camera.setY(base.camera, 10 * dt)
        else:
            base.camera.setY(base.camera, -10 * dt)
        return

    def turn(self, dir, dt):
        turnRate = self.handling * (2 -
                                    (self.speed / self.maxSpeed))

        if (dir == "r"):
            turnRate = -turnRate
            self.turning = "r"

        self.actor.setH(self.actor, turnRate * dt)
        return

    def adjustThrottle(self, dir, dt):
        if (dir == "up"):
            self.throttle += .25 * dt
            if (self.throttle > 1 ): self.throttle = 1
        else:
            self.throttle -= .25 * dt
            if (self.throttle < -1 ): self.throttle = -1
        return

    def speedCheck(self, dt):
        if (self.freeFall == False):
            tSetting = (self.maxSpeed * self.throttle)

            if (self.speed < tSetting):
                if ((self.speed + (self.accel * dt)) > tSetting):
                    self.speed = tSetting
                else:
                    self.speed += (self.accel * dt)

            elif (self.speed > tSetting):
                if ((self.speed - (self.accel * dt)) < tSetting):
                    self.speed = tSetting
                else:
                    self.speed -= (self.accel * dt)
        else:
            self.speed -= (self.speed * .125) * dt

        speedRatio = self.speed / self.maxSpeed
        self.engineSfx.setPlayRate(.5 + speedRatio)
        return

    def simDrift(self, dt):
        self.refNP.setPos(self.dirNP, 0, 1, 0)
        self.dirVec.set(self.refNP.getX(), self.refNP.getY(), 0)

        self.refNP.setPos(self.actor, 0, 1, 0)
        self.actorVec.set(self.refNP.getX(), self.refNP.getY(), 0)

        self.refVec.set(0, 0, 1)

        vecDiff = self.dirVec.signedAngleDeg(self.actorVec,
                                             self.refVec)

        if (vecDiff < .1 and vecDiff > -.1):
            self.dirNP.setHpr(self.actor.getH(), 0, 0)

        else:
            self.dirNP.setHpr(self.dirNP, vecDiff * dt * 2.5, 0, 0)

        self.dirNP.setP(self.actor.getP())
        self.dirNP.setR(0)
        return

    def groundCheck(self, dt):
        self.gCTrav.traverse(render)

        points = [None, None]

        if (self.gHan.getNumEntries() > 1):
            self.gHan.sortEntries()

            for E in range(self.gHan.getNumEntries()):
                entry = self.gHan.getEntry(E)
                if (entry.getFrom() == self.fRay and points[0] == None):
                    points[0] = entry.getSurfacePoint(render)
                elif (entry.getFrom() == self.bRay and points[1] == None):
                    points[1] = entry.getSurfacePoint(render)

        if (points[0] == None or points[1] == None):
            self.teleport()
            return
        else:
            if (self.freeFall == False):
                self.refNP.setPos(points[1])
                self.refNP.lookAt(points[0])

                pDiff = self.refNP.getP() - self.actor.getP()

                if (pDiff < .1 and pDiff > -.1):
                    self.actor.setP(self.refNP.getP())
                else:
                    self.actor.setP(self.actor, pDiff * dt * 5)

            elif ((self.actor.getP() - (dt * 10)) > -15):
                self.actor.setP(self.actor, -(dt * 10))
            else:
                self.actor.setP(-15)
            if (self.speed >= 0):
                self.trackNP.setPos(points[0].getX(),
                                    points[0].getY(), points[0].getZ())
            else:
                self.trackNP.setPos(points[1].getX(),
                                    points[1].getY(), points[1].getZ())

            height = self.root.getZ(self.trackNP)

            if (height > 2 and self.freeFall == False):
                self.freeFall = True
                self.fallSpeed = 0

            if (self.freeFall == True):
                self.fallSpeed += (self.track.gravity * 9.8) * dt
                newHeight = height - (self.fallSpeed * dt)
            else:
                hDiff = 1 - height
                if (hDiff > .01 or hDiff < -.01):
                    newHeight = height + (hDiff * dt * 5)
                else:
                    newHeight = 1

            if (newHeight >= 0):
                self.root.setZ(self.trackNP, newHeight)
            else:
                self.root.setZ(self.trackNP, 0)
                self.freeFall = False
            self.actor.setR(0)

        return

    def move(self, dt):
        mps = self.speed * 1000 / 3600

        self.refNP.setPos(self.dirNP, 0, 1, 0)
        self.dirVec.set(self.refNP.getX(), self.refNP.getY(),
                        self.refNP.getZ())

        self.root.setPos(self.root,
                         self.dirVec.getX() * dt * mps,
                         self.dirVec.getY() * dt * mps,
                         self.dirVec.getZ() * dt * mps)

        currentLean = self.model.getR()

        if (self.turning == "r"):
            self.lean -= 2.5
            if (self.lean < -25): self.lean = -25
            self.model.setR(self.model,
                            (self.lean - currentLean) * dt * 5)

        elif (self.turning == "l"):
            self.lean += 2.5
            if (self.lean > 25): self.lean = 25
            self.model.setR(self.model,
                            (self.lean - currentLean) * dt * 5)

        else:
            self.lean = 0
            self.model.setR(self.model,
                            (self.lean - currentLean) * dt * 5)

        self.fd.setH(self.fd, 5 + (20 * self.throttle))
        self.rd.setH(self.rd, -5 + (-20 * self.throttle))

        return

    def checkMarkers(self):
        if (self.uc1.checkInFront(self) == True):
            self.uc1 = self.uc2
            self.uc2 = self.uc3
            self.uc3 = self.uc2.nextMarker

            self.markerCount += 1

            if (self.uc1 == self.lanes[0][1] or self.uc1 == self.lanes[1][1]):
                self.currentLap += 1

        return

    def recharge(self, dt):
        if (self.energy < self.maxEnergy and self.shutDown == False):

            newEnergy = self.energy + (self.energyRchrg * dt)

            if (newEnergy > self.maxEnergy):
                self.energy = self.maxEnergy
            else:
                self.energy = newEnergy

        if (self.shield <= 0 and self.shutDown == False):
            self.shutDown = True
            self.throttle = 0
            self.shield = 0

        if (self.shutDown == True):
            newShield = self.shield + (self.shieldRchrg * dt) * 10
            if (newShield >= self.maxShield):
                self.shutDown = False

        elif (self.shield < self.maxShield):
            newShield = self.shield + (self.shieldRchrg * dt)

        else:
            return

        if (newShield <= self.maxShield):
            self.shield = newShield
        else:
            self.shield = self.maxShield

        return

    def teleport(self):
        marker = self.track.trackLanes.getNearestMarker(self)
        markerPos = marker.getPos()
        self.root.setPos(markerPos.getX(),
                         markerPos.getY(), self.root.getZ())

        self.gCTrav.traverse(render)

        points = [None, None]

        if (self.gHan.getNumEntries() > 1):

            self.gHan.sortEntries()

            for E in range(self.gHan.getNumEntries()):

                entry = self.gHan.getEntry(E)

                if (entry.getFrom() == self.fRay and points[0] == None):
                    points[0] = entry.getSurfacePoint(render)
                elif (entry.getFrom() == self.bRay and points[1] == None):
                    points[1] = entry.getSurfacePoint(render)

            if (self.speed >= 0):
                self.trackNP.setPos(points[0].getX(),
                                    points[0].getY(), points[0].getZ())
            else:
                self.trackNP.setPos(points[1].getX(),
                                    points[1].getY(), points[1].getZ())

            self.root.setZ(self.trackNP, 1)

        self.dirNP.setHpr(marker.getHpr())
        self.actor.setHpr(marker.getHpr())

        self.speed /= 2

        return

    def bump(self, entry):
        #print(entry.getFromNodePath().getPythonTag("owner").name)
        #print("has bumped into:")
        #print(entry.getIntoNodePath().getPythonTag("owner").name)
        #print("")
        return

    def hit(self, damage):
        self.shield -= damage

        instability = (damage / 2) - self.stability

        if (instability > 0):
            self.speed -= instability

        return

    def getPos(self, ref=None):
        if (ref == None):
            return (self.root.getPos())
        else:
            return (self.root.getPos(ref))

    def destroy(self):
        self.root.removeNode()
        self.actor.removeNode()
        #self.mounts.delete()
        self.model.removeNode()
        self.fd.removeNode()
        self.rd.removeNode()
        self.dirNP.removeNode()
        self.refNP.removeNode()
        self.trackNP.removeNode()
        self.shieldCNP.removeNode()
        self.gRayCNP.removeNode()
        #self.trgtrCNP.removeNode()
        self.glow.removeNode()

        self.audio3D.detachSound(self.engineSfx)

        self.actor = None

        if (self.ai != None):
            self.ai = None

        return
