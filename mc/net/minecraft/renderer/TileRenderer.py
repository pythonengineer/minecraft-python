class TileRenderer:

    def __init__(self, mc):
        self.minecraft = mc
        self.tile = None
        self.progress = 0.0
        self.oProgress = 0.0
        self.rot = 0
        self.move = False
