from mc.net.minecraft.model.Cube import Cube
from mc.net.minecraft.model.Vertex import Vertex
from mc.net.minecraft.model.Polygon import Polygon

class ItemModel:

    def __init__(self, tex):
        self.__cube = Cube(0, 0)
        self.__cube.vertices = [None] * 8
        self.__cube.polygons = [None] * 6
        ptx = Vertex.fromPos(-2.0, -2.0, -2.0, 0.0, 0.0)
        ptx2 = Vertex.fromPos(2.0, -2.0, -2.0, 0.0, 8.0)
        ptx3 = Vertex.fromPos(2.0, 2.0, -2.0, 8.0, 8.0)
        ptx4 = Vertex.fromPos(-2.0, 2.0, -2.0, 8.0, 0.0)
        ptx5 = Vertex.fromPos(-2.0, -2.0, 2.0, 0.0, 0.0)
        ptx6 = Vertex.fromPos(2.0, -2.0, 2.0, 0.0, 8.0)
        ptx7 = Vertex.fromPos(2.0, 2.0, 2.0, 8.0, 8.0)
        ptx8 = Vertex.fromPos(-2.0, 2.0, 2.0, 8.0, 0.0)
        self.__cube.vertices[0] = ptx
        self.__cube.vertices[1] = ptx2
        self.__cube.vertices[2] = ptx3
        self.__cube.vertices[3] = ptx4
        self.__cube.vertices[4] = ptx5
        self.__cube.vertices[5] = ptx6
        self.__cube.vertices[6] = ptx7
        self.__cube.vertices[7] = ptx8
        f4 = 0.25
        f5 = 0.25
        f6 = ((tex % 16) + (1.0 - f4)) / 16.0
        f7 = ((tex // 16) + (1.0 - f5)) / 16.0
        f4 = ((tex % 16) + f4) / 16.0
        f8 = ((tex // 16) + f5) / 16.0
        self.__cube.polygons[0] = Polygon([ptx6, ptx2, ptx3, ptx7], f6, f7, f4, f8)
        self.__cube.polygons[1] = Polygon([ptx, ptx5, ptx8, ptx4], f6, f7, f4, f8)
        self.__cube.polygons[2] = Polygon([ptx6, ptx5, ptx, ptx2], f6, f7, f4, f8)
        self.__cube.polygons[3] = Polygon([ptx3, ptx4, ptx8, ptx7], f6, f7, f4, f8)
        self.__cube.polygons[4] = Polygon([ptx2, ptx, ptx4, ptx3], f6, f7, f4, f8)
        self.__cube.polygons[5] = Polygon([ptx5, ptx6, ptx7, ptx8], f6, f7, f4, f8)

    def render(self):
        self.__cube.render(0.0625)
