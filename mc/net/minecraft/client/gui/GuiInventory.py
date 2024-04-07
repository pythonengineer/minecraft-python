from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.Slot import Slot
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import window, gl

class GuiInventory(GuiScreen):

    def __init__(self):
        self.__blockRenderer = RenderBlocks(tessellator)
        self.__selectedItem = -1
        self.__inventorySlots = []
        self.allowUserInput = True

        for armorSlots in range(4):
            self.__inventorySlots.append(Slot(self, 63 - armorSlots, 8, 8 + armorSlots * 18))

        for rows in range(3):
            for slots in range(9):
                self.__inventorySlots.append(Slot(
                        self, slots + (rows + 1) * 9, 8 + slots * 18, 84 + rows * 18
                    ))

        for slots in range(9):
            self.__inventorySlots.append(Slot(self, slots, 8 + slots * 18, 142))

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        tex = self._mc.renderEngine.getTexture('gui/inventory.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        w = (self.width - 176) // 2
        h = (self.height - 184) // 2
        self.drawTexturedModalRect(w, h, 0, 0, 176, 184)
        gl.glPushMatrix()
        gl.glRotatef(180.0, 1.0, 0.0, 0.0)
        RenderHelper.enableStandardItemLighting()
        gl.glPopMatrix()
        gl.glPushMatrix()
        gl.glTranslatef(w, h, 0.0)
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glPushMatrix()
        gl.glTranslatef(52.0, 73.0, 24.0)
        gl.glScalef(24.0, -24.0, 24.0)
        gl.glRotatef(10.0, 0.0, 1.0, 0.0)
        gl.glRotatef(10.0, 1.0, 0.0, 0.0)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        self._mc.renderGlobal.renderManager.doRender(
            self._mc.thePlayer, self._mc.renderEngine, 0.0, 0.0, 0.0, 0.0, 0.0
        )
        gl.glPopMatrix()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_NORMALIZE)

        for i in range(len(self.__inventorySlots)):
            slot = self.__inventorySlots[i]
            self.__drawSlotInventory(slot.slotIndex, slot.xDisplayPosition,
                                     slot.yDisplayPosition)
            if slot.getIsMouseOverSlot(xm, ym):
                gl.glDisable(gl.GL_LIGHTING)
                gl.glDisable(gl.GL_DEPTH_TEST)
                xPos = slot.xDisplayPosition
                yPos = slot.yDisplayPosition
                self._drawGradientRect(xPos, yPos, xPos + 16, yPos + 16,
                                       -2130706433, -2130706433)
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_DEPTH_TEST)

        if self.__selectedItem >= 0:
            gl.glTranslatef(0.0, 0.0, 32.0)
            item = self.__selectedItem
            self.__selectedItem = -1
            self.__drawSlotInventory(item, xm - w - 8, ym - h - 8)
            self.__selectedItem = item

        gl.glDisable(gl.GL_NORMALIZE)
        RenderHelper.disableStandardItemLighting()
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self._font.drawString('PLAYER NAME', 84, 8, 4210752)
        self._font.drawString('ATK: 100', 84, 24, 4210752)
        self._font.drawString('DEF: 100', 84, 32, 4210752)
        self._font.drawString('SPD: 100', 84, 40, 4210752)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def __drawSlotInventory(self, slotIndex, xPos, yPos):
        item = self._mc.thePlayer.inventory.mainInventory[slotIndex]
        if item and self.__selectedItem != slotIndex:
            slotIndex = item.itemID
            if slotIndex > 0:
                tex = self._mc.renderEngine.getTexture('terrain.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                block = blocks.blocksList[slotIndex]
                gl.glPushMatrix()
                gl.glTranslatef(xPos - 2, yPos + 3, 0.0)
                gl.glScalef(10.0, 10.0, 10.0)
                gl.glTranslatef(1.0, 0.5, 8.0)
                gl.glRotatef(210.0, 1.0, 0.0, 0.0)
                gl.glRotatef(45.0, 0.0, 1.0, 0.0)
                gl.glColor4f(1.0, 1.0, 1.0, 1.0)
                self.__blockRenderer.renderBlockOnInventory(block)
                gl.glPopMatrix()
            elif item.iconIndex >= 0:
                gl.glDisable(gl.GL_LIGHTING)
                tex = self._mc.renderEngine.getTexture('gui/items.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                self.drawTexturedModalRect(xPos, yPos, item.iconIndex % 16 << 4,
                                       item.iconIndex // 16 << 4, 16, 16)
                gl.glEnable(gl.GL_LIGHTING)

            if item.stackSize > 1:
                size = '' + str(item.stackSize)
                gl.glDisable(gl.GL_LIGHTING)
                gl.glDisable(gl.GL_DEPTH_TEST)
                self._font.drawStringWithShadow(
                    size, xPos + 19 - 2 - self._font.getStringWidth(size),
                    yPos + 6 + 3, 16777215
                )
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_DEPTH_TEST)
        elif slotIndex > 50:
            gl.glDisable(gl.GL_LIGHTING)
            tex = self._mc.renderEngine.getTexture('gui/items.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            self.drawTexturedModalRect(xPos, yPos, 240, 63 - slotIndex << 4, 16, 16)
            gl.glEnable(gl.GL_LIGHTING)

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            slots = 0
            slot = None
            while True:
                if slots >= len(self.__inventorySlots):
                    slot = None
                    break

                maybeSlot = self.__inventorySlots[slots]
                if maybeSlot.getIsMouseOverSlot(xm, ym):
                    slot = maybeSlot
                    break

                slots += 1

            if slot:
                if slot.slotIndex == self.__selectedItem:
                    self.__selectedItem = -1
                    return

                if self._mc.thePlayer.inventory.mainInventory[slot.slotIndex]:
                    if self.__selectedItem < 0:
                        self.__selectedItem = slot.slotIndex
                        return

                    self._mc.thePlayer.inventory.setInventorySlotContents(self.__selectedItem, slot.slotIndex)
                    return

                if self.__selectedItem >= 0:
                    self._mc.thePlayer.inventory.setInventorySlotContents(self.__selectedItem, slot.slotIndex)
                    self.__selectedItem = -1
            elif self.__selectedItem > 0:
                w = (self.width - 176) // 2
                h = (self.height - 184) // 2
                if xm < w or ym < h or xm >= w + 176 or ym >= h + 176:
                    self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__selectedItem)

    def _keyTyped(self, key, char, motion):
        if key == window.key.ESCAPE or key == self._mc.options.keyBindInventory.keyCode:
            self._mc.displayGuiScreen(None)
