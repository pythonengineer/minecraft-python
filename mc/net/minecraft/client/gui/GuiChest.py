from mc.net.minecraft.client.gui.GuiInventory import GuiInventory
from mc.net.minecraft.client.gui.Slot import Slot
from pyglet import gl

class GuiChest(GuiInventory):

    def __init__(self, upperChestInventory, lowerChestInventory):
        super().__init__(None)
        self.__upperChestInventory = upperChestInventory
        self.__lowerChestInventory = lowerChestInventory
        self.__inventoryRows = lowerChestInventory.getSizeInventory() // 9
        self.ySize = 114 + self.__inventoryRows * 18
        yOffset = (self.__inventoryRows - 4) * 18
        for row in range(self.__inventoryRows):
            for col in range(9):
                self._slotsList.append(Slot(self, lowerChestInventory, col + row * 9,
                                            8 + col * 18, 18 + row * 18))

        for row in range(3):
            for col in range(9):
                self._slotsList.append(Slot(self, upperChestInventory, col + (row + 1) * 9,
                                            8 + col * 18, 103 + row * 18 + yOffset))

        for row in range(9):
            self._slotsList.append(Slot(self, upperChestInventory, row,
                                        8 + row * 18, yOffset + 161))

    def _drawStrings(self):
        self._fontRenderer.drawString(self.__lowerChestInventory.getInvName(),
                                      8, 6, 4210752)
        self._fontRenderer.drawString(self.__upperChestInventory.getInvName(),
                                      8, self.ySize - 96 + 2, 4210752)

    def _drawRows(self):
        tex = self._mc.renderEngine.getTexture('gui/container.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        x = (self.width - self.xSize) // 2
        y = (self.height - self.ySize) // 2
        self.drawTexturedModalRect(x, y, 0, 0, self.xSize,
                                   self.__inventoryRows * 18 + 17)
        self.drawTexturedModalRect(x, y + self.__inventoryRows * 18 + 17, 0,
                                   126, self.xSize, 96)
