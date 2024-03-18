from mc.net.minecraft.client.player.InventoryPlayer import InventoryPlayer
from mc.net.minecraft.client.player.EntityPlayerInput import EntityPlayerInput
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from pyglet import gl

import math

class EntityPlayer(EntityLiving):
    MAX_HEALTH = 20
    MAX_ARROWS = 99
    __skinID = -1
    skinData = None

    def __init__(self, world):
        super().__init__(world)
        if world:
            world.playerEntity = self
            world.releaseEntitySkin(self)
            world.spawnEntityInWorld(self)

        self.yOffset = 1.62
        self.movementInput = None
        self.inventory = InventoryPlayer()
        self.health = EntityPlayer.MAX_HEALTH
        self.entityAI = EntityPlayerInput(self)
        self.prevCameraYaw = 0.0
        self.cameraYaw = 0.0
        self.score = 0
        self.getArrows = 20

    def preparePlayerToSpawn(self):
        self.yOffset = 1.62
        self.setSize(0.6, 1.8)
        super().preparePlayerToSpawn()
        if self.worldObj:
            self.worldObj.playerEntity = self

        self.health = EntityPlayer.MAX_HEALTH
        self.deathTime = 0

    def onLivingUpdate(self):
        self.inventory.tick()
        self.prevCameraYaw = self.cameraYaw
        self.movementInput.updatePlayerMoveState()
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
        entities = self.worldObj.getEntitiesWithinAABBExcludingEntity(self, self.boundingBox.expand(1.0, 0.0, 1.0))
        if self.health > 0 and entities:
            for entity in entities:
                pass

    def resetKeyState(self):
        self.movementInput.resetKeyState()

    def checkKeyForMovementInput(self, symbol, state):
        self.movementInput.checkKeyForMovementInput(symbol, state)

    def addResource(self, index):
        return self.inventory.addResource(index)

    def getScore(self):
        return 0

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

    def remove(self):
        pass

    @staticmethod
    def setupSkinImage(renderEngine):
        if EntityPlayer.skinData:
            EntityPlayer.__skinID = renderEngine.getTextureImg(EntityPlayer.skinData)
            EntityPlayer.skinData = None

        if EntityPlayer.__skinID < 0:
            gl.glBindTexture(gl.GL_TEXTURE_2D, renderEngine.getTexture('char.png'))
        else:
            gl.glBindTexture(gl.GL_TEXTURE_2D, EntityPlayer.__skinID)
