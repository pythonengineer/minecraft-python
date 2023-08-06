import pyglet
pyglet.options['debug_gl'] = False

from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.Player import Player
from mc.net.minecraft.Textures import Textures
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.character.Vec3 import Vec3
from mc.net.minecraft.character.Zombie import Zombie
from mc.net.minecraft.level.tile.Tile import Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.Tesselator import tesselator
from mc.net.minecraft.level.Frustum import Frustum
from mc.net.minecraft.level.Chunk import Chunk
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelRenderer import LevelRenderer
from mc.net.minecraft.particle.ParticleEngine import ParticleEngine
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis
from pyglet import window, canvas, clock, gl, compat_platform

import math

class Minecraft(window.Window):
    FULLSCREEN_MODE = False
    timer = Timer(20.0)
    running = True
    paintTexture = 1

    zombies = set()

    hitResult = None

    lb = BufferUtils.createFloatBuffer(16)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        col0 = 16710650
        col1 = 920330

        self.fogColor0 = ((col0 >> 16 & 0xFF) / 255.0, (col0 >> 8 & 0xFF) / 255.0, (col0 & 0xFF) / 255.0, (col0 & 0xFF) / 255.0, 1.0)
        self.fogColor1 = ((col1 >> 16 & 0xFF) / 255.0, (col1 >> 8 & 0xFF) / 255.0, (col1 & 0xFF) / 255.0, (col1 & 0xFF) / 255.0, 1.0)

        fr = 0.5
        fg = 0.8
        fb = 1.0

        self.set_fullscreen(self.FULLSCREEN_MODE)
        self.set_exclusive_mouse(True)

        display = canvas.Display()
        screen = display.get_default_screen()
        locationX = screen.width // 2 - self.width // 2
        locationY = screen.height // 2 - self.height // 2
        self.set_location(locationX, locationY)
        self.set_visible(True)

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glClearColor(fr, fg, fb, 0.0)
        gl.glClearDepth(1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glAlphaFunc(gl.GL_GREATER, 0.0)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)

        self.__chunk = Chunk(None, 0, 0, 0, 0, 0, 0, True)

        self.frustum = Frustum()
        self.level = Level(256, 256, 64)
        self.levelRenderer = LevelRenderer(self.level)
        self.player = Player(self.level)
        self.particleEngine = ParticleEngine(self.level)

        for i in range(10):
            zombie = Zombie(self.level, 128.0, 0.0, 128.0)
            zombie.resetPos()
            self.zombies.add(zombie)

    def destroy(self):
        self.level.save()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == window.mouse.RIGHT:
            if self.hitResult:
                oldTile = tiles.tiles[self.level.getTile(self.hitResult.x, self.hitResult.y, self.hitResult.z)]
                changed = self.level.setTile(self.hitResult.x, self.hitResult.y, self.hitResult.z, 0)
                if oldTile and changed:
                    oldTile.destroy(self.level, self.hitResult.x, self.hitResult.y, self.hitResult.z, self.particleEngine)
        elif button == window.mouse.LEFT:
            if self.hitResult:
                x = self.hitResult.x
                y = self.hitResult.y
                z = self.hitResult.z

                if self.hitResult.f == 0: y -= 1
                if self.hitResult.f == 1: y += 1
                if self.hitResult.f == 2: z -= 1
                if self.hitResult.f == 3: z += 1
                if self.hitResult.f == 4: x -= 1
                if self.hitResult.f == 5: x += 1
                self.level.setTile(x, y, z, self.paintTexture)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.turn(dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == window.key.R:
            self.player.resetPos()
        elif symbol == window.key.G:
            self.zombies.add(Zombie(self.level, self.player.x, self.player.y, self.player.z))
        elif symbol == window.key._1:
            self.paintTexture = 1
        elif symbol == window.key._2:
            self.paintTexture = 3
        elif symbol == window.key._3:
            self.paintTexture = 4
        elif symbol == window.key._4:
            self.paintTexture = 5
        elif symbol == window.key._6:
            self.paintTexture = 6
        elif symbol in (window.key.UP, window.key.W):
            self.player.upPressed = True
        elif symbol in (window.key.DOWN, window.key.S):
            self.player.downPressed = True
        elif symbol in (window.key.LEFT, window.key.A):
            self.player.leftPressed = True
        elif symbol in (window.key.RIGHT, window.key.D):
            self.player.rightPressed = True
        elif symbol in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA):
            self.player.spacePressed = True
        elif symbol == window.key.RETURN:
            self.level.save()
        elif symbol == window.key.ESCAPE:
            self.running = False

    def on_key_release(self, symbol, modifiers):
        if symbol in (window.key.UP, window.key.W):
            self.player.upPressed = False
        elif symbol in (window.key.DOWN, window.key.S):
            self.player.downPressed = False
        elif symbol in (window.key.LEFT, window.key.A):
            self.player.leftPressed = False
        elif symbol in (window.key.RIGHT, window.key.D):
            self.player.rightPressed = False
        elif symbol in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA):
            self.player.spacePressed = False

    def on_activate(self):
        # Remove this hack when the window boundary issue is fixed upstream:
        if compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_draw(self):
        self.clear()
        self.timer.advanceTime()
        for i in range(self.timer.ticks):
            self.tick()
        self.render(self.timer.a)

    def run(self):
        lastTime = getMillis()
        frames = 0
        while self.running:
            clock.tick()
            self.dispatch_events()
            self.dispatch_event('on_draw')
            self.flip()

            frames += 1
            while getMillis() >= lastTime + 1000:
                print(str(frames) + ' fps, ' + str(self.__chunk.updates) + ' chunk updates')
                self.__chunk.updates = 0
                lastTime += 1000
                frames = 0

        self.destroy()

    def tick(self):
        self.level.tick()
        self.particleEngine.tick()

        for zombie in self.zombies.copy():
            zombie.tick()
            if zombie.removed:
                self.zombies.remove(zombie)

        self.player.tick()

    def moveCameraToPlayer(self, a):
        gl.glTranslatef(0.0, 0.0, -0.3)
        gl.glRotatef(self.player.xRot, 1.0, 0.0, 0.0)
        gl.glRotatef(self.player.yRot, 0.0, 1.0, 0.0)

        x = self.player.xo + (self.player.x - self.player.xo) * a
        y = self.player.yo + (self.player.y - self.player.yo) * a
        z = self.player.zo + (self.player.z - self.player.zo) * a
        gl.glTranslatef(-x, -y, -z)

    def setupCamera(self, a):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(70.0, self.width / self.height, 0.05, 1000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        self.moveCameraToPlayer(a)

    def pick(self, a):
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

    def render(self, a):
        self.pick(a)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.setupCamera(a)
        gl.glEnable(gl.GL_CULL_FACE)

        self.frustum.calculateFrustum()
        self.levelRenderer.updateDirtyChunks(self.player)

        self.setupFog(0)
        gl.glEnable(gl.GL_FOG)
        self.levelRenderer.render(self.player, 0)
        for zombie in self.zombies:
            if zombie.isLit() and self.frustum.isVisible(zombie.bb):
                zombie.render(a)

        self.particleEngine.render(self.player, a, 0)
        self.setupFog(1)
        self.levelRenderer.render(self.player, 1)
        for zombie in self.zombies:
            if not zombie.isLit() and self.frustum.isVisible(zombie.bb):
                zombie.render(a)

        self.particleEngine.render(self.player, a, 1)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_FOG)
        if self.hitResult:
            gl.glDisable(gl.GL_ALPHA_TEST)
            self.levelRenderer.renderHit(self.hitResult)
            gl.glEnable(gl.GL_ALPHA_TEST)

        self.drawGui(a)

    def drawGui(self, a):
        screenWidth = self.width * 240 // self.height
        screenHeight = self.height * 240 // self.height

        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, screenWidth, screenHeight, 0.0, 100.0, 300.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -200.0)

        gl.glPushMatrix()
        gl.glTranslatef(screenWidth - 16, 16.0, 0.0)
        t = tesselator
        gl.glScalef(16.0, 16.0, 16.0)
        gl.glRotatef(30.0, 1.0, 0.0, 0.0)
        gl.glRotatef(45.0, 0.0, 1.0, 0.0)
        gl.glTranslatef(-1.5, 0.5, -0.5)
        gl.glScalef(-1.0, -1.0, 1.0)

        id_ = Textures.loadTexture('terrain.png', gl.GL_NEAREST)
        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)
        gl.glEnable(gl.GL_TEXTURE_2D)
        t.init()
        tiles.tiles[self.paintTexture].render(t, self.level, 0, -2, 0, 0)
        t.flush()
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()

        wc = screenWidth // 2
        hc = screenHeight // 2
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        t.init()
        t.vertex(wc + 1, hc - 4, 0.0)
        t.vertex(wc - 0, hc - 4, 0.0)
        t.vertex(wc - 0, hc + 5, 0.0)
        t.vertex(wc + 1, hc + 5, 0.0)

        t.vertex(wc + 5, hc - 0, 0.0)
        t.vertex(wc - 4, hc - 0, 0.0)
        t.vertex(wc - 4, hc + 1, 0.0)
        t.vertex(wc + 5, hc + 1, 0.0)
        t.flush()

    def setupFog(self, i):
        if i == 0:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
            gl.glFogf(gl.GL_FOG_DENSITY, 0.001)
            gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(self.fogColor0[0], self.fogColor0[1],
                                                         self.fogColor0[2], self.fogColor0[3]))
            gl.glDisable(gl.GL_LIGHTING)
        elif i == 1:
            gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
            gl.glFogf(gl.GL_FOG_DENSITY, 0.06)
            gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(self.fogColor1[0], self.fogColor1[1],
                                                         self.fogColor1[2], self.fogColor1[3]))
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_COLOR_MATERIAL)

            br = 0.6
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.getBuffer(br, br, br, 1.0))

    def getBuffer(self, a, b, c, d):
        self.lb.clear()
        self.lb.put(a).put(b).put(c).put(d)
        self.lb.flip()
        return self.lb

if __name__ == '__main__':
    Minecraft(width=1024, height=768, caption='Game', vsync=False, visible=False).run()
