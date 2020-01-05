# Faadbot

## Operation and Requirements

The use of this discord bot requires the host to have python 3 and discord.py installed.

#### Linux

First start with installation of Python 3.
`$sudo apt-get install python3.6`
After the installation is complete, install discord.py
`$pip install discord.py`

Once these dependancies are installed, the python files can be executed to connect the bot to the linked
test server. This model of the bot is dependant on a text file that contains the OAuth2 token for discord.
Create a new application on discord to generate a OAuth2 token for use. 

The helloWorld.py file contains a minimally viable product that connects the bot to the server and
responds to all inputs starting with the character`!` with "Hello World". The main.py file contains
the base module for the final product. 

*NOTE:*

In some circumstances, python 2 may be installed as part of the operating system. If this is the case, 
you will need to install pip 3 and use that to ensure that an old version of discord.py is not installed
`$pip3 install discord.py==1.0.1`
`$pip3 install --upgrade discord.py`

## Project Abstract

    Discord is a popular application that works in a similar manner to slack. Discord provides users the
    ability to create servers that other users can join to communicate with one another. Regardless of the
    focus of the server, there are often a number of features that can be troublesome to handle on larger
    sized servers. To fix this, discord bots can be made to handle common items like moderating chats, 
    assigning priviledges to particular users, or working with user management. This bot can also have 
    entertainment focused features like custom image posting or hosting of mini chat-based games. 
    For the purpose of this project, I plan on creating a discord bot that features several moderation 
    functions. All of these features will be implemented modularly using the discord api, and should 
    the project be too small, other entertainment focused modules can be implemented as well.
    
    For the complete project, interaction with the bot will be handled using the actual discord
    application. Since discord has a lot of bot friendly functionality, the bot would actually be
    added to a particular server as a bot, and interaction occurs in the text chat using a chosen
    special character. For example, if I have a help function with my bot, and use "!" as my 
    special character, I can invoke the help function by typing "!help" in chat.

## Background
    
    [https://github.com/CAPark/01-Park-FAADBot]
    
    Regarding the name of the project: the main function of the bot is to work as a ModeratorBot, which
    could simplify into ModBot. The problem with that name is that it is incredibly common and not
    distinguishable from the thousands of other ModBots. So to create the new name, I took the "Mod"
    section and converted the ascii values of letters into binary and then into hex. The final hex 
    number had 4 numbers in it and the letters "F" and "D". I just added the numbers up to get 20, 
    and chose "A" for the remaining to letters since "A" has a hex value of 10, having two adding 
    up to 20. As a result, I mashed together the letters "F", "A", "A", and "D" to get FAADBot.
    
## Vision

*FOR* discord users *WHO* have user requests that require moderator approval, the FAADBot 
is a discord bot *THAT* automates handling of these mundane tasks to reduce workload on moderators
*UNLIKE* most other discord bots, *OUR PRODUCT* will be created modularly to promote open-source additon 
of additional functionalities.

## Personas
#### Alex - Streamer

Alex, age 23, is a college student at XYZ university in Vermont. He is in his third year for an accounting degree.
When Alex isn't busy with his academics, he spends a significant amount of his time playing video games. Alex
frequently uses discord to coordinate and communicate with his friends while playing games with them. Recently, 
with the increasing popularity of video game streaming in the past year, Alex wanted to attempt it himself. 
Since a majority of the starting difficulty of a streamer stems from advertising your channel, Alex takes to
discord as a means of putting out awareness of his streams. 

#### Jimmy - New Member

Jimmy, age 20, is a criminal justice major at a university in New York. Jimmy likes to spend his free time
reading or watching documentaries. Jimmy has joined a club for other law majors to network, socialize and
share resources. Jimmy wants to form new connections and make friends with other undergraduates in his field. 
This club’s members use Discord to communicate. Jimmy isn’t tech-illiterate but is not necessarily tech-savvy 
either. The only messaging app he’s familiar with is Facebook Messenger, so Discord is a new experience for him. 
Jimmy downloads the app and joins the server linked on the club’s webpage. He is initially overwhelmed by the 
options and settings available. Jimmy doesn’t want to join any large group discussions and is more so seeking to 
get to know some people individually.

#### Summer - Moderator

Summer, age 32, is an owner of a baby product company and she herself is having one, 12 months old, daughter. 
In order to get information about customer needs for baby products, she runs a parenting club. There are 1 million 
members in the club, consist of 67.5% women and 32.5% men, and 88% of members are from 25-39 age groups. She uses 
Discord to communicate with announce to club members. Summer never used Discord before, and she is not a tech-friendly 
person. She was overwhelmed by a huge number of functions Discord have. Also, because she's running a company, she 
doesn't want to spend much time managing the Discord server but she still wants to make the Discord server page clean. 
Since the size of the club is big, there are some people who helps her running the club so she wants to assign some 
roles to people on Discord server. To keep the server page clean, she wants to filter new users and exorcise users who 
spoil the atmosphere. 

#### Phil - Existing Member

Phil, age 23, is a making a new soccer club at his University. His Club has attracted a lot of people lately to join the 
club as there isn't an existing soccer club at the university. With the increasing amount of members joining in and a lot 
of new members who are new to the sport, Phil wants to create a channel where he can communicate with the members in a 
much managable manner and share tutorials which can help them learn new skills. Phil is already aware of discord and all 
the functioanlities it can bring in creating a much mangable channel. Phil decides to use Discord as a mean of communication 
and teaching new skills through video tutorials to all the members. 

## Initially Planned Features

- Adding and removing roles (normal user)
- Change nicknames (normal user)
- Text to speech (normal user)
- Ban users (moderator/super user)
- Create or Delete roles (moderator/super user)

## Resources

[Link to Trello Board](https://trello.com/b/GrKoPabm/faadbot)

[Link to the discord server for testing](https://discord.gg/gv97GxT)

[Link to discord's python API](https://discordpy.readthedocs.io/en/latest/)

[Link to simple cog use example](https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be)

[Link to resource to search for in context use of specific methods in modules](https://www.programcreek.com/python/)


## Group Members

- Christopher Park
- Sungji Kim
- Maamar Bousseloub
- Dawud Baig
