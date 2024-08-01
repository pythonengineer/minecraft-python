from mc.net.minecraft.game.entity.player.InventoryPlayer import InventoryPlayer
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material
from pyglet import gl

import math

class EntityPlayer(EntityLiving):
    MAX_HEALTH = 20
    FIRE_RESISTANCE = 20

    def __init__(self, world):
        super().__init__(world)
        if world:
            world.playerEntity = self
            world.releaseEntitySkin(self)

        self.yOffset = 1.62
        self.inventory = InventoryPlayer()
        self.health = EntityPlayer.MAX_HEALTH
        self.fireResistance = EntityPlayer.FIRE_RESISTANCE
        self.userType = 0
        self.prevCameraYaw = 0.0
        self.cameraYaw = 0.0
        self._getScore = 0

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
                entity.onCollideWithPlayer(self)

    def getScore(self):
        return self._getScore

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

    def dropPlayerItemWithRandomChoice(self, stack):
        if not stack:
            return

        item = EntityItem(self._worldObj, self.posX, self.posY - 0.3,
                          self.posZ, stack)
        item.delayBeforeCanPickup = 40
        item.motionX = math.sin(self.rotationYaw / 180.0 * math.pi) * 0.2
        item.motionZ = -math.cos(self.rotationYaw / 180.0 * math.pi) * 0.2
        item.motionY = 0.2
        angle = self._rand.nextFloat() * math.pi * 2.0
        scale = self._rand.nextFloat() * 0.1
        item.motionX += math.cos(angle) * scale
        item.motionY += (self._rand.nextFloat() - self._rand.nextFloat()) * 0.1
        item.motionZ += math.sin(angle) * scale
        self._worldObj.spawnEntityInWorld(item)

    def getStrVsBlock(self, block):
        strength = 1.0
        stack = self.inventory.mainInventory[self.inventory.currentItem]
        if stack:
            strength = 1.0 * stack.getItem().getStrVsBlock(block)
        if self.isInsideOfMaterial():
            strength /= 5.0
        if not self.onGround:
            strength /= 5.0

        return strength

    def canHarvestBlock(self, block):
        if block.material != Material.rock and block.material != Material.iron:
            return True
        else:
            stack = self.inventory.getStackInSlot(self.inventory.currentItem)
            return items.itemsList[stack.itemID].canHarvestBlock(block) if stack else False

    def _writeEntityToNBT(self, compound):
        pass

    def _getEntityString(self):
        return ''

    def displayGUIChest(self, inventory):
        pass

    def displayWorkbenchGUI(self):
        pass

    def onItemPickup(self, item):
        pass

    def _getEyeHeight(self):
        return 0.12
