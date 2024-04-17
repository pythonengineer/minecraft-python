import pyglet
import platform
import os
pyglet.options['debug_gl'] = False
pyglet.options['search_local_libs'] = True
pyglet.options['audio'] = ('openal', 'silent')

if pyglet.compat_platform == 'win32':
    os.environ['PATH'] += os.pathsep + os.path.join(os.getcwd(), 'mc', 'lib')

    def load_library(*names, **kwargs):
        platformNames = kwargs.get('win32', [])
        if platformNames == 'openal32':
            if platform.architecture()[0] == '64bit':
                platformNames = 'soft_oal_64'
            elif platform.architecture()[0] == '32bit':
                platformNames = 'soft_oal_32'

            kwargs['win32'] = platformNames

        return pyglet.lib.loader.load_library(*names, **kwargs)

    pyglet.lib.load_library = load_library

pyglet.resource.path = ['../../../resources']
pyglet.resource.reindex()

from mc.net.minecraft.client import MinecraftError
from mc.net.minecraft.client.Timer import Timer
from mc.net.minecraft.client.GameSettings import GameSettings
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.LoadingScreenRenderer import LoadingScreenRenderer
from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.net.minecraft.game.level.World import World
from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.level.generator.LevelGenerator import LevelGenerator
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.player.EntityPlayerSP import EntityPlayerSP
from mc.net.minecraft.client.player.MovementInputFromOptions import MovementInputFromOptions
from mc.net.minecraft.client.gui.FontRenderer import FontRenderer
from mc.net.minecraft.client.gui.GuiErrorScreen import GuiErrorScreen
from mc.net.minecraft.client.gui.GuiIngameMenu import GuiIngameMenu
from mc.net.minecraft.client.gui.GuiGameOver import GuiGameOver
from mc.net.minecraft.client.gui.GuiIngame import GuiIngame
from mc.net.minecraft.client.effect.EffectRenderer import EffectRenderer
from mc.net.minecraft.client.render.texture.TextureFlamesFX import TextureFlamesFX
from mc.net.minecraft.client.render.texture.TextureWaterFlowFX import TextureWaterFlowFX
from mc.net.minecraft.client.render.texture.TextureWaterFX import TextureWaterFX
from mc.net.minecraft.client.render.texture.TextureLavaFX import TextureLavaFX
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.RenderGlobal import RenderGlobal
from mc.net.minecraft.client.render.EntityRenderer import EntityRenderer
from mc.net.minecraft.client.render.RenderEngine import RenderEngine
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.WorldRenderer import WorldRenderer
from mc.net.minecraft.client.controller.PlayerControllerCreative import PlayerControllerCreative
from mc.net.minecraft.client.controller.PlayerControllerSP import PlayerControllerSP
from mc.net.minecraft.client.sound.SoundManager import SoundManager
from mc.net.minecraft.client.ThreadDownloadSkin import ThreadDownloadSkin
from mc.net.minecraft.client.Session import Session
from mc.JavaUtils import BufferUtils, getMillis
from pyglet import window, app, canvas, clock
from pyglet import resource, gl, compat_platform

import traceback
import random
import math
import time
import gzip
import sys
import gc

GL_DEBUG = False

class Minecraft(window.Window):
    VERSION_STRING = '0.31'
    theWorld = None
    renderGlobal = None
    thePlayer = None
    effectRenderer = None

    minecraftUri = ''
    loadMapUser = ''
    loadMapID = 0

    __active = False

    ingameGUI = None
    skipRenderWorld = False

    ksh = window.key.KeyStateHandler()
    msh = window.mouse.MouseStateHandler()
    ingameFocus = False
    mouseX = 0
    mouseY = 0

    options = None

    screenChanged = False

    def __init__(self, fullscreen, creative, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModelBiped(0.0)

        self.__fullScreen = fullscreen

        if creative:
            self.playerController = PlayerControllerCreative(self)
        else:
            self.playerController = PlayerControllerSP(self)

        self.__timer = Timer(20.0)
        self.session = None
        self.currentScreen = None
        self.renderRain = False
        self.loadingScreen = LoadingScreenRenderer(self)
        self.entityRenderer = EntityRenderer(self)
        self.__ticksRan = 0
        self.objectMouseOver = None
        self.sndManager = SoundManager()
        self.__leftClickCounter = 0

        self.__serverIp = ''

        self.__textureWaterFX = TextureWaterFX()
        self.__textureLavaFX = TextureLavaFX()

        self.running = False
        self.debug = ''

        self.__prevFrameTime = 0

        self.push_handlers(self.ksh)
        self.push_handlers(self.msh)

    def setServer(self, server, port):
        self.__serverIp = server

    def displayGuiScreen(self, screen):
        if not isinstance(self.currentScreen, GuiErrorScreen):
            if self.currentScreen or screen:
                self.screenChanged = True
            if self.currentScreen:
                self.currentScreen.onGuiClose()

            if not screen and self.thePlayer.health <= 0:
                screen = GuiGameOver()

            self.currentScreen = screen
            if screen:
                self.__releaseMouse()
                screenWidth = self.width * 240 // self.height
                screenHeight = self.height * 240 // self.height
                screen.initGui(self, screenWidth, screenHeight)
                self.skipRenderWorld = False
            else:
                self.setIngameFocus()
        else:
            self.__releaseMouse()

    def __checkGLError(self, string):
        if GL_DEBUG:
            errorCode = gl.glGetError()
            if errorCode != 0:
                print('########## GL ERROR ##########')
                print('@ ' + string)
                print(errorCode)
                sys.exit(0)

    def destroy(self):
        self.sndManager.closeMinecraft()

    def isActive(self):
        return self.__active

    def on_close(self):
        self.running = False

    def on_activate(self):
        self.__active = True

        # Remove this hack when the window boundary issue is fixed upstream:
        if self.ingameFocus and compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_deactivate(self):
        self.__active = False
        self.__releaseMouse()

    def on_mouse_press(self, x, y, button, modifiers):
        try:
            if self.currentScreen:
                self.currentScreen.handleMouseInput(button)

            if self.screenChanged:
                self.screenChanged = False
                if compat_platform != 'darwin':
                    return

            if not self.currentScreen:
                if not self.ingameFocus:
                    self.setIngameFocus()
                elif button == window.mouse.LEFT:
                    self.__clickMouse(0)
                    self.__prevFrameTime = self.__ticksRan
                elif button == window.mouse.RIGHT:
                    self.__clickMouse(1)
                    self.__prevFrameTime = self.__ticksRan
                elif button == window.mouse.MIDDLE and self.objectMouseOver:
                    block = self.theWorld.getBlockId(self.objectMouseOver.blockX,
                                                     self.objectMouseOver.blockY,
                                                     self.objectMouseOver.blockZ)
                    if block == blocks.grass.blockID:
                        block = blocks.dirt.blockID
                    elif block == blocks.stairDouble.blockID:
                        block = blocks.stairSingle.blockID
                    elif block == blocks.bedrock.blockID:
                        block = blocks.stone.blockID

                    self.thePlayer.inventory.getFirstEmptyStack(block)
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_scroll(self, x, y, dx, dy):
        try:
            if not self.currentScreen or self.currentScreen.allowUserInput:
                if dy != 0:
                    self.thePlayer.inventory.swapPaint(dy)
        except Exception as e:
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_mouse_motion(self, x, y, dx, dy):
        try:
            self.mouseX = x
            self.mouseY = y
            if not self.ingameFocus:
                return

            xo = dx
            if self.options.invertMouse:
                yo = dy * -1
            else:
                yo = dy

            self.thePlayer.turn(xo, yo)
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_key_press(self, symbol, modifiers):
        try:
            if self.currentScreen:
                self.currentScreen.handleKeyboardEvent(key=symbol)

            if self.screenChanged:
                self.screenChanged = False
                if compat_platform != 'darwin':
                    return

            if not self.currentScreen or self.currentScreen.allowUserInput:
                if symbol != self.options.keyBindToggleFog.keyCode:
                    self.thePlayer.movementInput.checkKeyForMovementInput(symbol, True)

                    if symbol == window.key.ESCAPE:
                        self.displayInGameMenu()
                    elif symbol == window.key.F7:
                        self.entityRenderer.grabLargeScreenshot()
                    elif symbol == window.key.F5:
                        self.renderRain = not self.renderRain
                    elif symbol == self.options.keyBindInventory.keyCode:
                        self.playerController.openInventory()
                    elif symbol == self.options.keyBindDrop.keyCode:
                        self.thePlayer.dropPlayerItemWithRandomChoice(self.thePlayer.inventory.currentItem)

                    if isinstance(self.playerController, PlayerControllerCreative):
                        if symbol == self.options.keyBindLoad.keyCode:
                            self.thePlayer.preparePlayerToSpawn()
                        elif symbol == self.options.keyBindSave.keyCode:
                            self.theWorld.setSpawnLocation(int(self.thePlayer.posX),
                                                           int(self.thePlayer.posY),
                                                           int(self.thePlayer.posZ),
                                                           self.thePlayer.rotationYaw)
                            self.thePlayer.preparePlayerToSpawn()

                    for i in range(9):
                        if symbol == getattr(window.key, '_' + str(i + 1)):
                            self.thePlayer.inventory.currentItem = i
                else:
                    shift = modifiers & window.key.MOD_SHIFT
                    self.options.setOptionValue(4, -1 if shift else 1)
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_key_release(self, symbol, modifiers):
        try:
            if not self.currentScreen or self.currentScreen.allowUserInput:
                self.thePlayer.movementInput.checkKeyForMovementInput(symbol, False)
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_text(self, text):
        try:
            if self.screenChanged:
                self.screenChanged = False
                if compat_platform != 'darwin':
                    return

            if self.currentScreen:
                self.currentScreen.handleKeyboardEvent(char=text)
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_text_motion(self, motion):
        try:
            if self.currentScreen:
                self.currentScreen.handleKeyboardEvent(motion=motion)
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def on_draw(self):
        try:
            self.__timer.updateTimer()
            for i in range(self.__timer.elapsedTicks):
                self.__ticksRan += 1
                self.__runTick()

            self.__checkGLError('Pre render')
            self.sndManager.setListener(self.thePlayer, self.__timer.renderPartialTicks)
            gl.glEnable(gl.GL_TEXTURE_2D)

            self.playerController.setPartialTime(self.__timer.renderPartialTicks)
            self.entityRenderer.updateCameraAndRender(self.__timer.renderPartialTicks)
            if self.options.limitFramerate:
                time.sleep(0.005)

            self.__checkGLError('Post render')
        except Exception as e:
            print(traceback.format_exc())
            self.displayGuiScreen(GuiErrorScreen('Client error', 'The game broke! [' + str(e) + ']'))

    def run(self):
        self.running = True
        self.__dummyWorldRenderer = WorldRenderer(None, 0, 0, 0, 0, 0, True)

        self.set_fullscreen(self.__fullScreen)
        self.set_visible(True)

        if not self.__fullScreen:
            display = canvas.Display()
            screen = display.get_default_screen()
            locationX = screen.width // 2 - self.width // 2
            locationY = screen.height // 2 - self.height // 2
            self.set_location(locationX, locationY)

        self.set_icon(resource.image('icon/minecraft.png'))

        self.__checkGLError('Pre startup')

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
        self.__checkGLError('Startup')

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

        self.options = GameSettings(self, file)
        self.renderEngine = RenderEngine(self.options)
        self.renderEngine.registerTextureFX(self.__textureLavaFX)
        self.renderEngine.registerTextureFX(self.__textureWaterFX)
        self.renderEngine.registerTextureFX(TextureWaterFlowFX())
        self.renderEngine.registerTextureFX(TextureFlamesFX(0))
        self.renderEngine.registerTextureFX(TextureFlamesFX(1))
        self.fontRenderer = FontRenderer(self.options, 'default.png', self.renderEngine)

        imgData = BufferUtils.createIntBuffer(256)
        imgData.clear().limit(256)

        self.renderGlobal = RenderGlobal(self, self.renderEngine)

        #gl.glViewport(0, 0, self.width, self.height)

        if self.__serverIp and self.session:
            level = World()
            world.setLevel(8, 8, 8, bytearray(512))
            self.__setLevel(level)
        elif not self.theWorld:
            self.generateNewLevel(1, 0, 1, 0)

        self.effectRenderer = EffectRenderer(self.theWorld, self.renderEngine)
        self.sndManager.loadSoundSettings(self.options)

        self.__checkGLError('Post startup')
        self.ingameGUI = GuiIngame(self, self.width, self.height)
        ThreadDownloadSkin(self).start()

        lastTime = getMillis()
        frames = -2
        try:
            while self.running:
                clock.tick()
                self.dispatch_events()
                self.dispatch_event('on_draw')
                app.platform_event_loop.step(timeout=0.001)
                if frames >= 0:
                    self.flip()

                frames += 1
                while getMillis() >= lastTime + 1000:
                    self.debug = str(frames) + ' fps, ' + str(self.__dummyWorldRenderer.chunksUpdates) + ' chunk updates'
                    self.__dummyWorldRenderer.chunksUpdates = 0
                    lastTime += 1000
                    frames = 0
        except MinecraftError:
            pass
        finally:
            self.destroy()

    def setIngameFocus(self):
        if self.ingameFocus:
            return

        self.ingameFocus = True
        self.set_exclusive_mouse(True)
        self.displayGuiScreen(None)
        self.__prevFrameTime = self.__ticksRan + 10000

    def __releaseMouse(self):
        if not self.ingameFocus:
            return

        self.thePlayer.movementInput.resetKeyState()
        self.ingameFocus = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)

    def displayInGameMenu(self):
        if not isinstance(self.currentScreen, GuiIngameMenu):
            self.displayGuiScreen(GuiIngameMenu())

    def __clickMouse(self, editMode):
        item = self.thePlayer.inventory.getCurrentItem()
        if editMode == 0 and self.__leftClickCounter <= 0:
            self.entityRenderer.itemRenderer.swingItem()
            self.entityRenderer.updateRenderer()
        elif editMode == 1 and item:
            if item.getItem().onPlaced(item, self.thePlayer):
                if item.stackSize == 0:
                    self.thePlayer.inventory.mainInventory[self.thePlayer.inventory.currentItem] = None

                self.entityRenderer.itemRenderer.resetEquippedProgress2()

        if not self.objectMouseOver:
            if editMode == 0 and not isinstance(self.playerController, PlayerControllerCreative):
                self.__leftClickCounter = 10

            return
        elif self.objectMouseOver.typeOfHit == 1:
            if editMode == 0:
                self.objectMouseOver.entityHit.attackEntityFrom(self.thePlayer, 4)

            return
        elif self.objectMouseOver.typeOfHit != 0:
            return

        x = self.objectMouseOver.blockX
        y = self.objectMouseOver.blockY
        z = self.objectMouseOver.blockZ
        sideHit = self.objectMouseOver.sideHit
        block = blocks.blocksList[self.theWorld.getBlockId(x, y, z)]
        if editMode == 0:
            self.theWorld.extinguishFire(x, y, z, sideHit)
            if block != blocks.bedrock:
                self.playerController.clickBlock(x, y, z)
        else:
            item = self.thePlayer.inventory.getCurrentItem()
            if item is None:
                return

            prevSize = item.stackSize
            item.getItem().onItemUse(item, self.theWorld, x, y, z, sideHit)
            if item.stackSize == 0:
                self.thePlayer.inventory.mainInventory[self.thePlayer.inventory.currentItem] = None
                return

            if item.stackSize != prevSize:
                self.entityRenderer.itemRenderer.resetEquippedProgress2()

    def __runTick(self):
        self.playerController.onUpdate()
        self.ingameGUI.addChatMessage()

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.renderEngine.getTexture('terrain.png'))
        self.renderEngine.updateDynamicTextures()

        if not self.currentScreen and self.thePlayer and self.thePlayer.health <= 0:
            self.displayGuiScreen(None)
        if not self.currentScreen or self.currentScreen.allowUserInput:
            if self.__leftClickCounter > 0:
                self.__leftClickCounter -= 1

            if not self.currentScreen:
                if self.msh[window.mouse.LEFT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.ingameFocus:
                    self.__clickMouse(0)
                    self.__prevFrameTime = self.__ticksRan
                elif self.msh[window.mouse.RIGHT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.ingameFocus:
                    self.__clickMouse(1)
                    self.__prevFrameTime = self.__ticksRan

            leftHeld = not self.currentScreen and self.msh[window.mouse.LEFT] and self.ingameFocus
            if not self.playerController.isInTestMode and self.__leftClickCounter <= 0:
                if leftHeld and self.objectMouseOver and self.objectMouseOver.typeOfHit == 0:
                    x = self.objectMouseOver.blockX
                    y = self.objectMouseOver.blockY
                    z = self.objectMouseOver.blockZ
                    self.playerController.sendBlockRemoving(x, y, z, self.objectMouseOver.sideHit)
                    self.effectRenderer.addBlockHitEffects(x, y, z, self.objectMouseOver.sideHit)
                else:
                    self.playerController.resetBlockRemoving()
        else:
            self.__prevFrameTime = self.__ticksRan + 10000
            self.currentScreen.updateScreen()

        if not self.theWorld:
            return

        self.entityRenderer.updateRenderer()
        self.renderGlobal.updateClouds()
        self.theWorld.updateEntities()
        self.theWorld.tick()
        self.effectRenderer.updateEffects()

    def generateNewLevel(self, size, shape, levelType, theme):
        name = self.session.username if self.session else 'anonymous'
        levelGen = LevelGenerator(self.loadingScreen)
        levelGen.islandGen = levelType == 1
        levelGen.floatingGen = levelType == 2
        levelGen.flatGen = levelType == 3
        levelGen.levelType = theme
        width = 128 << size
        height = width
        length = 64
        if shape == 1:
            width //= 2
            height <<= 1
        elif shape == 2:
            width //= 2
            height = width
            length = 256

        self.__setLevel(levelGen.generate(name, width, height, length))

    def __setLevel(self, world):
        self.theWorld = world
        if world:
            world.load()
            self.playerController.onWorldChange(world)
            self.thePlayer = world.findSubclassOf(EntityPlayerSP)

        if not self.thePlayer:
            self.thePlayer = EntityPlayerSP(world)
            self.thePlayer.preparePlayerToSpawn()
            self.playerController.flipPlayer(self.thePlayer)
            if world:
                world.playerEntity = self.thePlayer

        self.thePlayer.movementInput = MovementInputFromOptions(self.options)
        self.playerController.flipPlayer(self.thePlayer)

        if self.renderGlobal:
            self.renderGlobal.changeWorld(world)

        if self.effectRenderer:
            self.effectRenderer.clearEffects(world)

        self.__textureWaterFX.textureId = 0
        self.__textureLavaFX.textureId = 0
        tex = self.renderEngine.getTexture('water.png')
        if world.defaultFluid == blocks.waterMoving.blockID:
            self.__textureWaterFX.textureId = tex
        else:
            self.__textureLavaFX.textureId = tex

        gc.collect()

if __name__ == '__main__':
    fullScreen = False
    server = None
    port = None
    name = 'guest'
    sessionId = ''
    creative = False
    for i, arg in enumerate(sys.argv):
        if arg == '-fullscreen':
            fullScreen = True
        elif arg == '-creative':
            creative = True

    game = Minecraft(fullScreen, creative, width=854, height=480,
                     resizable=True, vsync=False, visible=False,
                     caption='Minecraft 0.31')
    game.session = Session(name, sessionId)
    game.run()
