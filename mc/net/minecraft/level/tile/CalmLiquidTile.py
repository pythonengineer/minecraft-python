from mc.net.minecraft.level.tile.LiquidTile import LiquidTile
from mc.net.minecraft.level.liquid.Liquid import Liquid

class CalmLiquidTile(LiquidTile):

    def __init__(self, tiles, id_, liquid):
        super().__init__(tiles, id_, liquid)
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

        if type_ != 0:
            liquid = self.tiles.tiles[type_].getLiquidType()
            if self._liquid == Liquid.water and liquid == Liquid.lava or liquid == Liquid.water and self._liquid == Liquid.lava:
                level.setTile(x, y, z, self.tiles.rock.id)
                return

        if hasAirNeighbor:
            level.setTileNoUpdate(x, y, z, self._tileId)
            level.addToTickNextTick(x, y, z, self._tileId)
