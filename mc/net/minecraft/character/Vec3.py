import math

class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def subtract(self, vec):
        return Vec3(self.x - vec.x, self.y - vec.y, self.z - vec.z)

    def normalize(self):
        f1 = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return Vec3(self.x / f1, self.y / f1, self.z / f1)
