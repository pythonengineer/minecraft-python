from mc.net.minecraft.level.tile.Tiles import tiles

class User:
    creativeTiles = (tiles.rock, tiles.stoneBrick, tiles.brick, tiles.dirt, tiles.wood,
                     tiles.log, tiles.leaf, tiles.glass, tiles.slabHalf, tiles.mossStone,
                     tiles.bush, tiles.flower, tiles.rose, tiles.mushroomBrown,
                     tiles.mushroomRed, tiles.sand, tiles.gravel, tiles.sponge,
                     tiles.clothRed, tiles.clothOrange, tiles.clothYellow,
                     tiles.clothChartreuse, tiles.clothGreen, tiles.clothSpringGreen,
                     tiles.clothCyan, tiles.clothCapri, tiles.clothUltramarine,
                     tiles.clothViolet, tiles.clothPurple, tiles.clothMagenta,
                     tiles.clothRose, tiles.clothDarkGray, tiles.clothGray,
                     tiles.clothWhite, tiles.coalOre, tiles.ironOre, tiles.goldOre,
                     tiles.iron, tiles.gold, tiles.bookshelf, tiles.tnt, tiles.obsidian)

    def __init__(self, name, sessionId, mpPass):
        self.name = name
        self.sessionId = sessionId
        self.mpPass = mpPass
