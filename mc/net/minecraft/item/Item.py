from mc.net.minecraft.Entity import Entity
from mc.net.minecraft.item.ItemModel import ItemModel
from mc.net.minecraft.item.TakeEntityAnim import TakeEntityAnim
from mc.net.minecraft.level.tile.Tiles import tiles
from pyglet import gl

import random
import math

class Item(Entity):
    __models = [None] * 256

    @staticmethod
    def initModels():
        for i in range(256):
            tile = tiles.tiles[i]
            if tile:
                Item.__models[i] = ItemModel(tile.tex)

    def __init__(self, level, x, y, z, res):
        super().__init__(level)
        self.setSize(0.25, 0.25)
        self.heightOffset = self.bbHeight / 2.0
        self.setPos(x, y, z)
        self.__tickCount = 0
        self.__age = 0
        self.__resource = res
        self.__rot = random.random() * 360.0
        self.__xd = random.random() * 0.2 - 0.1
        self.__yd = 0.2
        self.__zd = random.random() * 0.2 - 0.1
        self.makeStepSound = False

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
        self.__tickCount += 1
        self.__age += 1
        if self.__age >= 6000:
            self.remove()

    def render(self, textures, translation):
        self.textureId = textures.loadTexture('terrain.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureId)
        b = self.level.getBrightness(self.x, self.y, self.z)
        f3 = self.__rot + (self.__tickCount + translation) * 3.0
        gl.glPushMatrix()
        gl.glColor4f(b, b, b, 1.0)
        f2 = math.sin(f3 / 10.0)
        f4 = f2 * 0.1 + 0.1
        gl.glTranslatef(self.xo + (self.x - self.xo) * translation,
                        self.yo + (self.y - self.yo) * translation + f4,
                        self.zo + (self.z - self.zo) * translation)
        gl.glRotatef(f3, 0.0, 1.0, 0.0)
        Item.__models[self.__resource].render()
        f2 = f2 * 0.5 + 0.5
        f2 *= f2
        f2 *= f2
        gl.glColor4f(1.0, 1.0, 1.0, f2 * 0.4)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        gl.glDisable(gl.GL_ALPHA_TEST)
        Item.__models[self.__resource].render()
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glDisable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glPopMatrix()
        gl.glEnable(gl.GL_TEXTURE_2D)

    def playerTouch(self, player):
        if player.addResource(self.__resource):
            self.level.addEntity(TakeEntityAnim(self.level, self, player))
            self.remove()
