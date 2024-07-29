from mc.net.minecraft.client.model.TexturedQuad import TexturedQuad
from mc.net.minecraft.client.model.PositionTextureVertex import PositionTextureVertex
from mc.net.minecraft.game.physics.Vec3D import Vec3D
from pyglet import gl

import math

class ModelRenderer:

    def __init__(self, xTexOffs, yTexOffs):
        self.__corners = []
        self.__faces = []
        self.__textureOffsetX = xTexOffs
        self.__textureOffsetY = yTexOffs
        self.__rotationPointX = 0.0
        self.__rotationPointY = 0.0
        self.__rotationPointZ = 0.0
        self.rotateAngleX = 0.0
        self.rotateAngleY = 0.0
        self.rotateAngleZ = 0.0
        self.__compiled = False
        self.__displayList = 0
        self.mirror = False
        self.__showModel = True
        self.__isHidden = False

    def addBox(self, x0, y0, z0, w, h, d, ofs):
        self.__corners = [None] * 8
        self.__faces = [None] * 6

        x1 = x0 + w
        y1 = y0 + h
        z1 = z0 + d
        x0 -= ofs
        y0 -= ofs
        z0 -= ofs
        x1 += ofs
        y1 += ofs
        z1 += ofs
        if self.mirror:
            prevX = x1
            x1 = x0
            x0 = prevX

        u0 = PositionTextureVertex.fromPos(x0, y0, z0, 0.0, 0.0)
        u1 = PositionTextureVertex.fromPos(x1, y0, z0, 0.0, 8.0)
        u2 = PositionTextureVertex.fromPos(x1, y1, z0, 8.0, 8.0)
        u3 = PositionTextureVertex.fromPos(x0, y1, z0, 8.0, 0.0)

        l0 = PositionTextureVertex.fromPos(x0, y0, z1, 0.0, 0.0)
        l1 = PositionTextureVertex.fromPos(x1, y0, z1, 0.0, 8.0)
        l2 = PositionTextureVertex.fromPos(x1, y1, z1, 8.0, 8.0)
        l3 = PositionTextureVertex.fromPos(x0, y1, z1, 8.0, 0.0)

        self.__corners[0] = u0
        self.__corners[1] = u1
        self.__corners[2] = u2
        self.__corners[3] = u3
        self.__corners[4] = l0
        self.__corners[5] = l1
        self.__corners[6] = l2
        self.__corners[7] = l3

        self.__faces[0] = TexturedQuad([l1, u1, u2, l2],
                                       self.__textureOffsetX + d + w,
                                       self.__textureOffsetY + d,
                                       self.__textureOffsetX + d + w + d,
                                       self.__textureOffsetY + d + h)
        self.__faces[1] = TexturedQuad([u0, l0, l3, u3],
                                       self.__textureOffsetX + 0,
                                       self.__textureOffsetY + d,
                                       self.__textureOffsetX + d,
                                       self.__textureOffsetY + d + h)
        self.__faces[2] = TexturedQuad([l1, l0, u0, u1],
                                       self.__textureOffsetX + d,
                                       self.__textureOffsetY + 0,
                                       self.__textureOffsetX + d + w,
                                       self.__textureOffsetY + d)
        self.__faces[3] = TexturedQuad([u2, u3, l3, l2],
                                       self.__textureOffsetX + d + w,
                                       self.__textureOffsetY + 0,
                                       self.__textureOffsetX + d + w + w,
                                       self.__textureOffsetY + d)
        self.__faces[4] = TexturedQuad([u1, u0, u3, u2],
                                       self.__textureOffsetX + d,
                                       self.__textureOffsetY + d,
                                       self.__textureOffsetX + d + w,
                                       self.__textureOffsetY + d + h)
        self.__faces[5] = TexturedQuad([l0, l1, l2, l3],
                                       self.__textureOffsetX + d + w + d,
                                       self.__textureOffsetY + d,
                                       self.__textureOffsetX + d + w + d + w,
                                       self.__textureOffsetY + d + h)

        if self.mirror:
            for face in self.__faces:
                vertexPos = []
                for i in range(len(face.vertexPositions)):
                    vertexPos.append(face.vertexPositions[len(face.vertexPositions) - i - 1])

                face.vertexPositions = vertexPos

    def setRotationPoint(self, x, y, z):
        self.__rotationPointX = x
        self.__rotationPointY = y
        self.__rotationPointZ = 0.0

    def render(self, translation):
        if not self.__showModel:
            return
        if not self.__compiled:
            self.__displayList = gl.glGenLists(1)
            gl.glNewList(self.__displayList, gl.GL_COMPILE)
            gl.glBegin(gl.GL_QUADS)
            for face in self.__faces:
                vec1 = face.vertexPositions[1].vector3D.subtract(
                    face.vertexPositions[0].vector3D
                ).normalize()
                vec2 = face.vertexPositions[1].vector3D.subtract(
                    face.vertexPositions[2].vector3D
                ).normalize()
                vec = Vec3D(vec1.yCoord * vec2.zCoord - vec1.zCoord * vec2.yCoord,
                           vec1.zCoord * vec2.xCoord - vec1.xCoord * vec2.zCoord,
                           vec1.xCoord * vec2.yCoord - vec1.yCoord * vec2.xCoord).normalize()
                gl.glNormal3f(-vec.xCoord, -vec.yCoord, -vec.zCoord)
                for i in range(4):
                    v = face.vertexPositions[i]
                    gl.glTexCoord2f(v.texturePositionX, v.texturePositionY)
                    gl.glVertex3f(v.vector3D.xCoord * translation,
                                  v.vector3D.yCoord * translation,
                                  v.vector3D.zCoord * translation)

            gl.glEnd()
            gl.glEndList()
            self.__compiled = True

        if self.rotateAngleX == 0.0 and self.rotateAngleY == 0.0 and \
           self.rotateAngleZ == 0.0:
            if self.__rotationPointX == 0.0 and self.__rotationPointY == 0.0 and \
               self.__rotationPointZ == 0.0:
                gl.glCallList(self.__displayList)
            else:
                gl.glTranslatef(self.__rotationPointX * translation,
                                self.__rotationPointY * translation,
                                self.__rotationPointZ * translation)
                gl.glCallList(self.__displayList)
                gl.glTranslatef(-self.__rotationPointX * translation,
                                -self.__rotationPointY * translation,
                                -self.__rotationPointZ * translation)
        else:
            gl.glPushMatrix()
            gl.glTranslatef(self.__rotationPointX * translation,
                            self.__rotationPointY * translation,
                            self.__rotationPointZ * translation)
            if self.rotateAngleZ != 0.0:
                gl.glRotatef(self.rotateAngleZ * (180.0 / math.pi), 0.0, 0.0, 1.0)
            if self.rotateAngleY != 0.0:
                gl.glRotatef(self.rotateAngleY * (180.0 / math.pi), 0.0, 1.0, 0.0)
            if self.rotateAngleX != 0.0:
                gl.glRotatef(self.rotateAngleX * (180.0 / math.pi), 1.0, 0.0, 0.0)

            gl.glCallList(self.__displayList)
            gl.glPopMatrix()
