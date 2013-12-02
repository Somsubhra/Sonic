from pandac.PandaModules import EggData, Point3

from MarkerClass import Marker
from UtilityFunctions import trueDist


class TrackLanes:
    def __init__(self):
        MarkerEgg = EggData()

        MarkerEgg.read("Models/Markers.egg")

        self.markerRoot = render.attachNewNode("MarkerRoot")

        markers = self.createMarkers(MarkerEgg)
        self.prepMarkers(markers)

        for L in self.lanes:
            for M in L:
                M.setFacing()

    def createMarkers(self, eggData):

        markers = []

        vertexPool = eggData.getFirstChild()

        count = 0

        while (count != -1):
            vertex = vertexPool.getVertex(count)

            if (vertex != None):

                if (vertex.getNumDimensions() == 3):
                    vertexPos = Point3(vertex.getPos3().getX(), vertex.getPos3().getZ() * -1, vertex.getPos3().getY())

                    markers.append(Marker(vertexPos))

                count += 1

            else:
                count = -1

        switch = False

        while (switch == False):

            child = eggData.getNextChild()

            if (child != None):

                if (str(child.getClassType()) == "EggLine"):
                    vertA = child.getVertex(0).getIndex()
                    vertB = child.getVertex(1).getIndex()

                    markers[vertA].adjMarkers.append(markers[vertB])
                    markers[vertB].adjMarkers.append(markers[vertA])

            else:
                switch = True
        return (markers)

    def prepMarkers(self, markers):
        self.lanes = []

        for M in markers:
            if (M.getPos().getY() == 0 and len(M.adjMarkers) < 2):
                self.lanes.append([M])

        if (self.lanes[0][0].getPos().getX() > self.lanes[1][0].getPos().getX()):
            self.lanes.append(self.lanes[0])
            del self.lanes[0]

        for L in self.lanes:
            processed = []
            L[0].nextMarker = L[0].adjMarkers[0]
            L[0].adjMarkers[0].prevMarker = L[0]

            L[0].lane = self.lanes.index(L)
            L[0].index = 0

            processed.append(L[0])

            M = L[0].nextMarker

            while M != None:

                if (len(M.adjMarkers) > 1):

                    if (M.adjMarkers[0] in processed):

                        M.nextMarker = M.adjMarkers[1]
                        M.adjMarkers[1].prevMarker = M

                    else:
                        M.nextMarker = M.adjMarkers[0]
                        M.adjMarkers[0].prevMarker = M

                    processed.append(M)

                    M.lane = self.lanes.index(L)
                    M.index = len(L)
                    L.append(M)

                    M = M.nextMarker
                else:
                    M.index = len(L)
                    L.append(M)

                    M.nextMarker = L[0]
                    L[0].prevMarker = M

                    M = None

        for M in markers:
            M.adjMarkers = None
            M.np.reparentTo(self.markerRoot)

        return

    def getNearestMarker(self, actor):
        marker = self.lanes[0][0]
        for L in self.lanes:
            for M in L:
                if (trueDist(actor.getPos(), M.getPos()) < trueDist(actor.getPos(), marker.getPos())):
                    marker = M
        return (marker)

    def destroy(self):
        for L in self.lanes:
            for M in L:
                M.destroy()

        return