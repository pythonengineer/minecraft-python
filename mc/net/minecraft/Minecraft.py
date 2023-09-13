import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['audio'] = ('openal', 'silent')

from mc.net.minecraft import StopGameException
from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.Options import Options
from mc.net.minecraft.LevelLoaderListener import LevelLoaderListener
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.phys.AABB import AABB
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import SoundType, tiles
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.level.LevelIO import LevelIO
from mc.net.minecraft.level.levelgen.LevelGen import LevelGen
from mc.net.minecraft.model.ModelCache import ModelCache
from mc.net.minecraft.model.Vec3 import Vec3
from mc.net.minecraft.player.Player import Player
from mc.net.minecraft.player.KeyboardInput import KeyboardInput
from mc.net.minecraft.net.Client import Client
from mc.net.minecraft.net.NetworkPlayer import NetworkPlayer
from mc.net.minecraft.net.Packet import Packet
from mc.net.minecraft.net import Packets
from mc.net.minecraft.gui.Font import Font
from mc.net.minecraft.gui.ChatScreen import ChatScreen
from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
from mc.net.minecraft.gui.PauseScreen import PauseScreen
from mc.net.minecraft.gui.DeathScreen import DeathScreen
from mc.net.minecraft.gui.Gui import Gui
from mc.net.minecraft.item.Arrow import Arrow
from mc.net.minecraft.item.Item import Item
from mc.net.minecraft.mob.Mob import Mob
from mc.net.minecraft.particle.ParticleEngine import ParticleEngine
from mc.net.minecraft.particle.WaterDropParticle import WaterDropParticle
from mc.net.minecraft.renderer.texture.WaterTexture import WaterTexture
from mc.net.minecraft.renderer.texture.LavaTexture import LavaTexture
from mc.net.minecraft.renderer.DirtyChunkSorter import DirtyChunkSorter
from mc.net.minecraft.renderer.LevelRenderer import LevelRenderer
from mc.net.minecraft.renderer.GameRenderer import GameRenderer
from mc.net.minecraft.renderer.Textures import Textures
from mc.net.minecraft.renderer.Tesselator import tesselator
from mc.net.minecraft.renderer.Frustum import Frustum
from mc.net.minecraft.renderer.Chunk import Chunk
from mc.net.minecraft.gamemode.CreativeGameMode import CreativeGameMode
from mc.net.minecraft.gamemode.SurvivalGameMode import SurvivalGameMode
from mc.net.minecraft.sound.SoundEngine import SoundEngine
from mc.net.minecraft.sound.SoundPlayer import SoundPlayer
from mc.net.minecraft.PlayerTextureLoader import PlayerTextureLoader
from mc.net.minecraft.User import User
from mc.CompatibilityShims import ByteArrayInputStream, ByteArrayOutputStream
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis, getNs
from pyglet import window, app, canvas, clock, media, gl, compat_platform

import traceback
import random
import math
import time
import gzip
import sys
import os
import gc

GL_DEBUG = False

class Minecraft(window.Window):
    VERSION_STRING = '0.28_01'
    level = None
    levelRenderer = None
    player = None
    particleEngine = None

    minecraftUri = ''

    __active = False

    gui = None
    networkClient = None

    ksh = window.key.KeyStateHandler()
    msh = window.mouse.MouseStateHandler()
    mouseGrabbed = False
    mouseX = 0
    mouseY = 0

    options = None

    guiScreenChanged = False

    def __init__(self, fullscreen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__fullscreen = fullscreen

        self.gamemode = CreativeGameMode(self)
        self.__timer = Timer(20.0)
        self.user = None
        self.guiScreen = None
        self.raining = False
        self.loadingScreen = LevelLoaderListener(self)
        self.gameRenderer = GameRenderer(self)
        self.levelIo = LevelIO(self.loadingScreen)
        self.soundEngine = SoundEngine()
        self.__frames = 0
        self.loadMapUser = ''
        self.loadMapId = 0
        self.hideScreen = False
        self.hitResult = None
        self.__clickCounter = 0

        self.server = ''
        self.port = 0

        self.running = False
        self.fpsString = ''

        self.__oFrames = 0

        self.push_handlers(self.ksh)
        self.push_handlers(self.msh)

    def setServer(self, server, port):
        self.server = server
        self.port = port

    def setScreen(self, screen):
        if not isinstance(self.guiScreen, ErrorScreen):
            if self.guiScreen or screen:
                self.guiScreenChanged = True
            if self.guiScreen:
                self.guiScreen.removed()

            if not screen and self.player.health <= 0:
                screen = DeathScreen()

            self.guiScreen = screen
            if screen:
                self.__releaseMouse()
                screenWidth = self.width * 240 // self.height
                screenHeight = self.height * 240 // self.height
                screen.init(self, screenWidth, screenHeight)
                self.hideScreen = False
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
                sys.exit(0)

    def destroy(self):
        try:
            if self.soundPlayer:
                self.soundPlayer.running = False
        except Exception as e:
            print(traceback.format_exc())

        try:
            self.levelIo.save(self.level, gzip.open('level.dat', 'wb'))
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
                self.guiScreen.mouseEvent(button)

            if self.guiScreenChanged:
                self.guiScreenChanged = False
                if compat_platform != 'darwin':
                    return

            if not self.guiScreen or self.guiScreen.allowUserInput:
                if not self.mouseGrabbed:
                    self.grabMouse()
                elif button == window.mouse.LEFT:
                    self.__clickMouse(0)
                    self.__oFrames = self.__frames
                elif button == window.mouse.RIGHT:
                    self.__clickMouse(1)
                    self.__oFrames = self.__frames
                elif button == window.mouse.MIDDLE and self.hitResult:
                    tile = self.level.getTile(self.hitResult.x,
                                              self.hitResult.y,
                                              self.hitResult.z)
                    if tile == tiles.grass.id:
                        tile = tiles.dirt.id
                    elif tile == tiles.slabFull.id:
                        tile = tiles.slabHalf.id

                    self.player.inventory.grabTexture(tile, isinstance(self.gamemode, CreativeGameMode))
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_scroll(self, x, y, dx, dy):
        try:
            if not self.guiScreen or self.guiScreen.allowUserInput:
                if dy != 0:
                    self.player.inventory.swapPaint(dy)
        except Exception as e:
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_motion(self, x, y, dx, dy):
        try:
            self.mouseX = x
            self.mouseY = y

            if not self.mouseGrabbed:
                return

            xo = dx
            if self.options.invertYMouse:
                yo = dy * -1
            else:
                yo = dy

            self.player.turn(xo, yo)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_key_press(self, symbol, modifiers):
        try:
            if self.guiScreen:
                self.guiScreen.keyboardEvent(key=symbol)

            if self.guiScreenChanged:
                self.guiScreenChanged = False
                if compat_platform != 'darwin':
                    return

            if not self.guiScreen or self.guiScreen.allowUserInput:
                if symbol != self.options.toggleFog.key:
                    self.player.setKey(symbol, True)

                    if symbol == window.key.ESCAPE:
                        self.pauseScreen()
                    elif symbol == window.key.F5 and not self.networkClient:
                        self.raining = not self.raining
                    elif symbol == window.key.TAB and not self.networkClient and self.player.arrows > 0:
                        self.level.addEntity(Arrow(self.level, self.player, self.player.x,
                                                   self.player.y, self.player.z,
                                                   self.player.yRot, self.player.xRot, 1.2))
                        self.player.arrows -= 1
                    elif symbol == self.options.chat.key and self.networkClient and self.networkClient.isConnected():
                        self.player.releaseAllKeys()
                        self.setScreen(ChatScreen())
                    elif symbol == self.options.build.key:
                        self.gamemode.handleOpenInventory()

                    if isinstance(self.gamemode, CreativeGameMode):
                        if symbol == self.options.load.key:
                            self.player.resetPos()
                        elif symbol == self.options.save.key:
                            self.level.setSpawnPos(int(self.player.x),
                                                   int(self.player.y),
                                                   int(self.player.z),
                                                   self.player.yRot)
                            self.player.resetPos()

                    for i in range(9):
                        if symbol == getattr(window.key, '_' + str(i + 1)):
                            self.player.inventory.selected = i
                else:
                    shift = modifiers & window.key.MOD_SHIFT
                    self.options.setOption(4, -1 if shift else 1)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_key_release(self, symbol, modifiers):
        try:
            if not self.guiScreen or self.guiScreen.allowUserInput:
                self.player.setKey(symbol, False)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_text(self, text):
        try:
            if self.guiScreenChanged:
                self.guiScreenChanged = False
                if compat_platform != 'darwin':
                    return

            if self.guiScreen:
                self.guiScreen.keyboardEvent(char=text)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_text_motion(self, motion):
        try:
            if self.guiScreen:
                self.guiScreen.keyboardEvent(motion=motion)
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_draw(self):
        try:
            now = getMillis()
            passedMs = now - self.__timer.msPerTick
            j11 = getNs() // Timer.NS_PER_SECOND
            if passedMs > 1000:
                j13 = j11 - self.__timer.passedTime
                d15 = passedMs / j13
                self.__timer.averageFrameTime += (d15 - self.__timer.averageFrameTime) * 0.2
                self.__timer.msPerTick = now
                self.__timer.passedTime = j11
            elif passedMs < 0:
                self.__timer.msPerTick = now
                self.__timer.passedTime = j11

            d48 = j11 / 1000.0
            d15 = (d48 - self.__timer.lastTime) * self.__timer.averageFrameTime
            self.__timer.lastTime = d48
            if d15 < 0.0:
                d15 = 0.0
            elif d15 > 1.0:
                d15 = 1.0

            self.__timer.ticks += d15 * self.__timer.fps * self.__timer.ticksPerSecond
            self.__timer.frames = int(self.__timer.ticks)
            if self.__timer.frames > Timer.MAX_TICKS_PER_UPDATE:
                self.__timer.frames = Timer.MAX_TICKS_PER_UPDATE

            self.__timer.ticks -= float(self.__timer.frames)
            self.__timer.alpha = self.__timer.ticks

            for i in range(self.__timer.frames):
                self.__frames += 1
                self.__tick()

            self.__checkGlError('Pre render')

            if not self.hideScreen:
                gl.glEnable(gl.GL_TEXTURE_2D)
                self.gamemode.render(self.__timer.alpha)
                self.soundPlayer.setListener(self.player, self.__timer.frames)

                if self.gameRenderer.displayActive and not self.__active:
                    self.pauseScreen()

                self.gameRenderer.displayActive = self.__active

                if not self.hideScreen:
                    screenWidth = self.width * 240 // self.height
                    screenHeight = self.height * 240 // self.height
                    xMouse = self.mouseX * screenWidth // self.width
                    yMouse = screenHeight - self.mouseY * screenHeight // self.height - 1

                    if self.level:
                        self.__render(self.__timer.alpha)
                        self.gui.render(self.__timer.alpha, self.guiScreen is not None, xMouse, yMouse)
                    else:
                        #gl.glViewport(0, 0, self.width, self.height)
                        gl.glClearColor(0.0, 0.0, 0.0, 0.0)
                        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                        gl.glMatrixMode(gl.GL_PROJECTION)
                        gl.glLoadIdentity()
                        gl.glMatrixMode(gl.GL_MODELVIEW)
                        gl.glLoadIdentity()
                        self.gameRenderer.render()

                    if self.guiScreen:
                        self.guiScreen.render(xMouse, yMouse)

            if self.options.limitFramerate:
                time.sleep(0.005)

            self.__checkGlError('Post render')
        except Exception as e:
            print(traceback.format_exc())
            self.setScreen(ErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def run(self):
        self.running = True
        self.__frustum = Frustum()
        self.__dummyChunk = Chunk(None, 0, 0, 0, 0, 0, True)
        PlayerTextureLoader(self).start()

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

        name = 'minecraft'
        home = os.path.expanduser('~') or '.'
        if 'unix' in sys.platform or 'linux' in sys.platform or \
           'solaris' in sys.platform or 'sunos' in sys.platform:
            file = os.path.join(home, '.' + name)
        elif 'win' in sys.platform:
            if 'APPDATA' in os.environ:
                file = os.path.join(os.environ['APPDATA'], '.' + name)
            else:
                file = os.path.join(home, '.' + name)
        elif 'mac' in sys.platform or 'darwin' in sys.platform:
            file = os.path.join(home, 'Library', 'Application Support', name)
        else:
            file = os.path.join(home, name)

        if not os.path.isdir(file):
            os.mkdir(file)

        if not os.path.isdir(file):
            raise RuntimeError(f'The working directory could not be created: {file}')

        self.options = Options(self, file)
        self.textures = Textures(self.options)
        self.textures.addDynamicTexture(LavaTexture())
        self.textures.addDynamicTexture(WaterTexture())
        self.font = Font(self.options, 'default.png', self.textures)

        imgData = BufferUtils.createIntBuffer(256)
        imgData.clear().limit(256)

        self.levelRenderer = LevelRenderer(self, self.textures)

        Item.initModels()
        Mob(None).modelCache = ModelCache()

        #gl.glViewport(0, 0, self.width, self.height)

        if self.server and self.user:
            level = Level()
            level.setDataLegacy(8, 8, 8, bytearray(512))
            self.loadLevel(level)
        else:
            success = False

            try:
                level = self.levelIo.load(gzip.open('level.dat', 'rb'))
                success = level is not None
                if success:
                    self.loadLevel(level)
            except Exception as e:
                print(traceback.format_exc())
                success = False

            if not self.level:
                self.generateLevel(1)

        self.particleEngine = ParticleEngine(self.level, self.textures)

        path = os.path.abspath(os.path.join(os.getcwd(), 'mc', 'resources', 'sound'))
        for root, dirs, files in os.walk(path):
            for fileName in files:
                folder = os.path.basename(root)
                if folder == 'music':
                    self.soundEngine.registerMusic(os.path.join(root, fileName), fileName)
                else:
                    self.soundEngine.registerSound(os.path.join(root, fileName), os.path.join(folder, fileName).replace('\\', '/'))

        try:
            self.soundPlayer = SoundPlayer(self.options)
            self.soundPlayer.player = media.Player()
            self.soundPlayer.listener = media.get_audio_driver().get_listener()
        except:
            print(traceback.format_exc())

        self.__checkGlError('Post startup')
        self.gui = Gui(self, self.width, self.height)
        if self.server and self.user:
            self.networkClient = Client(self, self.server, self.port, self.user.name, self.user.mpPass)

        lastTime = getMillis()
        frames = -2
        try:
            while self.running:
                clock.tick()
                self.dispatch_events()
                self.dispatch_event('on_draw')
                app.platform_event_loop.step(timeout=0.001)
                if not self.hideScreen and frames >= 0:
                    self.flip()

                frames += 1
                while getMillis() >= lastTime + 1000:
                    self.fpsString = str(frames) + ' fps, ' + str(self.__dummyChunk.updates) + ' chunk updates'
                    self.__dummyChunk.updates = 0
                    lastTime += 1000
                    frames = 0
        except StopGameException:
            pass
        finally:
            self.destroy()

    def grabMouse(self):
        if self.mouseGrabbed:
            return

        self.mouseGrabbed = True
        self.set_exclusive_mouse(True)
        self.setScreen(None)
        self.__oFrames = self.__frames + 10000

    def __releaseMouse(self):
        if not self.mouseGrabbed:
            return

        self.player.releaseAllKeys()
        self.mouseGrabbed = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)

    def pauseScreen(self):
        if not isinstance(self.guiScreen, PauseScreen):
            self.setScreen(PauseScreen())

    def __clickMouse(self, editMode):
        item = self.player.inventory.getSelected()
        if editMode == 0:
            if self.__clickCounter > 0:
                return

            self.gameRenderer.tileRenderer.rot = -1
            self.gameRenderer.tileRenderer.move = True
        elif editMode == 1 and item > 0 and self.gamemode.removeResource(self.player, item):
            self.gameRenderer.tileRenderer.progress = 0.0
            return

        if not self.hitResult:
            if editMode == 0 and not isinstance(self.gamemode, CreativeGameMode):
                self.__clickCounter = 10

            return

        if self.hitResult.typeOfHit == 1:
            if editMode == 0:
                self.hitResult.entity.hurt(self.player, 4)

            return
        elif self.hitResult.typeOfHit != 0:
            return

        x = self.hitResult.x
        y = self.hitResult.y
        z = self.hitResult.z
        if editMode != 0:
            if self.hitResult.sideHit == 0: y -= 1
            if self.hitResult.sideHit == 1: y += 1
            if self.hitResult.sideHit == 2: z -= 1
            if self.hitResult.sideHit == 3: z += 1
            if self.hitResult.sideHit == 4: x -= 1
            if self.hitResult.sideHit == 5: x += 1

        oldTile = tiles.tiles[self.level.getTile(x, y, z)]
        if editMode == 0:
            if oldTile != tiles.unbreakable or self.player.userType >= 100:
                self.gamemode.startDestroyBlock(x, y, z)
                return
        else:
            texture = self.player.inventory.getSelected()
            if texture <= 0:
                return

            tile = tiles.tiles[self.level.getTile(x, y, z)]
            if tile and tile != tiles.water and tile != tiles.calmWater and tile != tiles.lava and tile != tiles.calmLava:
                return

            aabb = tiles.tiles[texture].getTileAABB(x, y, z)
            if aabb and (self.player.bb.intersectsBB(aabb) or not self.level.isFree(aabb)):
                return
            elif not self.gamemode.consumeBlock(texture):
                return

            if self.isOnlineClient():
                self.networkClient.sendTileUpdated(x, y, z, editMode, texture)

            self.level.netSetTile(x, y, z, texture)
            self.gameRenderer.tileRenderer.progress = 0.0
            tiles.tiles[texture].onPlace(self.level, x, y, z)

    def __tick(self):
        if self.soundPlayer:
            if self.options.music:
                if getMillis() > self.soundEngine.lastMusic and \
                   self.soundEngine.playMusic(self.soundPlayer, 'calm'):
                    self.soundEngine.lastMusic = getMillis() + math.floor(self.soundEngine.random.random() * 900000) + 300000
            else:
                self.soundEngine.stopMusic()

        self.gamemode.tick()
        self.gui.tickCounter += 1
        for message in self.gui.messages.copy():
            message.counter += 1

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.loadTexture('terrain.png'))

        for texture in self.textures.textureList:
            texture.anaglyph = self.options.anaglyph3d
            texture.tick()
            self.textures.pixels.clear()
            self.textures.pixels.put(texture.pixels)
            self.textures.pixels.position(0).limit(len(texture.pixels))
            gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, texture.tex % 16 << 4,
                               texture.tex // 16 << 4, 16, 16, gl.GL_RGBA,
                               gl.GL_UNSIGNED_BYTE, self.textures.pixels)

        if self.networkClient and not isinstance(self.guiScreen, ErrorScreen):
            if not self.networkClient.isConnected():
                self.loadingScreen.beginLevelLoading('Connecting..')
                self.loadingScreen.setLoadingProgress()
            else:
                if self.networkClient.processData:
                    if self.networkClient.serverConnection.connected:
                        try:
                            self.networkClient.serverConnection.processData()
                        except Exception as e:
                            self.setScreen(ErrorScreen('Disconnected!', 'You\'ve lost connection to the server'))
                            self.hideScreen = False
                            print(traceback.format_exc())
                            self.networkClient.serverConnection.disconnect()
                            self.networkClient = None

                if self.networkClient and self.networkClient.connected:
                    i10 = int(self.player.x * 32.0)
                    i4 = int(self.player.y * 32.0)
                    i5 = int(self.player.z * 32.0)
                    i6 = int(self.player.yRot * 256.0 / 360.0) & 255
                    i9 = int(self.player.xRot * 256.0 / 360.0) & 255
                    self.networkClient.serverConnection.sendPacket(Packets.PLAYER_TELEPORT, [-1, i10, i4, i5, i6, i9])

        if not self.guiScreen and self.player and self.player.health <= 0:
            self.setScreen(None)
        if not self.guiScreen or self.guiScreen.allowUserInput:
            if self.__clickCounter > 0:
                self.__clickCounter -= 1

            if self.msh[window.mouse.LEFT] and float(self.__frames - self.__oFrames) >= self.__timer.ticksPerSecond / 4.0 and self.mouseGrabbed:
                self.__clickMouse(0)
                self.__oFrames = self.__frames
            elif self.msh[window.mouse.RIGHT] and float(self.__frames - self.__oFrames) >= self.__timer.ticksPerSecond / 4.0 and self.mouseGrabbed:
                self.__clickMouse(1)
                self.__oFrames = self.__frames

            leftHeld = not self.guiScreen and self.msh[window.mouse.LEFT] and self.mouseGrabbed
            if not self.gamemode.mode and self.__clickCounter <= 0:
                if leftHeld and self.hitResult and self.hitResult.typeOfHit == 0:
                    x = self.hitResult.x
                    y = self.hitResult.y
                    z = self.hitResult.z
                    self.gamemode.continueDestroyBlock(x, y, z, self.hitResult.sideHit)
                else:
                    self.gamemode.stopDestroyBlock()
        else:
            self.__oFrames = self.__frames + 10000
            self.guiScreen.tick()

        if self.level:
            self.gameRenderer.rainTicks += 1
            tileRenderer = self.gameRenderer.tileRenderer
            tileRenderer.oProgress = tileRenderer.progress
            if tileRenderer.move:
                tileRenderer.rot += 1
                if tileRenderer.rot == 7:
                    tileRenderer.rot = 0
                    tileRenderer.move = False

            tile = self.player.inventory.getSelected()
            block = None
            if tile > 0:
                block = tiles.tiles[tile]

            decrease = 1.0 if block == tileRenderer.tile else 0.0
            progress = decrease - tileRenderer.progress
            if progress > 0.4:
                progress = 0.4

            tileRenderer.progress += progress
            if tileRenderer.progress < 0.1:
                tileRenderer.tile = block

            if self.raining:
                x = self.player.x
                y = self.player.y
                z = self.player.z
                for i in range(50):
                    xr = x + int(random.random() * 9) - 4
                    zr = z + int(random.random() * 9) - 4
                    highest = self.level.getHighestTile(xr, zr)
                    if highest <= y + 4 and highest >= y - 4:
                        self.particleEngine.addParticle(WaterDropParticle(self.level,
                                                                          xr + random.random(),
                                                                          highest + 0.1,
                                                                          zr + random.random()))

            self.levelRenderer.cloudTickCounter += 1
            self.level.tickEntities()
            if not self.isOnlineClient():
                self.level.tick()

            self.particleEngine.tick()

    def isOnlineClient(self):
        return self.networkClient is not None

    def __orientCamera(self, alpha):
        gl.glTranslatef(0.0, 0.0, -0.1)
        gl.glRotatef(self.player.xRotO + (self.player.xRot - self.player.xRotO) * alpha, 1.0, 0.0, 0.0)
        gl.glRotatef(self.player.yRotO + (self.player.yRot - self.player.yRotO) * alpha, 0.0, 1.0, 0.0)

        x = self.player.xo + (self.player.x - self.player.xo) * alpha
        y = self.player.yo + (self.player.y - self.player.yo) * alpha
        z = self.player.zo + (self.player.z - self.player.zo) * alpha
        gl.glTranslatef(-x, -y, -z)

    def __setupCamera(self, i, alpha):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        if self.options.anaglyph3d:
            gl.glTranslatef(-((i << 1) - 1) * 0.07, 0.0, 0.0)

        fov = 70.0
        if self.player.health <= 0:
            t = self.player.deathTime + alpha
            fov /= (1.0 - 500.0 / (t + 500.0)) * 2.0 + 1.0

        gluPerspective(fov, self.width / self.height, 0.05, self.gameRenderer.renderDistance)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        if self.options.anaglyph3d:
            gl.glTranslatef(((i << 1) - 1) * 0.1, 0.0, 0.0)

        self.gameRenderer.renderHurtFrames(alpha)
        if self.options.bobView:
            self.gameRenderer.cameraBob(alpha)

        self.__orientCamera(alpha)

    def __pick(self, alpha):
        xRot = self.player.xRotO + (self.player.xRot - self.player.xRotO) * alpha
        yRot = self.player.yRotO + (self.player.yRot - self.player.yRotO) * alpha

        rotVec = self.gameRenderer.getPlayerRotVec(alpha)
        y1 = math.cos(-yRot * 0.017453292 - math.pi)
        y2 = math.sin(-yRot * 0.017453292 - math.pi)
        x1 = math.cos(-xRot * 0.017453292)
        x2 = math.sin(-xRot * 0.017453292)
        xy = y2 * x1
        y1 *= x1
        d = self.gamemode.getPickRange()
        vec2 = rotVec.add(xy * d, x2 * d, y1 * d)
        self.hitResult = self.level.clip(rotVec, vec2)

        vec = self.gameRenderer.getPlayerRotVec(alpha)
        if self.hitResult:
            d = self.hitResult.vec.distanceTo(vec)

        entities = self.level.blockMap.getEntitiesWithinAABBExcludingEntity(self.player, self.player.bb.expand(xy * d, x2 * d, y1 * d))
        for entity in entities:
            if not entity.isPickable():
                continue

            axisAlignedBB = entity.bb.grow(0.1, 0.1, 0.1)
            di = 0.0
            while di < d:
                if not axisAlignedBB.contains(vec.add(xy * di, x2 * di, y1 * di)):
                    di += 0.05
                    continue

                d = di
                self.hitResult = HitResult(entity)
                di += 0.05
                break

    def __render(self, alpha):
        for i in range(2):
            if self.options.anaglyph3d:
                if i == 0:
                    gl.glColorMask(False, True, True, False)
                else:
                    gl.glColorMask(True, False, False, False)

            #gl.glViewport(0, 0, self.width, self.height)

            f4 = 1.0 - pow(1.0 / (4 - self.options.viewDistance), 0.25)
            x = (self.level.skyColor >> 16 & 0xFF) / 255.0
            y = (self.level.skyColor >> 8 & 0xFF) / 255.0
            z = (self.level.skyColor & 0xFF) / 255.0
            self.gameRenderer.fogRed = x
            self.gameRenderer.fogGreen = y
            self.gameRenderer.fogBlue = z
            self.gameRenderer.fogRed += (x - self.gameRenderer.fogRed) * f4
            self.gameRenderer.fogGreen += (y - self.gameRenderer.fogGreen) * f4
            self.gameRenderer.fogBlue += (z - self.gameRenderer.fogBlue) * f4
            self.gameRenderer.fogRed *= self.gameRenderer.fogColorMultiplier
            self.gameRenderer.fogGreen *= self.gameRenderer.fogColorMultiplier
            self.gameRenderer.fogBlue *= self.gameRenderer.fogColorMultiplier
            tile = tiles.tiles[self.level.getTile(int(self.player.x), int(self.player.y + 0.12), int(self.player.z))]
            if tile and tile.getLiquidType() != Liquid.none:
                liquid = tile.getLiquidType()
                if liquid == Liquid.water:
                    self.gameRenderer.fogRed = 0.02
                    self.gameRenderer.fogGreen = 0.02
                    self.gameRenderer.fogBlue = 0.2
                elif liquid == Liquid.lava:
                    self.gameRenderer.fogRed = 0.6
                    self.gameRenderer.fogGreen = 0.1
                    self.gameRenderer.fogBlue = 0.0

            if self.options.anaglyph3d:
                x = (self.gameRenderer.fogRed * 30.0 + self.gameRenderer.fogGreen * 59.0 + self.gameRenderer.fogBlue * 11.0) / 100.0
                y = (self.gameRenderer.fogRed * 30.0 + self.gameRenderer.fogGreen * 70.0) / 100.0
                z = (self.gameRenderer.fogRed * 30.0 + self.gameRenderer.fogBlue * 70.0) / 100.0
                self.gameRenderer.fogRed = x
                self.gameRenderer.fogGreen = y
                self.gameRenderer.fogBlue = z

            gl.glClearColor(self.gameRenderer.fogRed, self.gameRenderer.fogGreen, self.gameRenderer.fogBlue, 0.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            self.gameRenderer.fogColorMultiplier = 1.0

            gl.glEnable(gl.GL_CULL_FACE)
            self.gameRenderer.renderDistance = float(512 >> (self.options.viewDistance << 1))

            self.__setupCamera(i, alpha)
            self.__pick(alpha)

            self.__frustum.calculateFrustum()
            for chunk in self.levelRenderer.chunks:
                chunk.updateInFrustum(self.__frustum)

            for chunk in self.levelRenderer.allDirtyChunks.copy():
                chunk.rebuild()
                self.levelRenderer.allDirtyChunks.remove(chunk)
                chunk.dirty = False

            self.gameRenderer.setupFog()
            gl.glEnable(gl.GL_FOG)
            self.levelRenderer.render(self.player, 0)
            if self.level.isSolid(self.player.x, self.player.y, self.player.z, 0.1):
                x = int(self.player.x)
                y = int(self.player.y)
                z = int(self.player.z)

                for xx in range(x - 1, x + 2):
                    for yy in range(y - 1, y + 2):
                        for zz in range(z - 1, z + 2):
                            self.levelRenderer.renderBasicTile(xx, yy, zz)

            self.gameRenderer.toggleLight(True)
            vec = self.gameRenderer.getPlayerRotVec(alpha)
            self.level.blockMap.render(vec, self.__frustum, self.levelRenderer.textures, alpha)
            self.gameRenderer.toggleLight(False)
            self.gameRenderer.setupFog()
            self.particleEngine.render(self.player, alpha)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.levelRenderer.textures.loadTexture('rock.png'))
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glCallList(self.levelRenderer.surroundLists)
            self.gameRenderer.setupFog()
            self.levelRenderer.renderClouds(alpha)
            self.gameRenderer.setupFog()

            if self.hitResult:
                gl.glDisable(gl.GL_ALPHA_TEST)
                self.levelRenderer.renderHit(self.hitResult, 0, self.player.inventory.getSelected())
                gl.glEnable(gl.GL_BLEND)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                gl.glColor4f(0.0, 0.0, 0.0, 0.4)
                gl.glLineWidth(2.0)
                gl.glDisable(gl.GL_TEXTURE_2D)
                gl.glDepthMask(False)
                tile = self.levelRenderer.level.getTile(self.hitResult.x,
                                                        self.hitResult.y,
                                                        self.hitResult.z)
                tiles.tiles[tile].getAABB(self.hitResult.x,
                                          self.hitResult.y,
                                          self.hitResult.z).grow(0.002, 0.002, 0.002).render()
                gl.glDepthMask(True)
                gl.glEnable(gl.GL_TEXTURE_2D)
                gl.glDisable(gl.GL_BLEND)
                gl.glEnable(gl.GL_ALPHA_TEST)

            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            self.gameRenderer.setupFog()
            gl.glEnable(gl.GL_BLEND)
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.levelRenderer.textures.loadTexture('water.png'))
            gl.glCallList(self.levelRenderer.surroundLists + 1)
            gl.glDisable(gl.GL_BLEND)
            gl.glEnable(gl.GL_BLEND)
            gl.glColorMask(False, False, False, False)
            remaining = self.levelRenderer.render(self.player, 1)
            gl.glColorMask(True, True, True, True)
            if self.options.anaglyph3d:
                if i == 0:
                    gl.glColorMask(False, True, True, False)
                else:
                    gl.glColorMask(True, False, False, False)

            if remaining > 0:
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.levelRenderer.textures.loadTexture('terrain.png'))
                gl.glCallLists(self.levelRenderer.ib.capacity(), gl.GL_INT, self.levelRenderer.ib)

            gl.glDepthMask(True)
            gl.glDisable(gl.GL_BLEND)
            gl.glDisable(gl.GL_FOG)
            if self.raining:
                self.gameRenderer.renderRain(alpha)

            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            gl.glLoadIdentity()
            if self.options.anaglyph3d:
                gl.glTranslatef(((i << 1) - 1) * 0.1, 0.0, 0.0)

            self.gameRenderer.renderHurtFrames(alpha)
            if self.options.bobView:
                self.gameRenderer.cameraBob(alpha)

            tileRenderer = self.gameRenderer.tileRenderer
            progress = tileRenderer.oProgress + (tileRenderer.progress - tileRenderer.oProgress) * alpha
            gl.glPushMatrix()
            gl.glRotatef(self.player.xRotO + (self.player.xRot - self.player.xRotO) * alpha, 1.0, 0.0, 0.0)
            gl.glRotatef(self.player.yRotO + (self.player.yRot - self.player.yRotO) * alpha, 0.0, 1.0, 0.0)
            self.gameRenderer.toggleLight(True)
            gl.glPopMatrix()
            gl.glPushMatrix()
            if tileRenderer.move:
                if tileRenderer.rot == -1:
                    tileRenderer.rot += 1

                slot = (tileRenderer.rot + alpha) / 7.0
                f20 = math.sin(slot * math.pi)
                f3 = math.sin(math.sqrt(slot) * math.pi)
                gl.glTranslatef(-f3 * 0.4, math.sin(math.sqrt(slot) * math.pi * 2.0) * 0.2, -f20 * 0.2)

            gl.glTranslatef(0.7 * 0.8, -0.65 * 0.8 - (1.0 - progress) * 0.6, -0.9 * 0.8)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glEnable(gl.GL_NORMALIZE)
            if tileRenderer.move:
                slot = (tileRenderer.rot + alpha) / 7.0
                f20 = math.sin((slot * slot) * math.pi)
                f3 = math.sin(math.sqrt(slot) * math.pi)
                gl.glRotatef(f3 * 80.0, 0.0, 1.0, 0.0)
                gl.glRotatef(-f20 * 20.0, 1.0, 0.0, 0.0)

            brightness = self.level.getBrightness(int(self.player.x), int(self.player.y), int(self.player.z))
            gl.glColor4f(brightness, brightness, brightness, 1.0)
            t = tesselator
            if tileRenderer.tile:
                gl.glScalef(0.4, 0.4, 0.4)
                gl.glTranslatef(-0.5, -0.5, -0.5)
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures.loadTexture('terrain.png'))
                tileRenderer.tile.renderGuiTile(t)
            else:
                self.player.bindTexture(self.textures)
                gl.glScalef(1.0, -1.0, -1.0)
                gl.glTranslatef(0.0, 0.2, 0.0)
                gl.glRotatef(-120.0, 0.0, 0.0, 1.0)
                gl.glScalef(1.0, 1.0, 1.0)
                cube = self.player.getModel().leftArm
                if not cube.compiled:
                    cube.translateTo(0.0625)

                gl.glCallList(cube.list)

            gl.glDisable(gl.GL_NORMALIZE)
            gl.glPopMatrix()
            self.gameRenderer.toggleLight(False)
            if not self.options.anaglyph3d:
                break

        gl.glColorMask(True, True, True, False)

    def generateLevel(self, size):
        name = self.user.name if self.user else 'anonymous'
        level = LevelGen(self.loadingScreen).generateLevel(name, 128 << size,
                                                           128 << size, 64)
        self.gamemode.createPlayer(level)
        self.loadLevel(level)

    def saveLevel(self):
        return self.levelIo.save(self.level, gzip.open('level.dat', 'wb'))

    def loadLevel(self, level):
        self.level = level
        if level:
            level.init()
            self.gamemode.initLevel(level)
            level.font = self.font
            level.rendererContext = self
            self.player = level.findSubclassOf(Player)

        if not self.player:
            self.player = Player(level)
            self.player.resetPos()
            self.gamemode.initPlayer(self.player)
            if level:
                level.player = self.player

        self.player.input = KeyboardInput(self.options)
        self.gamemode.adjustPlayer(self.player)

        if self.levelRenderer:
            self.levelRenderer.setLevel(level)

        if self.particleEngine:
            if self.level:
                self.level.particleEngine = self.particleEngine

            for i in range(2):
                self.particleEngine.particles[i].clear()

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

    game = Minecraft(fullScreen, width=854, height=480, caption='Minecraft')
    game.user = User(name, 0, mpPass)
    if server and port:
        game.setServer(server, int(port))
    game.run()
