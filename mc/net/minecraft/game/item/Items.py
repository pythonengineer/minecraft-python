from mc.net.minecraft.game.item.ItemFlintAndSteel import ItemFlintAndSteel
from mc.net.minecraft.game.item.ItemPickaxe import ItemPickaxe
from mc.net.minecraft.game.item.ItemSword import ItemSword
from mc.net.minecraft.game.item.ItemSpade import ItemSpade
from mc.net.minecraft.game.item.ItemBlock import ItemBlock
from mc.net.minecraft.game.item.ItemFood import ItemFood
from mc.net.minecraft.game.item.ItemAxe import ItemAxe
from mc.net.minecraft.game.item.ItemBow import ItemBow
from mc.net.minecraft.game.item.Item import Item
from mc.net.minecraft.game.level.block.Blocks import blocks

class Items:

    def __init__(self):
        self.itemsList = [None] * 1024

        ironShovel = ItemSpade(self, 0)
        ironShovel.iconIndex = 82
        ironPickaxe = ItemPickaxe(self, 1)
        ironPickaxe.iconIndex = 98
        ironAxe = ItemAxe(self, 2)
        ironAxe.iconIndex = 114

        flint = ItemFlintAndSteel(self, 3)
        flint.iconIndex = 5

        self.apple = ItemFood(self, 4, 4)
        self.apple.iconIndex = 4

        bow = ItemBow(self, 5)
        bow.iconIndex = 21

        self.arrow = Item(self, 6)
        self.arrow.iconIndex = 37
        self.coal = Item(self, 7)
        self.coal.iconIndex = 7
        self.diamond = Item(self, 8)
        self.diamond.iconIndex = 55
        iron = Item(self, 9)
        iron.iconIndex = 23
        gold = Item(self, 10)
        gold.iconIndex = 39

        ironSword = ItemSword(self, 11)
        ironSword.iconIndex = 66
        woodSword = ItemSword(self, 12)
        woodSword.iconIndex = 64
        woodShovel = ItemSpade(self, 13)
        woodShovel.iconIndex = 80
        woodPickaxe = ItemPickaxe(self, 14)
        woodPickaxe.iconIndex = 96
        woodAxe = ItemAxe(self, 15)
        woodAxe.iconIndex = 112

        stoneSword = ItemSword(self, 16)
        stoneSword.iconIndex = 65
        stoneShovel = ItemSpade(self, 17)
        stoneShovel.iconIndex = 81
        stonePickaxe = ItemPickaxe(self, 18)
        stonePickaxe.iconIndex = 97
        stoneAxe = ItemAxe(self, 19)
        stoneAxe.iconIndex = 113

        diamondSword = ItemSword(self, 20)
        diamondSword.iconIndex = 67
        diamondShovel = ItemSpade(self, 21)
        diamondShovel.iconIndex = 83
        diamondPickaxe = ItemPickaxe(self, 22)
        diamondPickaxe.iconIndex = 99
        diamondAxe = ItemAxe(self, 23)
        diamondAxe.iconIndex = 115

        for i in range(256):
            if blocks.blocksList[i]:
                self.itemsList[i] = ItemBlock(self, i - 256)

items = Items()
