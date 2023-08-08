from mc.net.minecraft.character.ZombieModel import ZombieModel
from mc.net.minecraft.Entity import Entity
from mc.CompatibilityShims import getNs
from pyglet import gl

import random
import math

class Zombie(Entity):
    __zombieModel = ZombieModel()

    def __init__(self, level, textures, x, y, z):
        super().__init__(level)
        self.__textures = textures
        self.__rotA = (random.random() + 1.0) * 0.01
        self.setPos(x, y, z)
        self.__timeOffs = random.random() * 1239813.0
        self.__rot = random.random() * math.pi * 2.0
        self.__speed = 1.0

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        xa = 0.0
        ya = 0.0

        if self.y < -100.0:
            self.removed = True

        self.__rot += self.__rotA
        self.__rotA *= 0.99
        self.__rotA += (random.random() - random.random()) * random.random() * random.random() * 0.08
        xa = math.sin(self.__rot)
        ya = math.cos(self.__rot)

        if self.onGround and random.random() < 0.08:
            self.yd = 0.5

        self.moveRelative(xa, ya, 0.1 if self.onGround else 0.02)

        self.yd -= 0.08
        self.move(self.xd, self.yd, self.zd)
        self.xd *= 0.91
        self.yd *= 0.98
        self.zd *= 0.91

        if self.onGround:
            self.xd *= 0.7
            self.zd *= 0.7

    def render(self, a):
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textures.loadTexture('char.png', gl.GL_NEAREST))

        gl.glPushMatrix()
        t = getNs() / 1000000000.0 * 10.0 * self.__speed + self.__timeOffs

        size = 0.05833333
        yy = -abs(math.sin(t * 0.6662)) * 5.0 - 23.0
        gl.glTranslatef(self.xo + (self.x - self.xo) * a, self.yo + (self.y - self.yo) * a, self.zo + (self.z - self.zo) * a)
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glScalef(size, size, size)
        gl.glTranslatef(0.0, yy, 0.0)
        c = 57.29578
        gl.glRotatef(self.__rot * c + 180.0, 0.0, 1.0, 0.0)
        self.__zombieModel.head.yRot = math.sin(t * 0.83) * 1.0
        self.__zombieModel.head.xRot = math.sin(t) * 0.8
        self.__zombieModel.arm0.xRot = math.sin(t * 0.6662 + math.pi) * 2.0
        self.__zombieModel.arm0.zRot = (math.sin(t * 0.2312) + 1.0) * 1.0
        self.__zombieModel.arm1.xRot = math.sin(t * 0.6662) * 2.0
        self.__zombieModel.arm1.zRot = (math.sin(t * 0.2812) - 1.0) * 1.0
        self.__zombieModel.leg0.xRot = math.sin(t * 0.6662) * 1.4
        self.__zombieModel.leg1.xRot = math.sin(t * 0.6662 + math.pi) * 1.4
        self.__zombieModel.head.render()
        self.__zombieModel.body.render()
        self.__zombieModel.arm0.render()
        self.__zombieModel.arm1.render()
        self.__zombieModel.leg0.render()
        self.__zombieModel.leg1.render()
        gl.glPopMatrix()
        gl.glDisable(gl.GL_TEXTURE_2D)
