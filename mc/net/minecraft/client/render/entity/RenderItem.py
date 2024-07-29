from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils import Random
from pyglet import gl

import math

class RenderItem(Render):

    def __init__(self):
        super().__init__()
        self.__renderBlocks = RenderBlocks(tessellator)
        self.__random = Random()

    def renderItemIntoGUI(self, renderEngine, stack, width, height):
        if not stack:
            return

        if stack.itemID < 256 and blocks.blocksList[stack.itemID].getRenderType() == 0:
            tex = renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            block = blocks.blocksList[stack.itemID]
            gl.glPushMatrix()
            gl.glTranslatef(width - 2, height + 3, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(210.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            self.__renderBlocks.renderBlockOnInventory(block)
            gl.glPopMatrix()
        elif stack.getItem().getIconIndex() >= 0:
            gl.glDisable(gl.GL_LIGHTING)
            if stack.itemID < 256:
                tex = renderEngine.getTexture('terrain.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            else:
                tex = renderEngine.getTexture('gui/items.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)

            u = stack.getItem().getIconIndex() % 16 << 4
            v = stack.getItem().getIconIndex() // 16 << 4
            t = tessellator
            t.startDrawingQuads()
            t.addVertexWithUV(width, height + 16, 0.0, u * 0.00390625, (v + 16) * 0.00390625)
            t.addVertexWithUV(width + 16, height + 16, 0.0, (u + 16) * 0.00390625, (v + 16) * 0.00390625)
            t.addVertexWithUV(width + 16, height, 0.0, (u + 16) * 0.00390625, v * 0.00390625)
            t.addVertexWithUV(width, height, 0.0, u * 0.00390625, v * 0.00390625)
            t.draw()
            gl.glEnable(gl.GL_LIGHTING)

    def renderItemDamage(self, fontRenderer, stack, width, height):
        if not stack:
            return

        if stack.stackSize > 1:
            size = str(stack.stackSize)
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_DEPTH_TEST)
            fontRenderer.drawStringWithShadow(
                size, width + 19 - 2 - fontRenderer.getStringWidth(size),
                height + 6 + 3, 16777215)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_DEPTH_TEST)
        if stack.itemDamage > 0:
            x = 13 - stack.itemDamage * 13 // stack.isItemStackDamageable()
            z1 = 255 - stack.itemDamage * 255 // stack.isItemStackDamageable()
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_DEPTH_TEST)
            gl.glDisable(gl.GL_TEXTURE_2D)
            t = tessellator
            z0 = 255 - z1 << 16 | z1 << 8
            z1 = (255 - z1) // 4 << 16 | 16128
            self.__drawToolDamage(t, width + 2, height + 13, 13, 2, 0)
            self.__drawToolDamage(t, width + 2, height + 13, 12, 1, z1)
            self.__drawToolDamage(t, width + 2, height + 13, x, 1, z0)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glEnable(gl.GL_TEXTURE_2D)

    @staticmethod
    def __drawToolDamage(t, width, height, x, y, z):
        t.startDrawingQuads()
        t.setColorOpaque_I(z)
        t.addVertex(width, height, 0.0)
        t.addVertex(width, height + y, 0.0)
        t.addVertex(width + x, height + y, 0.0)
        t.addVertex(width + x, height, 0.0)
        t.draw()

    def doRender(self, entity, xd, yd, zd, yaw, a):
        self.__random.setSeed(187)
        item = entity.item
        gl.glPushMatrix()
        hoverY = math.sin((entity.age + a) / 10.0 + entity.hoverStart) * 0.1 + 0.1
        rot = ((entity.age + a) / 20.0 + entity.hoverStart) * (180.0 / math.pi)
        renders = 1
        if entity.item.stackSize > 1:
            renders = 2
        if entity.item.stackSize > 5:
            renders = 3
        if entity.item.stackSize > 20:
            renders = 4

        gl.glTranslatef(xd, yd + hoverY, zd)
        gl.glEnable(gl.GL_NORMALIZE)
        if item.itemID < 256 and blocks.blocksList[item.itemID].getRenderType() == 0:
            gl.glRotatef(rot, 0.0, 1.0, 0.0)
            self._loadTexture('terrain.png')
            scale = 0.25
            if not blocks.blocksList[item.itemID].renderAsNormalBlock() and \
               item.itemID != blocks.stairSingle.blockID:
                scale = 0.5

            gl.glScalef(scale, scale, scale)

            for i in range(renders):
                gl.glPushMatrix()
                if i > 0:
                    x = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    y = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    z = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    gl.glTranslatef(x, y, z)

                self.__renderBlocks.renderBlockOnInventory(blocks.blocksList[item.itemID])
                gl.glPopMatrix()
        else:
            gl.glScalef(0.5, 0.5, 0.5)
            iconIndex = item.getItem().getIconIndex()
            if item.itemID < 256:
                self._loadTexture('terrain.png')
            else:
                self._loadTexture('gui/items.png')
            t = tessellator
            u0 = (iconIndex % 16 << 4) / 256.0
            u1 = ((iconIndex % 16 << 4) + 16) / 256.0
            v0 = (iconIndex // 16 << 4) / 256.0
            v1 = ((iconIndex // 16 << 4) + 16) / 256.0

            for i in range(renders):
                gl.glPushMatrix()
                if i > 0:
                    x = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                    y = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                    z = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                    gl.glTranslatef(x, y, z)

                gl.glRotatef(-self._renderManager.playerViewY, 0.0, 1.0, 0.0)
                t.startDrawingQuads()
                t.setNormal(0.0, 1.0, 0.0)
                t.addVertexWithUV(-0.5, -0.25, 0.0, u0, v1)
                t.addVertexWithUV(0.5, -0.25, 0.0, u1, v1)
                t.addVertexWithUV(0.5, 12.0 / 16.0, 0.0, u1, v0)
                t.addVertexWithUV(-0.5, 12.0 / 16.0, 0.0, u0, v0)
                t.draw()
                gl.glPopMatrix()

        gl.glDisable(gl.GL_NORMALIZE)
        gl.glPopMatrix()
