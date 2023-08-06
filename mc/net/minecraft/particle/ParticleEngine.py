from mc.net.minecraft.level.Tesselator import tesselator
from mc.net.minecraft.Textures import Textures
from pyglet import gl

import math

class ParticleEngine:
    particles = set()

    def __init__(self, level):
        self.level = level

    def add(self, p):
        self.particles.add(p)

    def tick(self):
        for p in self.particles.copy():
            p.tick()
            if p.removed:
                self.particles.remove(p)

    def render(self, player, a, layer):
        gl.glEnable(gl.GL_TEXTURE_2D)
        id_ = Textures.loadTexture('terrain.png', gl.GL_NEAREST)
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        xa = -math.cos(player.yRot * math.pi / 180.0)
        za = -math.sin(player.yRot * math.pi / 180.0)

        xa2 = -za * math.sin(player.xRot * math.pi / 180.0)
        za2 = xa * math.sin(player.xRot * math.pi / 180.0)
        ya = math.cos(player.xRot * math.pi / 180.0)

        t = tesselator
        gl.glColor4f(0.8, 0.8, 0.8, 1.0)
        t.init()
        for p in self.particles:
            if p.isLit() ^ layer == 1:
                p.render(t, a, xa, ya, za, xa2, za2)
        t.flush()
        gl.glDisable(gl.GL_TEXTURE_2D)
