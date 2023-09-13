## Minecraft public server alpha release ##


To change any settings, edit server.properties.
To run a private server, set isPublic to false in the properties. To connec to your server, people should open the following url in their browsers:
http://www.minecraft.net/play.jsp?server=<YOUR IP>&port=<SERVER PORT>

To start the server, run "start server.bat" on windows. On any other system, the command you want is:
java -cp minecraft-server.jar com.mojang.minecraft.server.MinecraftServer

Add any user names you want to have op to admin.txt

Ingame, ops can use the following commands:
/op <name>         Ops the player with name <name>. They have to be logged in.
/deop <name>       De-ops a player.
/kick <name>       Kicks a player
/ban <name>        Bans and kicks a player
/unban <name>      Pardons a banned player
/banip <name>      Bans a player by ip number. Cannot be undone ingame, you must manually change banned-ip.txt
/say <message>     Broadcasts <message> across the entire server.
/setspawn          Sets the current location as the default spawn location for new players
/tp <name>         Teleports to a player.   
/solid             Switches between placing normal and placing unbreakable stone



## Changelog:

Version 1.8.3:

+ Added support for new tile types.
+ Fixed exploit where someone logging in with an illegal name would cause players to disconnect.

Version 1.8.2:

+ Ooops, everyone could build unbreakable blocks! Fixed!

Version 1.8.1:

+ Fixed a protocol error.

Version 1.8:

+ Added a whole bunch of new tile types
+ Players can no longer destroy unbreakable stone. Admins can, though!
+ Added /solid command to toggle stone tile type between normal and unbreakable

Version 1.7:

+ Added /tp as an alias for teleport

Version 1.6:

+ Fixed sponge working weirdly

Version 1.5:

+ Fixed a client crash bug on chat
+ You can now send most admin commands via stdin
+ Added chat throttling. Players who spam the chat will get muted for eight seconds
+ Added movement throttling. The server will not process more than a single move command per tick.
  (stand still to catch up if you're lagging)
+ Added max-connections to server.properties. This is the maximum number of connections per ip to the server. Default is three. 

Version 1.4.1:

+ Fixed bad names connecting and crashing all players

Version 1.4:

+ Added a /teleport command. It doesn't work yet, though, since it requires a client update.
+ Tried to fix two remove client crashes

Version 1.3:

+ Name security
+ Server-side client verification
+ Add logged-in.txt on the server
+ added /setspawn command for admins
+ Fix heartbeat pausing the game
+ Don’t let people spam ping requests
+ Fix ban ip (it was working, but not intuitive)
+ Various server fill exploit preventions. No more lava floods!
+ Private server adresses changed behavior, sorry. The server generates an externalurl.txt when run now.
+ Added verify-names to properties. Set this to false to allow people to connect directly via http://www.minecraft.net/play.jsp?ip=<ip>&port=<port>

Version 1.2:

+ Fixed a connection problem
+ Maybe fixed /banip

Version 1.1:

+ Made the private flag work
+ Added a /say command. Used to be /broadcast

Version 1.0:

  Initial release