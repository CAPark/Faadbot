import discord
from discord.ext import commands
import random
import mysql.connector
from mysql.connector import Error
import math
from games.werewolfMod.helpers.werewolfSQL import werewolfSQL
from games.werewolfMod.helpers.werewolfLogic import werewolfLogic

#currently supports a maximum of 10 players

class werewolfMan(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.rolesAdded = False
        self.roleSet = None
        self.lynchActive = False
        self.lynchSeconded = False
        self.lynchAttempt = 2 #counts down remaining attempts
        self.isDay = True
        self.statusList = None
        self.statusRef = [] #reference to statusList message in chat for editing
        self.actionRef = [] #reference to action messages list in chat for editing
        
        self.votesNeeded = 0 #number of votes needed for a vote to pass
        self.votesAcquired = 0 #current number of votes held
        self.votesAgainst = 0 #tallies votes against
        self.initiatorID = 0 #used to make sure initiator does try seconding his/her own things
        self.victimID = 0 #person vote is initiated against. Can also be set to kill victim at night
        self.protectID = 0 #person to be protected

        self.werewolfSQL = werewolfSQL()
        self.werewolfLogic = werewolfLogic()

        self.killDone = False
        self.protectDone = False
        self.checkDone = False

    @commands.command(name = 'Wstartup')
    async def Wstartup(self, ctx):
        await ctx.send("Initializing werewolf mod. \n")
        self.rolesAdded = False
        self.statusList = None
        self.statusRef = None

        self.werewolfSQL.WLstartup() #handles all MySQL actions for startup

        await ctx.send("Please input your name to join the game \n \
Ideally you should join in the order you are sitting \n \
Join Syntax: ``!Wjoin Playername`` \n \
After all players have joined but before starting the game you have to establish a role-set \n \
Current role-sets: ``justVillagers``, ``basicSpecials``, ``allSpecials`` \n \
Change roles Syntax: ``!WroleSetting justVillagers`` \n \
Game Start Syntax: ``!WbeginGame``")

    @commands.command(name = 'Whelp')
    async def Whelp(self,ctx):
        await ctx.send("Please input your name to join the game \n \
Ideally you should join in the order you are sitting \n \
Join Syntax: ``!Wjoin Playername`` \n \
After all players have joined but before starting the game you have to establish a role-set \n \
Current role-sets: ``justVillagers``, ``basicSpecials`` \n \
Change roles Syntax: ``!WroleSetting justVillagers`` \n \
Game Start Syntax: ``!WbeginGame``")

    @commands.command(name = 'WroleSetting')
    async def WroleSetting(self, ctx, arg1):
        playerCount = self.werewolfSQL.getPlayerCount()
        numWerewolves = int(math.floor(int(playerCount[0])/5))
        if arg1 == "justVillagers":
            await ctx.send("all special roles are disabled\n\
There will be {} werewolves".format(numWerewolves))
            self.werewolfSQL.WLroleSetting(playerCount[0], numWerewolves, 1)
            self.rolesAdded = True

        elif arg1 == "allSpecials":
            await ctx.send("This feature is not yet implemented. Please choose another")
        
        elif arg1 == "basicSpecials":
            await ctx.send("only seer and doctor are enabled\n\
There will be {} werewolves".format(numWerewolves))
            self.werewolfSQL.WLroleSetting(playerCount[0], numWerewolves, 2)
            self.rolesAdded = True

        else:
            await ctx.send("Invalid input")

    @commands.command(name = 'Wjoin')
    async def Wjoin(self, ctx, arg1):
        userID = "%s" % int(ctx.message.author.id)
        statusCode = self.werewolfSQL.WLjoin(userID, arg1)
        if statusCode == 0: #except error code
            await ctx.send("An error has occurred")
        elif statusCode == 1: #pass code
            await ctx.send("{} has joined the game".format(arg1))
        elif statusCode == 2: # duplicate name code
            await ctx.send("Duplicate name detected. Player names must be unique, please choose another name")
        elif statusCode == 3: #duplicate id code
            await ctx.send("Player name updated to {}".format(arg1))

    @commands.command(name = 'WbeginGame')
    async def WbeginGame(self, ctx):
        if self.rolesAdded:
            msgList = []
            msgActList = []
            self.werewolfSQL.WLcreateRound() #assigns roles to players
            playerList = self.werewolfSQL.getPlayerList() #gets list of userIDs
            for playerID in playerList:
                UIstring = self.werewolfSQL.makeUI(playerID[0], self.isDay) #gets UI string to send to player
                user = self.bot.get_user(int(playerID[0]))
                msg = await user.send(UIstring)
                msgList.append(msg)

                msgAct = await user.send("```Information on events will be shown in this window```")
                msgActList.append(msgAct)
            #self.statusRef.reverse()#puts inputs back in original order
            self.statusRef = msgList.copy()
            self.actionRef = msgActList.copy()
            print("verifying statusRef list")
            for msg in self.statusRef:
                print(msg)
            print("verifying actionRef list")
            for msg in self.actionRef:
                print(msg)

                playerCount = self.werewolfSQL.getPlayerCount()
                self.votesNeeded = math.ceil(int(playerCount[0])/2)
                print("Majority needed for lynch votes is {}".format(self.votesNeeded))
        else:
            await ctx.send("roles not yet set. Please set roles first")
  

# Action commands #########################################
###########################################################                                                         
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
# Action commands #########################################

    @commands.command(name = 'Wlynch')
    async def Wlynch(self, ctx, arg1):
        playerList = self.werewolfSQL.getPlayerList()
        msgActList = []
        if self.isDay and not self.lynchActive:
            arg1Exists = False
            initiator = None

            for player in playerList:
                if ctx.message.author.id == int(player[0]):
                    initiator = player[1]
                    self.initiatorID = int(player[0])
                if arg1 == player[1]:
                    arg1Exists = True
                    self.victimID = int(player[0])

            if arg1Exists:
                self.lynchActive = True
                self.lynchAttempt -= 1
                Notification = "```{} has start a lynch vote against {} but needs \
someone to second this notion! (Use !Wlynch Second to second the notion or !Wlynch Reject to reject)```".format(initiator, arg1)

                for player in playerList:
                    user = self.bot.get_user(int(player[0]))
                    msg = await user.send(Notification)
                    msgActList.append(msg)
                self.replaceOldMessage(msgActList)

        elif self.isDay and self.lynchActive:
            if arg1 == "Second" and not ctx.message.author.id == self.initiatorID:
                Notification = "```Notion to lynch passed. Select a reaction to vote\nVotes for: {}\nVotes against: {}```".format(self.votesAcquired, self.votesAgainst)
                self.initiatorID = 0
                for player in playerList:
                    user = self.bot.get_user(int(player[0]))
                    msg = await user.send(Notification)
                    msgActList.append(msg)
                self.replaceOldMessage(msgActList)
                await self.addVoteReactions()

            elif arg1 == "Reject" and not ctx.message.author.id == self.initiatorID:
                self.initiatorID = 0
                self.victimID = 0
                if self.lynchAttempt == 0:
                    self.isDay = False
                    self.lynchAttempt = 2
                    Notification = "```Notion to lynch rejected. The Day has ended```"
                else:
                    Notification = "```Notion to lynch rejected. There is 1 attempt left today```"
                for player in playerList:
                    user = self.bot.get_user(int(player[0]))
                    msg = await user.send(Notification)
                    msgActList.append(msg)
                self.replaceOldMessage(msgActList)
            else:
                await ctx.send("Invalid input. Please use only ``!Wlynch Second`` or ``!Wlynch Reject`` for responding to lynch requests")

    @commands.command(name = 'Wkill')
    async def Wkill(self, ctx, toKill):
        checkPermission = self.werewolfLogic.checkNightActionPermission(
            self.isDay, "!Wkill", ctx.message.author.id, toKill)
        
        permission = checkPermission[0]
        if not permission:
            status = checkPermission[1]
            await ctx.send(status)

        else:
            #TODO current implementation only supports single werewolf
            #TODO add vote system for additional werewolves
            self.victimID = self.werewolfSQL.getPlayerid(toKill)
            msg = "```You will kill {} tonight```".format(toKill)
            await ctx.send(msg)
            self.killDone = True

            shouldCycle = self.werewolfLogic.checkNightDone(
                self.roleSet, self.killDone, self.protectDone, self.checkDone,
                self.victimID, self.protectID)

            if shouldCycle:
                self.cycleNight()

    @commands.command(name = 'Wprotect')
    async def Wprotect(self, ctx, toProtect):
        checkPermission = self.werewolfLogic.checkNightActionPermission(
            self.isDay, "!Wprotect", ctx.message.author.id, toProtect)

        permission = checkPermission[0]
        if not permission:
            status = checkPermission[1]
            await ctx.send(status)

        else:
            self.protectID = self.werewolfSQL.getPlayerid(toProtect)
            msg = "```You will protect {} tonight```".format(toProtect)
            await ctx.send(msg)
            self.protectDone = True

            shouldCycle = self.werewolfLogic.checkNightDone(
                self.roleSet, self.killDone, self.protectDone, self.checkDone,
                self.victimID, self.protectID)

            if shouldCycle:
                self.cycleNight()


    @commands.command(name = 'Wcheck')
    async def Wcheck(self, ctx, toCheck):
        checkPermission = self.werewolfLogic.checkNightActionPermission(
            self.isDay, "!Wcheck", ctx.message.author.id, toCheck)

        permission = checkPermission[0]
        if not permission:
            status = checkPermission[1]
            await ctx.send(status)
        else:
            targetList = self.werewolfLogic.findAdjPlayers(toCheck)
            msg = "```You are checking the players "
            names = ', '.join(targetList)
            msg = msg + names
            tList = set(targetList)
            werewolfList = set(self.werewolfSQL.listWerewolves())
            if (tList & werewolfList):
                msg = msg + "\nThere is a werewolf among them```"
            else:
                msg = msg + "\nThere is no werewolf among them```"

        await ctx.send(msg)
        self.checkDone = True

        shouldCycle = self.werewolfLogic.checkNightDone(
            self.roleSet, self.killDone, self.protectDone, self.checkDone,
            self.victimID, self.protectID)

        if shouldCycle:
            self.cycleNight()


    

# Dev commands ############################################
###########################################################                                                         
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
# Dev commands ############################################

    @commands.command(name = 'WsaveUsers')
    async def WsaveUsers(self, ctx):
        await ctx.send("Attempting to save users in database locally")
        self.werewolfSQL.WLsaveUsers()

    @commands.command(name = 'WfillUsers')
    async def WfillUsers(self, ctx):
        await ctx.send("Attempting to fill database with saved users")
        self.werewolfSQL.WLfillUsers()

# Helper commands #########################################
###########################################################                                                         
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
# Helper commands #########################################

    def cycleNight(self): #used to reset variables in the instance of a day cycle completing or similar
        print("Initiating cycleNight")
        self.lynchActive = False
        self.lynchSeconded = False
        self.lynchAttempt = 2
        
        self.isDay = True
        self.votesAcquired = 0
        self.votesAgainst = 0
        self.initiatorID = 0
        self.victimID = 0
        self.protectID = 0

        self.killDone = False
        self.protectDone = False
        self.checkDone = False
    


    def replaceOldMessage(self, newMsg):#deletes old messages in self.actionRef and replaces them with the new action msgs
        print("Initiating replaceOldMessage()")
        for msg in self.actionRef:
            msg.delete()
        print("Old messages removed")
        self.actionRef = newMsg.copy()
        print("New messages added")
        for msg in self.actionRef:
            print(msg)
        print("replaceOldMessage() complete!")

    async def addVoteReactions(self): #adds checkbox and x reactions for voting on action messages
        print("Initiating addVoteReactions()")
        reactions = ['✅', '❌']
        for msg in self.actionRef:
            for item in reactions:
                await msg.add_reaction(item)
        print("addVoteReactions() complete!")

    async def updateLynchMessage(self, vote):
        print("Initiating updateLynchMessage")
        votePassed = False
        if vote == "yes":
            self.votesAcquired += 1
            if self.votesAcquired >= self.votesNeeded:
                print("Lynch vote has passed")
                votePassed = True
                self.votesAgainst = 0
                self.votesAcquired = 0
                self.isDay = False
            elif self.votesAgainst >= self.votesNeeded: #vote failed
                print("Lynch vote has failed")
                self.votesAgainst = 0
                self.votesAcquired = 0
                if self.lynchAttempt == 0:
                    self.isDay = False
                    self.lynchAttempt = 2
            self.lynchActive = False
        else:
            self.votesAgainst += 1
        Notification = "```Notion to lynch passed. Select a reaction to vote\nVotes for: {}\nVotes against: {}".format(self.votesAcquired, self.votesAgainst)
        if votePassed:
            Notification = Notification + "\n The vote to lynch has passed. Lynching will commence..."
            self.werewolfSQL.WLkill(self.victimID)
            
        Notification = Notification + "```"
        for msg in self.actionRef:
            await msg.edit(content = Notification)
        if votePassed:
            playerList = self.werewolfSQL.getPlayerList()
            for player in playerList:
                newUI = self.werewolfSQL.makeUI(player[0], self.isDay)
                user = self.bot.get_user(int(player[0]))
                await user.send(newUI)
        print("updateLynchMessage() complete!")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            print("Reaction detected")
            if reaction.emoji == '✅':
                print("Checkmark reaction detected")
                await self.updateLynchMessage("yes")
            elif reaction.emoji == '❌':
                print("X mark reaction detected")
                await self.updateLynchMessage("no")




def setup(bot):
    bot.add_cog(werewolfMan(bot))