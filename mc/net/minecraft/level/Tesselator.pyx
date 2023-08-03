# cython: language_level=3

from mc.CompatibilityShims import BufferUtils
from pyglet import gl

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

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertexBuffer)
        if self.hasTexture:
            gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, self.texCoordBuffer)
        if self.hasColor:
            gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorBuffer)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        if self.hasTexture:
            gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        if self.hasColor:
            gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glDrawArrays(gl.GL_QUADS, 0, self.vertices)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        if self.hasTexture:
            gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        if self.hasColor:
            gl.glDisableClientState(gl.GL_COLOR_ARRAY)

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
