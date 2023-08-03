class Vec3:

    def __init__(self, x, y, z):
        self.set(x, y, z)

    def interpolateTo(self, t, p):
        xt = self.x + (t.x - self.x) * p
        yt = self.y + (t.y - self.y) * p
        zt = self.z + (t.z - self.z) * p

        return Vec3(xt, yt, zt)

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
