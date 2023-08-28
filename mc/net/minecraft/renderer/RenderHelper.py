from mc.net.minecraft.character.Vec3 import Vec3
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.CompatibilityShims import BufferUtils
from pyglet import gl

class RenderHelper:
    fogColorMultiplier = 1.0

    displayActive = False

    fogColorRed = 0.5
    fogColorGreen = 0.8
    fogColorBlue = 1.0

    renderDistance = 0.0

    __unusedInt1 = 0
    __unusedInt2 = 0

    __lb = BufferUtils.createFloatBuffer(16)

    def __init__(self, minecraft):
        self.minecraft = minecraft

    def toggleLight(self, z1):
        if not z1:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_LIGHT0)
        else:
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_LIGHT0)
            gl.glEnable(gl.GL_COLOR_MATERIAL)
            gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
            f4 = 0.7
            f2 = 0.3
            vec = Vec3(0.0, -1.0, 0.5).normalize()
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.__getBuffer(vec.x, vec.y, vec.z, 0.0))
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, self.__getBuffer(f2, f2, f2, 1.0))
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, self.__getBuffer(0.0, 0.0, 0.0, 1.0))
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(f4, f4, f4, 1.0))

    def initGui(self):
        screenWidth = self.minecraft.width * 240 // self.minecraft.height
        screenHeight = self.minecraft.height * 240 // self.minecraft.height

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -200.0)

    def setupFog(self):
        gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(self.fogColorRed, self.fogColorGreen, self.fogColorBlue, 1.0))
        gl.glNormal3f(0.0, -1.0, 0.0)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        currentTile = tiles.tiles[self.minecraft.level.getTile(int(self.minecraft.player.x), int(self.minecraft.player.y + 0.12), int(self.minecraft.player.z))]
        if currentTile and currentTile.getLiquidType() != Liquid.none:
            liquid = currentTile.getLiquidType()
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_EXP)
            if liquid == Liquid.water:
                gl.glFogf(gl.GL_FOG_DENSITY, 0.1)
                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(0.4, 0.4, 0.9, 1.0))
            elif liquid == Liquid.lava:
                gl.glFogf(gl.GL_FOG_DENSITY, 2.0)
                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(0.4, 0.3, 0.3, 1.0))
        else:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_LINEAR)
            gl.glFogf(gl.GL_FOG_START, 0.0)
            gl.glFogf(gl.GL_FOG_END, self.renderDistance)
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(1.0, 1.0, 1.0, 1.0))

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT)
        gl.glEnable(gl.GL_LIGHTING)

    def __getBuffer(self, a, b, c, d):
        self.__lb.clear()
        self.__lb.put(a).put(b).put(c).put(d)
        self.__lb.flip()
        return self.__lb
