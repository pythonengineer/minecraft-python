from mc.net.minecraft.model.Polygon import Polygon
from mc.net.minecraft.model.Vertex import Vertex
from mc.net.minecraft.model.Vec3 import Vec3
from pyglet import gl

class Cube:

    def __init__(self, xTexOffs, yTexOffs):
        self.vertices = []
        self.polygons = []
        self.xTexOffs = xTexOffs
        self.yTexOffs = yTexOffs
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.xRot = 0.0
        self.yRot = 0.0
        self.zRot = 0.0
        self.compiled = False
        self.list = 0
        self.mirror = False
        self.showModel = True
        self.__isHidden = False

    def addBox(self, x0, y0, z0, w, h, d, f):
        self.vertices = [None] * 8
        self.polygons = [None] * 6

        x1 = x0 + w
        y1 = y0 + h
        z1 = z0 + d
        x0 -= f
        y0 -= f
        z0 -= f
        x1 += f
        y1 += f
        z1 += f
        if self.mirror:
            f = x1
            x1 = x0
            x0 = f

        u0 = Vertex.fromPos(x0, y0, z0, 0.0, 0.0)
        u1 = Vertex.fromPos(x1, y0, z0, 0.0, 8.0)
        u2 = Vertex.fromPos(x1, y1, z0, 8.0, 8.0)
        u3 = Vertex.fromPos(x0, y1, z0, 8.0, 0.0)

        l0 = Vertex.fromPos(x0, y0, z1, 0.0, 0.0)
        l1 = Vertex.fromPos(x1, y0, z1, 0.0, 8.0)
        l2 = Vertex.fromPos(x1, y1, z1, 8.0, 8.0)
        l3 = Vertex.fromPos(x0, y1, z1, 8.0, 0.0)

        self.vertices[0] = u0
        self.vertices[1] = u1
        self.vertices[2] = u2
        self.vertices[3] = u3
        self.vertices[4] = l0
        self.vertices[5] = l1
        self.vertices[6] = l2
        self.vertices[7] = l3

        self.polygons[0] = Polygon([l1, u1, u2, l2],
                                   self.xTexOffs + d + w,
                                   self.yTexOffs + d,
                                   self.xTexOffs + d + w + d,
                                   self.yTexOffs + d + h)
        self.polygons[1] = Polygon([u0, l0, l3, u3],
                                   self.xTexOffs + 0,
                                   self.yTexOffs + d,
                                   self.xTexOffs + d,
                                   self.yTexOffs + d + h)
        self.polygons[2] = Polygon([l1, l0, u0, u1],
                                   self.xTexOffs + d,
                                   self.yTexOffs + 0,
                                   self.xTexOffs + d + w,
                                   self.yTexOffs + d)
        self.polygons[3] = Polygon([u2, u3, l3, l2],
                                   self.xTexOffs + d + w,
                                   self.yTexOffs + 0,
                                   self.xTexOffs + d + w + w,
                                   self.yTexOffs + d)
        self.polygons[4] = Polygon([u1, u0, u3, u2],
                                   self.xTexOffs + d,
                                   self.yTexOffs + d,
                                   self.xTexOffs + d + w,
                                   self.yTexOffs + d + h)
        self.polygons[5] = Polygon([l0, l1, l2, l3],
                                   self.xTexOffs + d + w + d,
                                   self.yTexOffs + d,
                                   self.xTexOffs + d + w + d + w,
                                   self.yTexOffs + d + h)

        if self.mirror:
            for face in self.polygons:
                vertexPos = []
                for i in range(len(face.vertices)):
                    vertexPos.append(face.vertices[len(face.vertices) - i - 1])

                face.vertices = vertexPos

    def setPos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def render(self, translation):
        if not self.showModel:
            return
        if not self.compiled:
            self.translateTo(translation)

        if self.xRot == 0.0 and self.yRot == 0.0 and self.zRot == 0.0:
            if self.x == 0.0 and self.y == 0.0 and self.z == 0.0:
                gl.glCallList(self.list)
            else:
                gl.glTranslatef(self.x * translation,
                                self.y * translation,
                                self.z * translation)
                gl.glCallList(self.list)
                gl.glTranslatef(-self.x * translation,
                                -self.y * translation,
                                -self.z * translation)
        else:
            c = 57.295776
            gl.glPushMatrix()
            gl.glTranslatef(self.x * translation, self.y * translation, self.z * translation)
            if self.zRot != 0.0:
                gl.glRotatef(self.zRot * c, 0.0, 0.0, 1.0)
            if self.yRot != 0.0:
                gl.glRotatef(self.yRot * c, 0.0, 1.0, 0.0)
            if self.xRot != 0.0:
                gl.glRotatef(self.xRot * c, 1.0, 0.0, 0.0)

            gl.glCallList(self.list)
            gl.glPopMatrix()

    def translateTo(self, translation):
        self.list = gl.glGenLists(1)
        gl.glNewList(self.list, gl.GL_COMPILE)
        gl.glBegin(gl.GL_QUADS)
        for face in self.polygons:
            vec1 = face.vertices[1].pos.subtract(face.vertices[0].pos).normalize()
            vec2 = face.vertices[1].pos.subtract(face.vertices[2].pos).normalize()
            vec = Vec3(vec1.y * vec2.z - vec1.z * vec2.y,
                       vec1.z * vec2.x - vec1.x * vec2.z,
                       vec1.x * vec2.y - vec1.y * vec2.x).normalize()
            gl.glNormal3f(vec.x, vec.y, vec.z)
            for i in range(4):
                v = face.vertices[i]
                gl.glTexCoord2f(v.u, v.v)
                gl.glVertex3f(v.pos.x * translation, v.pos.y * translation, v.pos.z * translation)

        gl.glEnd()
        gl.glEndList()
        self.compiled = True
