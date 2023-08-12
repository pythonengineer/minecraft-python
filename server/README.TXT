## Minecraft public server alpha release ##

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


##

This is the very first release of the public minecraft server.

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




