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

    def addVector(self, x, y, z):
        return Vec3(self.x + x, self.y + y, self.z + z)
