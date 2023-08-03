from mc.CompatibilityShims import getNs

class Timer:
    NS_PER_SECOND = 1000000000
    MAX_NS_PER_UPDATE = 1000000000
    MAX_TICKS_PER_UPDATE = 100
    ticks = 0
    a = 0.0
    timeScale = 1.0
    fps = 0.0
    passedTime = 0.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = ticksPerSecond
        self.lastTime = getNs()

    def advanceTime(self):
        now = getNs()
        passedNs = now - self.lastTime
        self.lastTime = now

        if passedNs < 0:
            passedNs = 0
        if passedNs > 1000000000:
            passedNs = 1000000000
        if passedNs == 0:
            passedNs = 1000000000
        self.fps = 1000000000 / passedNs

        self.passedTime += passedNs * self.timeScale * self.ticksPerSecond / 1.0E+009

        self.ticks = int(self.passedTime)
        if self.ticks > 100:
            self.ticks = 100
        self.passedTime -= self.ticks
        self.a = self.passedTime
