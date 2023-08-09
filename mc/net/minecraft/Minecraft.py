import pyglet
pyglet.options['debug_gl'] = False

from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.character.Vec3 import Vec3
from mc.net.minecraft.character.Zombie import Zombie
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelIO import LevelIO
from mc.net.minecraft.level.levelgen.LevelGen import LevelGen
from mc.net.minecraft.player.Player import Player
from mc.net.minecraft.player.MovementInputFromOptions import MovementInputFromOptions
from mc.net.minecraft.gui.Font import Font
from mc.net.minecraft.gui.PauseScreen import PauseScreen
from mc.net.minecraft.particle.ParticleEngine import ParticleEngine
from mc.net.minecraft.renderer.DirtyChunkSorter import DirtyChunkSorter
from mc.net.minecraft.renderer.LevelRenderer import LevelRenderer
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.renderer.Textures import Textures
from mc.net.minecraft.renderer.Frustum import Frustum
from mc.net.minecraft.renderer.Chunk import Chunk
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis, getNs
from pyglet import window, canvas, clock, gl, compat_platform

import math
import time
import gzip
import sys
import gc

GL_DEBUG = False

class Minecraft(window.Window):
    VERSION_STRING = '0.0.14a_08'
    __timer = Timer(20.0)
    __level = None
    __levelRenderer = None
    __player = None
    __paintTexture = 1
    __particleEngine = None

    user = None
    minecraftUri = ''

    __yMouseAxis = 1
    __editMode = 0
    __screen = None

    __ticksRan = 0

    loadMapUser = ''
    loadMapID = 0

    __creativeTiles = [tiles.rock.id, tiles.dirt.id, tiles.stoneBrick.id,
                       tiles.wood.id, tiles.bush.id, tiles.log.id,
                       tiles.leaf.id, tiles.sand.id, tiles.gravel.id]
    __fogColorRed = 0.5
    __fogColorGreen = 0.8
    __fogColorBlue = 1.0

    __running = True
    __fpsString = ''

    __ksh = window.key.KeyStateHandler()
    __msh = window.mouse.MouseStateHandler()
    __mouseGrabbed = False
    mouseX = 0
    mouseY = 0

    __prevFrameTime = 0
    __renderDistance = 0.0

    __hitResult = None

    __unusedInt1 = 0
    __unusedInt2 = 0

    __lb = BufferUtils.createFloatBuffer(16)

    __title = ''
    __text = ''

    def __init__(self, fullscreen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__fullscreen = fullscreen
        self.__textures = Textures()

        self.push_handlers(self.__ksh)
        self.push_handlers(self.__msh)

    def setScreen(self, screen):
        if self.__screen:
            self.__screen.closeScreen()

        self.__screen = screen
        if screen:
            screenWidth = self.width * 240 // self.height
            screenHeight = self.height * 240 // self.height
            screen.init(self, screenWidth, screenHeight)

    def __checkGlError(self, string):
        if GL_DEBUG:
            errorCode = gl.glGetError()
            if errorCode != 0:
                print('########## GL ERROR ##########')
                print('@ ' + string)
                print(errorCode)
                sys.exit(1)

    def destroy(self):
        try:
            LevelIO.save(self.__level, gzip.open('level.dat', 'wb'))
        except Exception as e:
            print(e)

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
            self.__clickMouse()
            self.__prevFrameTime = self.__ticksRan
        elif button == window.mouse.RIGHT:
            self.__editMode = (self.__editMode + 1) % 2
        elif button == window.mouse.MIDDLE:
            if self.__hitResult:
                tile = self.__level.getTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z)
                if tile == tiles.grass.id:
                    tile = tiles.dirt.id

                for t in self.__creativeTiles:
                    if tile == t:
                        self.__paintTexture = t

    def on_mouse_scroll(self, x, y, dx, dy):
        if self.__screen:
            return

        if dy == 0:
            return
        elif dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1

        i3 = 0

        for i, tile in enumerate(self.__creativeTiles):
            if tile == self.__paintTexture:
                i3 = i

        i3 += dy
        while i3 < 0:
            i3 += len(self.__creativeTiles)

        while i3 >= len(self.__creativeTiles):
            i3 -= len(self.__creativeTiles)

        self.__paintTexture = self.__creativeTiles[i3]

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouseX = x
        self.mouseY = y
        if self.__mouseGrabbed:
            xo = dx
            yo = dy * self.__yMouseAxis
            self.__player.turn(xo, yo)

    def on_key_press(self, symbol, modifiers):
        if self.__screen:
            self.__screen.updateEvents(key=symbol, modifiers=modifiers)
            if self.__screen:
                self.__screen.tick()
            return

        self.__player.setKey(symbol, True)

        if symbol == window.key.ESCAPE:
            self.__releaseMouse()
        elif symbol == window.key.R:
            self.__player.resetPos()
        elif symbol == window.key.RETURN:
            self.__level.setSpawnPos(int(self.__player.x), int(self.__player.y), int(self.__player.z), self.__player.yRot)
            self.__player.resetPos()

        for i in range(9):
            if symbol == getattr(window.key, '_' + str(i + 1)):
                self.__paintTexture = self.__creativeTiles[i]

        if symbol == window.key.Y:
            self.__yMouseAxis = -self.__yMouseAxis
        elif symbol == window.key.G and len(self.__level.entities) < 256:
            self.__level.entities.add(Zombie(self.__level, self.__player.x, self.__player.y, self.__player.z))
        elif symbol == window.key.F:
            self.__levelRenderer.drawDistance = (self.__levelRenderer.drawDistance + 1) % 4

    def on_key_release(self, symbol, modifiers):
        if self.__screen:
            self.__screen.updateEvents(key=symbol, state=False)
            if self.__screen:
                self.__screen.tick()
            return

        self.__player.setKey(symbol, False)

    def on_activate(self):
        # Remove this hack when the window boundary issue is fixed upstream:
        if self.__mouseGrabbed and compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_deactivate(self):
        self.__releaseMouse()

    def on_draw(self):
        now = getNs()
        passedNs = now - self.__timer.lastTime
        self.__timer.lastTime = now

        if passedNs < 0:
            passedNs = 1
        elif passedNs > self.__timer.MAX_NS_PER_UPDATE:
            passedNs = self.__timer.MAX_NS_PER_UPDATE
        elif passedNs == 0:
            passedNs = 1

        self.__timer.fps += passedNs * self.__timer.timeScale * self.__timer.ticksPerSecond / self.__timer.MAX_NS_PER_UPDATE
        self.__timer.ticks = int(self.__timer.fps)
        if self.__timer.ticks > self.__timer.MAX_TICKS_PER_UPDATE:
            self.__timer.ticks = self.__timer.MAX_TICKS_PER_UPDATE

        self.__timer.fps -= float(self.__timer.ticks)
        self.__timer.a = self.__timer.fps

        for i in range(self.__timer.ticks):
            self.__ticksRan += 1
            self.__tick()

        self.__checkGlError('Pre render')
        self.render(self.__timer.a)
        self.__checkGlError('Post render')

    def run(self):
        self.__frustum = Frustum()
        self.__dummyChunk = Chunk(None, 0, 0, 0, 0, True)

        self.__fogColor0 = (self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 1.0)
        self.__fogColor1 = (14 / 255.0, 11 / 255.0, 10 / 255.0, 1.0)

        self.set_fullscreen(self.__fullscreen)

        if not self.__fullscreen:
            display = canvas.Display()
            screen = display.get_default_screen()
            locationX = screen.width // 2 - self.width // 2
            locationY = screen.height // 2 - self.height // 2
            self.set_location(locationX, locationY)

        self.__checkGlError('Pre startup')

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glShadeModel(gl.GL_SMOOTH)
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

        self.font = Font('default.gif', self.__textures)

        imgData = BufferUtils.createIntBuffer(256)
        imgData.clear().limit(256)

        gl.glViewport(0, 0, self.width, self.height)

        self.__levelIo = LevelIO(self)
        self.__levelGen = LevelGen(self)

        success = False

        try:
            if self.loadMapUser:
                success = self.loadLevel(self.loadMapUser, self.loadMapID)
            else:
                level = self.__levelIo.load(self.__level, gzip.open('level.dat', 'rb'))
                success = level != None
                if not success:
                    level = self.__levelIo.loadLegacy(self.__level, gzip.open('level.dat', 'rb'))
                    success = level != None

                self.__setLevel(level)
        except Exception as e:
            success = False

        if not success:
            self.generateLevel(1)

        self.__levelRenderer = LevelRenderer(self.__textures)
        self.__particleEngine = ParticleEngine(self.__level, self.__textures)
        self.__player = Player(self.__level, MovementInputFromOptions())
        self.__player.resetPos()
        if self.__level:
            self.__levelRenderer.setLevel(self.__level)

        self.__checkGlError('Post startup')

        lastTime = getMillis()
        frames = -2
        while self.__running:
            clock.tick()
            self.dispatch_events()
            self.dispatch_event('on_draw')
            if frames >= 0:
                self.flip()

            frames += 1
            while getMillis() >= lastTime + 1000:
                self.__fpsString = str(frames) + ' fps, ' + str(self.__dummyChunk.updates) + ' chunk updates'
                self.__dummyChunk.updates = 0
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

    def __releaseMouse(self):
        if not self.__mouseGrabbed:
            return

        self.__player.releaseAllKeys()
        self.__mouseGrabbed = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)
        self.setScreen(PauseScreen())

    def __clickMouse(self):
        if self.__hitResult:
            if self.__editMode == 0:
                oldTile = tiles.tiles[self.__level.getTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z)]
                changed = self.__level.setTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z, 0)
                if oldTile and changed:
                    oldTile.destroy(self.__level, self.__hitResult.x, self.__hitResult.y, self.__hitResult.z, self.__particleEngine)
            else:
                x = self.__hitResult.x
                y = self.__hitResult.y
                z = self.__hitResult.z

                if self.__hitResult.f == 0: y -= 1
                if self.__hitResult.f == 1: y += 1
                if self.__hitResult.f == 2: z -= 1
                if self.__hitResult.f == 3: z += 1
                if self.__hitResult.f == 4: x -= 1
                if self.__hitResult.f == 5: x += 1

                tile = tiles.tiles[self.__level.getTile(x, y, z)]
                aabb = tiles.tiles[self.__paintTexture].getAABB(x, y, z)
                if (tile is None or tile == tiles.water or tile == tiles.calmWater or tile == tiles.lava or tile == tiles.calmLava) and \
                   (aabb is None or (False if self.__player.bb.intersects(aabb) else self.__level.isFree(aabb))):
                    self.__level.setTile(x, y, z, self.__paintTexture)
                    tiles.tiles[self.__paintTexture].onBlockAdded(self.__level, x, y, z)

    def __tick(self):
        if self.__screen:
            self.__prevFrameTime = self.__ticksRan + 10000
            self.__screen.updateEvents()
            if self.__screen:
                self.__screen.tick()
        else:
            if self.__msh[window.mouse.LEFT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.__mouseGrabbed:
                self.__clickMouse()
                self.__prevFrameTime = self.__ticksRan

        self.__levelRenderer.cloudTickCounter += 1
        self.__level.tick()

        for p in self.__particleEngine.particles.copy():
            p.tick()
            if p.removed:
                self.__particleEngine.particles.remove(p)

        self.__player.tick()

    def __orientCamera(self, a):
        gl.glTranslatef(0.0, 0.0, -0.3)
        gl.glRotatef(self.__player.xRotO + (self.__player.xRot - self.__player.xRotO) * a, 1.0, 0.0, 0.0)
        gl.glRotatef(self.__player.yRotO + (self.__player.yRot - self.__player.yRotO) * a, 0.0, 1.0, 0.0)

        x = self.__player.xo + (self.__player.x - self.__player.xo) * a
        y = self.__player.yo + (self.__player.y - self.__player.yo) * a
        z = self.__player.zo + (self.__player.z - self.__player.zo) * a
        gl.glTranslatef(-x, -y, -z)

    def __setupCamera(self, a):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(70.0, self.width / self.height, 0.05, self.__renderDistance)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        self.__orientCamera(a)

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

        self.__fogColorRed = 0.92
        self.__fogColorGreen = 0.98
        self.__fogColorBlue = 1.0

        gl.glClearColor(self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 0.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.__renderDistance = float(1024 >> (self.__levelRenderer.drawDistance << 1))
        self.__setupCamera(a)
        self.__checkGlError('Set up camera')

        gl.glEnable(gl.GL_CULL_FACE)

        self.__frustum.calculateFrustum()
        for chunk in self.__levelRenderer.sortedChunks:
            chunk.isInFrustum(self.__frustum)

        for chunk in self.__levelRenderer.dirtyChunks.copy():
            chunk.rebuild()
            self.__levelRenderer.dirtyChunks.remove(chunk)

        self.__checkGlError('Update chunks')
        z21 = self.__level.isSolid(self.__player.x, self.__player.y, self.__player.z, 0.1)

        self.__setupFog(0)
        gl.glEnable(gl.GL_FOG)

        self.__levelRenderer.render(self.__player, 0)
        if z21:
            x = int(self.__player.x)
            y = int(self.__player.y)
            z = int(self.__player.z)

            for xx in range(x - 1, x + 2):
                for yy in range(y - 1, y + 2):
                    for zz in range(z - 1, z + 2):
                        self.__levelRenderer.render(xx, yy, zz)

        self.__checkGlError('Rendered level')
        self.__levelRenderer.renderEntities(self.__frustum, a)
        self.__checkGlError('Rendered entities')
        self.__particleEngine.render(self.__player, a)
        self.__checkGlError('Rendered particles')
        gl.glCallList(self.__levelRenderer.surroundLists)
        gl.glDisable(gl.GL_LIGHTING)
        self.__setupFog(-1)
        self.__levelRenderer.renderClouds(a)
        self.__setupFog(1)
        gl.glEnable(gl.GL_LIGHTING)

        if self.__hitResult:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.__levelRenderer.renderHit(self.__player, self.__hitResult, self.__editMode, self.__paintTexture)
            LevelRenderer.renderHitOutline(self.__hitResult, self.__editMode)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glEnable(gl.GL_LIGHTING)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.__setupFog(0)
        gl.glCallList(self.__levelRenderer.surroundLists + 1)

        gl.glEnable(gl.GL_BLEND)
        gl.glColorMask(False, False, False, False)
        self.__levelRenderer.render(self.__player, 1)
        gl.glColorMask(True, True, True, True)
        self.__levelRenderer.render(self.__player, 1)

        gl.glDisable(gl.GL_BLEND)

        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_FOG)
        gl.glDisable(gl.GL_TEXTURE_2D)

        if self.__hitResult:
            gl.glDepthFunc(gl.GL_LESS)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.__levelRenderer.renderHit(self.__player, self.__hitResult, self.__editMode, self.__paintTexture)
            LevelRenderer.renderHitOutline(self.__hitResult, self.__editMode)
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

        screenWidth //= 2
        screenHeight //= 2
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t.begin()
        t.vertex(screenWidth + 1, screenHeight - 4, 0.0)
        t.vertex(screenWidth - 0, screenHeight - 4, 0.0)
        t.vertex(screenWidth - 0, screenHeight + 5, 0.0)
        t.vertex(screenWidth + 1, screenHeight + 5, 0.0)

        t.vertex(screenWidth + 5, screenHeight - 0, 0.0)
        t.vertex(screenWidth - 4, screenHeight - 0, 0.0)
        t.vertex(screenWidth - 4, screenHeight + 1, 0.0)
        t.vertex(screenWidth + 5, screenHeight + 1, 0.0)
        t.end()

        self.__checkGlError('GUI: Draw crosshair')

        if self.__screen:
            self.__screen.render(xMouse, yMouse)

    def __setupFog(self, i):
        if i == -1:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_LINEAR)
            gl.glFogf(gl.GL_FOG_START, 0.0)
            gl.glFogf(gl.GL_FOG_END, self.__renderDistance)
            gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 1.0))
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(1.0, 1.0, 1.0, 1.0))
        else:
            currentTile = tiles.tiles[self.__level.getTile(int(self.__player.x), int(self.__player.y + 0.12), int(self.__player.z))]
            if currentTile and currentTile.getLiquidType() == 1:
                gl.glFogi(gl.GL_FOG_MODE, gl.GL_EXP)
                gl.glFogf(gl.GL_FOG_DENSITY, 0.1)
                gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(0.02, 0.02, 0.2, 1.0))
                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(0.3, 0.3, 0.7, 1.0))
            elif currentTile and currentTile.getLiquidType() == 2:
                gl.glFogi(gl.GL_FOG_MODE, gl.GL_EXP)
                gl.glFogf(gl.GL_FOG_DENSITY, 2.0)
                gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(0.6, 0.1, 0.0, 1.0))
                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(0.4, 0.3, 0.3, 1.0))
            elif i == 0:
                gl.glFogi(gl.GL_FOG_MODE, gl.GL_LINEAR)
                gl.glFogf(gl.GL_FOG_START, 0.0)
                gl.glFogf(gl.GL_FOG_END, self.__renderDistance)
                gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 1.0))
                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(1.0, 1.0, 1.0, 1.0))
            elif i == 1:
                gl.glFogi(gl.GL_FOG_MODE, gl.GL_EXP)
                gl.glFogf(gl.GL_FOG_DENSITY, 0.01)
                gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(self.__fogColor1[0], self.__fogColor1[1],
                                                             self.__fogColor1[2], self.__fogColor1[3]))
                br = 0.6
                gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(br, br, br, 1.0))

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT)
        gl.glEnable(gl.GL_LIGHTING)

    def __getBuffer(self, a, b, c, d):
        self.__lb.clear()
        self.__lb.put(a).put(b).put(c).put(1.0)
        self.__lb.flip()
        return self.__lb

    def beginLevelLoading(self, title):
        self.__title = title
        screenWidth = self.width * 240 / self.height
        screenHeight = self.height * 240 / self.height

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -200.0)

    def levelLoadUpdate(self, status):
        self.__text = status
        self.setLoadingProgress()

    def setLoadingProgress(self):
        screenWidth = self.width * 240 // self.height
        screenHeight = self.height * 240 // self.height

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        t = tesselator
        gl.glEnable(gl.GL_TEXTURE_2D)
        id_ = self.__textures.loadTexture('dirt.png', gl.GL_NEAREST)
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        s = 32.0
        t.begin()
        t.color(4210752)
        t.vertexUV(0.0, screenHeight, 0.0, 0.0, screenHeight / s)
        t.vertexUV(screenWidth, screenHeight, 0.0, screenWidth / s, screenHeight / s)
        t.vertexUV(screenWidth, 0.0, 0.0, screenWidth / s, 0.0)
        t.vertexUV(0.0, 0.0, 0.0, 0.0, 0.0)
        t.end()

        self.font.drawShadow(self.__title, (screenWidth - self.font.width(self.__title)) // 2, screenHeight // 2 - 4 - 16, 0xFFFFFF)
        self.font.drawShadow(self.__text, (screenWidth - self.font.width(self.__text)) // 2, screenHeight // 2 - 4 + 8, 0xFFFFFF)
        clock.tick()
        self.flip()

    def generateLevel(self, i):
        name = self.user.name if self.user else 'anonymous'
        self.__setLevel(self.__levelGen.generateLevel(name, 128 << i, 128 << i, 64))

    def saveLevel(self, i, name):
        return self.__levelIo.save(self.__level, gzip.open('level.dat', 'wb'))

    def loadLevel(self, name, i):
        level = self.__levelIo.load(self.__level, gzip.open('level.dat', 'rb'))
        if not level:
            return False
        else:
            self.__setLevel(level)
            return True

    def __setLevel(self, level):
        self.__level = level
        if self.__levelRenderer:
            self.__levelRenderer.setLevel(level)

        if self.__particleEngine:
            self.__particleEngine.particles.clear()

        if self.__player:
            self.__player.setLevel(level)
            self.__player.resetPos()

        gc.collect()

if __name__ == '__main__':
    fullScreen = False
    for arg in sys.argv:
        if arg == '-fullscreen':
            fullScreen = True

    Minecraft(fullScreen, width=854, height=480, caption='Minecraft 0.0.14a_08').run()
