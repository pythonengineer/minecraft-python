from mc.net.minecraft.client.model.TexturedQuad import TexturedQuad
from mc.net.minecraft.client.model.PositionTextureVertex import PositionTextureVertex

class ModelRenderer:

    def __init__(self, xTexOffs, yTexOffs):
        self.__corners = []
        self.__faces = []
        self.__textureOffsetX = xTexOffs
        self.__textureOffsetY = yTexOffs
        self.mirror = False

    def setBounds(self, x0, y0, z0, w, h, d, ofs):
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
