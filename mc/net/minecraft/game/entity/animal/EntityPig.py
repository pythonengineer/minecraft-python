from mc.net.minecraft.game.entity.EntityLiving import EntityLiving

class EntityPig(EntityLiving):

    def __init__(self, world):
        super().__init__(world)
        self.texture = 'mob/pig.png'
        self.setSize(0.9, 0.9)
