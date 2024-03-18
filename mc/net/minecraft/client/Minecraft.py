import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['audio'] = ('silent',)

pyglet.resource.path = ['../../../resources']
pyglet.resource.reindex()

from mc.net.minecraft.client import MinecraftError
from mc.net.minecraft.client.Timer import Timer
from mc.net.minecraft.client.GameSettings import GameSettings
from mc.net.minecraft.client.LoadingScreenRenderer import LoadingScreenRenderer
from mc.net.minecraft.game.physics.MovingObjectPosition import MovingObjectPosition
from mc.net.minecraft.game.physics.AxisAlignedBB import AxisAlignedBB
from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.net.minecraft.game.level.World import World
from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.level.generator.LevelGenerator import LevelGenerator
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.client.player.MovementInputFromKeys import MovementInputFromKeys
from mc.net.minecraft.client.gui.FontRenderer import FontRenderer
from mc.net.minecraft.client.gui.GuiErrorScreen import GuiErrorScreen
from mc.net.minecraft.client.gui.GuiIngameMenu import GuiIngameMenu
from mc.net.minecraft.client.gui.GuiGameOver import GuiGameOver
from mc.net.minecraft.client.gui.GuiIngame import GuiIngame
from mc.net.minecraft.client.effect.EffectRenderer import EffectRenderer
from mc.net.minecraft.client.effect.EntityDiggingFX import EntityDiggingFX
from mc.net.minecraft.client.effect.EntityRainFX import EntityRainFX
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
from mc.net.minecraft.client.ThreadDownloadSkin import ThreadDownloadSkin
from mc.net.minecraft.client.Session import Session
from mc.CompatibilityShims import BufferUtils, getMillis
from pyglet import window, app, canvas, clock
from pyglet import resource, media, gl, compat_platform

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
    VERSION_STRING = '0.31'
    theWorld = None
    renderGlobal = None
    thePlayer = None
    effectRenderer = None

    minecraftUri = ''

    __active = False

    ingameGUI = None

    ksh = window.key.KeyStateHandler()
    msh = window.mouse.MouseStateHandler()
    inventoryScreen = False
    mouseX = 0
    mouseY = 0

    options = None

    screenChanged = False

    def __init__(self, fullscreen, survival, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModelBiped(0.0)

        self.__fullScreen = fullscreen

        if survival:
            self.playerController = PlayerControllerSP(self)
        else:
            self.playerController = PlayerControllerCreative(self)

        self.__timer = Timer(20.0)
        self.session = None
        self.currentScreen = None
        self.thirdPersonView = False
        self.__loadingScreen = LoadingScreenRenderer(self)
        self.entityRenderer = EntityRenderer(self)
        self.__ticksRan = 0
        self.hideScreen = False
        self.objectMouseOver = None
        self.__leftClickCounter = 0

        self.serverIp = ''

        self.running = False
        self.debug = ''

        self.__prevFrameTime = 0

        self.push_handlers(self.ksh)
        self.push_handlers(self.msh)

    def setServer(self, server, port):
        self.serverIp = server

    def displayGuiScreen(self, screen):
        if not isinstance(self.currentScreen, GuiErrorScreen):
            if self.currentScreen or screen:
                self.screenChanged = True
            if self.currentScreen:
                self.currentScreen.onClose()

            if not screen and self.thePlayer.health <= 0:
                screen = GuiGameOver()

            self.currentScreen = screen
            if screen:
                self.__releaseMouse()
                screenWidth = self.width * 240 // self.height
                screenHeight = self.height * 240 // self.height
                screen.initGui(self, screenWidth, screenHeight)
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
        pass

    def on_close(self):
        self.running = False

    def on_activate(self):
        self.__active = True

        # Remove this hack when the window boundary issue is fixed upstream:
        if self.inventoryScreen and compat_platform == 'win32':
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

            if not self.currentScreen or self.currentScreen.allowUserInput:
                if not self.inventoryScreen:
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

                    self.thePlayer.inventory.grabTexture(block, isinstance(self.playerController, PlayerControllerCreative))
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
            if not self.inventoryScreen:
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
                    self.thePlayer.checkKeyForMovementInput(symbol, True)

                    if symbol == window.key.ESCAPE:
                        self.__displayInGameMenu()
                    elif symbol == window.key.F5:
                        self.thirdPersonView = not self.thirdPersonView
                    elif symbol == self.options.keyBindInventory.keyCode:
                        self.playerController.displayInventoryGUI()

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
                self.thePlayer.checkKeyForMovementInput(symbol, False)
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
            now = getMillis()
            passedMs = now - self.__timer.lastSyncSysClock
            j11 = time.time_ns() // Timer.NS_PER_SECOND
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

            self.__timer.elapsedPartialTicks += d15 * self.__timer.timerSpeed * self.__timer.ticksPerSecond
            self.__timer.elapsedTicks = int(self.__timer.elapsedPartialTicks)
            if self.__timer.elapsedTicks > Timer.MAX_TICKS_PER_UPDATE:
                self.__timer.elapsedTicks = Timer.MAX_TICKS_PER_UPDATE

            self.__timer.elapsedPartialTicks -= float(self.__timer.elapsedTicks)
            self.__timer.renderPartialTicks = self.__timer.elapsedPartialTicks

            for i in range(self.__timer.elapsedTicks):
                self.__ticksRan += 1
                self.__runTick()

            self.__checkGLError('Pre render')
            gl.glEnable(gl.GL_TEXTURE_2D)
            self.playerController.setPartialTime(self.__timer.renderPartialTicks)
            if self.entityRenderer.displayActive and not self.__active:
                self.__displayInGameMenu()

            self.entityRenderer.displayActive = self.__active

            screenWidth = self.width * 240 // self.height
            screenHeight = self.height * 240 // self.height
            xMouse = self.mouseX * screenWidth // self.width
            yMouse = screenHeight - self.mouseY * screenHeight // self.height - 1

            if self.theWorld:
                self.entityRenderer.updateCameraAndRender(self.__timer.renderPartialTicks)
                self.ingameGUI.renderGameOverlay(self.__timer.renderPartialTicks)
            else:
                #gl.glViewport(0, 0, self.width, self.height)
                pass

            if self.currentScreen:
                self.currentScreen.drawScreen(xMouse, yMouse)

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
        self.renderEngine.registerTextureFX(TextureLavaFX())
        self.renderEngine.registerTextureFX(TextureWaterFX())
        self.renderEngine.registerTextureFX(TextureWaterFlowFX())
        self.fontRenderer = FontRenderer(self.options, 'default.png', self.renderEngine)

        imgData = BufferUtils.createIntBuffer(256)
        imgData.clear().limit(256)

        self.renderGlobal = RenderGlobal(self, self.renderEngine)

        #gl.glViewport(0, 0, self.width, self.height)

        if self.serverIp and self.session:
            level = World()
            world.generate(8, 8, 8, bytearray(512))
            self.__setLevel(level)
        else:
            success = False
            if not self.theWorld:
                self.generateLevel(0)

        self.effectRenderer = EffectRenderer(self.theWorld, self.renderEngine)

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
                if not self.hideScreen and frames >= 0:
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
        if self.inventoryScreen:
            return

        self.inventoryScreen = True
        self.set_exclusive_mouse(True)
        self.displayGuiScreen(None)
        self.__prevFrameTime = self.__ticksRan + 10000

    def __releaseMouse(self):
        if not self.inventoryScreen:
            return

        self.thePlayer.resetKeyState()
        self.inventoryScreen = False
        self.set_exclusive_mouse(False)
        self.set_mouse_position(self.width // 2, self.height // 2)

    def __displayInGameMenu(self):
        if not isinstance(self.currentScreen, GuiIngameMenu):
            self.displayGuiScreen(GuiIngameMenu())

    def __clickMouse(self, editMode):
        item = self.thePlayer.inventory.getCurrentItem()
        if editMode == 0:
            if self.__leftClickCounter > 0:
                return

            self.entityRenderer.itemRenderer.swingProgress = -1
            self.entityRenderer.itemRenderer.itemSwingState = True
        elif editMode == 1 and item > 0 and self.playerController.sendUseItem(self.thePlayer, item):
            self.entityRenderer.itemRenderer.equippedProgress = 0.0
            return

        if not self.objectMouseOver:
            if editMode == 0 and not isinstance(self.playerController, PlayerControllerCreative):
                self.__leftClickCounter = 0

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
        if editMode != 0:
            if self.objectMouseOver.sideHit == 0: y -= 1
            if self.objectMouseOver.sideHit == 1: y += 1
            if self.objectMouseOver.sideHit == 2: z -= 1
            if self.objectMouseOver.sideHit == 3: z += 1
            if self.objectMouseOver.sideHit == 4: x -= 1
            if self.objectMouseOver.sideHit == 5: x += 1

        oldBlock = blocks.blocksList[self.theWorld.getBlockId(x, y, z)]
        if editMode == 0:
            if oldBlock != blocks.bedrock:
                self.playerController.clickBlock(x, y, z)
                return
        else:
            texture = self.thePlayer.inventory.getCurrentItem()
            if texture <= 0:
                return

            block = blocks.blocksList[self.theWorld.getBlockId(x, y, z)]
            if block and block != blocks.waterMoving and block != blocks.waterStill and \
               block != blocks.lavaMoving and block != blocks.lavaStill:
                return

            aabb = blocks.blocksList[texture].getCollisionBoundingBoxFromPool(x, y, z)
            if aabb and (self.thePlayer.boundingBox.intersectsBB(aabb) or not self.theWorld.checkIfAABBIsClear(aabb)):
                return
            elif not self.playerController.canPlace(texture):
                return

            self.theWorld.setBlockWithNotify(x, y, z, texture)
            self.entityRenderer.itemRenderer.equippedProgress = 0.0
            blocks.blocksList[texture].onBlockPlaced(self.theWorld, x, y, z)

    def __runTick(self):
        self.playerController.onUpdate()
        self.ingameGUI.updateCounter += 1
        for message in self.ingameGUI.chatMessageList.copy():
            message.updateCounter += 1

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.renderEngine.getTexture('terrain.png'))

        for texture in self.renderEngine.textureList:
            texture.anaglyphEnabled = self.options.anaglyph
            texture.onTick()
            self.renderEngine.imageData.clear()
            self.renderEngine.imageData.putBytes(texture.imageData)
            self.renderEngine.imageData.position(0).limit(len(texture.imageData))
            self.renderEngine.imageData.glTexSubImage2D(gl.GL_TEXTURE_2D, 0,
                                                        texture.iconIndex % 16 << 4,
                                                        texture.iconIndex // 16 << 4,
                                                        16, 16, gl.GL_RGBA,
                                                        gl.GL_UNSIGNED_BYTE)

        if not self.currentScreen and self.thePlayer and self.thePlayer.health <= 0:
            self.displayGuiScreen(None)
        if not self.currentScreen or self.currentScreen.allowUserInput:
            if self.__leftClickCounter > 0:
                self.__leftClickCounter -= 1

            if self.msh[window.mouse.LEFT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.inventoryScreen:
                self.__clickMouse(0)
                self.__prevFrameTime = self.__ticksRan
            elif self.msh[window.mouse.RIGHT] and float(self.__ticksRan - self.__prevFrameTime) >= self.__timer.ticksPerSecond / 4.0 and self.inventoryScreen:
                self.__clickMouse(1)
                self.__prevFrameTime = self.__ticksRan

            leftHeld = not self.currentScreen and self.msh[window.mouse.LEFT] and self.inventoryScreen
            if not self.playerController.isInTestMode and self.__leftClickCounter <= 0:
                if leftHeld and self.objectMouseOver and self.objectMouseOver.typeOfHit == 0:
                    x = self.objectMouseOver.blockX
                    y = self.objectMouseOver.blockY
                    z = self.objectMouseOver.blockZ
                    self.playerController.sendBlockRemoving(x, y, z)

                    block = self.theWorld.getBlockId(x, y, z)
                    if block != 0:
                        block = blocks.blocksList[block]
                        var = 0.1
                        posX = x + random.random() * (block.maxX - block.minX - var * 2.0) + var + block.minX
                        posY = y + random.random() * (block.maxY - block.minY - var * 2.0) + var + block.minY
                        posZ = z + random.random() * (block.maxZ - block.minZ - var * 2.0) + var + block.minZ
                        if y == 0:
                            posY = y + block.minY - var
                        elif y == 1:
                            posY = y + block.maxY + var
                        elif y == 2:
                            posZ = z + block.minZ - var
                        elif y == 3:
                            posZ = z + block.maxZ + var
                        elif y == 4:
                            posX = x + block.minX - var
                        elif y == 5:
                            posX = x + block.maxX + var

                        self.effectRenderer.addEffect(
                            EntityDiggingFX(
                                self.effectRenderer.worldObj, posX, posY, posZ,
                                0.0, 0.0, 0.0, block
                            ).multiplyVelocity(0.2).multipleParticleScaleBy(0.6)
                        )
                else:
                    self.playerController.resetBlockRemoving()
        else:
            self.__prevFrameTime = self.__ticksRan + 10000
            self.currentScreen.updateScreen()

        if not self.theWorld:
            return

        self.entityRenderer.rainTicks += 1
        itemRenderer = self.entityRenderer.itemRenderer
        itemRenderer.prevEquippedProgress = itemRenderer.equippedProgress
        if itemRenderer.itemSwingState:
            itemRenderer.swingProgress += 1
            if itemRenderer.swingProgress == 7:
                itemRenderer.swingProgress = 0
                itemRenderer.itemSwingState = False

        blockId = self.thePlayer.inventory.getCurrentItem()
        block = None
        if blockId > 0:
            block = blocks.blocksList[blockId]

        decrease = 1.0 if block == itemRenderer.itemToRender else 0.0
        progress = decrease - itemRenderer.equippedProgress
        if progress > 0.4:
            progress = 0.4

        itemRenderer.equippedProgress += progress
        if itemRenderer.equippedProgress < 0.1:
            itemRenderer.itemToRender = block

        if self.thirdPersonView:
            x = self.thePlayer.posX
            y = self.thePlayer.posY
            z = self.thePlayer.posZ
            for i in range(50):
                xr = x + int(random.random() * 9) - 4
                zr = z + int(random.random() * 9) - 4
                highest = self.theWorld.getMapHeight(xr, zr)
                blockId = self.theWorld.getBlockId(xr, highest - 1, zr)
                if highest <= y + 4 and highest >= y - 4 and blockId > 0:
                    self.effectRenderer.addEffect(EntityRainFX(self.theWorld,
                                                               xr + random.random(),
                                                               highest + 0.1 - blocks.blocksList[blockId].minY,
                                                               zr + random.random()))

        self.renderGlobal.cloudOffsetX += 1
        self.theWorld.updateEntities()
        self.theWorld.tick()
        self.effectRenderer.tick()

    def generateLevel(self, size):
        name = self.session.username if self.session else 'anonymous'
        level = LevelGenerator(self.__loadingScreen).generateLevel(name, 128 << size,
                                                                   128 << size, 64)
        self.playerController.createPlayer(level)
        self.__setLevel(level)

    def __setLevel(self, world):
        self.theWorld = world
        if world:
            world.load()
            self.playerController.onWorldChange(world)
            self.thePlayer = world.findSubclassOf(EntityPlayer)

        if not self.thePlayer:
            self.thePlayer = EntityPlayer(world)
            self.thePlayer.preparePlayerToSpawn()
            self.playerController.preparePlayer(self.thePlayer)
            if world:
                world.playerEntity = self.thePlayer

        self.thePlayer.movementInput = MovementInputFromKeys(self.options)
        self.playerController.flipPlayer(self.thePlayer)

        if self.renderGlobal:
            if self.renderGlobal.worldObj:
                self.renderGlobal.worldObj.removeRenderer(self.renderGlobal)

            self.renderGlobal.renderManager.worldObj = world
            self.renderGlobal.worldObj = world
            self.renderGlobal.globalRenderBlocks = RenderBlocks(tessellator, world)
            if world:
                world.addRenderer(self.renderGlobal)
                self.renderGlobal.loadRenderers()

        if self.effectRenderer:
            self.effectRenderer.worldObj = world
            for i in range(2):
                self.effectRenderer.fxLayers[i].clear()

        gc.collect()

if __name__ == '__main__':
    fullScreen = False
    server = None
    port = None
    name = 'guest'
    mpPass = ''
    survival = False
    for i, arg in enumerate(sys.argv):
        if arg == '-fullscreen':
            fullScreen = True
        elif arg == '-survival':
            survival = True

    game = Minecraft(fullScreen, survival, width=854, height=480,
                     resizable=True, caption='Minecraft 0.31')
    game.session = Session(name)
    game.run()
