## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python using the **Pyglet** multimedia library and **Cython** for performance.

This project is currently recreating the **Preclassic** versions of Minecraft. The latest version is **Preclassic rd-132328** as released on _**May 13, 2009**_.

Learn more about this version [here](https://minecraft.fandom.com/wiki/Java_Edition_pre-Classic_rd-132328).

### General Usage

*Pyglet* and *Cython* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==132328`.

Alternatively, for a manual Cython build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

### Gameplay

Very basic block picking and placing are featured in this version. You can only place stone tiles, except at exact ground level where it is only grass.

Human mobs are featured in this version, but they are all spawned at game start as opposed to on key press.

Press *Esc* to exit the game.

### Additional Notes

The resources directory contains all of the textures that this version uses. However,
they are only there for convenience, as all of the texture buffers are already preloaded
in the `net.Resources` module.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
