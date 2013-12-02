from pandac.PandaModules import Vec3


class Marker:
    def __init__(self, pos):
        self.lane = 0
        self.index = 0

        self.np = render.attachNewNode("MarkerNP")
        self.np.setPos(pos.getX(), pos.getY(), pos.getZ())

        self.nextMarker = None
        self.prevMarker = None

        self.adjMarkers = []

        self.facingVec = Vec3(0, 1, 0)
        self.actorVec = Vec3(0, 0, 0)

    def getPos(self, ref=None):
        if (ref == None):
            return (self.np.getPos())
        else:
            return (self.np.getPos(ref))
        return

    def getHpr(self, ref=None):
        if (ref == None):
            return (self.np.getHpr())
        else:
            return (self.np.getHpr(ref))
        return

    def setFacing(self):
        nmp = self.nextMarker.getPos()
        self.np.lookAt(nmp.getX(), nmp.getY(), self.np.getPos().getZ())
        return

    def checkInFront(self, actor):

        actorPos = actor.root.getPos(self.np)
        self.actorVec.set(actorPos.getX(), actorPos.getY(), self.np.getZ())
        self.actorVec.normalize()

        actorAngle = self.facingVec.angleDeg(self.actorVec)

        if (actorAngle > 90):
            return (False)
        else:
            return (True)

    def destroy(self):
        self.np.removeNode()
        return
