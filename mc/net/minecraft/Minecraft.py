import pyglet
pyglet.options['debug_gl'] = False

from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.Player import Player
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.level.Chunk import Chunk
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelRenderer import LevelRenderer
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis
from pyglet import window, canvas, clock, gl, compat_platform

import math

class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Minecraft(window.Window):
    FULLSCREEN_MODE = False
    col = 920330
    fogColor = ((col >> 16 & 0xFF) / 255.0, (col >> 8 & 0xFF) / 255.0, (col & 0xFF) / 255.0, (col & 0xFF) / 255.0, 1.0)
    timer = Timer(60.0)
    hitResult = None
    running = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fr = 0.5
        fg = 0.8
        fb = 1.0

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glClearColor(fr, fg, fb, 0.0)
        gl.glClearDepth(1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)

        self.level = Level(256, 256, 64)
        self.levelRenderer = LevelRenderer(self.level)
        self.player = Player(self.level)

        self.set_exclusive_mouse(True)

    def destroy(self):
        self.level.save()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == window.mouse.RIGHT:
            if self.hitResult:
                self.level.setTile(self.hitResult.x, self.hitResult.y, self.hitResult.z, 0)
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
                self.level.setTile(x, y, z, 1)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.turn(dx, dy)

    def on_activate(self):
        # Remove this hack when the window boundary issue is fixed upstream:
        if compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_key_press(self, symbol, modifiers):
        if symbol == window.key.R:
            self.player.resetPos()
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

    def on_draw(self):
        self.clear()
        self.timer.advanceTime()
        for i in range(self.timer.ticks):
            self.tick()
        self.render(self.timer.a)

    def run(self):
        self.__chunk = Chunk(None, 0, 0, 0, 0, 0, 0, True)

        display = canvas.Display()
        screen = display.get_default_screen()
        locationX = screen.width // 2 - self.width // 2
        locationY = screen.height // 2 - self.height // 2
        self.set_location(locationX, locationY)
        self.set_visible(True)

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
        gl.glEnable(gl.GL_FOG)
        gl.glFogi(gl.GL_FOG_MODE, gl.GL_VIEWPORT_BIT)
        gl.glFogf(gl.GL_FOG_DENSITY, 0.2)
        gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(self.fogColor[0], self.fogColor[1],
                                                     self.fogColor[2], self.fogColor[3]))

        gl.glDisable(gl.GL_FOG)
        self.levelRenderer.render(self.player, 0)
        gl.glEnable(gl.GL_FOG)
        self.levelRenderer.render(self.player, 1)
        gl.glDisable(gl.GL_TEXTURE_2D)

        if self.hitResult:
            self.levelRenderer.renderHit(self.hitResult)

        gl.glDisable(gl.GL_FOG)

if __name__ == '__main__':
    Minecraft(width=1024, height=768, caption='Game', vsync=False, visible=False).run()
