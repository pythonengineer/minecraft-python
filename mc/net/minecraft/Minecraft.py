import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['audio'] = ('openal', 'silent')

from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.ProgressListener import ProgressListener
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import SoundType, tiles
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelIO import LevelIO
from mc.net.minecraft.level.levelgen.LevelGen import LevelGen
from mc.net.minecraft.character.Vec3 import Vec3
from mc.net.minecraft.character.Zombie import Zombie
from mc.net.minecraft.character.ZombieModel import ZombieModel
from mc.net.minecraft.player.Player import Player
from mc.net.minecraft.player.MovementInputFromOptions import MovementInputFromOptions
from mc.net.minecraft.net.ConnectionManager import ConnectionManager
from mc.net.minecraft.net.NetworkPlayer import NetworkPlayer
from mc.net.minecraft.net.Packet import Packet
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
from mc.net.minecraft.renderer.RenderHelper import RenderHelper
from mc.net.minecraft.renderer.Textures import Textures
from mc.net.minecraft.renderer.Frustum import Frustum
from mc.net.minecraft.renderer.Chunk import Chunk
from mc.net.minecraft.sound.SoundManager import SoundManager
from mc.net.minecraft.sound.SoundPlayer import SoundPlayer
from mc.net.minecraft.User import User
from mc.CompatibilityShims import ByteArrayInputStream, ByteArrayOutputStream
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis, getNs
from pyglet import window, app, canvas, clock, media, gl, compat_platform

import traceback
import math
import time
import gzip
import sys
import os
import gc

GL_DEBUG = False

class Minecraft(window.Window):
    VERSION_STRING = '0.0.22a_05'
    __timer = Timer(20.0)
    level = None
    levelRenderer = None
    player = None
    particleEngine = None

    user = None
    minecraftUri = ''

    __active = False
    yMouseAxis = 1
    editMode = 0
    guiScreen = None

    __ticksRan = 0

    loadMapUser = ''
    loadMapId = 0

    hud = None
    connectionManager = None

    server = ''
    port = 0

    running = True
    fpsString = ''

    ksh = window.key.KeyStateHandler()
    msh = window.mouse.MouseStateHandler()
    mouseGrabbed = False
    mouseX = 0
    mouseY = 0

    __prevFrameTime = 0

    hitResult = None

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
                self.hideGui = False
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
            if self.soundPlayer:
                self.soundPlayer.running = False
        except Exception as e:
            print(traceback.format_exc())

        try:
            LevelIO.save(self.level, gzip.open('level.dat', 'wb'))
        except Exception as e:
            print(traceback.format_exc())

    def on_close(self):
        self.running = False

    def on_activate(self):
        self.__active = True

        # Remove this hack when the window boundary issue is fixed upstream:
        if self.mouseGrabbed and compat_platform == 'win32':
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
                    if not self.mouseGrabbed:
                        self.grabMouse()
                    elif button == window.mouse.LEFT:
                        self.__clickMouse()
                        self.__prevFrameTime = self.__ticksRan
                    elif button == window.mouse.RIGHT:
                        self.editMode = (self.editMode + 1) % 2
                    elif button == window.mouse.MIDDLE and self.hitResult:
                        tile = self.level.getTile(self.hitResult.x, self.hitResult.y, self.hitResult.z)
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
                if dy != 0:
                    self.player.inventory.scrollHotbar(dy)
        except Exception as e:
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_motion(self, x, y, dx, dy):
        try:
            self.mouseX = x
            self.mouseY = y
            if self.mouseGrabbed:
                xo = dx
                yo = dy * self.yMouseAxis
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
                        self.pauseGame()
                    elif symbol == window.key.R:
                        self.player.resetPos()
                    elif symbol == window.key.M:
                        self.soundPlayer.enabled = not self.soundPlayer.enabled
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
                    self.yMouseAxis = -self.yMouseAxis
                elif symbol == window.key.F:
                    z15 = modifiers & window.key.MOD_SHIFT
                    self.levelRenderer.drawDistance = self.levelRenderer.drawDistance + (-1 if z15 else 1) & 3
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

            self.soundPlayer.setListener(self.player, self.__timer.fps)

            if self.renderHelper.displayActive and not self.__active:
                self.pauseGame()

            self.__displayActive = self.__active

            if not self.hideGui:
                if self.level:
                    self.__render(self.__timer.a)
                    self.hud.render()
                    self.__checkGlError('Rendered gui')
                else:
                    #gl.glViewport(0, 0, self.width, self.height)
                    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
                    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                    gl.glMatrixMode(gl.GL_PROJECTION)
                    gl.glLoadIdentity()
                    gl.glMatrixMode(gl.GL_MODELVIEW)
                    gl.glLoadIdentity()
                    self.renderHelper.initGui()

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

        self.loadingScreen = ProgressListener(self)
        self.renderHelper = RenderHelper(self)
        self.levelIo = LevelIO(self.loadingScreen)
        self.__levelGen = LevelGen(self.loadingScreen)
        self.soundManager = SoundManager()

        path = os.path.abspath(os.path.join(os.getcwd(), 'mc', 'resources', 'sound'))
        for root, dirs, files in os.walk(path):
            for fileName in files:
                folder = os.path.basename(root)
                if folder == 'music':
                    self.soundManager.registerMusic(os.path.join(root, fileName), fileName)
                else:
                    self.soundManager.registerSound(os.path.join(root, fileName), os.path.join(folder, fileName).replace('\\', '/'))

        if self.server and self.user:
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

        self.levelRenderer = LevelRenderer(self.textures)
        self.particleEngine = ParticleEngine(self.level, self.textures)
        self.player = Player(self.level, MovementInputFromOptions())
        self.player.resetPos()
        if self.level:
            self.setLevel(self.level)

        try:
            self.soundPlayer = SoundPlayer()
            self.soundPlayer.player = media.Player()
            self.soundPlayer.listener = media.get_audio_driver().get_listener()
            self.soundPlayer.entity = self.player
        except:
            print(traceback.format_exc())

        self.__checkGlError('Post startup')
        self.hud = InGameHud(self, self.width, self.height)
        if self.server and self.user:
            self.connectionManager = ConnectionManager(self, self.server, self.port, self.user.name, self.user.mpPass)

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
        if self.mouseGrabbed:
            return

        self.mouseGrabbed = True
        self.set_exclusive_mouse(True)
        self.setScreen(None)
        self.__prevFrameTime = self.__ticksRan + 10000

    def __releaseMouse(self):
        if not self.mouseGrabbed:
            return

        self.player.releaseAllKeys()
        self.mouseGrabbed = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)

    def pauseGame(self):
        if not isinstance(self.guiScreen, PauseScreen):
            self.setScreen(PauseScreen())

    def __clickMouse(self):
        if self.hitResult:
            x = self.hitResult.x
            y = self.hitResult.y
            z = self.hitResult.z
            if self.editMode != 0:
                if self.hitResult.f == 0: y -= 1
                if self.hitResult.f == 1: y += 1
                if self.hitResult.f == 2: z -= 1
                if self.hitResult.f == 3: z += 1
                if self.hitResult.f == 4: x -= 1
                if self.hitResult.f == 5: x += 1

            oldTile = tiles.tiles[self.level.getTile(x, y, z)]
            if self.editMode == 0:
                if oldTile != tiles.unbreakable or self.player.userType >= 100:
                    changed = self.level.netSetTile(x, y, z, 0)
                    if oldTile and changed:
                        if self.__isMultiplayer():
                            self.connectionManager.sendBlockChange(x, y, z, self.editMode, self.player.inventory.getSelected())

                        if oldTile.soundType != SoundType.none:
                            self.level.playSound('step.' + oldTile.soundType.name,
                                                 x, y, z,
                                                 (oldTile.soundType.getVolume() + 1.0) / 2.0,
                                                 oldTile.soundType.getPitch() * 0.8)
                            oldTile.destroy(self.level, x, y, z, self.particleEngine)
            else:
                tile = tiles.tiles[self.level.getTile(x, y, z)]
                texture = self.player.inventory.getSelected()
                aabb = tiles.tiles[texture].getTileAABB(x, y, z)
                if (tile is None or tile == tiles.water or tile == tiles.calmWater or tile == tiles.lava or tile == tiles.calmLava) and \
                   (aabb is None or (False if self.player.bb.intersects(aabb) else self.level.isFree(aabb))):
                    if self.__isMultiplayer():
                        self.connectionManager.sendBlockChange(x, y, z, self.editMode, texture)

                    self.level.netSetTile(x, y, z, self.player.inventory.getSelected())
                    tiles.tiles[texture].onBlockAdded(self.level, x, y, z)

    def __tick(self):
        if self.soundPlayer:
            if getMillis() > self.soundManager.lastMusic and \
               self.soundManager.playMusic(self.soundPlayer, 'calm'):
                self.soundManager.lastMusic = getMillis() + math.floor(self.soundManager.random.random() * 900000) + 300000

        for message in self.hud.messages.copy():
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

        if self.connectionManager and not isinstance(self.guiScreen, ErrorScreen):
            if not self.connectionManager.isConnected():
                self.loadingScreen.beginLevelLoading('Connecting..')
                self.loadingScreen.setLoadingProgress()
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

                if self.connectionManager and self.connectionManager.connected:
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
            if self.msh[window.mouse.LEFT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.mouseGrabbed:
                self.__clickMouse()
                self.__prevFrameTime = self.__ticksRan

        if self.level:
            self.levelRenderer.cloudTickCounter += 1
            self.level.tickEntities()
            if not self.__isMultiplayer():
                self.level.tick()

            self.particleEngine.tick()
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
        gluPerspective(70.0, self.width / self.height, 0.05, self.renderHelper.renderDistance)
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
        self.hitResult = self.level.clip(vec1, vec2)

    def __render(self, a):
        #gl.glViewport(0, 0, self.width, self.height)

        f4 = pow(1.0 / (4 - self.levelRenderer.drawDistance), 0.25)
        self.renderHelper.fogColorRed = 0.6 * (1.0 - f4) + f4
        self.renderHelper.fogColorGreen = 0.8 * (1.0 - f4) + f4
        self.renderHelper.fogColorBlue = 1.0 * (1.0 - f4) + f4
        self.renderHelper.fogColorRed *= self.renderHelper.fogColorMultiplier
        self.renderHelper.fogColorGreen *= self.renderHelper.fogColorMultiplier
        self.renderHelper.fogColorBlue *= self.renderHelper.fogColorMultiplier
        tile = tiles.tiles[self.level.getTile(int(self.player.x), int(self.player.y + 0.12), int(self.player.z))]
        if tile and tile.getLiquidType() != Liquid.none:
            liquid = tile.getLiquidType()
            if liquid == Liquid.water:
                self.renderHelper.fogColorRed = 0.02
                self.renderHelper.fogColorGreen = 0.02
                self.renderHelper.fogColorBlue = 0.2
            elif liquid == Liquid.lava:
                self.renderHelper.fogColorRed = 0.6
                self.renderHelper.fogColorGreen = 0.1
                self.renderHelper.fogColorBlue = 0.0

        gl.glClearColor(self.renderHelper.fogColorRed, self.renderHelper.fogColorGreen, self.renderHelper.fogColorBlue, 0.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.__checkGlError('Set viewport')

        self.__pick(a)

        self.renderHelper.fogColorMultiplier = 1.0
        self.renderHelper.renderDistance = float(512 >> (self.levelRenderer.drawDistance << 1))
        self.__setupCamera(a)

        gl.glEnable(gl.GL_CULL_FACE)

        self.__frustum.calculateFrustum()
        for chunk in self.levelRenderer.sortedChunks:
            chunk.isInFrustum(self.__frustum)

        for chunk in self.levelRenderer.dirtyChunks.copy():
            chunk.rebuild()
            self.levelRenderer.dirtyChunks.remove(chunk)

        z21 = self.level.isSolid(self.player.x, self.player.y, self.player.z, 0.1)
        self.renderHelper.setupFog()
        gl.glEnable(gl.GL_FOG)
        self.levelRenderer.render(self.player, 0)
        if z21:
            x = int(self.player.x)
            y = int(self.player.y)
            z = int(self.player.z)

            for xx in range(x - 1, x + 2):
                for yy in range(y - 1, y + 2):
                    for zz in range(z - 1, z + 2):
                        self.levelRenderer.render(xx, yy, zz)

        self.renderHelper.toggleLight(True)
        self.levelRenderer.renderEntities(self.__frustum, a)
        self.renderHelper.toggleLight(False)
        self.renderHelper.setupFog()
        self.particleEngine.render(self.player, a)
        gl.glCallList(self.levelRenderer.surroundLists)
        gl.glDisable(gl.GL_LIGHTING)
        self.renderHelper.setupFog()
        self.levelRenderer.renderClouds(a)
        self.renderHelper.setupFog()
        gl.glEnable(gl.GL_LIGHTING)

        if self.hitResult:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.levelRenderer.renderHit(self.player, self.hitResult, self.editMode, self.player.inventory.getSelected())
            LevelRenderer.renderHitOutline(self.hitResult, self.editMode)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glEnable(gl.GL_LIGHTING)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.renderHelper.setupFog()
        gl.glCallList(self.levelRenderer.surroundLists + 1)

        gl.glEnable(gl.GL_BLEND)
        gl.glColorMask(False, False, False, False)
        i20 = self.levelRenderer.render(self.player, 1)
        gl.glColorMask(True, True, True, True)
        if i20 > 0:
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.levelRenderer.textures.getTextureId('terrain.png'))
            gl.glCallLists(self.levelRenderer.dummyBuffer.capacity(), gl.GL_INT, self.levelRenderer.dummyBuffer)
            gl.glDisable(gl.GL_TEXTURE_2D)

        gl.glDepthMask(True)
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_FOG)
        gl.glDisable(gl.GL_TEXTURE_2D)
        if self.hitResult:
            gl.glDepthFunc(gl.GL_LESS)
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.levelRenderer.renderHit(self.player, self.hitResult, self.editMode, self.player.inventory.getSelected())
            LevelRenderer.renderHitOutline(self.hitResult, self.editMode)
            gl.glEnable(gl.GL_ALPHA_TEST)
            gl.glDepthFunc(gl.GL_LEQUAL)

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
        if level:
            level.rendererContext = self

        if self.levelRenderer:
            self.levelRenderer.setLevel(level)

        if self.particleEngine:
            self.particleEngine.particles.clear()

        if self.player:
            self.player.setLevel(level)
            self.player.resetPos()

        gc.collect()

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

    game = Minecraft(fullScreen, width=854, height=480, caption='Minecraft 0.0.22a_05')
    game.user = User(name, 0, mpPass)
    if server and port:
        game.setServer(server, int(port))
    game.run()
