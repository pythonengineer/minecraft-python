from mc.net.minecraft.client.player.EntityPlayerInput import EntityPlayerInput
from mc.net.minecraft.client.effect.EntityPickupFX import EntityPickupFX
from mc.net.minecraft.client.gui.container.GuiCrafting import GuiCrafting
from mc.net.minecraft.client.gui.container.GuiChest import GuiChest
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.game.item.ItemStack import ItemStack
from nbtlib.tag import Compound, List, Byte, Int

class EntityPlayerSP(EntityPlayer):

    def __init__(self, mc, world):
        super().__init__(world)
        self.__mc = mc
        self.movementInput = None
        self._entityAI = EntityPlayerInput(self)

    def onLivingUpdate(self):
        self.movementInput.updatePlayerMoveState()
        super().onLivingUpdate()

    def _writeEntityToNBT(self, compound):
        compound['Score'] = Int(self._getScore)
        invList = List[Compound]()
        for slot in range(len(self.inventory.mainInventory)):
            if self.inventory.mainInventory[slot]:
                comp = Compound({'Slot': Byte(slot)})
                self.inventory.mainInventory[slot].writeToNBT(comp)
                invList.append(comp)

        compound['Inventory'] = invList

    def _readEntityFromNBT(self, compound):
        self._getScore = compound['Score'].real
        invList = compound['Inventory']
        self.inventory.mainInventory = [None] * self.inventory.getSizeInventory()
        for comp in invList:
            slot = comp['Slot'].real & 255
            if slot >= 0 and slot < len(self.inventory.mainInventory):
                self.inventory.mainInventory[slot] = ItemStack(comp)

    def _getEntityString(self):
        return 'LocalPlayer'

    def displayGUIChest(self, inventory):
        self.__mc.displayGuiScreen(GuiChest(self.inventory, inventory))

    def displayWorkbenchGUI(self):
        self.__mc.displayGuiScreen(GuiCrafting(self.inventory))

    def displayGUIInventory(self):
        self.inventory.setInventorySlotContents(self.inventory.currentItem, None)

    def onItemPickup(self, item):
        self.__mc.effectRenderer.addEffect(EntityPickupFX(self.__mc.theWorld, item,
                                                          self, -0.5))
