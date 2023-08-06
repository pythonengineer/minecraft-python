from mc.net.minecraft.character.Polygon import Polygon
from mc.net.minecraft.character.Vertex import Vertex
from pyglet import gl

class Cube:
    vertices = []
    polygons = []
    x = 0.0
    y = 0.0
    z = 0.0
    xRot = 0.0
    yRot = 0.0
    zRot = 0.0
    compiled = False
    list = 0

    def __init__(self, xTexOffs, yTexOffs):
        self.setTexOffs(xTexOffs, yTexOffs)

    def setTexOffs(self, xTexOffs, yTexOffs):
        self.xTexOffs = xTexOffs
        self.yTexOffs = yTexOffs

    def addBox(self, x0, y0, z0, w, h, d):
        self.vertices = [None] * 8
        self.polygons = [None] * 6

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

        self.vertices[0] = u0
        self.vertices[1] = u1
        self.vertices[2] = u2
        self.vertices[3] = u3
        self.vertices[4] = l0
        self.vertices[5] = l1
        self.vertices[6] = l2
        self.vertices[7] = l3

        self.polygons[0] = Polygon([l1, u1, u2, l2], self.xTexOffs + d + w, self.yTexOffs + d, self.xTexOffs + d + w + d, self.yTexOffs + d + h)
        self.polygons[1] = Polygon([u0, l0, l3, u3], self.xTexOffs + 0, self.yTexOffs + d, self.xTexOffs + d, self.yTexOffs + d + h)

        self.polygons[2] = Polygon([l1, l0, u0, u1], self.xTexOffs + d, self.yTexOffs + 0, self.xTexOffs + d + w, self.yTexOffs + d)
        self.polygons[3] = Polygon([u2, u3, l3, l2], self.xTexOffs + d + w, self.yTexOffs + 0, self.xTexOffs + d + w + w, self.yTexOffs + d)

        self.polygons[4] = Polygon([u1, u0, u3, u2], self.xTexOffs + d, self.yTexOffs + d, self.xTexOffs + d + w, self.yTexOffs + d + h)
        self.polygons[5] = Polygon([l0, l1, l2, l3], self.xTexOffs + d + w + d, self.yTexOffs + d, self.xTexOffs + d + w + d + w, self.yTexOffs + d + h)

    def setPos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def render(self):
        if not self.compiled:
            self.compile()

        c = 57.29578
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, self.z)
        gl.glRotatef(self.zRot * c, 0.0, 0.0, 1.0)
        gl.glRotatef(self.yRot * c, 0.0, 1.0, 0.0)
        gl.glRotatef(self.xRot * c, 1.0, 0.0, 0.0)

        gl.glCallList(self.list)
        gl.glPopMatrix()

    def compile(self):
        self.list = gl.glGenLists(1)
        gl.glNewList(self.list, gl.GL_COMPILE)
        gl.glBegin(gl.GL_QUADS)
        for polygon in self.polygons:
            polygon.render()
        gl.glEnd()
        gl.glEndList()
        self.compiled = True
