from mc.net.minecraft.Entity import Entity
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.particle.SmokeParticle import SmokeParticle
from mc.net.minecraft.particle.TerrainParticle import TerrainParticle
from mc.net.minecraft.renderer.Tesselator import tesselator

from pyglet import gl

import random
import math

class PrimedTnt(Entity):

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.setSize(0.98, 0.98)
        self.heightOffset = self.bbHeight / 2.0
        self.setPos(x, y, z)
        level1 = random.random() * math.pi * 2.0
        self.__xd = -(math.sin(level1 * math.pi / 180.0)) * 0.02
        self.__yd = 0.2
        self.__zd = -(math.cos(level1 * math.pi / 180.0)) * 0.02
        self.makeStepSound = False
        self.life = 40
        self.xo = x
        self.yo = y
        self.zo = z

    def isPickable(self):
        return not self.removed

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        self.__yd -= 0.04
        self.move(self.__xd, self.__yd, self.__zd)
        self.__xd *= 0.98
        self.__yd *= 0.98
        self.__zd *= 0.98
        if self.onGround:
            self.__xd *= 0.7
            self.__zd *= 0.7
            self.__yd *= -0.5

        self.life -= 1
        if self.life + 1 > 0:
            self.level.particleEngine.addParticle(SmokeParticle(self.level,
                                                                self.x,
                                                                self.y + 0.6,
                                                                self.z))
        else:
            self.remove()
            r = 4.0
            self.level.explode(None, self.x, self.y, self.z, r)

            for i in range(100):
                x = random.gauss(0, 1) * r / 4.0
                y = random.gauss(0, 1) * r / 4.0
                z = random.gauss(0, 1) * r / 4.0
                d = math.sqrt(x * x + y * y + z * z)
                f8 = x / d / d
                f9 = y / d / d
                f10 = z / d / d
                self.level.particleEngine.addParticle(TerrainParticle(self.level,
                                                                      self.x + x,
                                                                      self.y + y,
                                                                      self.z + z,
                                                                      f8, f9, f10,
                                                                      tiles.tnt))

    def render(self, textures, translation):
        tex = textures.loadTexture('terrain.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        br = self.level.getBrightness(self.x, self.y, self.z)
        gl.glPushMatrix()
        gl.glColor4f(br, br, br, 1.0)
        gl.glTranslatef(self.xo + (self.x - self.xo) * translation - 0.5,
                        self.yo + (self.y - self.yo) * translation - 0.5,
                        self.zo + (self.z - self.zo) * translation - 0.5)
        gl.glPushMatrix()
        t = tesselator
        tiles.tnt.renderGuiTile(t)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glColor4f(1.0, 1.0, 1.0, (self.life // 4 + 1) % 2 * 0.4)
        if self.life <= 16:
            gl.glColor4f(1.0, 1.0, 1.0, (self.life + 1) % 2 * 0.6)

        if self.life <= 2:
            gl.glColor4f(1.0, 1.0, 1.0, 0.9)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        tiles.tnt.renderGuiTile(t)
        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glPopMatrix()
        gl.glPopMatrix()
