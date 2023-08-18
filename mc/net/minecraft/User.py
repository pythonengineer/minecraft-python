from mc.net.minecraft.level.tile.Tiles import tiles

class User:
    creativeTiles = [tiles.rock.id, tiles.dirt.id, tiles.stoneBrick.id,
                     tiles.wood.id, tiles.bush.id, tiles.log.id,
                     tiles.leaf.id, tiles.sand.id, tiles.gravel.id]

    def __init__(self, name, sessionId, mpPass):
        self.name = name
        self.sessionId = sessionId
        self.mpPass = mpPass
