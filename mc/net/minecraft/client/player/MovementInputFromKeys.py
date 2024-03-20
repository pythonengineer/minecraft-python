from mc.net.minecraft.client.player.MovementInput import MovementInput
from pyglet import window

class MovementInputFromKeys(MovementInput):

    def __init__(self, options):
        self.__options = options
        self.__keys = [False] * 10

    def checkKeyForMovementInput(self, symbol, state):
        id_ = -1
        if symbol == self.__options.keyBindForward.keyCode: id_ = 0
        if symbol == self.__options.keyBindBack.keyCode: id_ = 1
        if symbol == self.__options.keyBindLeft.keyCode: id_ = 2
        if symbol == self.__options.keyBindRight.keyCode: id_ = 3
        if symbol == self.__options.keyBindJump.keyCode: id_ = 4
        if id_ >= 0:
            self.__keys[id_] = state

    def resetKeyState(self):
        for i in range(10):
            self.__keys[i] = False

    def updatePlayerMoveState(self):
        self.moveStrafe = 0.0
        self.moveForward = 0.0
        if self.__keys[0]: self.moveForward -= 1.0
        if self.__keys[1]: self.moveForward += 1.0
        if self.__keys[2]: self.moveStrafe -= 1.0
        if self.__keys[3]: self.moveStrafe += 1.0

        self.jump = self.__keys[4]
