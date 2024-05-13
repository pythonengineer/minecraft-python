import math

class Vec3D:

    def __init__(self, x, y, z):
        self.xCoord = x
        self.yCoord = y
        self.zCoord = z

    def addVector(self, x, y, z):
        return Vec3D(self.xCoord + x, self.yCoord + y, self.zCoord + z)

    def distanceTo(self, vec):
        xd = vec.xCoord - self.xCoord
        yd = vec.yCoord - self.yCoord
        zd = vec.zCoord - self.zCoord
        return math.sqrt(xd * xd + yd * yd + zd * zd)

    def squaredDistanceTo(self, vec):
        xd = vec.xCoord - self.xCoord
        yd = vec.yCoord - self.yCoord
        zd = vec.zCoord - self.zCoord
        return xd * xd + yd * yd + zd * zd

    def getIntermediateWithXValue(self, vec, xa):
        xd = vec.xCoord - self.xCoord
        yd = vec.yCoord - self.yCoord
        zd = vec.zCoord - self.zCoord
        if xd * xd < 1.0E-7:
            return

        xa = (xa - self.xCoord) / xd
        if xa >= 0.0 and xa <= 1.0:
            return Vec3D(self.xCoord + xd * xa, self.yCoord + yd * xa,
                         self.zCoord + zd * xa)

    def getIntermediateWithYValue(self, vec, ya):
        xd = vec.xCoord - self.xCoord
        yd = vec.yCoord - self.yCoord
        zd = vec.zCoord - self.zCoord
        if yd * yd < 1.0E-7:
            return

        ya = (ya - self.yCoord) / yd
        if ya >= 0.0 and ya <= 1.0:
            return Vec3D(self.xCoord + xd * ya, self.yCoord + yd * ya,
                         self.zCoord + zd * ya)

    def getIntermediateWithZValue(self, vec, za):
        xd = vec.xCoord - self.xCoord
        yd = vec.yCoord - self.yCoord
        zd = vec.zCoord - self.zCoord
        if zd * zd < 1.0E-7:
            return

        za = (za - self.zCoord) / zd
        if za >= 0.0 and za <= 1.0:
            return Vec3D(self.xCoord + xd * za, self.yCoord + yd * za,
                         self.zCoord + zd * za)

    def toString(self):
        return '(' + self.xCoord + ', ' + self.yCoord + ', ' + self.zCoord + ')'
