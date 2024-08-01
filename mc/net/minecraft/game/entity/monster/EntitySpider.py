from mc.net.minecraft.game.entity.EntityLiving import EntityLiving

class EntitySpider(EntityLiving):

    def __init__(self, world):
        super().__init__(world)
        self.texture = 'mob/spider.png'
        self.setSize(1.4, 0.9)
