from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.model.md3.MD3Loader import MD3Loader
from mc.net.minecraft.client.model.md3.MD3Model import MD3Model

class RenderManager:

    def __init__(self):
        self.model = [None]
        self.worldObj = None
        ModelBiped()

        try:
            self.model[0] = MD3Model((MD3Loader()).loadModel('test2.md3'))
        except IOError as e:
            print(e)
