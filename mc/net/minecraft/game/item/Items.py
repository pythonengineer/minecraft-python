from mc.net.minecraft.game.item.ItemFlintAndSteel import ItemFlintAndSteel
from mc.net.minecraft.game.item.ItemPickaxe import ItemPickaxe
from mc.net.minecraft.game.item.ItemSword import ItemSword
from mc.net.minecraft.game.item.ItemSpade import ItemSpade
from mc.net.minecraft.game.item.ItemSoup import ItemSoup
from mc.net.minecraft.game.item.ItemBlock import ItemBlock
from mc.net.minecraft.game.item.ItemFood import ItemFood
from mc.net.minecraft.game.item.ItemAxe import ItemAxe
from mc.net.minecraft.game.item.ItemBow import ItemBow
from mc.net.minecraft.game.item.Item import Item
from mc.net.minecraft.game.level.block.Blocks import blocks

class Items:

    def __init__(self):
        self.itemsList = [None] * 1024

        self.shovel = ItemSpade(self, 0).setIconIndex(82)
        self.pickaxeSteel = ItemPickaxe(self, 1).setIconIndex(98)
        self.axeSteel = ItemAxe(self, 2).setIconIndex(114)

        self.flintSteel = ItemFlintAndSteel(self, 3).setIconIndex(5)

        apple = ItemFood(self, 4, 4).setIconIndex(4)

        self.bow = ItemBow(self, 5).setIconIndex(21)

        self.arrow = Item(self, 6).setIconIndex(37)
        self.coal = Item(self, 7).setIconIndex(7)
        self.diamond = Item(self, 8).setIconIndex(55)
        self.ingotIron = Item(self, 9).setIconIndex(23)
        self.ingotGold = Item(self, 10).setIconIndex(39)

        self.swordSteel = ItemSword(self, 11).setIconIndex(66)
        self.swordWood = ItemSword(self, 12).setIconIndex(64)
        self.shovelWood = ItemSpade(self, 13).setIconIndex(80)
        self.pickaxeWood = ItemPickaxe(self, 14).setIconIndex(96)
        self.axeWood = ItemAxe(self, 15).setIconIndex(112)

        self.swordStone = ItemSword(self, 16).setIconIndex(65)
        self.shovelStone = ItemSpade(self, 17).setIconIndex(81)
        self.pickaxeStone = ItemPickaxe(self, 18).setIconIndex(97)
        self.axeStone = ItemAxe(self, 19).setIconIndex(113)

        self.swordDiamond = ItemSword(self, 20).setIconIndex(67)
        self.shovelDiamond = ItemSpade(self, 21).setIconIndex(83)
        self.pickaxeDiamond = ItemPickaxe(self, 22).setIconIndex(99)
        self.axeDiamond = ItemAxe(self, 23).setIconIndex(115)

        self.stick = Item(self, 24).setIconIndex(53)

        self.bowlEmpty = Item(self, 25).setIconIndex(71)
        self.bowlSoup = ItemSoup(self, 26, 8).setIconIndex(72)

        self.swordGold = ItemSword(self, 27).setIconIndex(68)
        self.shovelGold = ItemSpade(self, 28).setIconIndex(84)
        self.pickaxeGold = ItemPickaxe(self, 29).setIconIndex(100)
        self.axeGold = ItemAxe(self, 30).setIconIndex(116)

        self.silk = Item(self, 31).setIconIndex(8)
        self.feather = Item(self, 32).setIconIndex(24)

        self.gunpowder = Item(self, 33).setIconIndex(40)

        for i in range(256):
            if blocks.blocksList[i]:
                self.itemsList[i] = ItemBlock(self, i - 256)

items = Items()
