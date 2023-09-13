## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python 3 using the **Pyglet** multimedia library and **Cython** for performance.

This project is currently recreating the **Late Classic** versions of Minecraft. The latest version is **Classic 0.29_02** as released on _**October 30, 2009**_.

Learn more about this version [here](https://minecraft.fandom.com/wiki/Java_Edition_Classic_0.29_02).

Or the server version [here](https://minecraft.fandom.com/wiki/Java_Edition_Classic_server_1.8.3).

This project is organized so that every commit is strictly the finished Python version of the Java game of the same version number.
This means that you can go back into this repository's commit history and see only the source code changes between versions of Minecraft,
or you can compare branches and see the changes made between them. For any version this project covers,
you can play it just by specifying the Minecraft version you want to play in the `pip install` command as demonstrated below.

### General Usage

*Pyglet*, *Cython*, *Pillow*, and *PyOgg* are required dependencies and can easily be installed with *pip*. Use the versions specified in `requirements.txt`.

For audio to work you will either need *PyOgg* which is recommended, or FFmpeg which is installed on the system.
GStreamer is also supported on Linux through the *gst-python* library. PyOgg requires that your system have one of the *Opus*, *FLAC*, or *Vorbis* codecs. OpenAL is required.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==0.29`.

Alternatively, for a manual Cython build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode.

It is possible to enable a limited survival mode by editing `self.gamemode` in `Minecraft.py`.

### Gameplay

This is a creative version of Classic, so no mobs exist. All ores and tiles are featured in this version.

If you enable survival mode, there will be limited functionality.
Only sheep will spawn, which you can get wool from. Apart from that, no items drop.

Press B to pick blocks. Press F5 to toggle rain. Other keys are listed in the regular options menu.

### Multiplayer

To launch the multiplayer game, run `python -m mc.net.minecraft.Minecraft -server <host:port> -user <username> -mppass [password]`.

This client is compatible with any 0.30 server that doesn't use an extended network protocol.

Press *Tab* in-game to view connected players.

To host a server, follow the instructions in the `README.TXT` file in the *server* directory.
Make sure `verify-names` is set to `false` in the server properties.

### Additional Notes

The `mc.resources` directory contains all of the textures and sounds that this version uses. However,
the textures are only there for convenience, as all of the texture buffers are already preloaded
in the `mc.Resources` module.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).
