## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python 3 using the **Pyglet** multimedia library and **Cython** for performance.

This project is currently recreating the **Survival Test Classic** versions of Minecraft. The latest version is **Classic 0.25_05 SURVIVAL TEST** as released on _**September 3, 2009**_.

Learn more about this version [here](https://minecraft.fandom.com/wiki/Java_Edition_Classic_0.25_05_SURVIVAL_TEST).

This project is organized so that every commit is strictly the finished Python version of the Java game of the same version number.
This means that you can go back into this repository's commit history and see only the source code changes between versions of Minecraft,
or you can compare branches and see the changes made between them. For any version this project covers,
you can play it just by specifying the Minecraft version you want to play in the `pip install` command as demonstrated below.

### General Usage

*Pyglet*, *Cython*, *Pillow*, and *PyOgg* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

For audio to work you will either need *PyOgg* which is recommended, or FFmpeg which is installed on the system.
GStreamer is also supported on Linux through the *gst-python* library. PyOgg requires that your system have one of the *Opus*, *FLAC*, or *Vorbis* codecs. OpenAL is required.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==0.25`.

Alternatively, for a manual Cython build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode.

### Gameplay

This version features early mobs (pigs, creepers, skeletons, zombies) and basic combat. Press Tab to launch arrows at enemies.

There are pigs that drop brown mushrooms. Creepers explode only upon death.

To heal, pick up mushrooms and right click to eat. Red mushrooms are poisonous and will take away health.

### Multiplayer

Since this is a Survival version of Classic, multiplayer support is disabled.

### Additional Notes

The `mc.resources` directory contains all of the textures and sounds that this version uses. However,
the textures are only there for convenience, as all of the texture buffers are already preloaded
in the `mc.Resources` module.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
