from mc.net.minecraft.game.entity.player.InventoryPlayer import InventoryPlayer
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.entity.player.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

import math

class EntityPlayer(EntityLiving):
    MAX_HEALTH = 20
    MAX_ARROWS = 99

    def __init__(self, world):
        super().__init__(world)
        if world:
            world.playerEntity = self
            world.releaseEntitySkin(self)
            world.spawnEntityInWorld(self)

        self.yOffset = 1.62
        self.inventory = InventoryPlayer()
        self.health = EntityPlayer.MAX_HEALTH
        self.userType = 0
        self.prevCameraYaw = 0.0
        self.cameraYaw = 0.0
        self.__getScore = 0
        self.getArrows = EntityPlayer.MAX_ARROWS

    def preparePlayerToSpawn(self):
        self.yOffset = 1.62
        self.setSize(0.6, 1.8)
        super().preparePlayerToSpawn()
        if self._worldObj:
            self._worldObj.playerEntity = self

        self.health = EntityPlayer.MAX_HEALTH
        self.deathTime = 0

    def onLivingUpdate(self):
        self.inventory.tick()
        self.prevCameraYaw = self.cameraYaw
        super().onLivingUpdate()

        d = math.sqrt(self.motionX * self.motionX + self.motionZ * self.motionZ)
        t = math.atan(-self.motionY * 0.2) * 15.0
        if d > 0.1:
            d = 0.1
        if not self.onGround or self.health <= 0:
            d = 0.0
        if self.onGround or self.health <= 0:
            t = 0.0

        self.cameraYaw += (d - self.cameraYaw) * 0.4
        self.cameraPitch += (t - self.cameraPitch) * 0.8
        entities = self._worldObj.getEntitiesWithinAABBExcludingEntity(self, self.boundingBox.expand(1.0, 0.0, 1.0))
        if self.health > 0 and entities:
            for entity in entities:
                if isinstance(entity, EntityItem):
                    if entity.delayBeforeCanPickup == 0 and self.inventory.addItemStackToInventory(entity.item):
                        self._worldObj.playSoundEffect(
                            entity, 'random.pop', 0.2,
                            ((self._rand.random() - self._rand.random()) * 0.7 + 1.0) * 2.0
                        )
                        self._worldObj.releaseEntitySkin(entity)

    def getScore(self):
        return self.__getScore

    def onDeath(self, entity):
        self.setSize(0.2, 0.2)
        self.setPosition(self.posX, self.posY, self.posZ)
        self.motionY = 0.1
        if entity:
            self.motionX = -(math.cos((self.attackedAtYaw + self.rotationYaw) * math.pi / 180.0)) * 0.1
            self.motionZ = -(math.sin((self.attackedAtYaw + self.rotationYaw) * math.pi / 180.0)) * 0.1
        else:
            self.motionX = self.motionZ = 0.0

        self.yOffset = 0.1

    def setEntityDead(self):
        pass

    def dropPlayerItemWithRandomChoice(self, currentItem):
        if self.inventory.mainInventory[currentItem]:
            if self.inventory.mainInventory[currentItem].stackSize == 1:
                stack = self.inventory.mainInventory[currentItem]
                self.inventory.mainInventory[currentItem] = None
            else:
                self.inventory.mainInventory[currentItem].stackSize -= 1
                stack = ItemStack(self.inventory.mainInventory[currentItem], 1)
        else:
            stack = None

        if stack:
            item = EntityItem(self._worldObj, self.posX, self.posY - 0.3,
                              self.posZ, stack)
            item.delayBeforeCanPickup = 40
            item.motionX1 = math.sin(self.rotationYaw / 180.0 * math.pi) * 0.2
            item.motionZ1 = -math.cos(self.rotationYaw / 180.0 * math.pi) * 0.2
            item.motionY1 = 0.2
            angle = self.rand.random() * math.pi * 2.0
            scale = self.rand.random() * 0.1
            item.motionX1 = item.motionX1 + math.cos(angle) * scale
            item.motionY1 += (self.rand.random() - self.rand.random()) * 0.1
            item.motionZ1 = item.motionZ1 + math.sin(angle) * scale
            self._worldObj.spawnEntityInWorld(item)
