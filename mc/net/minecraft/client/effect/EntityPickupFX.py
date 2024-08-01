from mc.net.minecraft.client.render.entity.RenderManager import RenderManager
from mc.net.minecraft.client.effect.EntityFX import EntityFX
from pyglet import gl

class EntityPickupFX(EntityFX):

    def __init__(self, world, item, entity, yOffs):
        super().__init__(world, item.posX, item.posY, item.posZ,
                         item.motionX, item.motionY, item.motionZ)
        self.__entityToPickUp = item
        self.__entityPickingUp = entity
        self.__age = 0
        self.__maxAge = 3
        self.__yOffs = -0.5

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        age = (self.__age + a) / self.__maxAge
        age *= age
        x = self.__entityToPickUp.posX
        y = self.__entityToPickUp.posY
        z = self.__entityToPickUp.posZ
        xd = self.__entityPickingUp.lastTickPosX + \
             (self.__entityPickingUp.posX - self.__entityPickingUp.lastTickPosX) * a
        yd = self.__entityPickingUp.lastTickPosY + \
             (self.__entityPickingUp.posY - self.__entityPickingUp.lastTickPosY) * a + self.__yOffs
        zd = self.__entityPickingUp.lastTickPosZ + \
             (self.__entityPickingUp.posZ - self.__entityPickingUp.lastTickPosZ) * a
        x += (xd - x) * age
        y += (yd - y) * age
        z += (zd - z) * age
        br = self._worldObj.getBlockLightValue(int(x), int(y), int(z))
        gl.glColor4f(br, br, br, 1.0)
        RenderManager.instance.renderEntityWithPosYaw(
            self.__entityToPickUp, x, y, z, self.__entityToPickUp.rotationYaw, a
        )

    def onEntityUpdate(self):
        self.__age += 1
        if self.__age == self.__maxAge:
            self.setEntityDead()

    def getFXLayer(self):
        return 2
