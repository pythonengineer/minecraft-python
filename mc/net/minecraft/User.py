from mc.net.minecraft.level.tile.Tiles import tiles

class User:
    creativeTiles = [tiles.rock.id, tiles.dirt.id, tiles.sponge.id,
                     tiles.wood.id, tiles.bush.id, tiles.log.id,
                     tiles.leaf.id, tiles.glass.id, tiles.gravel.id]

    def __init__(self, name, sessionId, mpPass):
        self.name = name
        self.sessionId = sessionId
        self.mpPass = mpPass
