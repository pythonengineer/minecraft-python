from mc.net.minecraft.client.effect.EntityDiggingFX import EntityDiggingFX
from mc.net.minecraft.game.level.block.Blocks import blocks

class PlayerController:

    def __init__(self, mc):
        self._mc = mc
        self.isInTestMode = False

    def onWorldChange(self, world):
        world.multiplayerWorld = True

    def displayInventoryGUI(self):
        pass

    def clickBlock(self, x, y, z):
        self.sendBlockRemoved(x, y, z)

    def canPlace(self, block):
        return True

    def sendBlockRemoved(self, x, y, z):
        blockId = self._mc.theWorld.getBlockId(x, y, z)
        if blockId:
            block = blocks.blocksList[blockId]

            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        xx = x + (i + 0.5) / 4
                        yy = y + (j + 0.5) / 4
                        zz = z + (k + 0.5) / 4
                        self._mc.effectRenderer.addEffect(
                            EntityDiggingFX(self._mc.effectRenderer.worldObj,
                                            xx, yy, zz, xx - x - 0.5, yy - y - 0.5,
                                            zz - z - 0.5, block)
                        )

        block = blocks.blocksList[self._mc.theWorld.getBlockId(x, y, z)]
        change = self._mc.theWorld.setBlockWithNotify(x, y, z, 0)
        if block and change:
            block.onBlockDestroyedByPlayer(self._mc.theWorld, x, y, z)

    def sendBlockRemoving(self, x, y, z, sideHit):
        pass

    def resetBlockRemoving(self):
        pass

    def setPartialTime(self, damageTime):
        pass

    def getBlockReachDistance(self):
        return 5.0

    def sendUseItem(self, player, quantity):
        return False

    def preparePlayer(self, player):
        pass

    def onUpdate(self):
        pass

    def createPlayer(self, level):
        pass

    def shouldDrawHUD(self):
        return True

    def flipPlayer(self, player):
        pass
