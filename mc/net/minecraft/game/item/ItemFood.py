from mc.net.minecraft.game.item.Item import Item

class ItemFood(Item):

    def __init__(self, items, itemId, healAmount):
        super().__init__(items, itemId)
        self.__healAmount = healAmount
        self._maxStackSize = 1

    def onItemRightClick(self, stack, world, player):
        stack.stackSize -= 1
        if player.health > 0:
            player.health += self.__healAmount
            if player.health > player.HEALTH:
                player.health = player.HEALTH

            player.heartsLife = player.heartsHalvesLife // 2

        return stack
