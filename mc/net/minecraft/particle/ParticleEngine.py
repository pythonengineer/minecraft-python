from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import gl

import math

class ParticleEngine:
    particles = []

    def __init__(self, level, textures):
        self.__textures = textures
        level.particleEngine = self

    def addParticle(self, p):
        self.particles.append(p)

    def tick(self):
        for p in self.particles.copy():
            p.tick()
            if p.removed:
                self.particles.remove(p)

    def render(self, player, translation):
        if not len(self.particles):
            return

        gl.glEnable(gl.GL_TEXTURE_2D)
        id_ = self.__textures.loadTexture('terrain.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        xa = -math.cos(player.yRot * math.pi / 180.0)
        za = -math.sin(player.yRot * math.pi / 180.0)

        xa2 = -za * math.sin(player.xRot * math.pi / 180.0)
        za2 = xa * math.sin(player.xRot * math.pi / 180.0)
        ya = math.cos(player.xRot * math.pi / 180.0)

        t = tesselator
        t.begin()
        for p in self.particles:
            f10 = 0.6 * p.getBrightness(translation)
            t.colorFloat(f10, f10, f10)
            p.render(t, translation, xa, ya, za, xa2, za2)

        t.end()
        gl.glDisable(gl.GL_TEXTURE_2D)
