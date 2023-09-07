from mc.net.minecraft.player.Player import Player
from mc.net.minecraft.Entity import Entity
from mc.net.minecraft.item.TakeEntityAnim import TakeEntityAnim
from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import gl

import random
import math

class Arrow(Entity):

    def __init__(self, level, entity, x, y, z, xr, yr, zr):
        super().__init__(level)
        self.__owner = entity
        self.__hasHit = False
        self.__stickTime = 0
        self.__time = 0
        self.setSize(0.3, 0.5)
        self.heightOffset = self.bbHeight / 2.0
        if isinstance(entity, Player):
            self.__type = 1
            self.__damage = 3
        else:
            self.__type = 0
            self.__damage = 7

        self.heightOffset = 0.25
        y0 = math.cos(-xr * math.pi / 180.0 - math.pi)
        y1 = math.sin(-xr * math.pi / 180.0 - math.pi)
        x0 = math.cos(-yr * math.pi / 180.0)
        x1 = math.sin(-yr * math.pi / 180.0)
        self.slide = False
        self.__gravity = 1.0 // zr
        self.xo -= y0 * 0.2
        self.zo += y1 * 0.2
        x -= y0 * 0.2
        z += y1 * 0.2
        self.__xd = y1 * x0 * zr
        self.__yd = x1 * zr
        self.__zd = y0 * x0 * zr
        self.setPos(x, y, z)
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
            if self.__type == 0:
                if self.__stickTime >= 300 and random.random() < 0.01:
                    self.remove()
            elif self.__type == 1 and self.__stickTime >= 20:
                self.remove()

            return

        self.__xd *= 0.998
        self.__yd *= 0.998
        self.__zd *= 0.998
        self.__yd -= 0.02 * self.__gravity
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
                if entity.isShootable() and (entity != self.__owner or self.__time > 5):
                    entity.hurt(self, self.__damage)
                    self.collision = True
                    self.remove()
                    return

            if self.collision:
                continue

            self.bb.move(x, y, z)
            self.x += x
            self.y += y
            self.z += z
            self.blockMap.moved(self)

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
        self.textureId = textures.loadTexture('item/arrows.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureId)
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
        translation = 0.5
        f3 = (0 + self.__type * 10) / 32.0
        f4 = (5 + self.__type * 10) / 32.0
        f5 = 0.15625
        f6 = (5 + self.__type * 10) / 32.0
        f8 = (10 + self.__type * 10) / 32.0
        f7 = 0.05625
        gl.glScalef(0.05625, f7, f7)
        gl.glNormal3f(f7, 0.0, 0.0)
        t.begin()
        t.vertexUV(-7.0, -2.0, -2.0, 0.0, f6)
        t.vertexUV(-7.0, -2.0, 2.0, f5, f6)
        t.vertexUV(-7.0, 2.0, 2.0, f5, f8)
        t.vertexUV(-7.0, 2.0, -2.0, 0.0, f8)
        t.end()
        gl.glNormal3f(-f7, 0.0, 0.0)
        t.begin()
        t.vertexUV(-7.0, 2.0, -2.0, 0.0, f6)
        t.vertexUV(-7.0, 2.0, 2.0, f5, f6)
        t.vertexUV(-7.0, -2.0, 2.0, f5, f8)
        t.vertexUV(-7.0, -2.0, -2.0, 0.0, f8)
        t.end()
        for i in range(4):
            gl.glRotatef(90.0, 1.0, 0.0, 0.0)
            gl.glNormal3f(0.0, -f7, 0.0)
            t.vertexUV(-8.0, -2.0, 0.0, 0.0, f3)
            t.vertexUV(8.0, -2.0, 0.0, translation, f3)
            t.vertexUV(8.0, 2.0, 0.0, translation, f4)
            t.vertexUV(-8.0, 2.0, 0.0, 0.0, f4)
            t.end()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glPopMatrix()

    def awardKillScore(self, entity, score):
        self.__owner.awardKillScore(entity, score)

    def getOwner(self):
        return self.__owner

    def playerTouch(self, player):
        if self.__hasHit and self.__owner == player and player.arrows < 99:
            self.level.addEntity(TakeEntityAnim(self.level, self, player))
            player.arrows += 1
            self.remove()
