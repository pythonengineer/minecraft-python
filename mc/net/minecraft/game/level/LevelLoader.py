from mc.net.minecraft.client.LoadingScreenRenderer import LoadingScreenRenderer
from mc.net.minecraft.game.level.block.tileentity.TileEntityChest import TileEntityChest
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.World import World

from nbtlib import File
from nbtlib.tag import Compound, ByteArray, List, String, Byte, Short, Long, Int

class LevelLoader:

    def __init__(self, loadingScreen):
        self.__loadingScreen = loadingScreen

    def load(self, file):
        if self.__loadingScreen:
            self.__loadingScreen.displayProgressMessage('Loading level')
            self.__loadingScreen.displayLoadingString('Reading..')

        levelTag = LoadingScreenRenderer.writeLevelTags(file)
        aboutTag = levelTag['About']
        mapTag = levelTag['Map']
        environmentTag = levelTag['Environment']
        entityTag = levelTag['Entities']
        width = mapTag['Width'].real
        length = mapTag['Length'].real
        height = mapTag['Height'].real
        world = World()
        if self.__loadingScreen:
            self.__loadingScreen.displayLoadingString('Preparing level..')

        spawnTag = mapTag['Spawn']
        world.xSpawn = spawnTag[0].real
        world.ySpawn = spawnTag[1].real
        world.zSpawn = spawnTag[2].real
        world.authorName = str(aboutTag['Author'])
        world.name = str(aboutTag['Name'])
        world.createTime = aboutTag['CreatedOn'].real
        world.cloudColor = environmentTag['CloudColor'].real
        world.skyColor = environmentTag['SkyColor'].real
        world.fogColor = environmentTag['FogColor'].real
        world.skyBrightness = environmentTag['SkyBrightness'].real / 100.0
        world.cloudHeight = environmentTag['CloudHeight'].real
        world.groundLevel = environmentTag['SurroundingGroundHeight'].real
        world.waterLevel = environmentTag['SurroundingWaterHeight'].real
        world.defaultFluid = environmentTag['SurroundingWaterType'].real
        world.generate(width, height, length, bytearray(mapTag['Blocks']))
        if self.__loadingScreen:
            self.__loadingScreen.displayLoadingString('Preparing entities..')

        for compound in entityTag:
            entityType = str(compound['id'])
            entity = self._loadEntity(world, entityType)
            if entity:
                entity.readFromNBT(compound)
                world.spawnEntityInWorld(entity)

        tileTag = levelTag['TileEntities']
        for compound in tileTag:
            pos = compound['Pos'].real
            entityType = str(compound['id'])
            chest = TileEntityChest() if entityType == 'Chest' else None
            if chest:
                chest.readFromNBT(compound)
                x = pos % 1024
                y = (pos >> 10) % 1024
                z = (pos >> 20) % 1024
                world.setBlockTileEntity(x, y, z, chest)

        return world

    def _loadEntity(self, world, entityId):
        return None

    def save(self, world, file):
        if self.__loadingScreen:
            self.__loadingScreen.displayProgressMessage('Saving level')
            self.__loadingScreen.displayLoadingString('Preparing level..')

        environmentTag = Compound({'CloudColor': Int(world.cloudColor),
                                   'SkyColor': Int(world.skyColor),
                                   'FogColor': Int(world.fogColor),
                                   'SkyBrightness': Byte(int(world.skyBrightness * 100.0)),
                                   'CloudHeight': Short(world.cloudHeight),
                                   'SurroundingGroundHeight': Short(world.groundLevel),
                                   'SurroundingWaterHeight': Short(world.waterLevel),
                                   'SurroundingGroundType': Byte(blocks.grass.blockID),
                                   'SurroundingWaterType': Byte(world.defaultFluid)})
        mapTag = Compound({'Width': Short(world.width), 'Length': Short(world.length),
                           'Height': Short(world.height),
                           'Blocks': ByteArray(world.getBlocks()),
                           'Data': ByteArray(world.getData())})
        posTag = List[Short]([Short(world.xSpawn), Short(world.ySpawn),
                              Short(world.zSpawn)])
        mapTag['Spawn'] = posTag
        aboutTag = Compound({'Author': String(world.authorName),
                             'Name': String(world.name),
                             'CreatedOn': Long(world.createTime)})

        if self.__loadingScreen:
            self.__loadingScreen.displayLoadingString('Preparing entities..')

        entityTag = List[Compound]()
        for entity in world.entityMap.all:
            compound = Compound()
            entity.writeToNBT(compound)
            if compound:
                entityTag.append(compound)

        tileTag = List[Compound]()
        for pos, entity in world.map.items():
            compound = Compound({'Pos': Int(pos)})
            entity.writeToNBT(compound)
            tileTag.append(compound)

        levelTag = Compound({'About': aboutTag, 'Map': mapTag,
                             'Environment': environmentTag, 'Entities': entityTag,
                             'TileEntities': tileTag})

        if self.__loadingScreen:
            self.__loadingScreen.displayLoadingString('Writing..')

        f = File(levelTag, gzipped=True)
        f.save(file)
