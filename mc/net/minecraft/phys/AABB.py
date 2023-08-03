class AABB:
    epsilon = 0.0

    def __init__(self, x0, y0, z0, x1, y1, z1):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

    def expand(self, xa, ya, za):
        _x0 = self.x0
        _y0 = self.y0
        _z0 = self.z0
        _x1 = self.x1
        _y1 = self.y1
        _z1 = self.z1

        if xa < 0.0: _x0 += xa
        if xa > 0.0: _x1 += xa
        if ya < 0.0: _y0 += ya
        if ya > 0.0: _y1 += ya
        if za < 0.0: _z0 += za
        if za > 0.0: _z1 += za

        return AABB(_x0, _y0, _z0, _x1, _y1, _z1)

    def grow(self, xa, ya, za):
        _x0 = self.x0 - xa
        _y0 = self.y0 - ya
        _z0 = self.z0 - za
        _x1 = self.x1 + xa
        _y1 = self.y1 + ya
        _z1 = self.z1 + za

        return AABB(_x0, _y0, _z0, _x1, _y1, _z1)

    def clipXCollide(self, c, xa):
        if c.y1 <= self.y0 or c.y0 >= self.y1:
            return xa
        if c.z1 <= self.z0 or c.z0 >= self.z1:
            return xa

        if xa > 0.0 and c.x1 <= self.x0:
            maximum = self.x0 - c.x1 - self.epsilon
            if maximum < xa:
                xa = maximum

        if xa < 0.0 and c.x0 >= self.x1:
            maximum = self.x1 - c.x0 + self.epsilon
            if maximum > xa:
                xa = maximum

        return xa

    def clipYCollide(self, c, ya):
        if c.x1 <= self.x0 or c.x0 >= self.x1:
            return ya
        if c.z1 <= self.z0 or c.z0 >= self.z1:
            return ya

        if ya > 0.0 and c.y1 <= self.y0:
            maximum = self.y0 - c.y1 - self.epsilon
            if maximum < ya:
                ya = maximum

        if ya < 0.0 and c.y0 >= self.y1:
            maximum = self.y1 - c.y0 + self.epsilon
            if maximum > ya:
                ya = maximum

        return ya

    def clipZCollide(self, c, za):
        if c.x1 <= self.x0 or c.x0 >= self.x1:
            return za
        if c.y1 <= self.y0 or c.y0 >= self.y1:
            return za

        if za > 0.0 and c.z1 <= self.z0:
            maximum = self.z0 - c.z1 - self.epsilon
            if maximum < za:
                za = maximum

        if za < 0.0 and c.z0 >= self.z1:
            maximum = self.z1 - c.z0 + self.epsilon
            if maximum > za:
                za = maximum

        return za

    def intersects(self, c):
        if c.x1 <= self.x0 or c.x0 >= self.x1:
            return False
        if c.y1 <= self.y0 or c.y0 >= self.y1:
            return False
        if c.z1 <= self.z0 or c.z0 >= self.z1:
            return False

        return True

    def move(self, xa, ya, za):
        self.x0 += xa
        self.y0 += ya
        self.z0 += za
        self.x1 += xa
        self.y1 += ya
        self.z1 += za
