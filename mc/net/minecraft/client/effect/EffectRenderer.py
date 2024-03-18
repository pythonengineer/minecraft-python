from mc.net.minecraft.client.render.Tessellator import tessellator
from pyglet import gl

import math

class EffectRenderer:

    def __init__(self, world, renderEngine):
        if world:
            self.worldObj = world

        self.renderEngine = renderEngine
        self.fxLayers = [[], []]

    def addEffect(self, fx):
        tex = fx.getFXLayer()
        self.fxLayers[tex].append(fx)

    def tick(self):
        for i in range(2):
            for p in self.fxLayers[i].copy():
                p.onEntityUpdate()
                if p.isDead:
                    self.fxLayers[i].remove(p)

    def render(self, player, translation):
        xa = -math.cos(player.rotationYaw * math.pi / 180.0)
        za = -math.sin(player.rotationYaw * math.pi / 180.0)

        xa2 = -za * math.sin(player.rotationPitch * math.pi / 180.0)
        za2 = xa * math.sin(player.rotationPitch * math.pi / 180.0)
        ya = math.cos(player.rotationPitch * math.pi / 180.0)

        for i in range(2):
            if not len(self.fxLayers[i]):
                continue

            if i == 0:
                id_ = self.renderEngine.getTexture('particles.png')
            elif i == 1:
                id_ = self.renderEngine.getTexture('terrain.png')

            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            t = tessellator
            t.startDrawingQuads()

            for p in self.fxLayers[i]:
                p.renderParticle(t, translation, xa, ya, za, xa2, za2)

            t.draw()
