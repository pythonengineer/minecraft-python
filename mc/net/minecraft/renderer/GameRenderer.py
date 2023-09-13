from mc.net.minecraft.model.Vec3 import Vec3
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.renderer.TileRenderer import TileRenderer
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.CompatibilityShims import BufferUtils
from pyglet import gl

import random
import math

class GameRenderer:
    fogColorMultiplier = 1.0

    displayActive = False

    renderDistance = 0.0
    rainTicks = 0
    entity = None
    rand = random.Random()

    __u1 = 0
    __u2 = 0

    __lb = BufferUtils.createFloatBuffer(16)

    fogRed = 0.0
    fogGreen = 0.0
    fogBlue = 0.0

    def __init__(self, minecraft):
        self.minecraft = minecraft
        self.tileRenderer = TileRenderer(self.minecraft)

    def getPlayerRotVec(self, rot):
        x = self.minecraft.player.xo + (self.minecraft.player.x - self.minecraft.player.xo) * rot
        y = self.minecraft.player.yo + (self.minecraft.player.y - self.minecraft.player.yo) * rot
        z = self.minecraft.player.zo + (self.minecraft.player.z - self.minecraft.player.zo) * rot
        return Vec3(x, y, z)

    def renderHurtFrames(self, a):
        ht = self.minecraft.player.hurtTime - a
        if self.minecraft.player.health <= 0:
            a = self.minecraft.player.deathTime + a
            gl.glRotatef(40.0 - 8000.0 / (a + 200.0), 0.0, 0.0, 1.0)
        if ht <= 0.0:
            return

        ht /= self.minecraft.player.hurtDuration
        ht = math.sin((ht * ht * ht * ht) * math.pi)
        d = self.minecraft.player.hurtDir
        gl.glRotatef(-d, 0.0, 1.0, 0.0)
        gl.glRotatef(-ht * 14.0, 0.0, 0.0, 1.0)
        gl.glRotatef(d, 0.0, 1.0, 0.0)

    def cameraBob(self, a):
        d = self.minecraft.player.walkDist - self.minecraft.player.walkDistO
        d = self.minecraft.player.walkDist + d * a
        bob = self.minecraft.player.oBob + (self.minecraft.player.bob - self.minecraft.player.oBob) * a
        tilt = self.minecraft.player.oTilt + (self.minecraft.player.tilt - self.minecraft.player.oTilt) * a
        gl.glTranslatef(math.sin(d * math.pi) * bob * 0.5, -(abs(math.cos(d * math.pi) * bob)), 0.0)
        gl.glRotatef(math.sin(d * math.pi) * bob * 3.0, 0.0, 0.0, 1.0)
        gl.glRotatef(abs(math.cos(d * math.pi + 0.2) * bob) * 5.0, 1.0, 0.0, 0.0)
        gl.glRotatef(tilt, 1.0, 0.0, 0.0)

    def renderRain(self, a):
        x = int(self.minecraft.player.x)
        y = int(self.minecraft.player.y)
        z = int(self.minecraft.player.z)
        t = tesselator
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glNormal3f(0.0, 1.0, 0.0)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.minecraft.textures.loadTexture('rain.png'))

        for xx in range(x - 5, x + 6):
            for zz in range(z - 5, z + 6):
                tile = self.minecraft.level.getHighestTile(xx, zz)
                i11 = y - 5
                i12 = y + 5
                if i11 < tile:
                    i11 = tile
                if i12 < tile:
                    i12 = tile

                if i11 != i12:
                    f15 = (((self.rainTicks + xx * 3121 + zz * 418711) % 32) + a) / 32.0
                    f13 = xx + 0.5 - self.minecraft.player.x
                    f14 = zz + 0.5 - self.minecraft.player.z
                    f13 = math.sqrt(f13 * f13 + f14 * f14) / 5
                    gl.glColor4f(1.0, 1.0, 1.0, (1.0 - f13 * f13) * 0.7)
                    t.begin()
                    t.vertexUV(xx, i11, zz, 0.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx + 1, i11, zz + 1, 2.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx + 1, i12, zz + 1, 2.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx, i12, zz, 0.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx, i11, zz + 1, 0.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx + 1, i11, zz, 2.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx + 1, i12, zz, 2.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                    t.vertexUV(xx, i12, zz + 1, 0.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                    t.end()

        gl.glEnable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_BLEND)

    def toggleLight(self, light):
        if not light:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_LIGHT0)
        else:
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_LIGHT0)
            gl.glEnable(gl.GL_COLOR_MATERIAL)
            gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
            light1 = 0.7
            f2 = 0.3
            vec = Vec3(0.0, -1.0, 0.5).normalize()
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.__getBuffer(vec.x, vec.y, vec.z, 0.0))
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, self.__getBuffer(f2, f2, f2, 1.0))
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, self.__getBuffer(0.0, 0.0, 0.0, 1.0))
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(light1, light1, light1, 1.0))

    def render(self):
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
        gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(self.fogRed, self.fogGreen, self.fogBlue, 1.0))
        gl.glNormal3f(0.0, -1.0, 0.0)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        currentTile = tiles.tiles[self.minecraft.level.getTile(int(self.minecraft.player.x), int(self.minecraft.player.y + 0.12), int(self.minecraft.player.z))]
        if currentTile and currentTile.getLiquidType() != Liquid.none:
            liquid = currentTile.getLiquidType()
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_EXP)
            if liquid == Liquid.water:
                gl.glFogf(gl.GL_FOG_DENSITY, 0.1)
                x = 0.4
                y = 0.4
                z = 0.9
                if self.minecraft.options.anaglyph3d:
                    f = (x * 30.0 + y * 59.0 + z * 11.0) / 100.0
                    y = (x * 30.0 + y * 70.0) / 100.0
                    z = (x * 30.0 + z * 70.0) / 100.0
                    x = f

                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(x, y, z, 1.0))
            elif liquid == Liquid.lava:
                gl.glFogf(gl.GL_FOG_DENSITY, 2.0)
                x = 0.4
                y = 0.3
                z = 0.3
                if self.minecraft.options.anaglyph3d:
                    f = (x * 30.0 + y * 59.0 + z * 11.0) / 100.0
                    y = (x * 30.0 + y * 70.0) / 100.0
                    z = (x * 30.0 + z * 70.0) / 100.0
                    x = f

                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(x, y, z, 1.0))
        else:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_LINEAR)
            gl.glFogf(gl.GL_FOG_START, 0.0)
            gl.glFogf(gl.GL_FOG_END, self.renderDistance)
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(1.0, 1.0, 1.0, 1.0))

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT)

    def __getBuffer(self, a, b, c, d):
        self.__lb.clear()
        self.__lb.put(a).put(b).put(c).put(d)
        self.__lb.flip()
        return self.__lb
