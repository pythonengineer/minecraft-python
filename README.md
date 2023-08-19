## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python 3 using the **Pyglet** multimedia library and **Cython** for performance.

This project is currently recreating the **Multiplayer Classic** versions of Minecraft. The latest version is **Classic 0.0.21a** as released on _**June 22, 2009**_.

Learn more about this version [here](https://minecraft.fandom.com/wiki/Java_Edition_Classic_0.0.21a).

Or the server version [here](https://minecraft.fandom.com/wiki/Java_Edition_Classic_server_1.8.2).

This project is organized so that every commit is strictly the completed release of the Python version of the Java game of the same version number.
This means that you can go back into this repository's commit history and see only the source code changes between versions of Minecraft,
or you can compare branches and see the changes made between them. For any version this project covers,
you can play it just by specifying the Minecraft version you want to play in the `pip install` command as demonstrated below.

### General Usage

*Pyglet*, *Cython*, and *Pillow* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==0.0.21`.

Alternatively, for a manual Cython build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode.

### Gameplay

This version features multiplayer, chat, more advanced terrain (including caves and expanding water tiles), level saving, and human mobs.

Press *B* to open the inventory menu. Press *Enter* to set your spawn position, *R* to teleport to your spawn position, *Y* to invert the mouse, *G* to spawn a mob, and *F* to toggle render distance.

### Multiplayer

To launch the multiplayer game, run `python -m mc.net.minecraft.Minecraft -server <host:port> -user <username> -mppass [password]`.

Press *Tab* in-game to view connected players.

To host a server, follow the instructions in the `README.TXT` file in the *server* directory.
Make sure `verify-names` is set to `false` in the server properties.

### Additional Notes

The resources directory contains all of the textures that this version uses. However,
they are only there for convenience, as all of the texture buffers are already preloaded
in the `mc.Resources` module.

The *server* directory contains the unmodified, original Minecraft server build for this version.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
