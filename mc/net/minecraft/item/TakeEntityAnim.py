from mc.net.minecraft.Entity import Entity

class TakeEntityAnim(Entity):

    def __init__(self, level, item, entity):
        super().__init__(level)
        self.__item = item
        self.__player = entity
        self.__time = 0
        self.setSize(1.0, 1.0)
        self.__xorg = item.x
        self.__yorg = item.y
        self.__zorg = item.z

    def tick(self):
        self.__time += 1
        if self.__time >= 3:
            self.remove()

        t = self.__time / 3.0
        t *= t
        self.xo = self.__item.xo = self.__item.x
        self.yo = self.__item.yo = self.__item.y
        self.zo = self.__item.zo = self.__item.z
        self.x = self.__item.x = self.__xorg + (self.__player.x - self.__xorg) * t
        self.y = self.__item.y = self.__yorg + (self.__player.y - 1.0 - self.__yorg) * t
        self.z = self.__item.z = self.__zorg + (self.__player.z - self.__zorg) * t
        self.setPos(self.x, self.y, self.z)

    def render(self, textures, translation):
        self.__item.render(textures, translation)
