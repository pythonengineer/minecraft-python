import pyglet
pyglet.options['debug_gl'] = False

from mc.net.minecraft.User import User
from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.Player import Player
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.character.Vec3 import Vec3
from mc.net.minecraft.character.Zombie import Zombie
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.Chunk import Chunk
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelIO import LevelIO
from mc.net.minecraft.level.LevelRenderer import LevelRenderer
from mc.net.minecraft.level.levelgen.LevelGen import LevelGen
from mc.net.minecraft.gui.Font import Font
from mc.net.minecraft.gui.PauseScreen import PauseScreen
from mc.net.minecraft.particle.ParticleEngine import ParticleEngine
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.renderer.Textures import Textures
from mc.net.minecraft.renderer.Frustum import Frustum
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis
from pyglet import window, canvas, clock, gl, compat_platform

import math
import time
import gzip
import sys

class Minecraft(window.Window):
    VERSION_STRING = '0.0.13a'
    __timer = Timer(20.0)
    __running = True
    __paintTexture = 1

    user = User('noname')

    __entities = set()

    __yMouseAxis = 1
    __editMode = 0
    __screen = None

    __fpsString = ''

    __mouseGrabbed = False
    mouseX = 0
    mouseY = 0

    __hitResult = None

    lb = BufferUtils.createFloatBuffer(16)

    __title = ''

    def __init__(self, fullscreen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.textures = Textures()

        col1 = 920330
        fr = 0.5
        fg = 0.8
        fb = 1.0
        self.__fogColor0 = (fr, fg, fb, 1.0)
        self.__fogColor1 = ((col1 >> 16 & 0xFF) / 255.0, (col1 >> 8 & 0xFF) / 255.0, (col1 & 0xFF) / 255.0, 1.0)

        self.set_fullscreen(fullscreen)

        if not fullscreen:
            display = canvas.Display()
            screen = display.get_default_screen()
            locationX = screen.width // 2 - self.width // 2
            locationY = screen.height // 2 - self.height // 2
            self.set_location(locationX, locationY)

        self.set_visible(True)

        self.__checkGlError('Pre startup')

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glClearColor(fr, fg, fb, 0.0)
        gl.glClearDepth(1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glAlphaFunc(gl.GL_GREATER, 0.0)
        gl.glCullFace(gl.GL_BACK)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        self.__checkGlError('Startup')

        self.font = Font('default.gif', self.textures)

        imgData = BufferUtils.createIntBuffer(256)
        imgData.clear().limit(256)

        gl.glViewport(0, 0, self.width, self.height)

        self.__chunk = Chunk(None, 0, 0, 0, 0, 0, 0, True)
        self.frustum = Frustum()

        self.__level = Level()
        self.__levelIo = LevelIO(self)
        self.__levelGen = LevelGen(self)

        success = False

        try:
            success = self.__levelIo.load(self.__level, gzip.open('level.dat', 'rb'))
            if not success:
                success = self.__levelIo.loadLegacy(self.__level, gzip.open('level.dat', 'rb'))
        except Exception as e:
            success = False
        if not success:
            self.__levelGen.generateLevel(self.__level, self.user.name, 256, 256, 64)

        self.__levelRenderer = LevelRenderer(self.__level, self.textures)
        self.__player = Player(self.__level)
        self.__particleEngine = ParticleEngine(self.__level, self.textures)
        for i in range(10):
            zombie = Zombie(self.__level, self.textures, 128.0, 0.0, 128.0)
            zombie.resetPos()
            self.__entities.add(zombie)

        self.__checkGlError('Post startup')

    def setScreen(self, screen):
        self.__screen = screen
        if screen:
            screenWidth = self.width * 240 // self.height
            screenHeight = self.height * 240 // self.height
            screen.init(self, screenWidth, screenHeight)

    def __checkGlError(self, string):
        errorCode = gl.glGetError()
        if errorCode != 0:
            print("########## GL ERROR ##########")
            print("@ " + string)
            print(errorCode)
            sys.exit(1)

    def _attemptSaveLevel(self):
        try:
            self.__levelIo.save(self.__level, gzip.open('level.dat', 'wb'))
        except Exception as e:
            print(e)

    def destroy(self):
        self._attemptSaveLevel()

    def on_close(self):
        self.__running = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.__screen:
            self.__screen.updateEvents(button=button)
            if self.__screen:
                self.__screen.tick()
            return

        if not self.__mouseGrabbed:
            self.grabMouse()
        elif button == window.mouse.LEFT:
            self.__handleMouseClick()
        elif button == window.mouse.RIGHT:
            self.__editMode = (self.__editMode + 1) % 2

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouseX = x
        self.mouseY = y
        if self.__mouseGrabbed:
            self.__player.turn(dx, dy * self.__yMouseAxis)

    def on_key_press(self, symbol, modifiers):
        if self.__screen:
            self.__screen.updateEvents(key=symbol)
            self.__screen.tick()
            return

        self.__player.setKey(symbol, True)
        if symbol == window.key.R:
            self.__player.resetPos()
        elif symbol == window.key.G:
            self.__entities.add(Zombie(self.__level, self.textures, self.__player.x, self.__player.y, self.__player.z))
        elif symbol == window.key.F:
            self.__levelRenderer.toggleDrawDistance()
        elif symbol == window.key.Y:
            self.__yMouseAxis *= -1
        elif symbol == window.key._1:
            self.__paintTexture = 1
        elif symbol == window.key._2:
            self.__paintTexture = 3
        elif symbol == window.key._3:
            self.__paintTexture = 4
        elif symbol == window.key._4:
            self.__paintTexture = 5
        elif symbol == window.key._6:
            self.__paintTexture = 6
        elif symbol == window.key.RETURN:
            self._attemptSaveLevel()
        elif symbol == window.key.ESCAPE:
            self.releaseMouse()

    def on_key_release(self, symbol, modifiers):
        if self.__screen:
            return

        self.__player.setKey(symbol, False)
        if symbol in (window.key.UP, window.key.W):
            self.__player.upPressed = False
        elif symbol in (window.key.DOWN, window.key.S):
            self.__player.downPressed = False
        elif symbol in (window.key.LEFT, window.key.A):
            self.__player.leftPressed = False
        elif symbol in (window.key.RIGHT, window.key.D):
            self.__player.rightPressed = False
        elif symbol in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA):
            self.__player.spacePressed = False

    def on_activate(self):
        # Remove this hack when the window boundary issue is fixed upstream:
        if self.__mouseGrabbed and compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_draw(self):
        self.__timer.advanceTime()
        for i in range(self.__timer.ticks):
            self.tick()
        self.__checkGlError('Pre render')
        self.render(self.__timer.a)
        self.__checkGlError('Post render')

    def run(self):
        lastTime = getMillis()
        frames = 0
        while self.__running:
            clock.tick()
            self.dispatch_events()
            self.dispatch_event('on_draw')
            self.flip()

            frames += 1
            while getMillis() >= lastTime + 1000:
                self.__fpsString = str(frames) + ' fps, ' + str(self.__chunk.updates) + ' chunk updates'
                self.__chunk.updates = 0
                lastTime += 1000
                frames = 0

        self.destroy()

    def stop(self):
        self.__running = False

    def grabMouse(self):
        if self.__mouseGrabbed:
            return

        self.__mouseGrabbed = True
        self.set_exclusive_mouse(True)
        self.setScreen(None)

    def releaseMouse(self):
        if not self.__mouseGrabbed:
            return

        self.__player.releaseAllKeys()
        self.__mouseGrabbed = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)
        self.setScreen(PauseScreen())

    def __handleMouseClick(self):
        if self.__editMode == 0:
            if self.__hitResult:
                oldTile = tiles.tiles[self.__level.getTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z)]
                changed = self.__level.setTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z, 0)
                if oldTile and changed:
                    oldTile.destroy(self.__level, self.__hitResult.x, self.__hitResult.y, self.__hitResult.z, self.__particleEngine)
        elif self.__hitResult:
            x = self.__hitResult.x
            y = self.__hitResult.y
            z = self.__hitResult.z

            if self.__hitResult.f == 0: y -= 1
            if self.__hitResult.f == 1: y += 1
            if self.__hitResult.f == 2: z -= 1
            if self.__hitResult.f == 3: z += 1
            if self.__hitResult.f == 4: x -= 1
            if self.__hitResult.f == 5: x += 1
            aabb = tiles.tiles[self.__paintTexture].getAABB(x, y, z)
            if not aabb or self.__isFree(aabb):
                self.__level.setTile(x, y, z, self.__paintTexture)

    def tick(self):
        self.__level.tick()
        self.__particleEngine.tick()

        for entity in self.__entities.copy():
            entity.tick()
            if entity.removed:
                self.__entities.remove(entity)

        self.__player.tick()

    def __isFree(self, aabb):
        if self.__player.bb.intersects(aabb):
            return False

        for entity in self.__entities:
            if entity.bb.intersects(aabb):
                return False

        return True

    def __moveCameraToPlayer(self, a):
        gl.glTranslatef(0.0, 0.0, -0.3)
        gl.glRotatef(self.__player.xRot, 1.0, 0.0, 0.0)
        gl.glRotatef(self.__player.yRot, 0.0, 1.0, 0.0)

        x = self.__player.xo + (self.__player.x - self.__player.xo) * a
        y = self.__player.yo + (self.__player.y - self.__player.yo) * a
        z = self.__player.zo + (self.__player.z - self.__player.zo) * a
        gl.glTranslatef(-x, -y, -z)

    def __setupCamera(self, a):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(70.0, self.width / self.height, 0.05, 1024.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        self.__moveCameraToPlayer(a)

    def __pick(self, a):
        xRot = self.__player.xRotO + (self.__player.xRot - self.__player.xRotO) * a
        yRot = self.__player.yRotO + (self.__player.yRot - self.__player.yRotO) * a
        x = self.__player.xo + (self.__player.x - self.__player.xo) * a
        y = self.__player.yo + (self.__player.y - self.__player.yo) * a
        z = self.__player.zo + (self.__player.z - self.__player.zo) * a

        vec1 = Vec3(x, y, z)
        y1 = math.cos((-yRot) * math.pi / 180.0 + math.pi)
        y2 = math.sin((-yRot) * math.pi / 180.0 + math.pi)
        x1 = math.cos((-xRot) * math.pi / 180.0)
        x2 = math.sin((-xRot) * math.pi / 180.0)
        x = (y2 * x1) * 5.0
        y = x2 * 5.0
        z = (y1 * x1) * 5.0
        vec2 = Vec3(vec1.x + x, vec1.y + y, vec1.z + z)
        self.__hitResult = self.__level.clip(vec1, vec2)

    def render(self, a):
        gl.glViewport(0, 0, self.width, self.height)
        self.__checkGlError('Set viewport')
        self.__pick(a)
        self.__checkGlError('Picked')

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.__setupCamera(a)
        self.__checkGlError('Set up camera')
        gl.glEnable(gl.GL_CULL_FACE)

        self.frustum.calculateFrustum()
        self.__levelRenderer.cull(self.frustum)
        self.__levelRenderer.updateDirtyChunks(self.__player)
        self.__checkGlError('Update chunks')

        self.__setupFog(0)
        gl.glEnable(gl.GL_FOG)

        self.__levelRenderer.render(self.__player, 0)
        self.__checkGlError('Rendered level')
        for entity in self.__entities:
            if entity.isLit() and self.frustum.isVisible(entity.bb):
                entity.render(a)

        self.__checkGlError('Rendered entities')
        self.__particleEngine.render(self.__player, a, 0)
        self.__setupFog(1)
        self.__levelRenderer.render(self.__player, 1)
        for entity in self.__entities:
            if not entity.isLit() and self.frustum.isVisible(entity.bb):
                entity.render(a)

        self.__particleEngine.render(self.__player, a, 1)
        self.__levelRenderer.renderSurroundingGround()

        if self.__hitResult:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.__levelRenderer.renderHit(self.__player, self.__hitResult, self.__editMode, self.__paintTexture)
            self.__levelRenderer.renderHitOutline(self.__player, self.__hitResult, self.__editMode, self.__paintTexture)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glEnable(gl.GL_LIGHTING)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.__setupFog(0)
        self.__levelRenderer.renderSurroundingWater()

        gl.glEnable(gl.GL_BLEND)
        gl.glColorMask(False, False, False, False)
        self.__levelRenderer.render(self.__player, 2)
        gl.glColorMask(True, True, True, True)
        self.__levelRenderer.render(self.__player, 2)

        gl.glDisable(gl.GL_BLEND)

        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_FOG)

        if self.__hitResult:
            gl.glDepthFunc(gl.GL_LESS)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.__levelRenderer.renderHit(self.__player, self.__hitResult, self.__editMode, self.__paintTexture)
            self.__levelRenderer.renderHitOutline(self.__player, self.__hitResult, self.__editMode, self.__paintTexture)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glDepthFunc(gl.GL_LEQUAL)

        self.__drawGui(a)
        self.__checkGlError('Rendered gui')

    def __drawGui(self, a):
        screenWidth = self.width * 240 // self.height
        screenHeight = self.height * 240 // self.height

        xMouse = self.mouseX * screenWidth // self.width
        yMouse = screenHeight - self.mouseY * screenHeight // self.height - 1

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -200.0)

        self.__checkGlError('GUI: Init')

        gl.glPushMatrix()
        gl.glTranslatef(screenWidth - 16, 16.0, -50.0)
        t = tesselator
        gl.glScalef(16.0, 16.0, 16.0)
        gl.glRotatef(-30.0, 1.0, 0.0, 0.0)
        gl.glRotatef(45.0, 0.0, 1.0, 0.0)
        gl.glTranslatef(-1.5, 0.5, 0.5)
        gl.glScalef(-1.0, -1.0, -1.0)

        id_ = Textures.loadTexture('terrain.png', gl.GL_NEAREST)
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        gl.glEnable(gl.GL_TEXTURE_2D)
        t.begin()
        tiles.tiles[self.__paintTexture].render(t, self.__level, 0, -2, 0, 0)
        t.end()
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()

        self.__checkGlError('GUI: Draw selected')

        self.font.drawShadow(self.VERSION_STRING, 2, 2, 16777215)
        self.font.drawShadow(self.__fpsString, 2, 12, 16777215)
        self.__checkGlError('GUI: Draw text')

        wc = screenWidth // 2
        hc = screenHeight // 2
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t.begin()
        t.vertex(wc + 1, hc - 4, 0.0)
        t.vertex(wc - 0, hc - 4, 0.0)
        t.vertex(wc - 0, hc + 5, 0.0)
        t.vertex(wc + 1, hc + 5, 0.0)

        t.vertex(wc + 5, hc - 0, 0.0)
        t.vertex(wc - 4, hc - 0, 0.0)
        t.vertex(wc - 4, hc + 1, 0.0)
        t.vertex(wc + 5, hc + 1, 0.0)
        t.end()

        self.__checkGlError('GUI: Draw crosshair')

        if self.__screen:
            self.__screen.render(xMouse, yMouse)

    def __setupFog(self, i):
        currentTile = tiles.tiles[self.__level.getTile(int(self.__player.x), int(self.__player.y + 0.12), int(self.__player.z))]
        if currentTile and currentTile.getLiquidType() == 1:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
            gl.glFogf(gl.GL_FOG_DENSITY, 0.1)
            gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(0.02, 0.02, 0.2, 1.0))
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(0.3, 0.3, 0.7, 1.0))
        elif currentTile and currentTile.getLiquidType() == 2:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
            gl.glFogf(gl.GL_FOG_DENSITY, 2.0)
            gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(0.6, 0.1, 0.0, 1.0))
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(0.4, 0.3, 0.3, 1.0))
        elif i == 0:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
            gl.glFogf(gl.GL_FOG_DENSITY, 0.001)
            gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(self.__fogColor0[0], self.__fogColor0[1],
                                                         self.__fogColor0[2], self.__fogColor0[3]))
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(1.0, 1.0, 1.0, 1.0))
        elif i == 1:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
            gl.glFogf(gl.GL_FOG_DENSITY, 0.01)
            gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(self.__fogColor1[0], self.__fogColor1[1],
                                                         self.__fogColor1[2], self.__fogColor1[3]))
            br = 0.6
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(br, br, br, 1.0))
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT)
        gl.glEnable(gl.GL_LIGHTING)

    def __getBuffer(self, a, b, c, d):
        self.lb.clear()
        self.lb.put(a).put(b).put(c).put(d)
        self.lb.flip()
        return self.lb

    def beginLevelLoading(self, title):
        self.title = title
        screenWidth = self.width * 240 // self.height
        screenHeight = self.height * 240 // self.height

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -200.0)

    def levelLoadUpdate(self, status):
        screenWidth = self.width * 240 // self.height
        screenHeight = self.height * 240 // self.height

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        t = tesselator
        gl.glEnable(gl.GL_TEXTURE_2D)
        id_ = self.textures.loadTexture('dirt.png', gl.GL_NEAREST)
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        t.begin()
        t.color(8421504)
        s = 32.0
        t.vertexUV(0.0, screenHeight, 0.0, 0.0, screenHeight / s)
        t.vertexUV(screenWidth, screenHeight, 0.0, screenWidth / s, screenHeight / s)
        t.vertexUV(screenWidth, 0.0, 0.0, screenWidth / s, 0.0)
        t.vertexUV(0.0, 0.0, 0.0, 0.0, 0.0)
        t.end()
        gl.glEnable(gl.GL_TEXTURE_2D)

        self.font.drawShadow(self.title, (screenWidth - self.font.width(self.title)) // 2, screenHeight // 2 - 4 - 8, 16777215)
        self.font.drawShadow(status, (screenWidth - self.font.width(status)) // 2, screenHeight // 2 - 4 + 4, 16777215)
        clock.tick()
        self.flip()

    def generateNewLevel(self):
        self.__levelGen.generateLevel(self.__level, self.user.name, 32, 512, 64)
        self.__player.resetPos()
        for entity in self.__entities.copy():
            self.__entities.remove(entity)

if __name__ == '__main__':
    fullScreen = False
    for arg in sys.argv:
        if arg == '-fullscreen':
            fullScreen = True

    Minecraft(fullScreen, width=854, height=480, caption='Minecraft 0.0.13a', vsync=False, visible=False).run()
