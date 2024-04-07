from mc.net.minecraft.client.particle.EntityDiggingFX import EntityDiggingFX
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

    def canPlace(self, x, y, z, block):
        if block > 0:
            block = blocks.blocksList[block]
            if block:
                speed = (block.stepSound.speed + 1.0) / 2.0
                self._mc.sndManager.playSoundAtPos(
                    f'step.{block.stepSound.name}', x + 0.5, y + 0.5, z + 0.5,
                    speed, block.stepSound.pitch * 0.8
                )

        return True

    def sendBlockRemoved(self, x, y, z):
        self._mc.effectRenderer.addBlockDigEffects(x, y, z)

        block = blocks.blocksList[self._mc.theWorld.getBlockId(x, y, z)]
        change = self._mc.theWorld.setBlockWithNotify(x, y, z, 0)
        if block and change:
            speed = (block.stepSound.speed + 1.0) / 2.0
            self._mc.sndManager.playSoundAtPos(
                f'step.{block.stepSound.name}', x + 0.5, y + 0.5, z + 0.5,
                speed, block.stepSound.pitch * 0.8
            )
            block.onBlockDestroyedByPlayer(self._mc.theWorld, x, y, z)

    def hitBlock(self, x, y, z, sideHit):
        pass

    def resetBlockRemoving(self):
        pass

    def setPartialTime(self, damageTime):
        pass

    def getBlockReachDistance(self):
        return 5.0

    def onRespawn(self, player):
        pass

    def onUpdate(self):
        pass

    def createPlayer(self, level):
        pass

    def shouldDrawHUD(self):
        return True

    def flipPlayer(self, player):
        pass
