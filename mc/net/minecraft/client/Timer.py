from mc.CompatibilityShims import getMillis

import time

class Timer:
    NS_PER_SECOND = 1000000
    MAX_TICKS_PER_UPDATE = 100
    lastHRTime = 0.0
    elapsedTicks = 0
    renderPartialTicks = 0.0
    timerSpeed = 1.0
    elapsedPartialTicks = 0.0
    timeSyncAdjustment = 1.0

    def __init__(self, ticksPerSecond):
        self.ticksPerSecond = ticksPerSecond
        self.lastSyncSysClock = getMillis()
        self.lastSyncHRClock = time.time_ns() // self.NS_PER_SECOND
