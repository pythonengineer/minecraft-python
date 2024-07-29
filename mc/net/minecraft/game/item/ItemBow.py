from mc.net.minecraft.game.entity.projectile.EntityArrow import EntityArrow
from mc.net.minecraft.game.item.Item import Item

class ItemBow(Item):

    def __init__(self, items, itemId):
        super().__init__(items, 5)
        self._maxStackSize = 1

    def onItemRightClick(self, stack, world, player):
        if player.inventory.consumeInventoryItem(self.items.arrow.shiftedIndex):
            world.playSoundAtEntity(
                player, 'random.bow', 1.0,
                1.0 / (self._rand.nextFloat() * 0.4 + 0.8)
            )
            world.spawnEntityInWorld(EntityArrow(world, player))
            return stack
