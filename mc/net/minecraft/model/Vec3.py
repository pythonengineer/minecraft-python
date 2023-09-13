import math

class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def subtract(self, vec):
        return Vec3(self.x - vec.x, self.y - vec.y, self.z - vec.z)

    def normalize(self):
        f = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return Vec3(self.x / f, self.y / f, self.z / f)

    def add(self, x, y, z):
        return Vec3(self.x + x, self.y + y, self.z + z)

    def distanceTo(self, vec):
        xd = vec.x - self.x
        yd = vec.y - self.y
        zd = vec.z - self.z
        return math.sqrt(xd * xd + yd * yd + zd * zd)

    def distanceToSqr(self, vec):
        xd = vec.x - self.x
        yd = vec.y - self.y
        zd = vec.z - self.z
        return xd * xd + yd * yd + zd * zd

    def clipX(self, vec, xa):
        xd = vec.x - self.x
        yd = vec.y - self.y
        zd = vec.z - self.z
        if xd * xd < 1.0E-7:
            return

        xa = (xa - self.x) / xd
        if xa >= 0.0 and xa <= 1.0:
            return Vec3(self.x + xd * xa, self.y + yd * xa, self.z + zd * xa)

    def clipY(self, vec, ya):
        xd = vec.x - self.x
        yd = vec.y - self.y
        zd = vec.z - self.z
        if yd * yd < 1.0E-7:
            return

        ya = (ya - self.y) / yd
        if ya >= 0.0 and ya <= 1.0:
            return Vec3(self.x + xd * ya, self.y + yd * ya, self.z + zd * ya)

    def clipZ(self, vec, za):
        xd = vec.x - self.x
        yd = vec.y - self.y
        zd = vec.z - self.z
        if zd * zd < 1.0E-7:
            return

        za = (za - self.z) / zd
        if za >= 0.0 and za <= 1.0:
            return Vec3(self.x + xd * za, self.y + yd * za, self.z + zd * za)

    def toString(self):
        return '(' + self.x + ', ' + self.y + ', ' + self.z + ')'
