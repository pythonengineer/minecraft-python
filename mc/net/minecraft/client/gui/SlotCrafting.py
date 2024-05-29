from mc.net.minecraft.client.gui.Slot import Slot

class SlotCrafting(Slot):

    def __init__(self, guiHandler, inventory, slotIndex, xPos, yPos):
        super().__init__(guiHandler, inventory, 0, 124, 34)
        self.__craftMatrix = guiHandler

    def isItemValid(self):
        return False

    def onPickupFromSlot(self):
        for slot in range(9):
            if self.__craftMatrix.inventoryCrafting.getStackInSlot(slot):
                self.__craftMatrix.inventoryCrafting.decrStackSize(slot, 1)
