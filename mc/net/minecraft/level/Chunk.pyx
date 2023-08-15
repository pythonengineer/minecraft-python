from pyglet import gl as opengl

from mc.net.minecraft.level.Tesselator cimport Tesselator
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.level.Tiles import tiles
from mc.net.minecraft.phys.AABB import AABB
from mc.net.minecraft.Textures import Textures


cdef object Chunk_t = Tesselator()

cdef int Chunk_updates = 0
cdef int Chunk_rebuiltThisFrame = 0


cdef class Chunk:
    texture = Textures.loadTexture('terrain.png', opengl.GL_NEAREST)

    cdef:
        public Level level

        public int x0
        public int y0
        public int z0
        public int x1
        public int y1
        public int z1

        public object aabb
        public int lists
        public bint dirty

    property t:

        def __get__(self):
            return Chunk_t

        def __set__(self, x):
            global Chunk_t
            Chunk_t = x

    property updates:

        def __get__(self):
            return Chunk_updates

        def __set__(self, x):
            global Chunk_updates
            Chunk_updates = x

    property rebuiltThisFrame:

        def __get__(self):
            return Chunk_rebuiltThisFrame

        def __set__(self, x):
            global Chunk_rebuiltThisFrame
            Chunk_rebuiltThisFrame = x

    def __cinit__(self):
        self.dirty = True
        self.lists = -1

    def __init__(self, Level level, int x0, int y0, int z0,
                 int x1, int y1, int z1, bint fake=False):
        if fake:
            return

        self.level = level
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.aabb = AABB(x0, y0, z0, x1, y1, z1)
        self.lists = opengl.glGenLists(2)

    cpdef rebuild(self, int layer):
        cdef int count, x, y, z, tex
        cdef Tesselator t

        if self.rebuiltThisFrame == 2:
            return

        self.dirty = False

        self.updates += 1
        self.rebuiltThisFrame += 1

        opengl.glNewList(self.lists + layer, opengl.GL_COMPILE)
        opengl.glEnable(opengl.GL_TEXTURE_2D)
        opengl.glBindTexture(opengl.GL_TEXTURE_2D, self.texture)

        t = <Tesselator>self.t
        t.init()
        count = 0
        for x in range(self.x0, self.x1):
            for y in range(self.y0, self.y1):
                for z in range(self.z0, self.z1):
                    if self.level.isTile(x, y, z):
                        tex = 0 if y == self.level.depth * 2 // 3 else 1
                        count += 1
                        if tex == 0:
                            tiles.rock.render(t, self.level, layer, x, y, z)
                        else:
                            tiles.grass.render(t, self.level, layer, x, y, z)
        t.flush()
        opengl.glDisable(opengl.GL_TEXTURE_2D)
        opengl.glEndList()

    cpdef render(self, int layer):
        if self.dirty:
            self.rebuild(0)
            self.rebuild(1)

        opengl.glCallList(self.lists + layer)

    def setDirty(self):
        self.dirty = True
