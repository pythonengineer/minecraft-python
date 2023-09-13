from mc.net.minecraft.model.Cube import Cube
from mc.net.minecraft.model.BaseModel import BaseModel

import math

class SpiderModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.__head = Cube(32, 4)
        self.__head.addBox(-4.0, -4.0, -8.0, 8, 8, 8, 0.0)
        self.__head.setPos(0.0, 0.0, -3.0)
        self.__neck = Cube(0, 0)
        self.__neck.addBox(-3.0, -3.0, -3.0, 6, 6, 6, 0.0)
        self.__body = Cube(0, 12)
        self.__body.addBox(-5.0, -4.0, -6.0, 10, 8, 12, 0.0)
        self.__body.setPos(0.0, 0.0, 9.0)
        self.__leg1 = Cube(18, 0)
        self.__leg1.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg1.setPos(-4.0, 0.0, 2.0)
        self.__leg2 = Cube(18, 0)
        self.__leg2.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg2.setPos(4.0, 0.0, 2.0)
        self.__leg3 = Cube(18, 0)
        self.__leg3.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg3.setPos(-4.0, 0.0, 1.0)
        self.__leg4 = Cube(18, 0)
        self.__leg4.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg4.setPos(4.0, 0.0, 1.0)
        self.__leg5 = Cube(18, 0)
        self.__leg5.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg5.setPos(-4.0, 0.0, 0.0)
        self.__leg6 = Cube(18, 0)
        self.__leg6.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg6.setPos(4.0, 0.0, 0.0)
        self.__leg7 = Cube(18, 0)
        self.__leg7.addBox(-15.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg7.setPos(-4.0, 0.0, -1.0)
        self.__leg8 = Cube(18, 0)
        self.__leg8.addBox(-1.0, -1.0, -1.0, 16, 2, 2, 0.0)
        self.__leg8.setPos(4.0, 0.0, -1.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.__head.yRot = xRot / 57.295776
        self.__head.xRot = yRot / 57.295776
        xRot = 0.7853982
        self.__leg1.zRot = -xRot
        self.__leg2.zRot = xRot
        self.__leg3.zRot = -xRot * 0.74
        self.__leg4.zRot = xRot * 0.74
        self.__leg5.zRot = -xRot * 0.74
        self.__leg6.zRot = xRot * 0.74
        self.__leg7.zRot = -xRot
        self.__leg8.zRot = xRot
        xRot = 0.3926991
        self.__leg1.yRot = xRot * 2.0
        self.__leg2.yRot = -xRot * 2.0
        self.__leg3.yRot = xRot
        self.__leg4.yRot = -xRot
        self.__leg5.yRot = -xRot
        self.__leg6.yRot = xRot
        self.__leg7.yRot = -xRot * 2.0
        self.__leg8.yRot = xRot * 2.0
        xRot = -(math.cos(x * 0.6662 * 2.0) * 0.4) * y
        yRot = -(math.cos(x * 0.6662 * 2.0 + math.pi) * 0.4) * y
        f7 = -(math.cos(x * 0.6662 * 2.0 + math.pi / 2) * 0.4) * y
        f8 = -(math.cos(x * 0.6662 * 2.0 + 4.712389) * 0.4) * y
        f9 = abs(math.sin(x * 0.6662) * 0.4) * y
        f10 = abs(math.sin(x * 0.6662 + math.pi) * 0.4) * y
        f11 = abs(math.sin(x * 0.6662 + math.pi / 2) * 0.4) * y
        y = abs(math.sin(x * 0.6662 + 4.712389) * 0.4) * y
        self.__leg1.yRot += xRot
        self.__leg2.yRot -= xRot
        self.__leg3.yRot += yRot
        self.__leg4.yRot -= yRot
        self.__leg5.yRot += f7
        self.__leg6.yRot -= f7
        self.__leg7.yRot += f8
        self.__leg8.yRot -= f8
        self.__leg1.zRot += f9
        self.__leg2.zRot -= f9
        self.__leg3.zRot += f10
        self.__leg4.zRot -= f10
        self.__leg5.zRot += f11
        self.__leg6.zRot -= f11
        self.__leg7.zRot += y
        self.__leg8.zRot -= y
        self.__head.render(zRot)
        self.__neck.render(zRot)
        self.__body.render(zRot)
        self.__leg1.render(zRot)
        self.__leg2.render(zRot)
        self.__leg3.render(zRot)
        self.__leg4.render(zRot)
        self.__leg5.render(zRot)
        self.__leg6.render(zRot)
        self.__leg7.render(zRot)
        self.__leg8.render(zRot)
