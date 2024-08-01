from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material

class ItemPickaxe(ItemTool):
    __blocksEffectiveAgainst = (blocks.cobblestone, blocks.stairDouble, blocks.stairSingle,
                                blocks.stone, blocks.cobblestoneMossy, blocks.oreIron,
                                blocks.blockSteel, blocks.oreCoal, blocks.blockGold,
                                blocks.oreGold, blocks.oreDiamond, blocks.blockDiamond)

    def __init__(self, items, itemId, strength):
        super().__init__(items, itemId, 2, strength, self.__blocksEffectiveAgainst)
        self.__damage = strength

    def canHarvestBlock(self, block):
        if block == blocks.obsidian:
            return self.__damage == 3
        elif block != blocks.blockDiamond and block != blocks.oreDiamond:
            if block != blocks.blockGold and block != blocks.oreGold:
                if block != blocks.blockSteel and block != blocks.oreIron:
                    if block.material == Material.rock:
                        return True
                    else:
                        return block.material == Material.iron
                else:
                    return self.__damage > 0
            else:
                return self.__damage >= 2
        else:
            return self.__damage >= 2
