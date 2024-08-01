from mc.net.minecraft.game.entity.EntityLiving import EntityLiving

class EntitySheep(EntityLiving):

    def __init__(self, world):
        super().__init__(world)
        self.texture = 'mob/sheep.png'
        self.setSize(0.9, 1.3)
