from enum import Enum

class Material(Enum):
    air = ('air', False)
    ground = ('ground', False)
    wood = ('wood', False)
    rock = ('rock', False)
    iron = ('iron', False)
    water = ('water', True)
    lava = ('lava', True)
    plants = ('plants', False)
    sponge = ('sponge', False)
    cloth = ('cloth', False)
    fire = ('fire', False)
    sand = ('sand', False)
    circuits = ('circuits', False)
    glass = ('glass', False)
    tnt = ('tnt', False)

    def __init__(self, name, isLiquid):
        self.__name = name
        self.__isLiquid = isLiquid

    def getIsLiquid(self):
        return self.__isLiquid
