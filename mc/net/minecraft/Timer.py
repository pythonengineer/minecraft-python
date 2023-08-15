from mc import compat


NS_PER_SECOND = 1000000000
MAX_NS_PER_UPDATE = 1000000000
MAX_TICKS_PER_UPDATE = 100


class Timer:

    ticks = 0
    a = 0.0
    timeScale = 1.0
    fps = 0.0
    passedTime = 0.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = ticksPerSecond
        self.lastTime = compat.getNs()

    def advanceTime(self):
        now = compat.getNs()
        passed = (now - self.lastTime)
        self.lastTime = now

        passed = max(passed, 0)
        if (passed == 0) or (passed > 1e9):
            passed = 1e9

        self.fps = (1e9 / passed)
        self.passedTime += (
            ((passed
              * self.timeScale
              * self.ticksPerSecond
              ) / 1e9))

        self.ticks = int(self.passedTime)
        if self.ticks > 100:
            self.ticks = 100

        self.passedTime -= self.ticks
        self.a = self.passedTime
