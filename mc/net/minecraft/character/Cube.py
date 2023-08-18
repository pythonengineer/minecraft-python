from mc.net.minecraft.character.Polygon import Polygon
from mc.net.minecraft.character.Vertex import Vertex
from mc.net.minecraft.character.Vec3 import Vec3
from pyglet import gl

class Cube:
    __vertices = []
    __polygons = []
    __x = 0.0
    __y = 0.0
    __z = 0.0
    xRot = 0.0
    yRot = 0.0
    zRot = 0.0
    __compiled = False
    __list = 0

    def __init__(self, xTexOffs, yTexOffs):
        self.__xTexOffs = xTexOffs
        self.__yTexOffs = yTexOffs

    def addBox(self, x0, y0, z0, w, h, d):
        self.__vertices = [None] * 8
        self.__polygons = [None] * 6

        x1 = x0 + w
        y1 = y0 + h
        z1 = z0 + d

        u0 = Vertex.fromPos(x0, y0, z0, 0.0, 0.0)
        u1 = Vertex.fromPos(x1, y0, z0, 0.0, 8.0)
        u2 = Vertex.fromPos(x1, y1, z0, 8.0, 8.0)
        u3 = Vertex.fromPos(x0, y1, z0, 8.0, 0.0)

        l0 = Vertex.fromPos(x0, y0, z1, 0.0, 0.0)
        l1 = Vertex.fromPos(x1, y0, z1, 0.0, 8.0)
        l2 = Vertex.fromPos(x1, y1, z1, 8.0, 8.0)
        l3 = Vertex.fromPos(x0, y1, z1, 8.0, 0.0)

        self.__vertices[0] = u0
        self.__vertices[1] = u1
        self.__vertices[2] = u2
        self.__vertices[3] = u3
        self.__vertices[4] = l0
        self.__vertices[5] = l1
        self.__vertices[6] = l2
        self.__vertices[7] = l3

        self.__polygons[0] = Polygon([l1, u1, u2, l2], self.__xTexOffs + d + w, self.__yTexOffs + d, self.__xTexOffs + d + w + d, self.__yTexOffs + d + h)
        self.__polygons[1] = Polygon([u0, l0, l3, u3], self.__xTexOffs + 0, self.__yTexOffs + d, self.__xTexOffs + d, self.__yTexOffs + d + h)

        self.__polygons[2] = Polygon([l1, l0, u0, u1], self.__xTexOffs + d, self.__yTexOffs + 0, self.__xTexOffs + d + w, self.__yTexOffs + d)
        self.__polygons[3] = Polygon([u2, u3, l3, l2], self.__xTexOffs + d + w, self.__yTexOffs + 0, self.__xTexOffs + d + w + w, self.__yTexOffs + d)

        self.__polygons[4] = Polygon([u1, u0, u3, u2], self.__xTexOffs + d, self.__yTexOffs + d, self.__xTexOffs + d + w, self.__yTexOffs + d + h)
        self.__polygons[5] = Polygon([l0, l1, l2, l3], self.__xTexOffs + d + w + d, self.__yTexOffs + d, self.__xTexOffs + d + w + d + w, self.__yTexOffs + d + h)

    def setPos(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = 0.0

    def render(self, a):
        if not self.__compiled:
            self.__list = gl.glGenLists(1)
            gl.glNewList(self.__list, gl.GL_COMPILE)
            gl.glBegin(gl.GL_QUADS)
            for polygon in self.__polygons:
                vec37 = polygon.vertices[1].pos.subtract(polygon.vertices[0].pos).normalize()
                vec38 = polygon.vertices[1].pos.subtract(polygon.vertices[2].pos).normalize()
                vec37 = Vec3(vec37.y * vec38.z - vec37.z * vec38.y,
                             vec37.z * vec38.x - vec37.x * vec38.z,
                             vec37.x * vec38.y - vec37.y * vec38.x).normalize()
                gl.glNormal3f(vec37.x, vec37.y, vec37.z)

                for i in range(4):
                    v = polygon.vertices[i]
                    gl.glTexCoord2f(v.u / 64.0, v.v / 32.0)
                    gl.glVertex3f(v.pos.x * a, v.pos.y * a, v.pos.z * a)
            gl.glEnd()
            gl.glEndList()
            self.__compiled = True

        c = 57.29578
        gl.glPushMatrix()
        gl.glTranslatef(self.__x * a, self.__y * a, self.__z * a)
        gl.glRotatef(self.zRot * c, 0.0, 0.0, 1.0)
        gl.glRotatef(self.yRot * c, 0.0, 1.0, 0.0)
        gl.glRotatef(self.xRot * c, 1.0, 0.0, 0.0)

        gl.glCallList(self.__list)
        gl.glPopMatrix()
