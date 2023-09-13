from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import gl

import math

class ParticleEngine:
    particles = [[], []]

    def __init__(self, level, textures):
        if level:
            level.particleEngine = self

        self.textures = textures

    def addParticle(self, p):
        tex = p.getParticleTexture()
        self.particles[tex].append(p)

    def tick(self):
        for i in range(2):
            for p in self.particles[i].copy():
                p.tick()
                if p.removed:
                    self.particles[i].remove(p)

    def render(self, player, translation):
        xa = -math.cos(player.yRot * math.pi / 180.0)
        za = -math.sin(player.yRot * math.pi / 180.0)

        xa2 = -za * math.sin(player.xRot * math.pi / 180.0)
        za2 = xa * math.sin(player.xRot * math.pi / 180.0)
        ya = math.cos(player.xRot * math.pi / 180.0)

        for i in range(2):
            if not len(self.particles[i]):
                continue

            if i == 0:
                id_ = self.textures.loadTexture('particles.png')
            elif i == 1:
                id_ = self.textures.loadTexture('terrain.png')

            gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
            t = tesselator
            t.begin()

            for p in self.particles[i]:
                p.renderParticle(t, translation, xa, ya, za, xa2, za2)

            t.end()
