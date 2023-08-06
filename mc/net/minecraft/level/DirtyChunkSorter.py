from mc.CompatibilityShims import getMillis

class DirtyChunkSorter:
    now = getMillis()

    def __init__(self, player, frustum):
        self.player = player
        self.frustum = frustum

    def compare(self, c0, c1):
        i0 = self.frustum.isVisible(c0.aabb)
        i1 = self.frustum.isVisible(c1.aabb)
        if i0 and not i1:
            return -1
        if i1 and not i0:
            return 1
        t0 = int((self.now - c0.dirtiedTime) / 2000)
        t1 = int((self.now - c1.dirtiedTime) / 2000)
        if t0 < t1:
            return -1
        if t0 > t1:
            return 1
        return -1 if c0.distanceToSqr(self.player) < c1.distanceToSqr(self.player) else 1
