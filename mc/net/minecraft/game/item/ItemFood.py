from mc.net.minecraft.game.item.Item import Item

class ItemFood(Item):

    def __init__(self, items, itemId, healAmount):
        super().__init__(items, 4)
        self.__healAmount = 4

    def onItemRightClick(self, stack, world, player):
        stack.stackSize -= 1
        if player.health > 0:
            player.health += self.__healAmount
            if player.health > 20:
                player.health = 20

            player.heartsLife = player.heartsHalvesLife // 2

        return True
