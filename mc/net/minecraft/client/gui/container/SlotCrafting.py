from mc.net.minecraft.client.gui.container.Slot import Slot

class SlotCrafting(Slot):

    def __init__(self, guiHandler, inventory, craftResult, slotIndex, xPos, yPos):
        super().__init__(guiHandler, craftResult, 0, xPos, yPos)
        self.__craftMatrix = inventory

    def isItemValid(self):
        return False

    def onPickupFromSlot(self):
        for slot in range(self.__craftMatrix.getSizeInventory()):
            if self.__craftMatrix.getStackInSlot(slot):
                self.__craftMatrix.decrStackSize(slot, 1)
