import math

from pyglet import gl as opengl

from mc import compat
from mc.net.minecraft.level.LevelListener import LevelListener
from mc.net.minecraft.level.Tesselator import Tesselator
from mc.net.minecraft.level.Frustum import Frustum
from mc.net.minecraft.level.Chunk import Chunk
from mc.net.minecraft.level.Tiles import tiles


class LevelRenderer(LevelListener):

    CHUNK_SIZE = 16
    t = Tesselator()

    def __init__(self, level):
        self.level = level
        level.addListener(self)

        self.frustum = Frustum()

        self.xChunks = level.width // self.CHUNK_SIZE
        self.yChunks = level.depth // self.CHUNK_SIZE
        self.zChunks = level.height // self.CHUNK_SIZE

        self.chunks = [None] * self.xChunks * self.yChunks * self.zChunks
        for x in range(self.xChunks):
            for y in range(self.yChunks):
                for z in range(self.zChunks):
                    x0 = x * self.CHUNK_SIZE
                    y0 = y * self.CHUNK_SIZE
                    z0 = z * self.CHUNK_SIZE
                    x1 = (x + 1) * self.CHUNK_SIZE
                    y1 = (y + 1) * self.CHUNK_SIZE
                    z1 = (z + 1) * self.CHUNK_SIZE

                    if x1 > level.width: x1 = level.width
                    if y1 > level.depth: y1 = level.depth
                    if z1 > level.height: z1 = level.height
                    self.chunks[(x + y * self.xChunks) * self.zChunks + z] = Chunk(level, x0, y0, z0, x1, y1, z1)

    def render(self, player, layer):
        self.chunks[-1].rebuiltThisFrame = 0
        #self.frustum.calculateFrustum()
        for chunk in self.chunks:
            chunk.render(layer)
            #if self.frustum.isVisible(chunk.aabb):
            #    chunk.render(layer)

    def renderHit(self, h):
        opengl.glEnable(opengl.GL_BLEND)

        opengl.glBlendFunc(opengl.GL_SRC_ALPHA, 1)
        opengl.glColor4f(1.0, 1.0, 1.0, math.sin(compat.getMillis() / 100.0) * 0.2 + 0.4)
        self.t.init()
        tiles.rock.renderFace(self.t, h.x, h.y, h.z, h.f)
        self.t.flush()
        opengl.glDisable(opengl.GL_BLEND)

    def setDirty(self, x0, y0, z0, x1, y1, z1):
        x0 //= self.CHUNK_SIZE
        x1 //= self.CHUNK_SIZE
        y0 //= self.CHUNK_SIZE
        y1 //= self.CHUNK_SIZE
        z0 //= self.CHUNK_SIZE
        z1 //= self.CHUNK_SIZE

        if x0 < 0: x0 = 0
        if y0 < 0: y0 = 0
        if z0 < 0: z0 = 0
        if x1 >= self.xChunks: x1 = self.xChunks - 1
        if y1 >= self.yChunks: y1 = self.yChunks - 1
        if z1 >= self.zChunks: z1 = self.zChunks - 1

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.chunks[((x + y * self.xChunks) * self.zChunks + z)].setDirty()

    def tileChanged(self, x, y, z):
        self.setDirty(x - 1, y - 1, z - 1, x + 1, y + 1, z + 1)

    def lightColumnChanged(self, x, z, y0, y1):
        self.setDirty(x - 1, y0 - 1, z - 1, x + 1, y1 + 1, z + 1)

    def allChanged(self):
        self.setDirty(0, 0, 0, self.level.width, self.level.depth, self.level.height)
