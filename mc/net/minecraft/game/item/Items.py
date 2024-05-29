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

        self.shovel = ItemSpade(self, 0)
        self.shovel.iconIndex = 82
        self.pickaxeSteel = ItemPickaxe(self, 1)
        self.pickaxeSteel.iconIndex = 98
        self.axeSteel = ItemAxe(self, 2)
        self.axeSteel.iconIndex = 114

        self.flintSteel = ItemFlintAndSteel(self, 3)
        self.flintSteel.iconIndex = 5

        apple = ItemFood(self, 4, 4)
        apple.iconIndex = 4

        bow = ItemBow(self, 5)
        bow.iconIndex = 21

        self.arrow = Item(self, 6)
        self.arrow.iconIndex = 37
        self.coal = Item(self, 7)
        self.coal.iconIndex = 7
        self.diamond = Item(self, 8)
        self.diamond.iconIndex = 55
        self.ingotIron = Item(self, 9)
        self.ingotIron.iconIndex = 23
        self.ingotGold = Item(self, 10)
        self.ingotGold.iconIndex = 39

        self.swordSteel = ItemSword(self, 11)
        self.swordSteel.iconIndex = 66
        self.swordWood = ItemSword(self, 12)
        self.swordWood.iconIndex = 64
        self.shovelWood = ItemSpade(self, 13)
        self.shovelWood.iconIndex = 80
        self.pickaxeWood = ItemPickaxe(self, 14)
        self.pickaxeWood.iconIndex = 96
        self.axeWood = ItemAxe(self, 15)
        self.axeWood.iconIndex = 112

        self.swordStone = ItemSword(self, 16)
        self.swordStone.iconIndex = 65
        self.shovelStone = ItemSpade(self, 17)
        self.shovelStone.iconIndex = 81
        self.pickaxeStone = ItemPickaxe(self, 18)
        self.pickaxeStone.iconIndex = 97
        self.axeStone = ItemAxe(self, 19)
        self.axeStone.iconIndex = 113

        self.swordDiamond = ItemSword(self, 20)
        self.swordDiamond.iconIndex = 67
        self.shovelDiamond = ItemSpade(self, 21)
        self.shovelDiamond.iconIndex = 83
        self.pickaxeDiamond = ItemPickaxe(self, 22)
        self.pickaxeDiamond.iconIndex = 99
        self.axeDiamond = ItemAxe(self, 23)
        self.axeDiamond.iconIndex = 115

        self.stick = Item(self, 24)
        self.stick.iconIndex = 53

        for i in range(256):
            if blocks.blocksList[i]:
                self.itemsList[i] = ItemBlock(self, i - 256)

items = Items()
