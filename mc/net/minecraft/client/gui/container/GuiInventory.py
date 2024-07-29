from mc.net.minecraft.client.gui.container.InventoryCraftResult import InventoryCraftResult
from mc.net.minecraft.client.gui.container.InventoryCrafting import InventoryCrafting
from mc.net.minecraft.client.gui.container.GuiContainer import GuiContainer
from mc.net.minecraft.client.gui.container.Slot import Slot
from mc.net.minecraft.client.gui.container.SlotCrafting import SlotCrafting
from mc.net.minecraft.game.item.recipe.CraftingManager import CraftingManager
from pyglet import gl

class GuiInventory(GuiContainer):

    def __init__(self, inventory):
        super().__init__()
        self.__inventoryCrafting = InventoryCrafting(self, 2, 2)
        self.__craftResult = InventoryCraftResult()

        self.allowUserInput = True

        self._inventorySlots.append(SlotCrafting(
                self, self.__inventoryCrafting, self.__craftResult, 0, 144, 36
            ))
        for row in range(2):
            for col in range(2):
                self._inventorySlots.append(Slot(
                        self, self.__inventoryCrafting, col + (row << 1),
                        88 + col * 18, 26 + row * 18
                    ))

        for armorSlots in range(4):
            self._inventorySlots.append(Slot(
                    self, inventory, inventory.getSizeInventory() - 1 - armorSlots,
                    8, 8 + armorSlots * 18
                ))

        for row in range(3):
            for col in range(9):
                self._inventorySlots.append(Slot(
                        self, inventory, col + (row + 1) * 9,
                        8 + col * 18, 84 + row * 18
                    ))

        for barSlots in range(9):
            self._inventorySlots.append(Slot(self, inventory, barSlots,
                                             8 + barSlots * 18, 142))

    def onGuiClosed(self):
        super().onGuiClosed()
        for i in range(self.__inventoryCrafting.getSizeInventory()):
            stack = self.__inventoryCrafting.getStackInSlot(i)
            if stack:
                self.mc.thePlayer.dropPlayerItemWithRandomChoice(stack)

    def guiCraftingItemsCheck(self):
        items = [0] * 9
        for row in range(3):
            for col in range(3):
                slot = -1
                if row < 2 and col < 2:
                    stack = self.__inventoryCrafting.getStackInSlot(row + (col << 1))
                    if stack:
                        slot = stack.itemID

                items[row + col * 3] = slot

        self.__craftResult.setInventorySlotContents(
            0, CraftingManager.getInstance().findMatchingRecipe(items)
        )

    def _drawGuiContainerForegroundLayer(self):
        self._fontRenderer.drawString('Crafting', 86, 16, 4210752)

    def _drawGuiContainerBackgroundLayer(self):
        tex = self.mc.renderEngine.getTexture('gui/inventory.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        w = (self.width - self.xSize) // 2
        h = (self.height - self.ySize) // 2
        self.drawTexturedModalRect(w, h, 0, 0, self.xSize, self.ySize)
