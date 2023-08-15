from .net.minecraft.Minecraft import Minecraft


app = Minecraft(
    width = 1024,
    height = 768,
    caption = 'Game',
    vsync = False,
    visible = False,
    )
app.run()
