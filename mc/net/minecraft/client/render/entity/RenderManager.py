from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.RenderEntity import RenderEntity
from mc.net.minecraft.client.render.entity.RenderArrow import RenderArrow
from mc.net.minecraft.client.render.entity.RenderLiving import RenderLiving
from mc.net.minecraft.client.render.entity.RenderItem import RenderItem
from mc.net.minecraft.client.render.entity.RenderTNTPrimed import RenderTNTPrimed
from mc.net.minecraft.client.model.ModelSpider import ModelSpider
from mc.net.minecraft.client.model.ModelSheep import ModelSheep
from mc.net.minecraft.client.model.ModelPig import ModelPig
from mc.net.minecraft.client.model.ModelCreeper import ModelCreeper
from mc.net.minecraft.client.model.ModelSkeleton import ModelSkeleton
from mc.net.minecraft.client.model.ModelZombie import ModelZombie
from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.game.entity.Entity import Entity
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.animal.EntityPig import EntityPig
from mc.net.minecraft.game.entity.animal.EntitySheep import EntitySheep
from mc.net.minecraft.game.entity.monster.EntityCreeper import EntityCreeper
from mc.net.minecraft.game.entity.monster.EntitySkeleton import EntitySkeleton
from mc.net.minecraft.game.entity.monster.EntitySpider import EntitySpider
from mc.net.minecraft.game.entity.monster.EntityZombie import EntityZombie
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.entity.misc.EntityTNTPrimed import EntityTNTPrimed
from mc.net.minecraft.game.entity.projectile.EntityArrow import EntityArrow
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class RenderManager:
    instance = None

    def __init__(self):
        self.worldObj = None
        self.renderEngine = None
        self.playerViewY = 0.0
        self.__viewerPosX = 0.0
        self.__viewerPosY = 0.0
        self.__viewerPosZ = 0.0
        self.__entityRenderMap = {}
        self.__entityRenderMap[EntitySpider] = RenderLiving(ModelSpider(), 1.0)
        self.__entityRenderMap[EntityPig] = RenderLiving(ModelPig(), 0.7)
        self.__entityRenderMap[EntitySheep] = RenderLiving(ModelSheep(), 0.7)
        self.__entityRenderMap[EntityCreeper] = RenderLiving(ModelCreeper(), 0.5)
        self.__entityRenderMap[EntitySkeleton] = RenderLiving(ModelSkeleton(), 0.5)
        self.__entityRenderMap[EntityZombie] = RenderLiving(ModelZombie(), 0.5)
        self.__entityRenderMap[EntityLiving] = RenderLiving(ModelBiped(), 0.5)
        self.__entityRenderMap[Entity] = RenderEntity()
        self.__entityRenderMap[EntityArrow] = RenderArrow()
        self.__entityRenderMap[EntityItem] = RenderItem()
        self.__entityRenderMap[EntityTNTPrimed] = RenderTNTPrimed()
        for render in self.__entityRenderMap.values():
            render.setRenderManager(self)

    def cacheActiveRenderInfo(self, world, renderEngine, player, a):
        self.worldObj = world
        self.renderEngine = renderEngine
        self.playerViewY = player.prevRotationYaw + (player.rotationYaw - player.prevRotationYaw) * a
        self.__viewerPosX = player.lastTickPosX + (player.posX - player.lastTickPosX) * a
        self.__viewerPosY = player.lastTickPosY + (player.posY - player.lastTickPosY) * a
        self.__viewerPosZ = player.lastTickPosZ + (player.posZ - player.lastTickPosZ) * a

    def renderEntity(self, entity, a):
        xd = entity.lastTickPosX + (entity.posX - entity.lastTickPosX) * a
        yd = entity.lastTickPosY + (entity.posY - entity.lastTickPosY) * a
        zd = entity.lastTickPosZ + (entity.posZ - entity.lastTickPosZ) * a
        yaw = entity.prevRotationYaw + (entity.rotationYaw - entity.prevRotationYaw) * a
        light = self.worldObj.getBlockLightValue(
            int(xd),
            int(yd + entity.getShadowSize()),
            int(zd)
        )
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

    def setWorld(self, world):
        self.worldObj = world

    def getDistanceToCamera(self, x, y, z):
        x -= self.__viewerPosX
        y -= self.__viewerPosY
        z -= self.__viewerPosZ
        return x * x + y * y + z * z
