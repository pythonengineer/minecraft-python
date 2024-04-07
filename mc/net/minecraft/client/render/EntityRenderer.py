from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.net.minecraft.game.physics.MovingObjectPosition import MovingObjectPosition
from mc.net.minecraft.client.render.ClippingHelper import ClippingHelper
from mc.net.minecraft.client.render.ItemRenderer import ItemRenderer
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.particle.EntityRainFX import EntityRainFX
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.controller.PlayerControllerCreative import PlayerControllerCreative
from mc.CompatibilityShims import BufferUtils

from pyglet import gl
from PIL import Image

import traceback
import random
import math
import os

class EntityRenderer:
    __fogColorMultiplier = 1.0

    __displayActive = False

    __farPlaneDistance = 0.0
    __rainTicks = 0
    __pointedEntity = None

    __entityByteBuffer = None
    __entityFloatBuffer = BufferUtils.createFloatBuffer(16)

    __rand = random.Random()

    __unusedInt1 = 0
    __unusedInt2 = 0

    __fogColorBuffer = BufferUtils.createFloatBuffer(16)

    __fogColorRed = 0.0
    __fogColorGreen = 0.0
    __fogColorBlue = 0.0

    __prevFogColor = 0.0
    __fogColor = 0.0

    def __init__(self, minecraft):
        self.__mc = minecraft
        self.itemRenderer = ItemRenderer(self.__mc)
        self.__clippingHelper = ClippingHelper()

    def updateRenderer(self):
        self.__prevFogColor = self.__fogColor
        light = self.__mc.theWorld.getBlockLightValue(int(self.__mc.thePlayer.posX),
                                                      int(self.__mc.thePlayer.posY),
                                                      int(self.__mc.thePlayer.posZ))
        d = (3 - self.__mc.options.renderDistance) / 3.0
        light = light * (1.0 - d) + d
        self.__fogColor += (light - self.__fogColor) * 0.1
        self.__rainTicks += 1

        self.itemRenderer.updateEquippedItem()

        if self.__mc.thirdPersonView:
            x = self.__mc.thePlayer.posX
            y = self.__mc.thePlayer.posY
            z = self.__mc.thePlayer.posZ
            for i in range(50):
                xr = x + int(random.random() * 9) - 4
                zr = z + int(random.random() * 9) - 4
                highest = self.__mc.theWorld.getMapHeight(xr, zr)
                blockId = self.__mc.theWorld.getBlockId(xr, highest - 1, zr)
                if highest <= y + 4 and highest >= y - 4 and blockId > 0:
                    self.__mc.effectRenderer.addEffect(EntityRainFX(
                            self.__mc.theWorld, xr + random.random(),
                            highest + 0.1 - blocks.blocksList[blockId].minY,
                            zr + random.random()
                        ))

    def __orientCamera(self, rot):
        x = self.__mc.thePlayer.prevPosX + (self.__mc.thePlayer.posX - self.__mc.thePlayer.prevPosX) * rot
        y = self.__mc.thePlayer.prevPosY + (self.__mc.thePlayer.posY - self.__mc.thePlayer.prevPosY) * rot
        z = self.__mc.thePlayer.prevPosZ + (self.__mc.thePlayer.posZ - self.__mc.thePlayer.prevPosZ) * rot
        return Vec3D(x, y, z)

    def __hurtCameraEffect(self, a):
        ht = self.__mc.thePlayer.hurtTime - a
        if self.__mc.thePlayer.health <= 0:
            a = self.__mc.thePlayer.deathTime + a
            gl.glRotatef(40.0 - 8000.0 / (a + 200.0), 0.0, 0.0, 1.0)
        if ht < 0.0:
            return

        try:
            ht /= self.__mc.thePlayer.maxHurtTime
        except ZeroDivisionError:
            ht = 0.0

        ht = math.sin((ht * ht * ht * ht) * math.pi)
        d = self.__mc.thePlayer.attackedAtYaw
        gl.glRotatef(-d, 0.0, 1.0, 0.0)
        gl.glRotatef(-ht * 14.0, 0.0, 0.0, 1.0)
        gl.glRotatef(d, 0.0, 1.0, 0.0)

    def __setupViewBobbing(self, a):
        d = self.__mc.thePlayer.distanceWalkedModified - self.__mc.thePlayer.prevDistanceWalkedModified
        d = self.__mc.thePlayer.distanceWalkedModified + d * a
        bob = self.__mc.thePlayer.prevCameraYaw + (self.__mc.thePlayer.cameraYaw - self.__mc.thePlayer.prevCameraYaw) * a
        cameraPitch = self.__mc.thePlayer.prevCameraPitch + (self.__mc.thePlayer.cameraPitch - self.__mc.thePlayer.prevCameraPitch) * a
        gl.glTranslatef(math.sin(d * math.pi) * bob * 0.5, -(abs(math.cos(d * math.pi) * bob)), 0.0)
        gl.glRotatef(math.sin(d * math.pi) * bob * 3.0, 0.0, 0.0, 1.0)
        gl.glRotatef(abs(math.cos(d * math.pi + 0.2) * bob) * 5.0, 1.0, 0.0, 0.0)
        gl.glRotatef(cameraPitch, 1.0, 0.0, 0.0)

    def updateCameraAndRender(self, alpha):
        if self.__displayActive and not self.__mc.isActive():
            self.__mc.displayIngameMenu()

        self.__displayActive = self.__mc.isActive()

        screenWidth = self.__mc.width * 240 // self.__mc.height
        screenHeight = self.__mc.height * 240 // self.__mc.height
        xMouse = self.__mc.mouseX * screenWidth // self.__mc.width
        yMouse = screenHeight - self.__mc.mouseY * screenHeight // self.__mc.height - 1
        if self.__mc.theWorld:
            rotationPitch = self.__mc.thePlayer.prevRotationPitch + (self.__mc.thePlayer.rotationPitch - self.__mc.thePlayer.prevRotationPitch) * alpha
            rotationYaw = self.__mc.thePlayer.prevRotationYaw + (self.__mc.thePlayer.rotationYaw - self.__mc.thePlayer.prevRotationYaw) * alpha

            rotVec = self.__orientCamera(alpha)
            y1 = math.cos(-rotationYaw * (math.pi / 180.0) - math.pi)
            y2 = math.sin(-rotationYaw * (math.pi / 180.0) - math.pi)
            x1 = math.cos(-rotationPitch * (math.pi / 180.0))
            x2 = math.sin(-rotationPitch * (math.pi / 180.0))
            xy = y2 * x1
            y1 *= x1
            d = self.__mc.playerController.getBlockReachDistance()
            vec2 = rotVec.addVector(xy * d, x2 * d, y1 * d)
            self.__mc.objectMouseOver = self.__mc.theWorld.rayTraceBlocks(rotVec, vec2)
            if self.__mc.objectMouseOver:
                d = self.__mc.objectMouseOver.hitVec.distanceTo(rotVec)

            vec = self.__orientCamera(alpha)
            if isinstance(self.__mc.playerController, PlayerControllerCreative):
                d = 32.0

            vec2 = vec.addVector(xy * d, x2 * d, y1 * d)
            self.__pointedEntity = None
            entities = self.__mc.theWorld.entityMap.getEntitiesWithinAABBExcludingEntity(
                self.__mc.thePlayer, self.__mc.thePlayer.boundingBox.addCoord(xy * d, x2 * d, y1 * d)
            )
            d = 0.0
            for entity in entities:
                if not entity.canBeCollidedWith():
                    continue

                hit = entity.boundingBox.expand(0.1, 0.1, 0.1).calculateIntercept(vec, vec2)
                if hit:
                    di = vec.distanceTo(hit.hitVec)
                    if di < d or d == 0.0:
                        self.__pointedEntity = entity
                        d = di

            if self.__pointedEntity and not isinstance(self.__mc.playerController, PlayerControllerCreative):
                self.__mc.objectMouseOver = MovingObjectPosition(self.__pointedEntity)

            for i in range(2):
                if self.__mc.options.anaglyph:
                    if i == 0:
                        gl.glColorMask(False, True, True, False)
                    else:
                        gl.glColorMask(True, False, False, False)

                #gl.glViewport(0, 0, self.__mc.width, self.__mc.height)

                self.__updateFogColor(alpha)
                gl.glClear(gl.GL_DEPTH_BUFFER_BIT | gl.GL_COLOR_BUFFER_BIT)
                self.__fogColorMultiplier = 1.0

                gl.glEnable(gl.GL_CULL_FACE)
                self.__farPlaneDistance = 512 >> (self.__mc.options.renderDistance << 1)

                gl.glMatrixMode(gl.GL_PROJECTION)
                gl.glLoadIdentity()
                if self.__mc.options.anaglyph:
                    gl.glTranslatef(-((i << 1) - 1) * 0.07, 0.0, 0.0)

                fov = 70.0
                if self.__mc.thePlayer.health <= 0:
                    t = self.__mc.thePlayer.deathTime + alpha
                    fov /= (1.0 - 500.0 / (t + 500.0)) * 2.0 + 1.0

                aspect = self.__mc.width / self.__mc.height
                zNear = 0.05
                zFar = self.__farPlaneDistance

                fH = math.tan(fov / 360 * math.pi) * zNear
                fW = fH * aspect

                gl.glFrustum(-fW, fW, -fH, fH, zNear, zFar)
                gl.glMatrixMode(gl.GL_MODELVIEW)
                gl.glLoadIdentity()
                if self.__mc.options.anaglyph:
                    gl.glTranslatef(((i << 1) - 1) * 0.1, 0.0, 0.0)

                self.__hurtCameraEffect(alpha)
                if self.__mc.options.viewBobbing:
                    self.__setupViewBobbing(alpha)

                gl.glTranslatef(0.0, 0.0, -0.1)
                gl.glRotatef(
                    self.__mc.thePlayer.prevRotationPitch + (self.__mc.thePlayer.rotationPitch - self.__mc.thePlayer.prevRotationPitch) * alpha,
                    1.0, 0.0, 0.0
                )
                gl.glRotatef(
                    self.__mc.thePlayer.prevRotationYaw + (self.__mc.thePlayer.rotationYaw - self.__mc.thePlayer.prevRotationYaw) * alpha,
                    0.0, 1.0, 0.0
                )

                x = self.__mc.thePlayer.prevPosX + (self.__mc.thePlayer.posX - self.__mc.thePlayer.prevPosX) * alpha
                y = self.__mc.thePlayer.prevPosY + (self.__mc.thePlayer.posY - self.__mc.thePlayer.prevPosY) * alpha
                z = self.__mc.thePlayer.prevPosZ + (self.__mc.thePlayer.posZ - self.__mc.thePlayer.prevPosZ) * alpha
                gl.glTranslatef(-x, -y, -z)

                self.__clippingHelper.init()
                self.__mc.renderGlobal.clipRenderersByFrustrum(self.__clippingHelper)
                self.__mc.renderGlobal.updateRenderers(self.__mc.thePlayer)

                self.__setupFog()
                gl.glEnable(gl.GL_FOG)
                self.__mc.renderGlobal.sortAndRender(self.__mc.thePlayer, 0)
                if self.__mc.theWorld.isSolid(self.__mc.thePlayer.posX,
                                              self.__mc.thePlayer.posY,
                                              self.__mc.thePlayer.posZ, 0.1):
                    x = int(self.__mc.thePlayer.posX)
                    y = int(self.__mc.thePlayer.posY)
                    z = int(self.__mc.thePlayer.posZ)
                    renderBlocks = RenderBlocks(tessellator, self.__mc.theWorld)

                    for xx in range(x - 1, x + 2):
                        for yy in range(y - 1, y + 2):
                            for zz in range(z - 1, z + 2):
                                blockId = self.__mc.theWorld.getBlockId(xx, yy, zz)
                                if blockId > 0:
                                    renderBlocks.renderBlockAllFaces(
                                        blocks.blocksList[blockId], xx, yy, zz
                                    )

                RenderHelper.enableStandardItemLighting()
                self.__mc.renderGlobal.renderEntities(self.__orientCamera(alpha),
                                                      self.__clippingHelper, alpha)
                RenderHelper.disableStandardItemLighting()
                self.__setupFog()
                self.__mc.effectRenderer.renderParticles(self.__mc.thePlayer, alpha)
                self.__mc.renderGlobal.oobGroundRenderer()
                self.__setupFog()
                self.__mc.renderGlobal.renderClouds(alpha)
                self.__setupFog()

                if self.__mc.objectMouseOver:
                    gl.glDisable(gl.GL_ALPHA_TEST)
                    self.__mc.renderGlobal.drawBlockBreaking(
                        self.__mc.objectMouseOver, 0,
                        self.__mc.thePlayer.inventory.getCurrentItem()
                    )
                    self.__mc.renderGlobal.drawSelectionBox(self.__mc.objectMouseOver, 0)
                    gl.glEnable(gl.GL_ALPHA_TEST)

                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                self.__setupFog()
                self.__mc.renderGlobal.oobWaterRenderer()
                gl.glEnable(gl.GL_BLEND)
                gl.glDisable(gl.GL_CULL_FACE)
                gl.glColorMask(False, False, False, False)
                remaining = self.__mc.renderGlobal.sortAndRender(self.__mc.thePlayer, 1)
                gl.glColorMask(True, True, True, True)
                if self.__mc.options.anaglyph:
                    if i == 0:
                        gl.glColorMask(False, True, True, False)
                    else:
                        gl.glColorMask(True, False, False, False)

                if remaining > 0:
                    self.__mc.renderGlobal.renderAllRenderLists()

                gl.glDepthMask(True)
                gl.glEnable(gl.GL_CULL_FACE)
                gl.glDisable(gl.GL_BLEND)
                gl.glDisable(gl.GL_FOG)
                if self.__mc.thirdPersonView:
                    x = int(self.__mc.thePlayer.posX)
                    y = int(self.__mc.thePlayer.posY)
                    z = int(self.__mc.thePlayer.posZ)
                    t = tessellator
                    gl.glDisable(gl.GL_CULL_FACE)
                    gl.glNormal3f(0.0, 1.0, 0.0)
                    gl.glEnable(gl.GL_BLEND)
                    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                    gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('rain.png'))

                    for xx in range(x - 5, x + 6):
                        for zz in range(z - 5, z + 6):
                            block = self.__mc.theWorld.getMapHeight(xx, zz)
                            minY = y - 5
                            maxY = y + 5
                            if minY < block:
                                minY = block
                            if maxY < block:
                                maxY = block

                            if minY != maxY:
                                v = (((self.__rainTicks + xx * 3121 + zz * 418711) % 32) + alpha) / 32.0
                                xd = xx + 0.5 - self.__mc.thePlayer.posX
                                zd = zz + 0.5 - self.__mc.thePlayer.posZ
                                xd = math.sqrt(xd * xd + zd * zd) / 5
                                gl.glColor4f(1.0, 1.0, 1.0, (1.0 - xd * xd) * 0.7)
                                t.startDrawingQuads()
                                t.addVertexWithUV(xx, minY, zz, 0.0,
                                                  minY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx + 1, minY, zz + 1, 2.0,
                                                  minY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx + 1, maxY, zz + 1, 2.0,
                                                  maxY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx, maxY, zz, 0.0,
                                                  maxY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx, minY, zz + 1, 0.0,
                                                  minY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx + 1, minY, zz, 2.0,
                                                  minY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx + 1, maxY, zz, 2.0,
                                                  maxY * 2.0 / 8.0 + v * 2.0)
                                t.addVertexWithUV(xx, maxY, zz + 1, 0.0,
                                                  maxY * 2.0 / 8.0 + v * 2.0)
                                t.draw()

                    gl.glEnable(gl.GL_CULL_FACE)
                    gl.glDisable(gl.GL_BLEND)

                gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
                gl.glLoadIdentity()
                if self.__mc.options.anaglyph:
                    gl.glTranslatef(((i << 1) - 1) * 0.1, 0.0, 0.0)

                self.__hurtCameraEffect(alpha)
                if self.__mc.options.viewBobbing:
                    self.__setupViewBobbing(alpha)

                self.itemRenderer.renderItemInFirstPerson(alpha)

                if not self.__mc.options.anaglyph:
                    break

            gl.glColorMask(True, True, True, False)
            self.__mc.ingameGUI.renderGameOverlay()
        else:
            #gl.glViewport(0, 0, self.__mc.width, self.__mc.height)
            gl.glClearColor(0.0, 0.0, 0.0, 0.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            self.setupOverlayRendering()

        if self.__mc.currentScreen:
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            self.__mc.currentScreen.drawScreen(xMouse, yMouse)

    def renderLargeScreenshot(self):
        self.__mc.loadingScreen.displayProgressMessage('Grabbing large screenshot')
        home = os.path.expanduser('~') or '.'
        file = os.path.join(home, 'minecraft_map.png')
        self.__mc.loadingScreen.displayLoadingString('Rendering')

        try:
            size = max(self.__mc.theWorld.width, self.__mc.theWorld.length)
            w = size << 1 << 4
            h = self.__mc.theWorld.height + size << 4
            img = Image.new('RGB', (w, h))

            for x in range(0, w, self.__mc.width):
                for y in range(0, h, self.__mc.height):
                    if not self.__entityByteBuffer:
                        self.__entityByteBuffer = BufferUtils.createByteBuffer(self.__mc.width * self.__mc.height << 2)

                    #gl.glViewport(0, 0, self.__mc.width, self.__mc.height)
                    self.__updateFogColor(0.0)
                    gl.glClear(gl.GL_DEPTH_BUFFER_BIT | gl.GL_COLOR_BUFFER_BIT)
                    self.__fogColorMultiplier = 1.0
                    gl.glEnable(gl.GL_CULL_FACE)
                    self.__farPlaneDistance = 512 >> (self.__mc.options.renderDistance << 1)
                    gl.glMatrixMode(gl.GL_PROJECTION)
                    gl.glLoadIdentity()
                    gl.glOrtho(0.0, self.__mc.width, 0.0, self.__mc.height, 10.0, 10000.0)
                    gl.glMatrixMode(gl.GL_MODELVIEW)
                    gl.glLoadIdentity()
                    gl.glTranslatef(-(x - w // 2), -(y - h // 2), -5000.0)
                    gl.glScalef(16.0, -16.0, -16.0)
                    self.__entityFloatBuffer.clear()
                    self.__entityFloatBuffer.put(1.0).put(-0.5).put(0.0).put(0.0)
                    self.__entityFloatBuffer.put(0.0).put(1.0).put(-1.0).put(0.0)
                    self.__entityFloatBuffer.put(1.0).put(0.5).put(0.0).put(0.0)
                    self.__entityFloatBuffer.put(0.0).put(0.0).put(0.0).put(1.0)
                    self.__entityFloatBuffer.flip()
                    self.__entityFloatBuffer.glMultMatrix()
                    gl.glTranslatef(-self.__mc.theWorld.width / 2.0,
                                    -self.__mc.theWorld.height / 2.0,
                                    -self.__mc.theWorld.length / 2.0)
                    clippingHelper = ClippingHelper().init()
                    self.__mc.renderGlobal.clipRenderersByFrustrum(clippingHelper)
                    self.__mc.renderGlobal.updateRenderers(self.__mc.thePlayer)
                    self.__setupFog()
                    gl.glDisable(gl.GL_FOG)
                    RenderHelper.enableStandardItemLighting()
                    self.__mc.renderGlobal.renderEntities(self.__orientCamera(0.0),
                                                     clippingHelper, 0.0)
                    RenderHelper.disableStandardItemLighting()
                    self.__mc.renderGlobal.sortAndRender(self.__mc.thePlayer, 0)
                    gl.glEnable(gl.GL_BLEND)
                    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                    gl.glColorMask(False, False, False, False)
                    remaining = self.__mc.renderGlobal.sortAndRender(self.__mc.thePlayer, 1)
                    gl.glColorMask(True, True, True, True)
                    if remaining > 0:
                        self.__mc.renderGlobal.renderAllRenderLists()

                    gl.glDepthMask(True)
                    gl.glDisable(gl.GL_BLEND)
                    gl.glDisable(gl.GL_FOG)
                    self.__entityByteBuffer.clear()
                    gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
                    self.__entityByteBuffer.glReadPixels(
                        0, 0, self.__mc.width, self.__mc.height,
                        gl.GL_RGB, gl.GL_UNSIGNED_BYTE
                    )
                    im = EntityRenderer.__screenshotBuffer(
                        self.__entityByteBuffer,
                        self.__mc.width, self.__mc.height
                    )
                    img.paste(im, (x, y))

            self.__mc.loadingScreen.displayLoadingString(f'Saving as {file}')
            img.save(file)
        except Exception as e:
            print(traceback.format_exc())

    @staticmethod
    def __screenshotBuffer(buffer, w, h):
        buffer.position(0).limit(w * h << 2)
        img = Image.new('RGB', (w, h))
        for i in range(w * h):
            r = buffer.getAt(i * 3) & 255
            g = buffer.getAt(i * 3 + 1) & 255
            b = buffer.getAt(i * 3 + 2) & 255
            img.putpixel((i % w, i // w), (r, g, b))

        return img

    def setupOverlayRendering(self):
        screenWidth = self.__mc.width * 240 // self.__mc.height
        screenHeight = self.__mc.height * 240 // self.__mc.height

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 1000.0, 3000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -2000.0)

    def __updateFogColor(self, alpha):
        d = 1.0 - pow(1.0 / (4 - self.__mc.options.renderDistance), 0.25)
        x = (self.__mc.theWorld.skyColor >> 16 & 0xFF) / 255.0
        y = (self.__mc.theWorld.skyColor >> 8 & 0xFF) / 255.0
        z = (self.__mc.theWorld.skyColor & 0xFF) / 255.0
        self.__fogColorRed = (self.__mc.theWorld.fogColor >> 16 & 255) / 255.0
        self.__fogColorGreen = (self.__mc.theWorld.fogColor >> 8 & 255) / 255.0
        self.__fogColorBlue = (self.__mc.theWorld.fogColor & 255) / 255.0
        self.__fogColorRed += (x - self.__fogColorRed) * d
        self.__fogColorGreen += (y - self.__fogColorGreen) * d
        self.__fogColorBlue += (z - self.__fogColorBlue) * d
        self.__fogColorRed *= self.__fogColorMultiplier
        self.__fogColorGreen *= self.__fogColorMultiplier
        self.__fogColorBlue *= self.__fogColorMultiplier
        block = blocks.blocksList[self.__mc.theWorld.getBlockId(
                int(self.__mc.thePlayer.posX), int(self.__mc.thePlayer.posY + 0.12),
                int(self.__mc.thePlayer.posZ)
            )]
        if block and block.getBlockMaterial() != Material.air:
            material = block.getBlockMaterial()
            if material == Material.water:
                self.__fogColorRed = 0.02
                self.__fogColorGreen = 0.02
                self.__fogColorBlue = 0.2
            elif material == Material.lava:
                self.__fogColorRed = 0.6
                self.__fogColorGreen = 0.1
                self.__fogColorBlue = 0.0

        fd = self.__prevFogColor + (self.__fogColor - self.__prevFogColor) * alpha
        self.__fogColorRed *= fd
        self.__fogColorGreen *= fd
        self.__fogColorBlue *= fd
        if self.__mc.options.anaglyph:
            x = (self.__fogColorRed * 30.0 + self.__fogColorGreen * 59.0 + self.__fogColorBlue * 11.0) / 100.0
            y = (self.__fogColorRed * 30.0 + self.__fogColorGreen * 70.0) / 100.0
            z = (self.__fogColorRed * 30.0 + self.__fogColorBlue * 70.0) / 100.0
            self.__fogColorRed = x
            self.__fogColorGreen = y
            self.__fogColorBlue = z

        gl.glClearColor(self.__fogColorRed, self.__fogColorGreen,
                        self.__fogColorBlue, 0.0)

    def __setupFog(self):
        self.__fogColorBuffer.clear()
        self.__fogColorBuffer.put(self.__fogColorRed).put(self.__fogColorGreen).put(self.__fogColorBlue).put(1.0)
        self.__fogColorBuffer.flip()
        self.__fogColorBuffer.glFogfv(gl.GL_FOG_COLOR)
        gl.glNormal3f(0.0, -1.0, 0.0)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        currentBlock = blocks.blocksList[self.__mc.theWorld.getBlockId(
                int(self.__mc.thePlayer.posX),
                int(self.__mc.thePlayer.posY + 0.12),
                int(self.__mc.thePlayer.posZ))]
        if currentBlock and currentBlock.getBlockMaterial() != Material.air:
            material = currentBlock.getBlockMaterial()
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_EXP)
            if material == Material.water:
                gl.glFogf(gl.GL_FOG_DENSITY, 0.1)
            elif material == Material.lava:
                gl.glFogf(gl.GL_FOG_DENSITY, 2.0)
        else:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_LINEAR)
            gl.glFogf(gl.GL_FOG_START, 0.0)
            gl.glFogf(gl.GL_FOG_END, self.__farPlaneDistance)

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT)
