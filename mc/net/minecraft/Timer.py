from mc.CompatibilityShims import getMillis, getNs

class Timer:
    NS_PER_SECOND = 1000000
    MAX_TICKS_PER_UPDATE = 100
    lastHRTime = 0.0
    ticks = 0
    a = 0.0
    timeScale = 1.0
    fps = 0.0
    timeSyncAdjustment = 1.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = ticksPerSecond
        self.lastSyncSysClock = getMillis()
        self.lastSyncHRClock = getNs() // self.NS_PER_SECOND
