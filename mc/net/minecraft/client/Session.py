from mc.net.minecraft.game.level.block.Blocks import blocks

class Session:
    allowedBlocks = (blocks.stone, blocks.cobblestone, blocks.brick, blocks.dirt,
                     blocks.planks, blocks.log, blocks.leaves, blocks.torch,
                     blocks.stairSingle, blocks.glass, blocks.cobblestoneMossy,
                     blocks.sapling, blocks.plantYellow, blocks.plantRed,
                     blocks.mushroomBrown, blocks.mushroomRed, blocks.sand,
                     blocks.gravel, blocks.sponge, blocks.clothRed,
                     blocks.clothOrange, blocks.clothYellow, blocks.clothChartreuse,
                     blocks.clothGreen, blocks.clothSpringGreen, blocks.clothCyan,
                     blocks.clothCapri, blocks.clothUltramarine, blocks.clothViolet,
                     blocks.clothPurple, blocks.clothMagenta, blocks.clothRose,
                     blocks.clothDarkGray, blocks.clothGray, blocks.clothWhite,
                     blocks.oreCoal, blocks.oreIron, blocks.oreGold, blocks.ironBlock,
                     blocks.goldBlock, blocks.bookshelf, blocks.tnt, blocks.obsidian)
    print(len(allowedBlocks))

    def __init__(self, username, sessionId):
        self.username = username
