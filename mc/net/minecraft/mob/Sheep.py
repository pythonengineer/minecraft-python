from mc.net.minecraft.item.Item import Item
from mc.net.minecraft.mob.SheepAI import SheepAI
from mc.net.minecraft.mob.QuadrupedMob import QuadrupedMob
from mc.net.minecraft.player.Player import Player
from mc.net.minecraft.level.tile.Tiles import tiles

from pyglet import gl

import random

class Sheep(QuadrupedMob):

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.hasFur = True
        self.grazing = False
        self.grazingTime = 0
        self.graze = 0.0
        self.grazeO = 0.0
        self.setSize(1.4, 1.72)
        self.setPos(x, y, z)
        self.heightOffset = 1.72
        self.modelName = 'sheep'
        self._textureName = 'mob/sheep.png'
        self.ai = SheepAI()

    def _aiStep(self):
        super().aiStep()
        self.grazeO = self.graze
        if self.grazing:
            self.graze += 0.2
        else:
            self.graze -= 0.2

        if self.graze < 0.0:
            self.graze = 0.0
        elif self.graze > 1.0:
            self.graze = 1.0

    def die(self, entity):
        if entity:
            entity.awardKillScore(self, 10)

        n = int(random.random() + random.random() + 1.0)
        for i in range(n):
            self.level.addEntity(Item(self.level, self.x, self.y, self.z, tiles.mushroomBrown.id))

        super().die(entity)

    def hurt(self, entity, hp):
        if self.hasFur and isinstance(entity, Player):
            self.hasFur = False

            n = int(random.random() * 3.0 + 1.0)
            for i in range(n):
                self.level.addEntity(Item(self.level, self.x, self.y, self.z, tiles.clothWhite.id))

        else:
            super().hurt(entity, hp)

    def renderModel(self, textures, x, y, z, rotX, rotY, rotZ):
        model = self.modelCache.getModel(self.modelName)
        orgY = model.head.y
        orgZ = model.head.z
        model.head.y += (self.grazeO + (self.graze - self.grazeO) * y) * 8.0
        model.head.z -= self.grazeO + (self.graze - self.grazeO) * y
        super().renderModel(textures, x, y, z, rotX, rotY, rotZ)
        if self.hasFur:
            gl.glBindTexture(gl.GL_TEXTURE_2D, textures.loadTexture('mob/sheep_fur.png'))
            gl.glDisable(gl.GL_CULL_FACE)
            fur = self.modelCache.getModel('sheep.fur')
            fur.head.yRot = model.head.yRot
            fur.head.xRot = model.head.xRot
            fur.head.y = model.head.y
            fur.head.x = model.head.x
            fur.body.yRot = model.body.yRot
            fur.body.xRot = model.body.xRot
            fur.leg1.xRot = model.leg1.xRot
            fur.leg2.xRot = model.leg2.xRot
            fur.leg3.xRot = model.leg3.xRot
            fur.leg4.xRot = model.leg4.xRot
            fur.head.render(rotZ)
            fur.body.render(rotZ)
            fur.leg1.render(rotZ)
            fur.leg2.render(rotZ)
            fur.leg3.render(rotZ)
            fur.leg4.render(rotZ)

        model.head.y = orgY
        model.head.z = orgZ
