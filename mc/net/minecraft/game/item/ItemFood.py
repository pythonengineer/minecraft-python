from mc.net.minecraft.game.item.Item import Item

class ItemFood(Item):

    def __init__(self, itemId, healAmount):
        super().__init__(260)
        self.__healAmount = 4

    def onPlaced(self, stack, player):
        stack.stackSize -= 1
        if player.health > 0:
            player.health += self.__healAmount
            if player.health > 20:
                player.health = 20

            player.heartsLife = player.heartsHalvesLife // 2

        return True
