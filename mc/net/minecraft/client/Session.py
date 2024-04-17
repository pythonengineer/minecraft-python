from mc.net.minecraft.game.level.block.Blocks import blocks

class Session:
    registeredBlocksList = (blocks.stone, blocks.cobblestone, blocks.brick, blocks.dirt,
                            blocks.planks, blocks.wood, blocks.leaves, blocks.torch,
                            blocks.stairSingle, blocks.glass, blocks.cobblestoneMossy,
                            blocks.sapling, blocks.plantYellow, blocks.plantRed,
                            blocks.mushroomBrown, blocks.mushroomRed, blocks.sand,
                            blocks.gravel, blocks.sponge, blocks.clothRed,
                            blocks.clothOrange, blocks.clothYellow, blocks.clothChartreuse,
                            blocks.clothGreen, blocks.clothSpringGreen, blocks.clothCyan,
                            blocks.clothCapri, blocks.clothUltramarine, blocks.clothViolet,
                            blocks.clothPurple, blocks.clothMagenta, blocks.clothRose,
                            blocks.clothDarkGray, blocks.clothGray, blocks.clothWhite,
                            blocks.oreCoal, blocks.oreIron, blocks.oreGold, blocks.blockSteel,
                            blocks.blockGold, blocks.bookShelf, blocks.tnt, blocks.obsidian)
    print(len(registeredBlocksList))

    def __init__(self, username, sessionId):
        self.username = username
