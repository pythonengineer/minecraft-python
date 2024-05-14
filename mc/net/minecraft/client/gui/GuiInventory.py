from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.Slot import Slot
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import window, gl

class GuiInventory(GuiScreen):

    def __init__(self, inventory=None):
        self.__blockRenderer = RenderBlocks(tessellator)
        self.__selectedItem = None
        self.xSize = 176
        self.ySize = 166
        self._slotsList = []
        self.allowUserInput = True
        if not inventory:
            return

        for armorSlots in range(4):
            self._slotsList.append(Slot(
                    self, inventory, inventory.getSizeInventory() - 1 - armorSlots,
                    8, 8 + armorSlots * 18
                ))

        for rows in range(3):
            for slots in range(9):
                self._slotsList.append(Slot(
                        self, inventory, slots + (rows + 1) * 9,
                        8 + slots * 18, 84 + rows * 18
                    ))

        for slots in range(9):
            self._slotsList.append(Slot(self, inventory, slots, 8 + slots * 18, 142))

    def drawScreen(self, xm, ym):
        self._drawGradientRect(0, 0, self.width, self.height, 1610941696, -1607454624)
        w = (self.width - self.xSize) // 2
        h = (self.height - self.ySize) // 2
        self._drawGuiContainerBackgroundLayer()
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
        self._mc.renderGlobal.renderManager.renderEntityWithPosYaw(
            self._mc.thePlayer, 0.0, 0.0, 0.0, 0.0, 0.0
        )
        gl.glPopMatrix()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_NORMALIZE)

        for i in range(len(self._slotsList)):
            slot = self._slotsList[i]
            self.__drawSlotInventory(slot.inventory, slot.slotIndex,
                                     slot.xDisplayPosition, slot.yDisplayPosition)
            if slot.getIsMouseOverSlot(xm, ym):
                gl.glDisable(gl.GL_LIGHTING)
                gl.glDisable(gl.GL_DEPTH_TEST)
                xPos = slot.xDisplayPosition
                yPos = slot.yDisplayPosition
                self._drawGradientRect(xPos, yPos, xPos + 16, yPos + 16,
                                       -2130706433, -2130706433)
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_DEPTH_TEST)

        if self.__selectedItem:
            gl.glTranslatef(0.0, 0.0, 32.0)
            slot = self.__selectedItem
            self.__selectedItem = None
            self.__drawSlotInventory(slot.inventory, slot.slotIndex,
                                     xm - w - 8, ym - h - 8)
            self.__selectedItem = slot

        gl.glDisable(gl.GL_NORMALIZE)
        RenderHelper.disableStandardItemLighting()
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self._drawGuiContainerForegroundLayer()
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def _drawGuiContainerForegroundLayer(self):
        self._fontRenderer.drawString('PLAYER NAME', 84, 8, 4210752)
        self._fontRenderer.drawString('ATK: 100', 84, 24, 4210752)
        self._fontRenderer.drawString('DEF: 100', 84, 32, 4210752)
        self._fontRenderer.drawString('SPD: 100', 84, 40, 4210752)

    def _drawGuiContainerBackgroundLayer(self):
        tex = self._mc.renderEngine.getTexture('gui/inventory.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        w = (self.width - self.xSize) // 2
        h = (self.height - self.ySize) // 2
        self.drawTexturedModalRect(w, h, 0, 0, self.xSize, self.ySize)

    def __drawSlotInventory(self, inventory, slotIndex, xPos, yPos):
        item = inventory.getStackInSlot(slotIndex)
        if not item or self.__selectedItem and \
           self.__selectedItem.slotIndex == slotIndex and \
           self.__selectedItem.inventory == inventory:
            if slotIndex > 50:
                gl.glDisable(gl.GL_LIGHTING)
                tex = self._mc.renderEngine.getTexture('gui/items.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                self.drawTexturedModalRect(
                    xPos, yPos, 240, 63 - slotIndex << 4, 16, 16
                )
                gl.glEnable(gl.GL_LIGHTING)

            return

        if item.itemID < 256:
            tex = self._mc.renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            block = blocks.blocksList[item.itemID]
            gl.glPushMatrix()
            gl.glTranslatef(xPos - 2, yPos + 3, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(210.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            self.__blockRenderer.renderBlockOnInventory(block)
            gl.glPopMatrix()
        elif item.getItem().getIconIndex() >= 0:
            gl.glDisable(gl.GL_LIGHTING)
            tex = self._mc.renderEngine.getTexture('gui/items.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            self.drawTexturedModalRect(
                xPos, yPos, item.getItem().getIconIndex() % 16 << 4,
                item.getItem().getIconIndex() // 16 << 4, 16, 16
            )
            gl.glEnable(gl.GL_LIGHTING)

        if item.stackSize > 1:
            size = '' + str(item.stackSize)
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_DEPTH_TEST)
            self._fontRenderer.drawStringWithShadow(
                size, xPos + 19 - 2 - self._fontRenderer.getStringWidth(size),
                yPos + 6 + 3, 16777215
            )
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_DEPTH_TEST)

    def _mouseClicked(self, xm, ym, button):
        if button == window.mouse.LEFT:
            slots = 0
            slot = None
            while True:
                if slots >= len(self._slotsList):
                    slot = None
                    break

                maybeSlot = self._slotsList[slots]
                if maybeSlot.getIsMouseOverSlot(xm, ym):
                    slot = maybeSlot
                    break

                slots += 1

            if slot:
                if slot == self.__selectedItem:
                    self.__selectedItem = None
                    return

                if slot.inventory.getStackInSlot(slot.slotIndex):
                    if not self.__selectedItem:
                        self.__selectedItem = slot
                        return

                    self.__selectedItem.putStacks(slot)
                    return

                if self.__selectedItem:
                    self.__selectedItem.putStacks(slot)
                    self.__selectedItem = None
            elif self.__selectedItem:
                w = (self.width - self.xSize) // 2
                h = (self.height - self.ySize) // 2
                if xm < w or ym < h or xm >= w + self.xSize or ym >= h + self.xSize:
                    stack = self.__selectedItem.inventory.decrStackSize(
                        self.__selectedItem.slotIndex, 1
                    )
                    self._mc.thePlayer.dropPlayerItemWithRandomChoice(stack)

    def _keyTyped(self, key, char, motion):
        if key == window.key.ESCAPE or key == self._mc.options.keyBindInventory.keyCode:
            self._mc.displayGuiScreen(None)
