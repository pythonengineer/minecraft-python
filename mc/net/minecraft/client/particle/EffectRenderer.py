from mc.net.minecraft.client.particle.EntityDiggingFX import EntityDiggingFX
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

import random
import math

class EffectRenderer:
    __rand = random.Random()

    def __init__(self, world, renderEngine):
        if world:
            self.__worldObj = world

        self.__renderEngine = renderEngine
        self.__fxLayers = [[], []]

    def addEffect(self, fx):
        tex = fx.getFXLayer()
        self.__fxLayers[tex].append(fx)

    def updateEffects(self):
        for i in range(2):
            for p in self.__fxLayers[i].copy():
                p.onEntityUpdate()
                if p.isDead:
                    self.__fxLayers[i].remove(p)

    def renderParticles(self, entity, translation):
        xa = -math.cos(entity.rotationYaw * math.pi / 180.0)
        za = -math.sin(entity.rotationYaw * math.pi / 180.0)

        xa2 = -za * math.sin(entity.rotationPitch * math.pi / 180.0)
        za2 = xa * math.sin(entity.rotationPitch * math.pi / 180.0)
        ya = math.cos(entity.rotationPitch * math.pi / 180.0)

        for i in range(2):
            if not len(self.__fxLayers[i]):
                continue

            if i == 0:
                id_ = self.__renderEngine.getTexture('particles.png')
            elif i == 1:
                id_ = self.__renderEngine.getTexture('terrain.png')

            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            t = tessellator
            t.startDrawingQuads()

            for p in self.__fxLayers[i]:
                p.renderParticle(t, translation, xa, ya, za, xa2, za2)

            t.draw()

    def clearEffects(self, world):
        self.__worldObj = world
        for i in range(2):
            self.__fxLayers[i].clear()

    def addBlockDigEffects(self, x, y, z):
        blockId = self.__worldObj.getBlockId(x, y, z)
        if blockId:
            block = blocks.blocksList[blockId]

            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        xx = x + (i + 0.5) / 4
                        yy = y + (j + 0.5) / 4
                        zz = z + (k + 0.5) / 4
                        self.addEffect(
                            EntityDiggingFX(self.__worldObj,
                                            xx, yy, zz, xx - x - 0.5, yy - y - 0.5,
                                            zz - z - 0.5, block)
                        )

    def addBlockHitEffects(self, x, y, z, sideHit):
        block = self.__worldObj.getBlockId(x, y, z)
        if block != 0:
            block = blocks.blocksList[block]
            posX = x + self.__rand.random() * (block.maxX - block.minX - 0.2) + 0.1 + block.minX
            posY = y + self.__rand.random() * (block.maxY - block.minY - 0.2) + 0.1 + block.minY
            posZ = z + self.__rand.random() * (block.maxZ - block.minZ - 0.2) + 0.1 + block.minZ
            if sideHit == 0:
                posY = y + block.minY - 0.1
            elif sideHit == 1:
                posY = y + block.maxY + 0.1
            elif sideHit == 2:
                posZ = z + block.minZ - 0.1
            elif sideHit == 3:
                posZ = z + block.maxZ + 0.1
            elif sideHit == 4:
                posX = x + block.minX - 0.1
            elif sideHit == 5:
                posX = x + block.maxX + 0.1

            self.addEffect(
                EntityDiggingFX(
                    self.__worldObj, posX, posY, posZ,
                    0.0, 0.0, 0.0, block
                ).multiplyVelocity(0.2).multipleParticleScaleBy(0.6)
            )
