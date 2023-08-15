# cython: language_level=3

from pyglet import gl as opengl

from mc.CompatibilityShims import BufferUtils


cdef class Tesselator:

    MAX_VERTICES = 100000

    def __cinit__(self):
        self.max_vertices = self.MAX_VERTICES

        self.u = 0.0
        self.v = 0.0
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0

        self.hasColor = False
        self.hasTexture = False

        self.vertexBuffer = BufferUtils.createFloatBuffer(300000)
        self.texCoordBuffer = BufferUtils.createFloatBuffer(200000)
        self.colorBuffer = BufferUtils.createFloatBuffer(300000)

    cpdef flush(self):
        self.vertexBuffer.flip()
        self.texCoordBuffer.flip()
        self.colorBuffer.flip()

        opengl.glVertexPointer(3, opengl.GL_FLOAT, 0, self.vertexBuffer)
        if self.hasTexture:
            opengl.glTexCoordPointer(2, opengl.GL_FLOAT, 0, self.texCoordBuffer)
        if self.hasColor:
            opengl.glColorPointer(3, opengl.GL_FLOAT, 0, self.colorBuffer)

        opengl.glEnableClientState(opengl.GL_VERTEX_ARRAY)
        if self.hasTexture:
            opengl.glEnableClientState(opengl.GL_TEXTURE_COORD_ARRAY)
        if self.hasColor:
            opengl.glEnableClientState(opengl.GL_COLOR_ARRAY)

        opengl.glDrawArrays(opengl.GL_QUADS, 0, self.vertices)

        opengl.glDisableClientState(opengl.GL_VERTEX_ARRAY)
        if self.hasTexture:
            opengl.glDisableClientState(opengl.GL_TEXTURE_COORD_ARRAY)
        if self.hasColor:
            opengl.glDisableClientState(opengl.GL_COLOR_ARRAY)

        self.clear()

    cdef clear(self):
        self.vertices = 0

        self.vertexBuffer.clear()
        self.texCoordBuffer.clear()
        self.colorBuffer.clear()

    cpdef init(self):
        self.clear()
        self.hasColor = False
        self.hasTexture = False

    cpdef tex(self, float u, float v):
        self.hasTexture = True
        self.u = u
        self.v = v

    cpdef color(self, float r, float g, float b):
        self.hasColor = True
        self.r = r
        self.g = g
        self.b = b

    cpdef vertex(self, float x, float y, float z):
        self.vertexBuffer.put(self.vertices * 3 + 0, x).put(self.vertices * 3 + 1, y).put(self.vertices * 3 + 2, z)
        if self.hasTexture:
            self.texCoordBuffer.put(self.vertices * 2 + 0, self.u).put(self.vertices * 2 + 1, self.v)
        if self.hasColor:
            self.colorBuffer.put(self.vertices * 3 + 0, self.r).put(self.vertices * 3 + 1, self.g).put(self.vertices * 3 + 2, self.b)

        self.vertices += 1
        if self.vertices == self.max_vertices:
            self.flush()
