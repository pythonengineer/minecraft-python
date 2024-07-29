from mc.net.minecraft.game.item.recipe.CraftingManager import CraftingManager
from mc.net.minecraft.client.gui.container.InventoryCraftResult import InventoryCraftResult
from mc.net.minecraft.client.gui.container.InventoryCrafting import InventoryCrafting
from mc.net.minecraft.client.gui.container.GuiContainer import GuiContainer
from mc.net.minecraft.client.gui.container.SlotCrafting import SlotCrafting
from mc.net.minecraft.client.gui.container.Slot import Slot
from pyglet import gl

class GuiCrafting(GuiContainer):

    def __init__(self, player):
        super().__init__()
        self.__inventoryCrafting = InventoryCrafting(self, 3, 3)
        self.__iInventory = InventoryCraftResult()
        self._inventorySlots.append(SlotCrafting(
                self, self.__inventoryCrafting, self.__iInventory, 0, 124, 35
            ))
        for row in range(3):
            for col in range(3):
                self._inventorySlots.append(Slot(self, self.__inventoryCrafting, col + row * 3,
                                            30 + col * 18, 17 + row * 18))

        for row in range(3):
            for col in range(9):
                self._inventorySlots.append(Slot(self, player, col + (row + 1) * 9,
                                            8 + col * 18, 84 + row * 18))

        for row in range(9):
            self._inventorySlots.append(Slot(self, player, row, 8 + row * 18, 142))

    def onGuiClosed(self):
        super().onGuiClosed()
        for slot in range(9):
            stack = self.__inventoryCrafting.getStackInSlot(slot)
            if stack:
                self.mc.thePlayer.dropPlayerItemWithRandomChoice(stack)

    def guiCraftingItemsCheck(self):
        items = [0] * 9
        for row in range(3):
            for col in range(3):
                slot = row + col * 3
                stack = self.__inventoryCrafting.getStackInSlot(slot)
                if stack:
                    items[slot] = stack.itemID
                else:
                    items[slot] = -1

        self.__iInventory.setInventorySlotContents(0, CraftingManager.getInstance().findMatchingRecipe(items))

    def _drawGuiContainerForegroundLayer(self):
        self._fontRenderer.drawString('Crafting', 28, 6, 4210752)
        self._fontRenderer.drawString('Inventory', 8, self.ySize - 96 + 2, 4210752)

    def _drawGuiContainerBackgroundLayer(self):
        tex = self.mc.renderEngine.getTexture('gui/crafting.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        x = (self.width - self.xSize) // 2
        y = (self.height - self.ySize) // 2
        self.drawTexturedModalRect(x, y, 0, 0, self.xSize, self.ySize)
