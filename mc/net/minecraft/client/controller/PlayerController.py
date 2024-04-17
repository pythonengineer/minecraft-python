from mc.net.minecraft.client.effect.EntityDiggingFX import EntityDiggingFX
from mc.net.minecraft.game.level.block.Blocks import blocks

class PlayerController:

    def __init__(self, mc):
        self._mc = mc
        self.isInTestMode = False

    def onWorldChange(self, world):
        pass

    def openInventory(self):
        pass

    def clickBlock(self, x, y, z):
        self.sendBlockRemoved(x, y, z)

    def sendBlockRemoved(self, x, y, z):
        self._mc.effectRenderer.addBlockDestroyEffects(x, y, z)
        block = blocks.blocksList[self._mc.theWorld.getBlockId(x, y, z)]
        change = self._mc.theWorld.setBlockWithNotify(x, y, z, 0)
        if block and change:
            speed = (block.stepSound.soundVolume + 1.0) / 2.0
            self._mc.sndManager.playSound(
                f'step.{block.stepSound.soundDir}', x + 0.5, y + 0.5, z + 0.5,
                speed, block.stepSound.soundPitch * 0.8
            )
            block.onBlockDestroyedByPlayer(self._mc.theWorld, x, y, z)

        return change

    def sendBlockRemoving(self, x, y, z, sideHit):
        pass

    def resetBlockRemoving(self):
        pass

    def setPartialTime(self, damageTime):
        pass

    def getBlockReachDistance(self):
        return 5.0

    def flipPlayer(self, player):
        pass

    def onUpdate(self):
        pass

    def createPlayer(self, level):
        pass

    def shouldDrawHUD(self):
        return True

    def flipPlayer(self, player):
        pass
