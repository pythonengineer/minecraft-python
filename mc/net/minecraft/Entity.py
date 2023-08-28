from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.level.tile.Tiles import SoundType, tiles
from mc.net.minecraft.phys.AABB import AABB

import random
import math

class Entity:
    xo = 0.0
    yo = 0.0
    zo = 0.0
    xd = 0.0
    yd = 0.0
    zd = 0.0
    yRot = 0.0
    xRot = 0.0
    yRotO = 0.0
    xRotO = 0.0
    onGround = False
    horizontalCollision = False
    removed = False

    heightOffset = 0.0
    _bbWidth = 0.6
    bbHeight = 1.8
    __walkDist = 0.0
    makeStepSound = True

    def __init__(self, level):
        self._level = level
        self.setPos(0.0, 0.0, 0.0)

    def resetPos(self):
        if self._level:
            x = self._level.xSpawn + 0.5
            y = self._level.ySpawn
            z = self._level.zSpawn + 0.5
            while y > 0.0:
                self.setPos(x, y, z)
                if len(self._level.getCubes(self.bb)) == 0:
                    break
                y += 1.0

            self.xd = self.yd = self.zd = 0.0
            self.yRot = self._level.rotSpawn
            self.xRot = 0.0

    def remove(self):
        self.removed = True

    def setSize(self, w, h):
        self._bbWidth = w
        self.bbHeight = h

    def setPos(self, x, y=None, z=None):
        if x and y is None:
            playerMove = x
            if playerMove.moving:
                self.setPos(playerMove.x, playerMove.y, playerMove.z)
            else:
                self.setPos(self.x, self.y, self.z)

            if playerMove.rotating:
                self._setRot(playerMove.yRot, playerMove.xRot)
            else:
                self._setRot(self.yRot, self.xRot)
            return

        self.x = x
        self.y = y
        self.z = z
        w = self._bbWidth / 2.0
        h = self.bbHeight / 2.0
        self.bb = AABB(x - w, y - h, z - w, x + w, y + h, z + w)

    def _setRot(self, yRot, xRot):
        self.yRot = yRot
        self.xRot = xRot

    def turn(self, xo, yo):
        orgXRot = self.xRot
        orgYRot = self.yRot
        self.yRot = self.yRot + xo * 0.15
        self.xRot = self.xRot - yo * 0.15
        if self.xRot < -90.0:
            self.xRot = -90.0
        if self.xRot > 90.0:
            self.xRot = 90.0

        self.xRotO += self.xRot - orgXRot
        self.yRotO += self.yRot - orgYRot

    def interpolateTurn(self, xo, yo):
        self.yRot = self.yRot + xo * 0.15
        self.xRot = self.xRot - yo * 0.15
        if self.xRot < -90.0:
            self.xRot = -90.0
        if self.xRot > 90.0:
            self.xRot = 90.0

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        self.xRotO = self.xRot
        self.yRotO = self.yRot

    def isFree(self, xa, ya, za):
        aABB = self.bb.cloneMove(xa, ya, za)
        return False if len(self._level.getCubes(aABB)) > 0 else not self._level.containsAnyLiquid(aABB)

    def move(self, xa, ya, za):
        xOrg = self.x
        zOrg = self.z
        xaOrg = xa
        yaOrg = ya
        zaOrg = za

        aABBs = self._level.getCubes(self.bb.expand(xa, ya, za))
        for aABB in aABBs:
            ya = aABB.clipYCollide(self.bb, ya)

        self.bb.move(0.0, ya, 0.0)

        for aABB in aABBs:
            xa = aABB.clipXCollide(self.bb, xa)

        self.bb.move(xa, 0.0, 0.0)

        for aABB in aABBs:
            za = aABB.clipZCollide(self.bb, za)

        self.bb.move(0.0, 0.0, za)

        self.horizontalCollision = xaOrg != xa or zaOrg != za
        self.onGround = yaOrg != ya and yaOrg < 0.0

        if xaOrg != xa:
            self.xd = 0.0
        if yaOrg != ya:
            self.yd = 0.0
        if zaOrg != za:
            self.zd = 0.0

        self.x = (self.bb.x0 + self.bb.x1) / 2.0
        self.y = self.bb.y0 + self.heightOffset
        self.z = (self.bb.z0 + self.bb.z1) / 2.0

        f13 = self.x - xOrg
        f1 = self.z - zOrg
        self.__walkDist = float(self.__walkDist + math.sqrt(f13 * f13 + f1 * f1) * 0.6)
        if self.makeStepSound:
            tile = self._level.getTile(int(self.x), int(self.y - 0.2 - self.heightOffset), int(self.z))
            if self.__walkDist > 1.0 and tile > 0:
                soundType = tiles.tiles[tile].soundType
                if soundType != SoundType.none:
                    self.__walkDist -= float(int(self.__walkDist))
                    self.playSound('step.' + soundType.name,
                                   soundType.getVolume() * 0.75,
                                   soundType.getPitch())

    def isInWater(self):
        return self._level.containsLiquid(self.bb.grow(0.0, -0.4, 0.0), Liquid.water)

    def isInLava(self):
        return self._level.containsLiquid(self.bb, Liquid.lava)

    def moveRelative(self, xa, za, speed):
        dist = math.sqrt(xa * xa + za * za)
        if dist < 0.01:
            return

        if dist < 1.0:
            dist = 1.0

        dist = speed / dist
        xa *= dist
        za *= dist

        sin = math.sin(self.yRot * math.pi / 180.0)
        cos = math.cos(self.yRot * math.pi / 180.0)

        self.xd += xa * cos - za * sin
        self.zd += za * cos + xa * sin

    def isLit(self):
        return self._level.isLit(int(self.x), int(self.y), int(self.z))

    def getBrightness(self):
        x = int(self.x)
        y = int(self.y + self.heightOffset / 2.0)
        z = int(self.z)
        return self._level.getBrightness(x, y, z)

    def render(self, a):
        pass

    def setLevel(self, level):
        self._level = level

    def playSound(self, name, volume, pitch):
        self._level.playSound(name, self.x, self.y - self.heightOffset, self.z, volume, pitch, self)

    def moveTo(self, x, y, z, yRot, xRot):
        self.xo = self.x = x
        self.yo = self.y = y
        self.zo = self.z = z
        self.yRot = yRot
        self.xRot = xRot
        self.setPos(x, y, z)

    def distanceTo(self, entity):
        x = self.x - entity.x
        y = self.y - entity.y
        z = self.z - entity.z
        return math.sqrt(x * x + y * y + z * z)

    def getDistanceSq(self, x, y, z):
        x -= self.x
        y -= self.y
        z = z - self.z
        d = math.sqrt(x * x + y * y + z * z)
        d = 1.0 - d / 32.0
        if d < 0.0:
            d = 0.0

        return d
