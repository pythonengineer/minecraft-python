from mc.CompatibilityShims import BufferUtils

from pyglet import gl

class MD3Model:

    def __init__(self, vertices):
        self.__vertices = vertices
        self.__displayList = 0

    def renderModelVertices(self):
        if self.__displayList == 0:
            self.__displayList = gl.glGenLists(self.__vertices.totalFrames)

            for frame in range(self.__vertices.totalFrames):
                gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
                gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
                gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
                gl.glNewList(self.__displayList + frame, gl.GL_COMPILE)

                for md3 in self.__vertices.buffersMD3:
                    md3.setAndClearBuffers(frame, frame, 0.0)
                    md3.vertices.position(0)
                    md3.triangles.position(0)
                    md3.normals.position(0)
                    md3.xBuffer.position(0)
                    md3.vertices.glVertexPointer(3, gl.GL_FLOAT, 0)
                    md3.normals.glNormalPointer(gl.GL_FLOAT, 0)
                    md3.xBuffer.glTexCoordPointer(2, gl.GL_FLOAT, 0)
                    md3.triangles.glDrawElements(gl.GL_TRIANGLES, md3.triangles.capacity(),
                                                 gl.GL_UNSIGNED_INT)

                gl.glEndList()
                gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
                gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
                gl.glDisableClientState(gl.GL_NORMAL_ARRAY)

        gl.glCallList(self.__displayList)
