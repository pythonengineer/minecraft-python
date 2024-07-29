from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material

class ItemPickaxe(ItemTool):
    __blocksEffectiveAgainst = (blocks.cobblestone, blocks.stairDouble, blocks.stairSingle,
                                blocks.stone, blocks.cobblestoneMossy, blocks.oreIron,
                                blocks.blockSteel, blocks.oreCoal, blocks.blockGold,
                                blocks.oreGold, blocks.oreDiamond, blocks.blockDiamond)

    def __init__(self, items, itemId, damage):
        super().__init__(items, itemId, damage, self.__blocksEffectiveAgainst)
        self.__damage = damage

    def canHarvestBlock(self, block):
        if block == blocks.obsidian:
            return self.__damage == 3
        elif block != blocks.blockDiamond and block != blocks.oreDiamond:
            if block != blocks.blockGold and block != blocks.oreGold:
                if block != blocks.blockSteel and block != blocks.oreIron:
                    return block.material == Material.rock
                else:
                    return self.__damage > 0
            else:
                return self.__damage >= 2
        else:
            return self.__damage >= 2
