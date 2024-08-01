from mc.net.minecraft.game.entity.EntityLiving import EntityLiving

class EntityZombie(EntityLiving):

    def __init__(self, world):
        super().__init__(world)
        self.texture = 'mob/zombie.png'
