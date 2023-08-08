## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python using the **Pyglet** multimedia library and **Cython** for performance.

This project is currently recreating the **Classic** versions of Minecraft. The latest version is **Classic 0.0.13a_03** as released on _**May 22, 2009**_.

Learn more about this version [here](https://minecraft.fandom.com/wiki/Java_Edition_Classic_0.0.13a_03).

### General Usage

*Pyglet* and *Cython* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==0.0.13a_03`.

Alternatively, for a manual Cython build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode.

### Gameplay

This version features more advanced terrain (including caves and expanding water tiles), level saving, and human mobs. There are five different tiles you can place.

Press *Esc* to pause. Press *R* to reset your position, *Y* to invert the mouse, *G* to spawn a mob, *F* to toggle render distance, *Enter* to save the level, and numbers *1-4* (*6* for sapling) to switch blocks.

### Additional Notes

The resources directory contains all of the textures that this version uses. However,
they are only there for convenience, as all of the texture buffers are already preloaded
in the `net.Resources` module.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
