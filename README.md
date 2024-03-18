## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python 3 using the **Pyglet** multimedia library and **Cython** for performance.

The project is currently working on the Indev versions of Minecraft.
The latest version is **Indev 0.31 20091223-2**, the first version of Indev which was released on _**December 23, 2009**_.

This version is the last available version of Minecraft to be released in creative mode exclusively.
However, the work-in-progress survival mode can be enabled by running the game with the argument `-survival`.
This is the first version to feature one of the MD3 mobs of Indev, Rana.

You can learn more about this version [on the Minecraft wiki.](https://minecraft.wiki/w/Java_Edition_Indev_0.31_20091223-2).

### Organization

This project's commits represent the Python versions of each Minecraft Java game version.
You can view source code changes between game versions by checking the commit history or comparing branches.
To play any version, specify it in the `pip install` command as demonstrated below.

### General Usage

*Pyglet*, *Cython*, and *Pillow* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

While the late Classic versions and later Indev versions feature audio, this version does not.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==0.31.20091223-2`.

Alternatively, for a manual Cython build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode.

### Gameplay

Press B to pick any of the ores and tiles that exist in this creative version.
Press F5 to toggle rain. Other keys are listed in the regular options menu.

If you enable survival mode, you will spawn with some lava and water blocks for testing.
You will be able to attack the Rana mobs, but items in general won't drop. Arrows and mushrooms are unusable.

### Additional Notes

The `mc.resources` directory contains all of the textures and sounds that this version uses. However,
the textures are only there for convenience, as all of the texture buffers are already preloaded
in the `mc.Resources` module.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
