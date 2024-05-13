from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.RenderEntity import RenderEntity
from mc.net.minecraft.client.render.entity.RenderArrow import RenderArrow
from mc.net.minecraft.client.render.entity.RenderMD3 import RenderMD3
from mc.net.minecraft.client.render.entity.RenderItem import RenderItem
from mc.net.minecraft.client.render.entity.RenderTNTPrimed import RenderTNTPrimed
from mc.net.minecraft.game.entity.Entity import Entity
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.entity.misc.EntityTNTPrimed import EntityTNTPrimed
from mc.net.minecraft.game.entity.projectile.EntityArrow import EntityArrow
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class RenderManager:

    def __init__(self):
        self.worldObj = None
        self.renderEngine = None
        self.playerViewY = 0.0
        self.__entityRenderMap = {}
        self.__entityRenderMap[Entity] = RenderEntity()
        self.__entityRenderMap[EntityArrow] = RenderArrow()
        self.__entityRenderMap[EntityLiving] = RenderMD3()
        self.__entityRenderMap[EntityItem] = RenderItem()
        self.__entityRenderMap[EntityTNTPrimed] = RenderTNTPrimed()
        for render in self.__entityRenderMap.values():
            render.setRenderManager(self)

    def renderEntity(self, entity, a):
        xd = entity.lastTickPosX + (entity.posX - entity.lastTickPosX) * a
        yd = entity.lastTickPosY + (entity.posY - entity.lastTickPosY) * a
        zd = entity.lastTickPosZ + (entity.posZ - entity.lastTickPosZ) * a
        light = self.worldObj.getBlockLightValue(
            int(xd),
            int(yd + entity.getShadowSize()),
            int(zd)
        )
        yaw = entity.prevRotationYaw + (entity.rotationYaw - entity.prevRotationYaw) * a
        gl.glColor3f(light, light, light)
        self.renderEntityWithPosYaw(entity, xd, yd, zd, yaw, a)

    def renderEntityWithPosYaw(self, entity, xd, yd, zd, yaw, a):
        render = self.__entityRenderMap.get(entity.__class__)
        if not render and entity.__class__ != Entity:
            render = self.__entityRenderMap.get(entity.__class__.__bases__[0])
            self.__entityRenderMap[entity.__class__] = render

        if render:
            render.doRender(entity, xd, yd, zd, yaw, a)
            render.renderShadow(entity, xd, yd, zd, a)

    def changeWorld(self, world):
        self.worldObj = world

    def setPlayerViewY(self, a):
        p = self.worldObj.getPlayerEntity()
        self.playerViewY = p.prevRotationYaw + (p.rotationYaw - p.prevRotationYaw) * a
