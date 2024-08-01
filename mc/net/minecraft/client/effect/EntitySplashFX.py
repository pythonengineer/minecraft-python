from mc.net.minecraft.client.effect.EntityRainFX import EntityRainFX

class EntitySplashFX(EntityRainFX):

    def __init__(self, world, x, y, z):
        super().__init__(world, x, y, z)
        self._particleScale *= 2.0
        self._particleGravity = 0.04
