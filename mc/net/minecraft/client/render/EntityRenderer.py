from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.physics.MovingObjectPosition import MovingObjectPosition
from mc.net.minecraft.client.render.ClippingHelper import ClippingHelper
from mc.net.minecraft.client.render.ItemRenderer import ItemRenderer
from mc.net.minecraft.client.render.RenderSorter import RenderSorter
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.controller.PlayerControllerCreative import PlayerControllerCreative
from mc.CompatibilityShims import BufferUtils
from pyglet import gl
from functools import cmp_to_key

import random
import math

class EntityRenderer:
    __fogColorMultiplier = 1.0

    displayActive = False

    __farPlaneDistance = 0.0
    rainTicks = 0
    __pointedEntity = None
    rand = random.Random()

    __unusedInt1 = 0
    __unusedInt2 = 0

    __fogColorBuffer = BufferUtils.createFloatBuffer(16)

    __fogColorRed = 0.0
    __fogColorGreen = 0.0
    __fogColorBlue = 0.0

    def __init__(self, minecraft):
        self.mc = minecraft
        self.itemRenderer = ItemRenderer(self.mc)
        self.__clippingHelper = ClippingHelper()

    def __orientCamera(self, rot):
        x = self.mc.thePlayer.prevPosX + (self.mc.thePlayer.posX - self.mc.thePlayer.prevPosX) * rot
        y = self.mc.thePlayer.prevPosY + (self.mc.thePlayer.posY - self.mc.thePlayer.prevPosY) * rot
        z = self.mc.thePlayer.prevPosZ + (self.mc.thePlayer.posZ - self.mc.thePlayer.prevPosZ) * rot
        return Vec3D(x, y, z)

    def __hurtCameraEffect(self, a):
        ht = self.mc.thePlayer.hurtTime - a
        if self.mc.thePlayer.health <= 0:
            a = self.mc.thePlayer.deathTime + a
            gl.glRotatef(40.0 - 8000.0 / (a + 200.0), 0.0, 0.0, 1.0)
        if ht <= 0.0:
            return

        ht /= self.mc.thePlayer.maxHurtTime
        ht = math.sin((ht * ht * ht * ht) * math.pi)
        d = self.mc.thePlayer.attackedAtYaw
        gl.glRotatef(-d, 0.0, 1.0, 0.0)
        gl.glRotatef(-ht * 14.0, 0.0, 0.0, 1.0)
        gl.glRotatef(d, 0.0, 1.0, 0.0)

    def __setupViewBobbing(self, a):
        d = self.mc.thePlayer.distanceWalkedModified - self.mc.thePlayer.prevDistanceWalkedModified
        d = self.mc.thePlayer.distanceWalkedModified + d * a
        bob = self.mc.thePlayer.prevCameraYaw + (self.mc.thePlayer.cameraYaw - self.mc.thePlayer.prevCameraYaw) * a
        cameraPitch = self.mc.thePlayer.prevCameraPitch + (self.mc.thePlayer.cameraPitch - self.mc.thePlayer.prevCameraPitch) * a
        gl.glTranslatef(math.sin(d * math.pi) * bob * 0.5, -(abs(math.cos(d * math.pi) * bob)), 0.0)
        gl.glRotatef(math.sin(d * math.pi) * bob * 3.0, 0.0, 0.0, 1.0)
        gl.glRotatef(abs(math.cos(d * math.pi + 0.2) * bob) * 5.0, 1.0, 0.0, 0.0)
        gl.glRotatef(cameraPitch, 1.0, 0.0, 0.0)

    def updateCameraAndRender(self, alpha):
        rotationPitch = self.mc.thePlayer.prevRotationPitch + (self.mc.thePlayer.rotationPitch - self.mc.thePlayer.prevRotationPitch) * alpha
        rotationYaw = self.mc.thePlayer.prevRotationYaw + (self.mc.thePlayer.rotationYaw - self.mc.thePlayer.prevRotationYaw) * alpha

        rotVec = self.__orientCamera(alpha)
        y1 = math.cos(-rotationYaw * 0.017453292 - math.pi)
        y2 = math.sin(-rotationYaw * 0.017453292 - math.pi)
        x1 = math.cos(-rotationPitch * 0.017453292)
        x2 = math.sin(-rotationPitch * 0.017453292)
        xy = y2 * x1
        y1 *= x1
        d = self.mc.playerController.getBlockReachDistance()
        vec2 = rotVec.addVector(xy * d, x2 * d, y1 * d)
        self.mc.objectMouseOver = self.mc.theWorld.rayTraceBlocks(rotVec, vec2)
        if self.mc.objectMouseOver:
            d = self.mc.objectMouseOver.hitVec.distanceTo(rotVec)

        vec = self.__orientCamera(alpha)
        if isinstance(self.mc.playerController, PlayerControllerCreative):
            d = 32.0

        vec2 = vec.addVector(xy * d, x2 * d, y1 * d)
        self.__pointedEntity = None
        entities = self.mc.theWorld.entityMap.getEntitiesWithinAABBExcludingEntity(
            self.mc.thePlayer, self.mc.thePlayer.boundingBox.addCoord(xy * d, x2 * d, y1 * d)
        )
        d = 0.0
        for entity in entities:
            if not entity.canBeCollidedWith():
                continue

            hit = entity.boundingBox.expand(0.1, 0.1, 0.1).clip(vec, vec2)
            if hit:
                di = vec.distanceTo(hit.hitVec)
                if di < d or d == 0.0:
                    self.__pointedEntity = entity
                    d = di

        if self.__pointedEntity and not isinstance(self.mc.playerController, PlayerControllerCreative):
            self.mc.objectMouseOver = MovingObjectPosition(self.__pointedEntity)

        for i in range(2):
            if self.mc.options.anaglyph:
                if i == 0:
                    gl.glColorMask(False, True, True, False)
                else:
                    gl.glColorMask(True, False, False, False)

            #gl.glViewport(0, 0, self.width, self.height)

            f4 = 1.0 - pow(1.0 / (4 - self.mc.options.renderDistance), 0.25)
            x = (self.mc.theWorld.skyColor >> 16 & 0xFF) / 255.0
            y = (self.mc.theWorld.skyColor >> 8 & 0xFF) / 255.0
            z = (self.mc.theWorld.skyColor & 0xFF) / 255.0
            self.__fogColorRed = x
            self.__fogColorGreen = y
            self.__fogColorBlue = z
            self.__fogColorRed += (x - self.__fogColorRed) * f4
            self.__fogColorGreen += (y - self.__fogColorGreen) * f4
            self.__fogColorBlue += (z - self.__fogColorBlue) * f4
            self.__fogColorRed *= self.__fogColorMultiplier
            self.__fogColorGreen *= self.__fogColorMultiplier
            self.__fogColorBlue *= self.__fogColorMultiplier
            block = blocks.blocksList[self.mc.theWorld.getBlockId(int(self.mc.thePlayer.posX),
                                                                  int(self.mc.thePlayer.posY + 0.12),
                                                                  int(self.mc.thePlayer.posZ))]
            if block and block.getMaterial() != Material.air:
                material = block.getMaterial()
                if material == Material.water:
                    self.__fogColorRed = 0.02
                    self.__fogColorGreen = 0.02
                    self.__fogColorBlue = 0.2
                elif material == Material.lava:
                    self.__fogColorRed = 0.6
                    self.__fogColorGreen = 0.1
                    self.__fogColorBlue = 0.0

            if self.mc.options.anaglyph:
                x = (self.__fogColorRed * 30.0 + self.__fogColorGreen * 59.0 + self.__fogColorBlue * 11.0) / 100.0
                y = (self.__fogColorRed * 30.0 + self.__fogColorGreen * 70.0) / 100.0
                z = (self.__fogColorRed * 30.0 + self.__fogColorBlue * 70.0) / 100.0
                self.__fogColorRed = x
                self.__fogColorGreen = y
                self.__fogColorBlue = z

            gl.glClearColor(self.__fogColorRed, self.__fogColorGreen, self.__fogColorBlue, 0.0)
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT | gl.GL_COLOR_BUFFER_BIT)
            self.__fogColorMultiplier = 1.0

            gl.glEnable(gl.GL_CULL_FACE)
            self.__farPlaneDistance = float(512 >> (self.mc.options.renderDistance << 1))

            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            if self.mc.options.anaglyph:
                gl.glTranslatef(-((i << 1) - 1) * 0.07, 0.0, 0.0)

            fov = 70.0
            if self.mc.thePlayer.health <= 0:
                t = self.mc.thePlayer.deathTime + alpha
                fov /= (1.0 - 500.0 / (t + 500.0)) * 2.0 + 1.0

            aspect = self.mc.width / self.mc.height
            zNear = 0.05
            zFar = self.__farPlaneDistance

            fH = math.tan(fov / 360 * math.pi) * zNear
            fW = fH * aspect

            gl.glFrustum(-fW, fW, -fH, fH, zNear, zFar)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()

            if self.mc.options.anaglyph:
                gl.glTranslatef(((i << 1) - 1) * 0.1, 0.0, 0.0)

            self.__hurtCameraEffect(alpha)
            if self.mc.options.viewBobbing:
                self.__setupViewBobbing(alpha)

            gl.glTranslatef(0.0, 0.0, -0.1)
            gl.glRotatef(
                self.mc.thePlayer.prevRotationPitch + (self.mc.thePlayer.rotationPitch - self.mc.thePlayer.prevRotationPitch) * alpha,
                1.0, 0.0, 0.0
            )
            gl.glRotatef(
                self.mc.thePlayer.prevRotationYaw + (self.mc.thePlayer.rotationYaw - self.mc.thePlayer.prevRotationYaw) * alpha,
                0.0, 1.0, 0.0
            )

            x = self.mc.thePlayer.prevPosX + (self.mc.thePlayer.posX - self.mc.thePlayer.prevPosX) * alpha
            y = self.mc.thePlayer.prevPosY + (self.mc.thePlayer.posY - self.mc.thePlayer.prevPosY) * alpha
            z = self.mc.thePlayer.prevPosZ + (self.mc.thePlayer.posZ - self.mc.thePlayer.prevPosZ) * alpha
            gl.glTranslatef(-x, -y, -z)

            self.__clippingHelper.init()
            for chunk in self.mc.renderGlobal.worldRenderers:
                chunk.updateInFrustrum(self.__clippingHelper)

            self.mc.renderGlobal.worldRenderersToUpdate = sorted(
                self.mc.renderGlobal.worldRenderersToUpdate,
                key=cmp_to_key(RenderSorter(self.mc.thePlayer).compare)
            )

            for i, chunk in enumerate(self.mc.renderGlobal.worldRenderersToUpdate.copy()):
                if i > self.mc.renderGlobal.MAX_REBUILDS_PER_FRAME:
                    break

                self.mc.renderGlobal.worldRenderersToUpdate.remove(chunk)
                chunk.updateRenderer()
                chunk.needsUpdate = False

            self.__setupFog()
            gl.glEnable(gl.GL_FOG)
            self.mc.renderGlobal.sortAndRender(self.mc.thePlayer, 0)
            if self.mc.theWorld.isSolid(self.mc.thePlayer.posX,
                                        self.mc.thePlayer.posY,
                                        self.mc.thePlayer.posZ, 0.1):
                x = int(self.mc.thePlayer.posX)
                y = int(self.mc.thePlayer.posY)
                z = int(self.mc.thePlayer.posZ)
                renderBlocks = RenderBlocks(tessellator, self.mc.theWorld)

                for xx in range(x - 1, x + 2):
                    for yy in range(y - 1, y + 2):
                        for zz in range(z - 1, z + 2):
                            blockId = self.mc.theWorld.getBlockId(xx, yy, zz)
                            if blockId > 0:
                                block = blocks.blocksList[blockId]
                                renderBlocks.flipTexture = True
                                renderBlocks.renderBlockByRenderType(block, xx, yy, zz)
                                renderBlocks.flipTexture = False

            RenderHelper.enableStandardItemLighting()
            vec = self.__orientCamera(alpha)
            self.mc.theWorld.entityMap.render(vec, self.__clippingHelper,
                                              self.mc.renderGlobal.renderManager,
                                              self.mc.renderEngine, alpha)
            RenderHelper.disableStandardItemLighting()
            self.__setupFog()
            self.mc.effectRenderer.render(self.mc.thePlayer, alpha)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('rock.png'))
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glCallList(self.mc.renderGlobal.glGenList)
            self.__setupFog()
            self.mc.renderGlobal.renderClouds(alpha)
            self.__setupFog()

            if self.mc.objectMouseOver:
                gl.glDisable(gl.GL_ALPHA_TEST)
                self.mc.renderGlobal.renderHit(self.mc.objectMouseOver)
                gl.glEnable(gl.GL_BLEND)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                gl.glColor4f(0.0, 0.0, 0.0, 0.4)
                gl.glLineWidth(2.0)
                gl.glDisable(gl.GL_TEXTURE_2D)
                #gl.glDepthMask(False)
                block = self.mc.renderGlobal.worldObj.getBlockId(self.mc.objectMouseOver.blockX,
                                                                 self.mc.objectMouseOver.blockY,
                                                                 self.mc.objectMouseOver.blockZ)
                if block > 0:
                    blocks.blocksList[block].getSelectedBoundingBoxFromPool(
                        self.mc.objectMouseOver.blockX, self.mc.objectMouseOver.blockY,
                        self.mc.objectMouseOver.blockZ
                    ).expand(0.002, 0.002, 0.002).render()

                #gl.glDepthMask(True)
                gl.glEnable(gl.GL_TEXTURE_2D)
                gl.glDisable(gl.GL_BLEND)
                gl.glEnable(gl.GL_ALPHA_TEST)

            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            self.__setupFog()
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glEnable(gl.GL_BLEND)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('water.png'))
            gl.glCallList(self.mc.renderGlobal.glGenList + 1)
            gl.glDisable(gl.GL_BLEND)
            gl.glEnable(gl.GL_BLEND)
            gl.glColorMask(False, False, False, False)
            remaining = self.mc.renderGlobal.sortAndRender(self.mc.thePlayer, 1)
            gl.glColorMask(True, True, True, True)
            if self.mc.options.anaglyph:
                if i == 0:
                    gl.glColorMask(False, True, True, False)
                else:
                    gl.glColorMask(True, False, False, False)

            if remaining > 0:
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('terrain.png'))
                self.mc.renderGlobal.renderIntBuffer.glCallLists(
                    self.mc.renderGlobal.renderIntBuffer.capacity(), gl.GL_INT
                )

            gl.glDepthMask(True)
            gl.glDisable(gl.GL_BLEND)
            gl.glDisable(gl.GL_FOG)
            if self.mc.thirdPersonView:
                x = int(self.mc.thePlayer.posX)
                y = int(self.mc.thePlayer.posY)
                z = int(self.mc.thePlayer.posZ)
                t = tessellator
                gl.glDisable(gl.GL_CULL_FACE)
                gl.glNormal3f(0.0, 1.0, 0.0)
                gl.glEnable(gl.GL_BLEND)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('rain.png'))

                for xx in range(x - 5, x + 6):
                    for zz in range(z - 5, z + 6):
                        block = self.mc.theWorld.getMapHeight(xx, zz)
                        i11 = y - 5
                        i12 = y + 5
                        if i11 < block:
                            i11 = block
                        if i12 < block:
                            i12 = block

                        if i11 != i12:
                            f15 = (((self.rainTicks + xx * 3121 + zz * 418711) % 32) + alpha) / 32.0
                            f13 = xx + 0.5 - self.mc.thePlayer.posX
                            f14 = zz + 0.5 - self.mc.thePlayer.posZ
                            f13 = math.sqrt(f13 * f13 + f14 * f14) / 5
                            gl.glColor4f(1.0, 1.0, 1.0, (1.0 - f13 * f13) * 0.7)
                            t.startDrawingQuads()
                            t.addVertexWithUV(xx, i11, zz, 0.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx + 1, i11, zz + 1, 2.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx + 1, i12, zz + 1, 2.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx, i12, zz, 0.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx, i11, zz + 1, 0.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx + 1, i11, zz, 2.0, i11 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx + 1, i12, zz, 2.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                            t.addVertexWithUV(xx, i12, zz + 1, 0.0, i12 * 2.0 / 8.0 + f15 * 2.0)
                            t.draw()

                gl.glEnable(gl.GL_CULL_FACE)
                gl.glDisable(gl.GL_BLEND)

            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            gl.glLoadIdentity()
            if self.mc.options.anaglyph:
                gl.glTranslatef(((i << 1) - 1) * 0.1, 0.0, 0.0)

            self.__hurtCameraEffect(alpha)
            if self.mc.options.viewBobbing:
                self.__setupViewBobbing(alpha)

            itemRenderer = self.itemRenderer
            progress = itemRenderer.prevEquippedProgress + (itemRenderer.equippedProgress - itemRenderer.prevEquippedProgress) * alpha
            gl.glPushMatrix()
            gl.glRotatef(self.mc.thePlayer.prevRotationPitch + (self.mc.thePlayer.rotationPitch - self.mc.thePlayer.prevRotationPitch) * alpha,
                         1.0, 0.0, 0.0)
            gl.glRotatef(self.mc.thePlayer.prevRotationYaw + (self.mc.thePlayer.rotationYaw - self.mc.thePlayer.prevRotationYaw) * alpha,
                         0.0, 1.0, 0.0)
            RenderHelper.enableStandardItemLighting()
            gl.glPopMatrix()
            gl.glPushMatrix()
            if itemRenderer.itemSwingState:
                if itemRenderer.swingProgress == -1:
                    itemRenderer.swingProgress += 1

                slot = (itemRenderer.swingProgress + alpha) / 7.0
                f20 = math.sin(slot * math.pi)
                f3 = math.sin(math.sqrt(slot) * math.pi)
                gl.glTranslatef(-f3 * 0.4, math.sin(math.sqrt(slot) * math.pi * 2.0) * 0.2, -f20 * 0.2)

            gl.glTranslatef(0.7 * 0.8, -0.65 * 0.8 - (1.0 - progress) * 0.6, -0.9 * 0.8)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glEnable(gl.GL_NORMALIZE)
            if itemRenderer.itemSwingState:
                slot = (itemRenderer.swingProgress + alpha) / 7.0
                f20 = math.sin((slot * slot) * math.pi)
                f3 = math.sin(math.sqrt(slot) * math.pi)
                gl.glRotatef(f3 * 80.0, 0.0, 1.0, 0.0)
                gl.glRotatef(-f20 * 20.0, 1.0, 0.0, 0.0)

            brightness = self.mc.theWorld.getBlockLightValue(int(self.mc.thePlayer.posX),
                                                             int(self.mc.thePlayer.posY),
                                                             int(self.mc.thePlayer.posZ))
            gl.glColor4f(brightness, brightness, brightness, 1.0)
            if itemRenderer.itemToRender:
                gl.glScalef(0.4, 0.4, 0.4)
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.mc.renderEngine.getTexture('terrain.png'))
                itemRenderer.renderBlocksInstance.renderBlockOnInventory(itemRenderer.itemToRender)
            else:
                EntityPlayer.setupSkinImage(self.mc.renderEngine)
                gl.glScalef(1.0, -1.0, -1.0)
                gl.glTranslatef(0.0, 0.2, 0.0)
                gl.glRotatef(-120.0, 0.0, 0.0, 1.0)
                gl.glScalef(1.0, 1.0, 1.0)

            gl.glDisable(gl.GL_NORMALIZE)
            gl.glPopMatrix()
            RenderHelper.disableStandardItemLighting()
            if not self.mc.options.anaglyph:
                break

        gl.glColorMask(True, True, True, False)

    def setupOverlayRendering(self):
        screenWidth = self.mc.width * 240 // self.mc.height
        screenHeight = self.mc.height * 240 // self.mc.height

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -200.0)

    def __setupFog(self):
        self.__fogColorBuffer.clear()
        self.__fogColorBuffer.put(self.__fogColorRed).put(self.__fogColorGreen).put(self.__fogColorBlue).put(1.0)
        self.__fogColorBuffer.flip()
        self.__fogColorBuffer.glFogfv(gl.GL_FOG_COLOR)
        gl.glNormal3f(0.0, -1.0, 0.0)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        currentBlock = blocks.blocksList[self.mc.theWorld.getBlockId(
                int(self.mc.thePlayer.posX),
                int(self.mc.thePlayer.posY + 0.12),
                int(self.mc.thePlayer.posZ))]
        if currentBlock and currentBlock.getMaterial() != Material.air:
            material = currentBlock.getMaterial()
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
