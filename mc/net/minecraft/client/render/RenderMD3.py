from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.model.md3.MD3Loader import MD3Loader
from mc.net.minecraft.client.model.md3.MD3Model import MD3Model
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.entity.misc.EntityTNTPrimed import EntityTNTPrimed
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl

class RenderMD3:

    def __init__(self):
        ModelBiped()
        self.__model = [None]
        self.__worldObj = None
        self.__renderBlocks = RenderBlocks(tessellator)
        self.__playerViewY = 0.0

        try:
            self.__model[0] = MD3Model((MD3Loader()).loadModel('test2.md3'))
        except IOError as e:
            print(e)

    def setPlayerViewY(self, a):
        player = self.__worldObj.getPlayerEntity()
        self.__playerViewY = player.prevRotationYaw + (player.rotationYaw - player.prevRotationYaw) * a

    def renderShadow(self, entity, renderEngine, a):
        xd = entity.lastTickPosX + (entity.posX - entity.lastTickPosX) * a
        yd = entity.lastTickPosY + (entity.posY - entity.lastTickPosY) * a
        zd = entity.lastTickPosZ + (entity.posZ - entity.lastTickPosZ) * a
        light = self.__worldObj.getBlockLightValue(
            int(xd),
            int(yd + entity.height * 2.0 / 3.0),
            int(zd)
        )
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        if isinstance(entity, EntityLiving):
            gl.glEnable(gl.GL_BLEND)
            renderEngine.setClampTexture(True)
            tex = renderEngine.getTexture('shadow.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            renderEngine.setClampTexture(False)
            gl.glDepthMask(False)

            for xx in range(int(xd - 0.5), int(xd + 0.5 + 1)):
                for yy in range(int(yd - 2.0), int(yd + 1)):
                    for zz in range(int(zd - 0.5), int(zd + 0.5 + 1)):
                        blockId = self.__worldObj.getBlockId(xx, yy - 1, zz)
                        if blockId > 0 and self.__worldObj.isHalfLit(xx, yy, zz):
                            block = blocks.blocksList[blockId]
                            t = tessellator
                            r0 = (1.0 - (yd - yy) / 2.0) * 0.5 * self.__worldObj.getBlockLightValue(xx, yy, zz)
                            if r0 >= 0.0:
                                gl.glColor4f(1.0, 1.0, 1.0, r0)
                                t.startDrawingQuads()
                                r0 = xx + block.minX
                                r1 = xx + block.maxX
                                g = yy + block.minY
                                b0 = zz + block.minZ
                                b1 = zz + block.maxZ
                                u0 = (xd - r0) / 2.0 / 0.5 + 0.5
                                u1 = (xd - r1) / 2.0 / 0.5 + 0.5
                                v0 = (zd - b0) / 2.0 / 0.5 + 0.5
                                v1 = (zd - b1) / 2.0 / 0.5 + 0.5
                                t.addVertexWithUV(r0, g, b0, u0, v0)
                                t.addVertexWithUV(r0, g, b1, u0, v1)
                                t.addVertexWithUV(r1, g, b1, u1, v1)
                                t.addVertexWithUV(r1, g, b0, u1, v0)
                                t.draw()

            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            gl.glDisable(gl.GL_BLEND)
            gl.glDepthMask(True)

        gl.glColor3f(light, light, light)
        self.doRender(entity, renderEngine, xd, yd, zd, 1.0, a)

    def doRender(self, entity, renderEngine, xd, yd, zd, yaw, a):
        if entity.fire > 0:
            gl.glDisable(gl.GL_LIGHTING)
            tex = blocks.fire.blockIndexInTexture
            xt = (tex & 15) << 4
            tex &= 240
            u0 = xt / 256.0
            u1 = (xt + 15.99) / 256.0
            v0 = tex / 256.0
            v1 = (tex + 15.99) / 256.0
            gl.glPushMatrix()
            gl.glTranslatef(xd, yd, zd)
            scale = entity.width * 1.4
            gl.glScalef(scale, scale, scale)
            tex = renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            t = tessellator
            xo = 1.0
            zo = 0.0
            aspect = entity.height / entity.width
            gl.glRotatef(-self.__playerViewY, 0.0, 1.0, 0.0)
            gl.glTranslatef(0.0, 0.0, 0.4 + int(aspect) * 0.02)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            t.startDrawingQuads()

            while aspect > 0.0:
                t.addVertexWithUV(-0.5, 0.0 - zo, 0.0, u0, v1)
                t.addVertexWithUV(xo - 0.5, 0.0 - zo, 0.0, u1, v1)
                t.addVertexWithUV(xo - 0.5, 1.4 - zo, 0.0, u1, v0)
                t.addVertexWithUV(-0.5, 1.4 - zo, 0.0, u0, v0)
                aspect -= 1.0
                zo -= 1.0
                xo *= 0.9
                gl.glTranslatef(0.0, 0.0, -0.04)

            t.draw()
            gl.glPopMatrix()
            gl.glEnable(gl.GL_LIGHTING)

        if isinstance(entity, EntityLiving):
            gl.glPushMatrix()

            try:
                zo = entity.prevRenderYawOffset + (entity.renderYawOffset - entity.prevRenderYawOffset) * a
                zo *= yaw
                gl.glTranslatef(xd, yd, zd)
                tex = renderEngine.getTexture('cube-nes.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                gl.glRotatef(-zo + 180.0, 0.0, 1.0, 0.0)
                gl.glRotatef(-90.0, 1.0, 0.0, 0.0)
                gl.glScalef(0.02, -0.02, 0.02)
                gl.glEnable(gl.GL_NORMALIZE)
                self.__model[0].renderModelVertices()
                gl.glDisable(gl.GL_NORMALIZE)
            except Exception as e:
                print(e)

            gl.glPopMatrix()
        elif isinstance(entity, EntityTNTPrimed):
            gl.glPushMatrix()
            gl.glTranslatef(xd, yd, zd)
            tex = renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            self.__renderBlocks.renderBlockOnInventory(blocks.tnt)
            gl.glPopMatrix()
        elif isinstance(entity, EntityItem):
            stack = entity.item
            gl.glPushMatrix()
            gl.glTranslatef(xd, yd, zd)
            gl.glEnable(gl.GL_NORMALIZE)
            if stack.itemID < 256:
                gl.glPushMatrix()
                gl.glScalef(0.25, 0.25, 0.25)
                tex = renderEngine.getTexture('terrain.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                self.__renderBlocks.renderBlockOnInventory(blocks.blocksList[stack.itemID])
                gl.glPopMatrix()
            else:
                gl.glScalef(0.5, 0.5, 0.5)
                tex = renderEngine.getTexture('gui/items.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                t = tessellator
                iconIndex = stack.getItem().getIconIndex()
                u0 = (iconIndex % 16 << 4) / 256.0
                u1 = ((iconIndex % 16 << 4) + 16) / 256.0
                v0 = (iconIndex // 16 << 4) / 256.0
                v1 = ((iconIndex // 16 << 4) + 16) / 256.0
                gl.glRotatef(-self.__playerViewY, 0.0, 1.0, 0.0)
                t.startDrawingQuads()
                tessellator.setNormal(0.0, 1.0, 0.0)
                t.addVertexWithUV(-0.5, -0.25, 0.0, u0, v1)
                t.addVertexWithUV(0.5, -0.25, 0.0, u1, v1)
                t.addVertexWithUV(0.5, 12.0 / 16.0, 0.0, u1, v0)
                t.addVertexWithUV(-0.5, 12.0 / 16.0, 0.0, u0, v0)
                t.draw()
                t.draw()

            gl.glDisable(gl.GL_NORMALIZE)
            gl.glPopMatrix()

    def changeWorld(self, world):
        self.__worldObj = world

    def setPlayerViewY(self, a):
        p = self.__worldObj.getPlayerEntity()
        self.__playerViewY = p.prevRotationYaw + (p.rotationYaw - p.prevRotationYaw) * a
