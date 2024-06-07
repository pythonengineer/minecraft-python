from mc.net.minecraft.client.render.entity.RenderItem import RenderItem
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.RenderHelper import RenderHelper
from pyglet import window, gl

class GuiContainer(GuiScreen):
    __itemRenderer = RenderItem()

    def __init__(self):
        self.__itemStack = None
        self.xSize = 176
        self.ySize = 166
        self._inventorySlots = []

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

        for slot in self._inventorySlots:
            stack = slot.inventory.getStackInSlot(slot.slotIndex)
            self.__itemRenderer.renderItemIntoGUI(
                self._fontRenderer, self._mc.renderEngine, stack,
                slot.xDisplayPosition, slot.yDisplayPosition
            )
            if slot.getIsMouseOverSlot(xm, ym):
                gl.glDisable(gl.GL_LIGHTING)
                gl.glDisable(gl.GL_DEPTH_TEST)
                self._drawGradientRect(slot.xDisplayPosition, slot.yDisplayPosition,
                                       slot.xDisplayPosition + 16, slot.yDisplayPosition + 16,
                                       -2130706433, -2130706433)
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_DEPTH_TEST)

        if self.__itemStack:
            gl.glTranslatef(0.0, 0.0, 32.0)
            self.__itemRenderer.renderItemIntoGUI(
                self._fontRenderer, self._mc.renderEngine, self.__itemStack,
                xm - w - 8, ym - h - 8
            )

        gl.glDisable(gl.GL_NORMALIZE)
        RenderHelper.disableStandardItemLighting()
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self._drawGuiContainerForegroundLayer()
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def _drawGuiContainerForegroundLayer(self):
        pass

    def _drawGuiContainerBackgroundLayer(self):
        pass

    def _mouseClicked(self, xm, ym, button):
        if button != window.mouse.LEFT and button != window.mouse.RIGHT:
            return

        slots = 0
        for slot in self._inventorySlots:
            if slot.getIsMouseOverSlot(xm, ym): break
            slots += 1
            if slot == self._inventorySlots[-1]: slot = None

        if slot:
            stack = slot.inventory.getStackInSlot(slot.slotIndex)
            if not stack and not self.__itemStack:
                return

            if stack and not self.__itemStack:
                size = stack.stackSize if button == window.mouse.LEFT else 1
                self.__itemStack = slot.inventory.decrStackSize(slot.slotIndex, size)
                if stack.stackSize == 0:
                    slot.putStack(None)

                slot.onPickupFromSlot()
            elif not stack and self.__itemStack and slot.isItemValid():
                size = self.__itemStack.stackSize if button == window.mouse.LEFT else 1
                size = min(size, slot.inventory.getInventoryStackLimit())
                slot.putStack(self.__itemStack.splitStack(size))
                if self.__itemStack.stackSize == 0:
                    self.__itemStack = None
            else:
                if not stack or not self.__itemStack or not slot.isItemValid():
                    return

                if stack.itemID != self.__itemStack.itemID:
                    if self.__itemStack.stackSize > slot.inventory.getInventoryStackLimit():
                        return

                    slot.putStack(self.__itemStack)
                    self.__itemStack = stack
                else:
                    if stack.itemID != self.__itemStack.itemID:
                        return

                    if button != window.mouse.LEFT:
                        if button == window.mouse.RIGHT:
                            size = min(1, slot.inventory.getInventoryStackLimit() - stack.stackSize)
                            size = min(size, self.__itemStack.getItem().getItemStackLimit() - stack.stackSize)
                            self.__itemStack.splitStack(size)
                            if self.__itemStack.stackSize == 0:
                                self.__itemStack = None

                            stack.stackSize += size

                        return

                    size = min(self.__itemStack.stackSize,
                               slot.inventory.getInventoryStackLimit() - stack.stackSize)
                    size = min(size, self.__itemStack.getItem().getItemStackLimit() - stack.stackSize)
                    self.__itemStack.splitStack(size)
                    if self.__itemStack.stackSize == 0:
                        self.__itemStack = None

                    stack.stackSize += size
        elif self.__itemStack:
            w = (self.width - self.xSize) // 2
            h = (self.height - self.ySize) // 2
            if xm < w or ym < h or xm >= w + self.xSize or ym >= h + self.xSize:
                if button == window.mouse.LEFT:
                    self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__itemStack)
                    self.__itemStack = None
                elif button == window.mouse.RIGHT:
                    self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__itemStack.splitStack(1))
                    if self.__itemStack.stackSize == 0:
                        self.__itemStack = None

    def _keyTyped(self, key, char, motion):
        if key == window.key.ESCAPE or key == self._mc.options.keyBindInventory.keyCode:
            self._mc.displayGuiScreen(None)

    def onGuiClosed(self):
        if self.__itemStack:
            self._mc.thePlayer.dropPlayerItemWithRandomChoice(self.__itemStack)

    def guiCraftingItemsCheck(self):
        pass
