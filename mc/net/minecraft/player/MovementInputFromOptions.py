from mc.net.minecraft.player.MovementInput import MovementInput
from pyglet import window

class MovementInputFromOptions(MovementInput):
    __keys = [False] * 10

    def setKey(self, symbol, state):
        id_ = -1
        if symbol in (window.key.UP, window.key.W): id_ = 0
        if symbol in (window.key.DOWN, window.key.S): id_ = 1
        if symbol in (window.key.LEFT, window.key.A): id_ = 2
        if symbol in (window.key.RIGHT, window.key.D): id_ = 3
        if symbol in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA): id_ = 4
        if id_ >= 0:
            self.__keys[id_] = state

    def releaseAllKeys(self):
        for i in range(10):
            self.__keys[i] = False

    def updatePlayerMoveState(self):
        self.moveStrafe = 0.0
        self.moveForward = 0.0
        if self.__keys[0]: self.moveForward -= 1.0
        if self.__keys[1]: self.moveForward += 1.0
        if self.__keys[2]: self.moveStrafe -= 1.0
        if self.__keys[3]: self.moveStrafe += 1.0

        self.jumpHeld = self.__keys[4]
