import pyglet
pyglet.options['debug_gl'] = False

from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.ChatLine import ChatLine
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.character.Vec3 import Vec3
from mc.net.minecraft.character.Zombie import Zombie
from mc.net.minecraft.character.ZombieModel import ZombieModel
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelIO import LevelIO
from mc.net.minecraft.level.levelgen.LevelGen import LevelGen
from mc.net.minecraft.player.Player import Player
from mc.net.minecraft.player.MovementInputFromOptions import MovementInputFromOptions
from mc.net.minecraft.net.ConnectionManager import ConnectionManager
from mc.net.minecraft.net import Packets
from mc.net.minecraft.gui.Font import Font
from mc.net.minecraft.gui.ChatScreen import ChatScreen
from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
from mc.net.minecraft.gui.PauseScreen import PauseScreen
from mc.net.minecraft.gui.InventoryScreen import InventoryScreen
from mc.net.minecraft.gui.InGameHud import InGameHud
from mc.net.minecraft.particle.ParticleEngine import ParticleEngine
from mc.net.minecraft.renderer.texture.TextureWaterFX import TextureWaterFX
from mc.net.minecraft.renderer.texture.TextureLavaFX import TextureLavaFX
from mc.net.minecraft.renderer.DirtyChunkSorter import DirtyChunkSorter
from mc.net.minecraft.renderer.LevelRenderer import LevelRenderer
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.renderer.Textures import Textures
from mc.net.minecraft.renderer.Frustum import Frustum
from mc.net.minecraft.renderer.Chunk import Chunk
from mc.net.minecraft.User import User
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis, getNs
from pyglet import window, app, canvas, clock, gl, compat_platform

import traceback
import math
import time
import gzip
import sys
import gc

GL_DEBUG = False

class StopGameException(Exception):
    pass

class Minecraft(window.Window):
    VERSION_STRING = '0.0.21a'
    __timer = Timer(20.0)
    level = None
    __levelRenderer = None
    player = None
    __particleEngine = None

    user = None
    minecraftUri = ''

    __active = False
    __yMouseAxis = 1
    __editMode = 0
    guiScreen = None

    __ticksRan = 0

    loadMapUser = ''
    loadMapId = 0

    __hud = None
    connectionManager = None

    server = ''
    port = 0

    __fogColorRed = 0.5
    __fogColorGreen = 0.8
    __fogColorBlue = 1.0

    running = True
    fpsString = ''

    ksh = window.key.KeyStateHandler()
    msh = window.mouse.MouseStateHandler()
    __mouseGrabbed = False
    mouseX = 0
    mouseY = 0

    __prevFrameTime = 0
    __renderDistance = 0.0

    __hitResult = None

    __fogColorMultiplier = 1.0
    __displayActive = False
    __unusedInt1 = 0
    __unusedInt2 = 0

    __lb = BufferUtils.createFloatBuffer(16)

    __title = ''
    __text = ''
    screenChanged = False
    hideGui = False
    playerModel = ZombieModel()

    def __init__(self, fullscreen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__fullscreen = fullscreen
        self.textures = Textures()
        self.textures.registerTextureFX(TextureLavaFX())
        self.textures.registerTextureFX(TextureWaterFX())

        self.push_handlers(self.ksh)
        self.push_handlers(self.msh)

    def setServer(self, server, port):
        self.server = server
        self.port = port

    def setScreen(self, screen):
        if not isinstance(self.guiScreen, ErrorScreen):
            if self.guiScreen or screen:
                self.screenChanged = True
            if self.guiScreen:
                self.guiScreen.closeScreen()

            self.guiScreen = screen
            if screen:
                self.__releaseMouse()
                screenWidth = self.width * 240 // self.height
                screenHeight = self.height * 240 // self.height
                screen.init(self, screenWidth, screenHeight)
            else:
                self.grabMouse()
        else:
            self.__releaseMouse()

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
            LevelIO.save(self.level, gzip.open('level.dat', 'wb'))
        except Exception as e:
            print(traceback.format_exc())

    def on_close(self):
        self.running = False

    def on_activate(self):
        self.__active = True

        # Remove this hack when the window boundary issue is fixed upstream:
        if self.__mouseGrabbed and compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_deactivate(self):
        self.__active = False
        self.__releaseMouse()

    def on_mouse_press(self, x, y, button, modifiers):
        try:
            if self.guiScreen:
                self.guiScreen.updateMouseEvents(button)

            if self.screenChanged:
                self.screenChanged = False
                if compat_platform != 'darwin':
                    return

            if not self.guiScreen or (self.guiScreen and self.guiScreen.allowUserInput):
                if not self.guiScreen:
                    if not self.__mouseGrabbed:
                        self.grabMouse()
                    elif button == window.mouse.LEFT:
                        self.__clickMouse()
                        self.__prevFrameTime = self.__ticksRan
                    elif button == window.mouse.RIGHT:
                        self.__editMode = (self.__editMode + 1) % 2
                    elif button == window.mouse.MIDDLE and self.__hitResult:
                        tile = self.level.getTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z)
                        if tile == tiles.grass.id:
                            tile = tiles.dirt.id

                        slot = self.player.inventory.getSlotContainsID(tile)
                        if slot >= 0:
                            self.player.inventory.selectedSlot = slot
                        elif tile > 0 and tiles.tiles[tile] in User.creativeTiles:
                            self.player.inventory.getSlotContainsTile(tiles.tiles[tile])
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_scroll(self, x, y, dx, dy):
        try:
            if not self.guiScreen or (self.guiScreen and self.guiScreen.allowUserInput):
                if dy == 0:
                    return
                elif dy > 0:
                    dy = 1
                elif dy < 0:
                    dy = -1

                self.player.inventory.selectedSlot -= dy
                while self.player.inventory.selectedSlot < 0:
                    self.player.inventory.selectedSlot += len(self.player.inventory.slots)

                while self.player.inventory.selectedSlot >= len(self.player.inventory.slots):
                    self.player.inventory.selectedSlot -= len(self.player.inventory.slots)
        except Exception as e:
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_motion(self, x, y, dx, dy):
        try:
            self.mouseX = x
            self.mouseY = y
            if self.__mouseGrabbed:
                xo = dx
                yo = dy * self.__yMouseAxis
                self.player.turn(xo, yo)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_key_press(self, symbol, modifiers):
        try:
            if self.guiScreen:
                self.guiScreen.updateKeyboardEvents(key=symbol)

            if self.screenChanged:
                self.screenChanged = False
                if compat_platform != 'darwin':
                    return

            if not self.guiScreen or (self.guiScreen and self.guiScreen.allowUserInput):
                self.player.setKey(symbol, True)

                if not self.guiScreen:
                    if symbol == window.key.ESCAPE:
                        self.__pauseGame()
                    elif symbol == window.key.R:
                        self.player.resetPos()
                    elif symbol == window.key.RETURN:
                        self.level.setSpawnPos(int(self.player.x), int(self.player.y), int(self.player.z), self.player.yRot)
                        self.player.resetPos()
                    elif symbol == window.key.G and self.connectionManager is None and len(self.level.entities) < 256:
                        self.level.entities.add(Zombie(self.level, self.player.x, self.player.y, self.player.z))
                    elif symbol == window.key.B:
                        self.setScreen(InventoryScreen())
                    elif symbol == window.key.T and self.connectionManager and self.connectionManager.isConnected():
                        self.player.releaseAllKeys()
                        self.setScreen(ChatScreen())

                for i in range(9):
                    if symbol == getattr(window.key, '_' + str(i + 1)):
                        self.player.inventory.selectedSlot = i

                if symbol == window.key.Y:
                    self.__yMouseAxis = -self.__yMouseAxis
                elif symbol == window.key.F:
                    z15 = modifiers & window.key.MOD_SHIFT
                    self.__levelRenderer.drawDistance = self.__levelRenderer.drawDistance + (-1 if z15 else 1) & 3
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_key_release(self, symbol, modifiers):
        try:
            if not self.guiScreen or (self.guiScreen and self.guiScreen.allowUserInput):
                self.player.setKey(symbol, False)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_text(self, text):
        try:
            if self.screenChanged:
                self.screenChanged = False
                if compat_platform != 'darwin':
                    return

            if self.guiScreen:
                self.guiScreen.updateKeyboardEvents(char=text)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_text_motion(self, motion):
        try:
            if self.guiScreen:
                self.guiScreen.updateKeyboardEvents(motion=motion)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_draw(self):
        try:
            now = getMillis()
            passedMs = now - self.__timer.lastSyncSysClock
            j11 = getNs() // self.__timer.NS_PER_SECOND
            if passedMs > 1000:
                j13 = j11 - self.__timer.lastSyncHRClock
                d15 = passedMs / j13
                self.__timer.timeSyncAdjustment += (d15 - self.__timer.timeSyncAdjustment) * 0.2
                self.__timer.lastSyncSysClock = now
                self.__timer.lastSyncHRClock = j11
            elif passedMs < 0:
                self.__timer.lastSyncSysClock = now
                self.__timer.lastSyncHRClock = j11

            d48 = j11 / 1000.0
            d15 = (d48 - self.__timer.lastHRTime) * self.__timer.timeSyncAdjustment
            self.__timer.lastHRTime = d48
            if d15 < 0.0:
                d15 = 0.0
            elif d15 > 1.0:
                d15 = 1.0

            self.__timer.fps += d15 * self.__timer.timeScale * self.__timer.ticksPerSecond
            self.__timer.ticks = int(self.__timer.fps)
            if self.__timer.ticks > self.__timer.MAX_TICKS_PER_UPDATE:
                self.__timer.ticks = self.__timer.MAX_TICKS_PER_UPDATE

            self.__timer.fps -= float(self.__timer.ticks)
            self.__timer.a = self.__timer.fps

            for i in range(self.__timer.ticks):
                self.__ticksRan += 1
                self.__tick()

            self.__checkGlError('Pre render')
            if self.__displayActive and not self.__active:
                self.__pauseGame()

            self.__displayActive = self.__active

            if not self.hideGui:
                if self.level:
                    self.__render(self.__timer.a)
                    self.__hud.render()
                    self.__checkGlError('Rendered gui')
                else:
                    #gl.glViewport(0, 0, self.width, self.height)
                    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
                    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                    gl.glMatrixMode(gl.GL_PROJECTION)
                    gl.glLoadIdentity()
                    gl.glMatrixMode(gl.GL_MODELVIEW)
                    gl.glLoadIdentity()
                    self.initGui()

                if self.guiScreen:
                    screenWidth = self.width * 240 // self.height
                    screenHeight = self.height * 240 // self.height
                    xMouse = self.mouseX * screenWidth // self.width
                    yMouse = screenHeight - self.mouseY * screenHeight // self.height - 1
                    self.guiScreen.render(xMouse, yMouse)

            self.__checkGlError('Post render')
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def run(self):
        self.__frustum = Frustum()
        self.__dummyChunk = Chunk(None, 0, 0, 0, 0, 0, True)

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

        self.font = Font('default.png', self.textures)

        imgData = BufferUtils.createIntBuffer(256)
        imgData.clear().limit(256)

        #gl.glViewport(0, 0, self.width, self.height)

        self.levelIo = LevelIO(self)
        self.__levelGen = LevelGen(self)

        if self.server and self.user:
            self.connectionManager = ConnectionManager(self, self.server, self.port, self.user.name, self.user.mpPass)
            self.level = None
        else:
            success = False

            try:
                if self.loadMapUser:
                    success = self.loadLevel(self.loadMapUser, self.loadMapId)
                else:
                    level = self.levelIo.load(self.level, gzip.open('level.dat', 'rb'))
                    success = level != None
                    if not success:
                        level = self.levelIo.loadLegacy(self.level, gzip.open('level.dat', 'rb'))
                        success = level != None

                    self.setLevel(level)
            except Exception as e:
                print(traceback.format_exc())
                success = False

            if not success:
                self.generateLevel(1)

        self.__levelRenderer = LevelRenderer(self.textures)
        self.__particleEngine = ParticleEngine(self.level, self.textures)
        self.player = Player(self.level, MovementInputFromOptions())
        self.player.resetPos()
        if self.level:
            self.setLevel(self.level)

        self.__checkGlError('Post startup')
        self.__hud = InGameHud(self, self.width, self.height)

        lastTime = getMillis()
        frames = -2
        while self.running:
            clock.tick()
            self.dispatch_events()
            self.dispatch_event('on_draw')
            app.platform_event_loop.step(timeout=0.001)
            if frames >= 0 and not self.hideGui:
                self.flip()

            frames += 1
            while getMillis() >= lastTime + 1000:
                self.fpsString = str(frames) + ' fps, ' + str(self.__dummyChunk.updates) + ' chunk updates'
                self.__dummyChunk.updates = 0
                lastTime += 1000
                frames = 0

        self.destroy()

    def grabMouse(self):
        if self.__mouseGrabbed:
            return

        self.__mouseGrabbed = True
        self.set_exclusive_mouse(True)
        self.setScreen(None)
        self.__prevFrameTime = self.__ticksRan + 10000

    def __releaseMouse(self):
        if not self.__mouseGrabbed:
            return

        self.player.releaseAllKeys()
        self.__mouseGrabbed = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)

    def __pauseGame(self):
        if not isinstance(self.guiScreen, PauseScreen):
            self.setScreen(PauseScreen())

    def __clickMouse(self):
        if self.__hitResult:
            x = self.__hitResult.x
            y = self.__hitResult.y
            z = self.__hitResult.z
            if self.__editMode != 0:
                if self.__hitResult.f == 0: y -= 1
                if self.__hitResult.f == 1: y += 1
                if self.__hitResult.f == 2: z -= 1
                if self.__hitResult.f == 3: z += 1
                if self.__hitResult.f == 4: x -= 1
                if self.__hitResult.f == 5: x += 1

            oldTile = tiles.tiles[self.level.getTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z)]
            if self.__editMode == 0:
                if oldTile != tiles.unbreakable or self.player.userType >= 100:
                    changed = self.level.netSetTile(self.__hitResult.x, self.__hitResult.y, self.__hitResult.z, 0)
                    if oldTile and changed:
                        if self.__isMultiplayer():
                            self.connectionManager.sendBlockChange(x, y, z, self.__editMode, self.player.inventory.getSelected())

                        oldTile.destroy(self.level, self.__hitResult.x, self.__hitResult.y, self.__hitResult.z, self.__particleEngine)
            else:
                tile = tiles.tiles[self.level.getTile(x, y, z)]
                texture = self.player.inventory.getSelected()
                aabb = tiles.tiles[texture].getTileAABB(x, y, z)
                if (tile is None or tile == tiles.water or tile == tiles.calmWater or tile == tiles.lava or tile == tiles.calmLava) and \
                   (aabb is None or (False if self.player.bb.intersects(aabb) else self.level.isFree(aabb))):
                    if self.__isMultiplayer():
                        self.connectionManager.sendBlockChange(x, y, z, self.__editMode, texture)

                    self.level.netSetTile(x, y, z, self.player.inventory.getSelected())
                    tiles.tiles[texture].onBlockAdded(self.level, x, y, z)

    def __tick(self):
        for message in self.__hud.messages.copy():
            message.counter += 1

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.getTextureId('terrain.png'))

        for texture in self.textures.textureList:
            texture.onTick()
            self.textures.textureBuffer.clear()
            self.textures.textureBuffer.put(texture.imageData)
            self.textures.textureBuffer.position(0).limit(len(texture.imageData))
            gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, texture.iconIndex % 16 << 4,
                               texture.iconIndex // 16 << 4, 16, 16,
                               gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                               self.textures.textureBuffer)

        if self.connectionManager:
            if not self.connectionManager.isConnected():
                self.beginLevelLoading('Connecting..')
                self.setLoadingProgress()
            else:
                if self.connectionManager.processData:
                    if self.connectionManager.connection.connected:
                        try:
                            self.connectionManager.connection.processData()
                        except Exception as e:
                            self.setScreen(ErrorScreen('Disconnected!', 'You\'ve lost connection to the server'))
                            self.hideGui = False
                            print(traceback.format_exc())
                            self.connectionManager.connection.disconnect()
                            self.connectionManager = None

                if self.connectionManager.connection.connected:
                    i10 = int(self.player.x * 32.0)
                    i4 = int(self.player.y * 32.0)
                    i5 = int(self.player.z * 32.0)
                    i6 = int(self.player.yRot * 256.0 / 360.0) & 255
                    i9 = int(self.player.xRot * 256.0 / 360.0) & 255
                    self.connectionManager.connection.sendPacket(Packets.PLAYER_TELEPORT, [-1, i10, i4, i5, i6, i9])

        if self.guiScreen:
            self.__prevFrameTime = self.__ticksRan + 10000
            self.guiScreen.tick()
        else:
            if self.msh[window.mouse.LEFT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.__mouseGrabbed:
                self.__clickMouse()
                self.__prevFrameTime = self.__ticksRan

        if self.level:
            self.__levelRenderer.cloudTickCounter += 1
            self.level.tickEntities()
            if not self.__isMultiplayer():
                self.level.tick()

            for p in self.__particleEngine.particles.copy():
                p.tick()
                if p.removed:
                    self.__particleEngine.particles.remove(p)

            self.player.tick()

    def __isMultiplayer(self):
        return self.connectionManager is not None

    def __orientCamera(self, a):
        gl.glTranslatef(0.0, 0.0, -0.3)
        gl.glRotatef(self.player.xRotO + (self.player.xRot - self.player.xRotO) * a, 1.0, 0.0, 0.0)
        gl.glRotatef(self.player.yRotO + (self.player.yRot - self.player.yRotO) * a, 0.0, 1.0, 0.0)

        x = self.player.xo + (self.player.x - self.player.xo) * a
        y = self.player.yo + (self.player.y - self.player.yo) * a
        z = self.player.zo + (self.player.z - self.player.zo) * a
        gl.glTranslatef(-x, -y, -z)

    def __setupCamera(self, a):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(70.0, self.width / self.height, 0.2, self.__renderDistance)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        self.__orientCamera(a)

    def __pick(self, a):
        xRot = self.player.xRotO + (self.player.xRot - self.player.xRotO) * a
        yRot = self.player.yRotO + (self.player.yRot - self.player.yRotO) * a
        x = self.player.xo + (self.player.x - self.player.xo) * a
        y = self.player.yo + (self.player.y - self.player.yo) * a
        z = self.player.zo + (self.player.z - self.player.zo) * a

        vec1 = Vec3(x, y, z)
        y1 = math.cos((-yRot) * math.pi / 180.0 + math.pi)
        y2 = math.sin((-yRot) * math.pi / 180.0 + math.pi)
        x1 = math.cos((-xRot) * math.pi / 180.0)
        x2 = math.sin((-xRot) * math.pi / 180.0)
        x = (y2 * x1) * 5.0
        y = x2 * 5.0
        z = (y1 * x1) * 5.0
        vec2 = Vec3(vec1.x + x, vec1.y + y, vec1.z + z)
        self.__hitResult = self.level.clip(vec1, vec2)

    def __render(self, a):
        #gl.glViewport(0, 0, self.width, self.height)

        f4 = pow(1.0 / (4 - self.__levelRenderer.drawDistance), 0.25)
        self.__fogColorRed = 0.6 * (1.0 - f4) + f4
        self.__fogColorGreen = 0.8 * (1.0 - f4) + f4
        self.__fogColorBlue = 1.0 * (1.0 - f4) + f4
        self.__fogColorRed *= self.__fogColorMultiplier
        self.__fogColorGreen *= self.__fogColorMultiplier
        self.__fogColorBlue *= self.__fogColorMultiplier
        tile = tiles.tiles[self.level.getTile(int(self.player.x), int(self.player.y + 0.12), int(self.player.z))]
        if tile and tile.getLiquidType() != Liquid.none:
            liquid = tile.getLiquidType()
            if liquid == Liquid.water:
                self.__fogColorRed = 0.02
                self.__fogColorGreen = 0.02
                self.__fogColorBlue = 0.2
            elif liquid == Liquid.lava:
                self.__fogColorRed = 0.6
                self.__fogColorGreen = 0.1
                self.__fogColorBlue = 0.0

        gl.glClearColor(self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 0.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.__checkGlError('Set viewport')

        self.__pick(a)
        self.__checkGlError('Picked')

        self.__fogColorMultiplier = 1.0
        self.__renderDistance = float(512 >> (self.__levelRenderer.drawDistance << 1))
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
        z21 = self.level.isSolid(self.player.x, self.player.y, self.player.z, 0.1)
        self.__setupFog()
        gl.glEnable(gl.GL_FOG)
        self.__levelRenderer.render(self.player, 0)
        if z21:
            x = int(self.player.x)
            y = int(self.player.y)
            z = int(self.player.z)

            for xx in range(x - 1, x + 2):
                for yy in range(y - 1, y + 2):
                    for zz in range(z - 1, z + 2):
                        self.__levelRenderer.render(xx, yy, zz)

        self.__checkGlError('Rendered level')
        self.__toggleLight(True)
        self.__levelRenderer.renderEntities(self.__frustum, a)
        self.__toggleLight(False)
        self.__setupFog()
        self.__checkGlError('Rendered entities')
        self.__particleEngine.render(self.player, a)
        self.__checkGlError('Rendered particles')
        gl.glCallList(self.__levelRenderer.surroundLists)
        gl.glDisable(gl.GL_LIGHTING)
        self.__setupFog()
        self.__levelRenderer.renderClouds(a)
        self.__setupFog()
        gl.glEnable(gl.GL_LIGHTING)

        if self.__hitResult:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.__levelRenderer.renderHit(self.player, self.__hitResult, self.__editMode, self.player.inventory.getSelected())
            LevelRenderer.renderHitOutline(self.__hitResult, self.__editMode)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glEnable(gl.GL_LIGHTING)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.__setupFog()
        gl.glCallList(self.__levelRenderer.surroundLists + 1)

        gl.glEnable(gl.GL_BLEND)
        gl.glColorMask(False, False, False, False)
        i20 = self.__levelRenderer.render(self.player, 1)
        gl.glColorMask(True, True, True, True)
        if i20 > 0:
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__levelRenderer.textures.getTextureId('terrain.png'))
            gl.glCallLists(self.__levelRenderer.dummyBuffer.capacity(), gl.GL_INT, self.__levelRenderer.dummyBuffer)
            gl.glDisable(gl.GL_TEXTURE_2D)

        gl.glDepthMask(True)
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_FOG)
        gl.glDisable(gl.GL_TEXTURE_2D)
        if self.__hitResult:
            gl.glDepthFunc(gl.GL_LESS)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.__levelRenderer.renderHit(self.player, self.__hitResult, self.__editMode, self.player.inventory.getSelected())
            LevelRenderer.renderHitOutline(self.__hitResult, self.__editMode)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glDepthFunc(gl.GL_LEQUAL)

    def __toggleLight(self, z1):
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

    def __setupFog(self):
        gl.glFogfv(gl.GL_FOG_COLOR, self.__getBuffer(self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 1.0))
        gl.glNormal3f(0.0, -1.0, 0.0)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        currentTile = tiles.tiles[self.level.getTile(int(self.player.x), int(self.player.y + 0.12), int(self.player.z))]
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
            gl.glFogf(gl.GL_FOG_END, self.__renderDistance)
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.__getBuffer(1.0, 1.0, 1.0, 1.0))

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT)
        gl.glEnable(gl.GL_LIGHTING)

    def __getBuffer(self, a, b, c, d):
        self.__lb.clear()
        self.__lb.put(a).put(b).put(c).put(d)
        self.__lb.flip()
        return self.__lb

    def beginLevelLoading(self, title):
        if not self.running:
            raise StopGameException
        else:
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
        if not self.running:
            raise StopGameException
        else:
            self.__text = status
            self.setLoadingProgress()

    def setLoadingProgress(self):
        if not self.running:
            raise StopGameException
        else:
            screenWidth = self.width * 240 // self.height
            screenHeight = self.height * 240 // self.height

            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            t = tesselator
            gl.glEnable(gl.GL_TEXTURE_2D)
            id_ = self.textures.getTextureId('dirt.png')
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
        self.setLevel(self.__levelGen.generateLevel(name, 128 << i, 128 << i, 64))

    def saveLevel(self, i, name):
        return self.levelIo.save(self.level, gzip.open('level.dat', 'wb'))

    def loadLevel(self, name, i):
        level = self.levelIo.load(self.level, gzip.open('level.dat', 'rb'))
        if not level:
            return False
        else:
            self.setLevel(level)
            return True

    def setLevel(self, level):
        self.level = level
        if self.__levelRenderer:
            self.__levelRenderer.setLevel(level)

        if self.__particleEngine:
            self.__particleEngine.particles.clear()

        if self.player:
            self.player.setLevel(level)
            self.player.resetPos()

        gc.collect()

    def addChatMessage(self, string):
        self.__hud.messages.insert(0, ChatLine(string))

        while len(self.__hud.messages) > 50:
            self.__hud.messages.pop(len(self.__hud.messages) - 1)

if __name__ == '__main__':
    fullScreen = False
    server = None
    port = None
    name = 'guest'
    mpPass = ''
    for i, arg in enumerate(sys.argv):
        if arg == '-fullscreen':
            fullScreen = True
        elif arg == '-server':
            server, port = sys.argv[i + 1].split(':')
        elif arg == '-user':
            name = sys.argv[i + 1]
        elif arg == '-mppass':
            mpPass = sys.argv[i + 1]

    game = Minecraft(fullScreen, width=854, height=480, caption='Minecraft 0.0.21a')
    game.user = User(name, 0, mpPass)
    if server and port:
        game.setServer(server, int(port))
    game.run()
