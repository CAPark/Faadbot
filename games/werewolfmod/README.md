# Werewolf Moderator

![](werewolfIMG.png)

This game is intended to work as a stand in for the player role of moderator so
that all people in attendance can play the game itself. This is done by using discord
as a medium for transmitting both public and private game information regarding the
events in the game. 

## Requirements

To run this game module, some form of database is needed. MySQL was used by the
developer when initially creating this. Other database options were not tested for 
so there is no guarantee that they will work. An account for your database is also required.
The module requires the "root" account with the password stored in a textfile labeled 
"dbPassLoc.txt"

### Setting up requirements

The entirety of faadbot requires Python 3.5+. If you have Python 3.4 or below, please
follow the guide on the main readme for upgrading to Python 3.6 and getting discord.py.

This guide will detail installation of both the client and the server for mysql.

Starting with the server use the following in your command line:
`sudo apt-get update`
`sudo apt-get install mysql-server`

This installer will install all required mysql utilities.
If the install tool does not automatically open use
`sudo mysql_secure_installation utility`

To access the now installed mysql server use
`mysql -u root -p`
The default password unless otherwise set will just be blank.

Now to install the client connector for the bot to connect:
`pip install mysql-connector`
or
`sudo apt-get install python3-mysql-connector`

### Using the module 

