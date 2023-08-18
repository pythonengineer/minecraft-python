from mc.net.minecraft.character.Cube import Cube
import math

class ZombieModel:

    def __init__(self):
        self.__head = Cube(0, 0)
        self.__head.addBox(-4.0, -8.0, -4.0, 8, 8, 8)

        self.__body = Cube(16, 16)
        self.__body.addBox(-4.0, 0.0, -2.0, 8, 12, 4)

        self.__arm0 = Cube(40, 16)
        self.__arm0.addBox(-3.0, -2.0, -2.0, 4, 12, 4)
        self.__arm0.setPos(-5.0, 2.0, 0.0)

        self.__arm1 = Cube(40, 16)
        self.__arm1.addBox(-1.0, -2.0, -2.0, 4, 12, 4)
        self.__arm1.setPos(5.0, 2.0, 0.0)

        self.__leg0 = Cube(0, 16)
        self.__leg0.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.__leg0.setPos(-2.0, 12.0, 0.0)

        self.__leg1 = Cube(0, 16)
        self.__leg1.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.__leg1.setPos(2.0, 12.0, 0.0)

    def render(self, a, f2, f3, f4, f5, f6):
        self.__head.yRot = f4 / 57.29578
        self.__head.xRot = f5 / 57.29578
        self.__arm0.xRot = math.cos(a * 0.6662 + math.pi) * 2.0 * f2
        self.__arm0.zRot = (math.cos(a * 0.2312) + 1.0) * f2
        self.__arm1.xRot = math.cos(a * 0.6662) * 2.0 * f2
        self.__arm1.zRot = (math.cos(a * 0.2812) - 1.0) * f2
        self.__leg0.xRot = math.cos(a * 0.6662) * 1.4 * f2
        self.__leg1.xRot = math.cos(a * 0.6662 + math.pi) * 1.4 * f2
        self.__arm0.zRot += math.cos(f3 * 0.09) * 0.05 + 0.05
        self.__arm1.zRot -= math.cos(f3 * 0.09) * 0.05 + 0.05
        self.__arm0.xRot += math.sin(f3 * 0.067) * 0.05
        self.__arm1.xRot -= math.sin(f3 * 0.067) * 0.05
        self.__head.render(f6)
        self.__body.render(f6)
        self.__arm0.render(f6)
        self.__arm1.render(f6)
        self.__leg0.render(f6)
        self.__leg1.render(f6)
