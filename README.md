## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python 3 using the **Pyglet** multimedia library and **Cython** for performance.

The project is currently working on the Indev versions of Minecraft.
The latest version is **Indev 0.31 20100110** as released on _**January 10, 2010**_.

This version introduces fire, apples, functional tools, and the customizable Indev level generator to the game.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==0.31.20100110`.

You can learn more about this version [on the Minecraft wiki.](https://minecraft.wiki/w/Java_Edition_Indev_0.31_20100110)

### Organization

This project's commits represent the Python versions of each Minecraft Java game version.
You can view source code changes between game versions by checking the commit history or comparing branches.
To play any version, specify it in the `pip install` command as demonstrated below.

### General Usage

*Pyglet*, *Cython*, *Pillow*, *PyOgg*, and *NumPy* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

For audio to work you will either need *PyOgg* which is recommended, or *FFmpeg* which has to be installed on your system.
*GStreamer* is also supported on Linux through the *gst-python* library.
PyOgg requires that your system have one of the Opus, FLAC, or Vorbis codecs.
*OpenAL* is required and comes bundled with the source on Windows.

For a manual Cython source build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode. The argument `-creative` will force the game to be in creative mode.

### Gameplay

Press I to open your inventory. All available tools (shovel, axe, pickaxe, flint and steel) are in the hotbar in addition to some building blocks and torches.
Press F7 to take a cool isometric screenshot and F5 to toggle rain. Q will drop items. Other keys are listed in the regular options menu.

The Indev level generator is customizable and you can choose between the *Inland*, *Island*, *Floating*, and *Flat* level types.
You can specify the world theme as *Normal* or *Hell* (lava and dirt instead of water and grass), world size, and world shape (*Square*, *Long*, *Deep*).

The only mobs around are the MD3 Ranas, but they don't drop anything when killed. Mushrooms are unusable, but apples will restore health.

![Isometric screenshot](/map.png?raw=true)

### Additional Notes

The `mc.resources` directory contains all of the textures and sounds that this version uses. However,
the textures are only there for convenience, as all of the texture buffers are already preloaded
in the `mc.Resources` module.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
