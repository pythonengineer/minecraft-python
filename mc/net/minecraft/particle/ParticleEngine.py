from mc.net.minecraft.renderer.Tesselator import tesselator
from pyglet import gl

import math

class ParticleEngine:
    particles = set()

    def __init__(self, level, textures):
        self.__textures = textures

    def add(self, p):
        self.particles.add(p)

    def render(self, player, a, layer):
        if not len(self.particles):
            return

        gl.glEnable(gl.GL_TEXTURE_2D)
        id_ = self.__textures.loadTexture('terrain.png', gl.GL_NEAREST)
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        xa = -math.cos(player.yRot * math.pi / 180.0)
        za = -math.sin(player.yRot * math.pi / 180.0)

        xa2 = -za * math.sin(player.xRot * math.pi / 180.0)
        za2 = xa * math.sin(player.xRot * math.pi / 180.0)
        ya = math.cos(player.xRot * math.pi / 180.0)

        t = tesselator
        gl.glColor4f(0.8, 0.8, 0.8, 1.0)
        t.begin()
        for p in self.particles:
            if p.isLit() ^ layer == 1:
                u0 = (p.tex % 16 + p.uo / 4.0) / 16.0
                u1 = u0 + 0.01560938
                v0 = (p.tex // 16 + p.vo / 4.0) / 16.0
                v1 = v0 + 0.01560938
                r = 0.1 * p.size

                x = p.xo + (p.x - p.xo) * a
                y = p.yo + (p.y - p.yo) * a
                z = p.zo + (p.z - p.zo) * a
                t.vertexUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - za2 * r, u0, v1)
                t.vertexUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + za2 * r, u0, v0)
                t.vertexUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + za2 * r, u1, v0)
                t.vertexUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - za2 * r, u1, v1)
        t.end()
        gl.glDisable(gl.GL_TEXTURE_2D)
