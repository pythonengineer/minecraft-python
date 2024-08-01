from mc.net.minecraft.game.entity.EntityLiving import EntityLiving

class EntityCreeper(EntityLiving):

    def __init__(self, world):
        super().__init__(world)
        self.texture = 'mob/creeper.png'
