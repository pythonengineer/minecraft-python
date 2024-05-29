from mc.net.minecraft.game.item.recipe.CraftingManager import CraftingManager
from mc.net.minecraft.client.gui.InventoryCraftResult import InventoryCraftResult
from mc.net.minecraft.client.gui.InventoryCrafting import InventoryCrafting
from mc.net.minecraft.client.gui.GuiInventory import GuiInventory
from mc.net.minecraft.client.gui.SlotCrafting import SlotCrafting
from mc.net.minecraft.client.gui.Slot import Slot
from pyglet import gl

class GuiCrafting(GuiInventory):

    def __init__(self, player):
        super().__init__(None)
        self.inventoryCrafting = InventoryCrafting(self)
        self.__iInventory = InventoryCraftResult(self)
        self._slotsList.append(SlotCrafting(self, self.__iInventory, 0, 124, 34))
        for row in range(3):
            for col in range(3):
                self._slotsList.append(Slot(self, self.inventoryCrafting, col + row * 3,
                                            30 + col * 18, 16 + row * 18))

        for row in range(3):
            for col in range(9):
                self._slotsList.append(Slot(self, player, col + (row + 1) * 9,
                                            8 + col * 18, 84 + row * 18))

        for row in range(9):
            self._slotsList.append(Slot(self, player, row, 8 + row * 18, 142))

    def onGuiClosed(self):
        super().onGuiClosed()
        for slot in range(9):
            stack = self.inventoryCrafting.getStackInSlot(slot)
            if stack:
                self._mc.thePlayer.dropPlayerItemWithRandomChoice(stack)

    def onCraftMatrixChanged(self):
        items = [0] * 9
        for slot in range(9):
            stack = self.inventoryCrafting.stackList[slot]
            if stack:
                items[slot] = stack.itemID
            else:
                items[slot] = -1

        self.__iInventory.setInventorySlotContents(0, CraftingManager.addRecipe(items))

    def _drawGuiContainerForegroundLayer(self):
        self._fontRenderer.drawString('Crafting', 8, 6, 4210752)
        self._fontRenderer.drawString('Inventory', 8, self.ySize - 96 + 2, 4210752)

    def _drawGuiContainerBackgroundLayer(self):
        tex = self._mc.renderEngine.getTexture('gui/crafting.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        x = (self.width - self.xSize) // 2
        y = (self.height - self.ySize) // 2
        self.drawTexturedModalRect(x, y, 0, 0, self.xSize, self.ySize)
