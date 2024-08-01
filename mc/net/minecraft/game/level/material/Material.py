from enum import Enum

Material = (False, True, True)
MaterialTransparent = (False, False, False)
MaterialLiquid = (True, False, True)
MaterialLogic = (False, False, False)

class Material(Enum):
    air = ('air', *MaterialTransparent)
    ground = ('ground', *Material)
    wood = ('wood', *Material)
    rock = ('rock', *Material)
    iron = ('iron', *Material)
    water = ('water', *MaterialLiquid)
    lava = ('lava', *MaterialLiquid)
    plants = ('plants', *MaterialLogic)
    sponge = ('sponge', *Material)
    cloth = ('cloth', *Material)
    fire = ('fire', *MaterialTransparent)
    sand = ('sand', *Material)
    circuits = ('circuits', *MaterialLogic)
    glass = ('glass', *Material)
    tnt = ('tnt', *Material)

    def __init__(self, name, isLiquid, isSolid, canBlockGrass):
        self.__name = name
        self.__isLiquid = isLiquid
        self.__isSolid = isSolid
        self.__canBlockGrass = canBlockGrass

    def getIsLiquid(self):
        return self.__isLiquid

    def isSolid(self):
        return self.__isSolid

    def getCanBlockGrass(self):
        return self.__canBlockGrass
