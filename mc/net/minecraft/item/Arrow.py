from mc.net.minecraft.Entity import Entity
from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import gl

import math

class Arrow(Entity):

    def __init__(self, minecraft, player, x, y, z, xr, yr):
        super().__init__(minecraft.level)
        self.__hasHit = False
        self.__stickTime = 0
        self.__time = 0
        self.__owner = player
        self.setSize(0.25, 0.5)
        self.heightOffset = self.bbHeight / 2.0
        self.heightOffset = 0.25
        y0 = math.cos(-xr * math.pi / 180.0 - math.pi)
        y1 = math.sin(-xr * math.pi / 180.0 - math.pi)
        x0 = math.cos(-yr * math.pi / 180.0)
        x1 = math.sin(-yr * math.pi / 180.0)
        self.slide = False
        self.xo -= y0 * 0.2
        self.zo += y1 * 0.2
        self.__xd = y1 * x0 * 0.8
        self.__yd = x1 * 0.8
        self.__zd = y0 * x0 * 0.8
        self.setPos(x - y0 * 0.2, y, z + y1 * 0.2)
        rot = math.sqrt(self.__xd * self.__xd + self.__zd * self.__zd)
        self.__yRotO = self.__yRot = math.atan2(self.__xd, self.__zd) * 180.0 / math.pi
        self.__xRotO = self.__xRot = math.atan2(self.__yd, rot) * 180.0 / math.pi
        self.makeStepSound = False

    def tick(self):
        self.__time += 1
        self.__xRotO = self.__xRot
        self.__yRotO = self.__yRot
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        if self.__hasHit:
            self.__stickTime += 1
            if self.__stickTime >= 20:
                self.remove()
            return

        self.__xd *= 0.992
        self.__yd *= 0.992
        self.__zd *= 0.992
        self.__yd -= 0.02
        rot = math.sqrt(self.__xd * self.__xd + self.__yd * self.__yd + self.__zd * self.__zd)
        n = int(rot / 0.2 + 1.0)
        x = self.__xd / n
        y = self.__yd / n
        z = self.__zd / n
        for i in range(n):
            if self.collision:
                break

            axisAlignedBB = self.bb.expand(x, y, z)
            if len(self.level.getCubes(axisAlignedBB)) > 0:
                self.collision = True

            entities = self.level.blockMap.getEntitiesWithinAABBExcludingEntity(self, axisAlignedBB)
            for entity in entities:
                if not entity.isShootable() or entity == self.__owner or self.__time > 20:
                    continue

                entity.hurt(self, 3)
                self.collision = True
                self.__stickTime = 20

            if self.collision:
                continue

            self.bb.move(x, y, z)
            self.x += x
            self.y += y
            self.z += z

        if self.collision:
            self.__hasHit = True
            self.__zd = 0.0
            self.__yd = 0.0
            self.__xd = 0.0

        if not self.__hasHit:
            rot = math.sqrt(self.__xd * self.__xd + self.__zd * self.__zd)
            self.__yRot = math.atan2(self.__xd, self.__zd) * 180.0 / math.pi
            self.__xRot = math.atan2(self.__yd, rot) * 180.0 / math.pi
            while self.__xRot - self.__xRotO < -180.0:
                self.__xRotO -= 360.0
            while self.__xRot - self.__xRotO >= 180.0:
                self.__xRotO += 360.0
            while self.__yRot - self.__yRotO < -180.0:
                self.__yRotO -= 360.0
            while self.__yRot - self.__yRotO >= 180.0:
                self.__yRotO += 360.0

    def render(self, textures, translation):
        gl.glEnable(gl.GL_TEXTURE_2D)
        tex = textures.loadTexture('item/arrows.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        br = self.level.getBrightness(int(self.x), int(self.y), int(self.z))
        gl.glPushMatrix()
        gl.glColor4f(br, br, br, 1.0)
        gl.glTranslatef(self.xo + (self.x - self.xo) * translation,
                        self.yo + (self.y - self.yo) * translation - self.heightOffset / 2.0,
                        self.zo + (self.z - self.zo) * translation)
        gl.glRotatef(self.__yRotO + (self.__yRot - self.__yRotO) * translation - 90.0, 0.0, 1.0, 0.0)
        gl.glRotatef(self.__xRotO + (self.__xRot - self.__xRotO) * translation, 0.0, 0.0, 1.0)
        gl.glRotatef(45.0, 1.0, 0.0, 0.0)
        t = tesselator
        gl.glScalef(0.05625, 0.05625, 0.05625)
        for i in range(4):
            gl.glRotatef(90.0, 1.0, 0.0, 0.0)
            gl.glNormal3f(0.0, -0.05625, 0.0)
            t.begin()
            t.vertexUV(-8.0, -2.0, 0.0, 0.0, 0.0)
            t.vertexUV(8.0, -2.0, 0.0, 0.5, 0.0)
            t.vertexUV(8.0, 2.0, 0.0, 0.5, 0.15625)
            t.vertexUV(-8.0, 2.0, 0.0, 0.0, 0.15625)
            t.end()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glPopMatrix()

    def awardKillScore(self, entity, n):
        self.__owner.awardKillScore(entity, n)
