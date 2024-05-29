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
        if not inventory:
            return

        self.allowUserInput = True

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
            self.__drawSlotInventory(slot.inventory.getStackInSlot(slot.slotIndex),
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
            self.__drawSlotInventory(self.__selectedItem,
                                     xm - w - 8, ym - h - 8)

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

    def __drawSlotInventory(self, stack, xPos, yPos):
        if not stack:
            return

        if stack.itemID < 256:
            tex = self._mc.renderEngine.getTexture('terrain.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            block = blocks.blocksList[stack.itemID]
            gl.glPushMatrix()
            gl.glTranslatef(xPos - 2, yPos + 3, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(210.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            self.__blockRenderer.renderBlockOnInventory(block)
            gl.glPopMatrix()
        elif stack.getItem().getIconIndex() >= 0:
            gl.glDisable(gl.GL_LIGHTING)
            tex = self._mc.renderEngine.getTexture('gui/items.png')
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
            self.drawTexturedModalRect(
                xPos, yPos, stack.getItem().getIconIndex() % 16 << 4,
                stack.getItem().getIconIndex() // 16 << 4, 16, 16
            )
            gl.glEnable(gl.GL_LIGHTING)

        if stack.stackSize > 1:
            size = '' + str(stack.stackSize)
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_DEPTH_TEST)
            self._fontRenderer.drawStringWithShadow(
                size, xPos + 19 - 2 - self._fontRenderer.getStringWidth(size),
                yPos + 6 + 3, 16777215
            )
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_DEPTH_TEST)

    def _mouseClicked(self, xm, ym, button):
        if button != window.mouse.LEFT and button != window.mouse.RIGHT:
            return

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
            stack = slot.getCurrentItemStack()
            if not stack and not self.__selectedItem:
                return

            if stack and not self.__selectedItem:
                size = stack.stackSize if button == window.mouse.LEFT else 1
                self.__selectedItem = stack.splitStack(size)
                if stack.stackSize == 0:
                    slot.putStack(None)

                slot.onPickupFromSlot()
            elif not stack and self.__selectedItem and slot.isItemValid():
                size = self.__selectedItem.stackSize if button == window.mouse.LEFT else 1
                size = min(size, slot.inventory.getInventoryStackLimit())
                slot.putStack(self.__selectedItem.splitStack(size))
                if self.__selectedItem.stackSize == 0:
                    self.__selectedItem = None
            else:
                if not stack or not self.__selectedItem or not slot.isItemValid():
                    return

                if stack.itemID != self.__selectedItem.itemID:
                    if self.__selectedItem.stackSize > slot.inventory.getInventoryStackLimit():
                        return

                    slot.putStack(self.__selectedItem)
                    self.__selectedItem = stack
                else:
                    if stack.itemID != self.__selectedItem.itemID:
                        return

                    if button != window.mouse.LEFT:
                        if button == window.mouse.RIGHT:
                            size = min(1, slot.inventory.getInventoryStackLimit() - stack.stackSize)
                            size = min(size, self.__selectedItem.getItem().getItemStackLimit() - stack.stackSize)
                            self.__selectedItem.splitStack(size)
                            if self.__selectedItem.stackSize == 0:
                                self.__selectedItem = None

                            stack.stackSize += size

                        return

                    size = min(self.__selectedItem.stackSize,
                               slot.inventory.getInventoryStackLimit() - stack.stackSize)
                    size = min(size, self.__selectedItem.getItem().getItemStackLimit() - stack.stackSize)
                    self.__selectedItem.splitStack(size)
                    if self.__selectedItem.stackSize == 0:
                        self.__selectedItem = None

                    stack.stackSize += size
        elif self.__selectedItem:
            w = (self.width - self.xSize) // 2
            h = (self.height - self.ySize) // 2
            if xm < w or ym < h or xm >= w + self.xSize or ym >= h + self.xSize:
                if button == window.mouse.LEFT:
                    self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__selectedItem)
                    self.__selectedItem = None
                elif button == window.mouse.RIGHT:
                    self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__selectedItem.splitStack(1))
                    if self.__selectedItem.stackSize == 0:
                        self.__selectedItem = None

    def _keyTyped(self, key, char, motion):
        if key == window.key.ESCAPE or key == self._mc.options.keyBindInventory.keyCode:
            self._mc.displayGuiScreen(None)

    def onGuiClosed(self):
        if self.__selectedItem:
            self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__selectedItem)
