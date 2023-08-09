from mc.net.minecraft.level.tile.LiquidTile import LiquidTile

class CalmLiquidTile(LiquidTile):

    def __init__(self, tiles, id_, liquidType):
        super().__init__(tiles, id_, liquidType)
        self._tileId = id_ - 1
        self._calmTileId = id_
        self._setTicking(False)

    def tick(self, level, x, y, z, random):
        pass

    def neighborChanged(self, level, x, y, z, type_):
        hasAirNeighbor = False
        if level.getTile(x - 1, y, z) == 0: hasAirNeighbor = True
        if level.getTile(x + 1, y, z) == 0: hasAirNeighbor = True
        if level.getTile(x, y, z - 1) == 0: hasAirNeighbor = True
        if level.getTile(x, y, z + 1) == 0: hasAirNeighbor = True
        if level.getTile(x, y - 1, z) == 0: hasAirNeighbor = True

        if self._liquidType == 1 and type_ == self.tiles.lava.id:
            level.setTileNoUpdate(x, y, z, self.tiles.rock.id)
        elif self._liquidType == 2 and type_ == self.tiles.water.id:
            level.setTileNoUpdate(x, y, z, self.tiles.rock.id)
        elif hasAirNeighbor:
            level.setTileNoUpdate(x, y, z, self._tileId)
            level.addToTickNextTick(x, y, z, self._tileId)
