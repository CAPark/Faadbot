import mysql.connector
from mysql.connector import Error
import math
import random
import re # used for multi-delimiter tokenizing

class werewolfSQL:
    def __init__(self):
        self.dbPassLoc = "games/werewolfMod/localhostDBPW.txt"
        self.testUserList = "games/werewolfMod/testUserInfo.txt"
        self.dbName = "testDB" #name of sql database, change if necessary
    
    def WLstartup(self):
        #get localhost mysql password for root
        TOKEN = open(self.dbPassLoc, "r").read()

        try:
            connection = mysql.connector.connect(
                host = 'localhost', 
                database = self.dbName, #change db name if necessary
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                print("****************************************************\n")
                print("Connected to database for reset\n")
                cursor = connection.cursor()

                #drops tables needed for game if exists
                cursor.execute("DROP TABLE IF EXISTS players")
                cursor.execute("DROP TABLE IF EXISTS roles")
                cursor.execute("DROP TABLE IF EXISTS round")
                #all require tables should no longer exist now. 
                #Recreating tables

                #in table players, name is the player chosen name for the game instance
                #userID is the userID number tied to the discord user in the game
                makePlayers = "CREATE TABLE players (userID VARCHAR(50) PRIMARY KEY, \
                    name VARCHAR(255) NOT NULL)"
                #in table roles, rolename is the name for a player role. Only role names
                #from the official werewolf game are acceptable here
                #roleStatus is a binary int that indicates if the role has been assigned to a player
                makeRoles = "CREATE TABLE roles (roleName VARCHAR(255), roleStatus TINYINT, specialAction VARCHAR(50))"
                #in table round, name is the player chosen name for the game instance
                #userID is the userID number tied to the discord user in the game
                #rolename is the name for a player role associated to the player entry
                #status is a binary int indicating if the player is alive or not (1 for alive)
                makeRound = "CREATE TABLE round (id INT AUTO_INCREMENT PRIMARY KEY, \
                    name VARCHAR(255), userID VARCHAR(50), roleName VARCHAR(255), \
                    status INT(1))"

                #execute above sql calls to create tables
                cursor.execute(makePlayers)
                cursor.execute(makeRoles)
                cursor.execute(makeRound)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection for reset is closed\n")
                print("****************************************************\n")

    def WLjoin(self, userID, inputName):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)
            
            if connection.is_connected():
                print("****************************************************")
                print("Accessing database to add player\n")
                cursor = connection.cursor()
                returnCode = 4
                unique = True
                print("userID is " + userID)
                cursor.execute("SELECT * FROM players")
                playerList = cursor.fetchall()
                for entry in playerList:
                    
                    print(entry[0] )#" " + userID)
                    #first check duplicate username
                    if entry[1] == inputName:
                        print("duplicate username {}. Aborting.\n".format(entry[1]))
                        print("****************************************************")
                        unique = False
                        returnCode = 2 #duplicate username code
                    elif entry[0] == userID:
                        print("duplicate id {}. Updating player name.\n".format(entry[0]))
                        sql = "UPDATE players SET name = %s WHERE userID = %s"
                        inVal = (inputName, entry[0])
                        cursor.execute(sql, inVal)
                        connection.commit()
                        print(cursor.rowcount, "record(s) affected")
                        unique = False
                        print("****************************************************")
                        returnCode = 3 #duplicate id code 
                
                if unique == True:
                    sql = "INSERT INTO players (userID, name) VALUES (%s, %s)"
                    print("Connected to database to add " + userID +":" + inputName)
                    inVal = (userID, inputName)
                    cursor.execute(sql, inVal)
                    connection.commit()
                    print(cursor.rowcount, "record inserted.")
                    returnCode = 1 #pass code

        except Error as e:
            print("Error while connecting to MySQL", e)
            returnCode = 0 #error code
        finally:
            if connection.is_connected:
                cursor.close()
                connection.close()
                print("returnCode is {}\n".format(returnCode))
                print("****************************************************")
                return returnCode #pass code, new user joined
    
    def WLroleSetting(self, playerCount, werewolfCount, roleSet):#roleSet is an int
        TOKEN = open(self.dbPassLoc, "r").read()
        wwinVal = ('werewolf', '0', '!Wkill')
        basicinVal = [
            ('seer', '0', '!Wcheck'),
            ('bodyguard', '0', '!Wprotect')
        ] 
        sql = "INSERT INTO roles( roleName, roleStatus, specialAction) VALUES (%s, %s, %s)"
        #roles for allSpecials not currently implemented
        #planned: seerInsane, hunter, fool, mason, pacifist, gunsmith
        #ref: https://boardgamegeek.com/wiki/page/BGG_Werewolf_PBF_Role_List

        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to insert roles")
                
                #first putting in werewolves
                for _ in range(werewolfCount):
                    cursor.execute(sql, wwinVal)
                    connection.commit()
                    print(cursor.rowcount, " werewolf added")

                #adding in seer/bodyguard if basicSpecials enabled
                villagerCount = playerCount - werewolfCount
                if roleSet == 2:
                    villagerCount -= 2
                    cursor.executemany(sql, basicinVal)
                    connection.commit()
                    print(cursor.rowcount, " special roles were added")
                
                #adding in villagers for remaining player count
                for _ in range(villagerCount):
                    cursor.execute(sql, ('villager', '0', None))
                    connection.commit()
                    print(cursor.rowcount, " villager added")

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************\n")
            
    def WLcreateRound(self):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)
            
            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************\n")
                cursor.execute("SELECT * FROM players")
                playerList = cursor.fetchall()
                for entry in playerList: #format (userID, name)
                    sql = "INSERT INTO round (name, userID, status) VALUES (%s, %s, %s)"
                    roundVal = (entry[1], entry[0], "1")
                    cursor.execute(sql, roundVal)
                    connection.commit()
                #all players now added to statusList
                #actually assigning roles now
                cursor.execute("SELECT * FROM round")
                roundList = cursor.fetchall()
                for entry in roundList:#format (id, name, userID, roleName, status, specialAction)
                    cursor.execute("SELECT * FROM roles WHERE roleStatus = '0'")
                    openRolesList = cursor.fetchall()
                    openRoles = []
                    for role in openRolesList:
                        openRoles.append(role[0])
                    chosenRole = random.choice(openRoles)


                    sql = "UPDATE round SET roleName = %s WHERE userID = %s"
                    inputVal = (chosenRole, entry[2])
                    cursor.execute(sql, inputVal)
                    connection.commit()
                    print("Player: {}:{} is role: {}".format(entry[1], entry[2], chosenRole))

                    #removing the chosenRole from openRole db
                    sql = "UPDATE roles SET roleStatus = %s WHERE roleName = %s AND roleStatus = '0' limit 1"
                    roleUpdate = ("1", chosenRole)
                    cursor.execute(sql, roleUpdate)
                    connection.commit()

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            cursor.close()
            connection.close
            print("****************************************************")
                

    #helper methods
    #returns a large string to display to players with current game information
    def makeUI(self, playerID, isDay):
        TOKEN = open(self.dbPassLoc, "r").read()
        UIstring = "```Use this chat to make your actions\n-------------------------------------------\nPlayer Statuses:\n"
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)
            
            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to create UI string for: " + playerID)
                werewolfList = self.listWerewolves()
                #print("Werewolves obtained. Creating string")
                PlayerisWerewolf = False
                PlayerisVillager = False

                cursor.execute("SELECT * FROM round")#format (id, name, userID, roleName, status)
                roundList = cursor.fetchall()
                for entry in roundList:
                    #print("processing entry: " + entry)
                    EntryisPlayer = False
                    #check if werewolf (determines if I should display other werewolves)
                    EntryisWerewolf = False #reset for each entry
                    for werewolf in werewolfList:
                        if not PlayerisWerewolf and werewolf == playerID:
                            PlayerisWerewolf = True
                        if entry[2] == werewolf:
                            EntryisWerewolf = True

                    #check player status
                    if int(entry[4]) == 0:
                        playerStatus = "Dead "
                    else:
                        playerStatus = "Alive "

                    #check if player (determines if I show role)
                    if entry[2] == playerID:
                        EntryisPlayer = True
                        if entry[3] == 'villager':
                            PlayerisVillager = True
                        else:
                            playerRole = entry[3]

                    #start putting entries into UI string
                    if EntryisPlayer:
                        UIstring = UIstring + entry[1] + ": " + playerStatus + entry[3] +"\n"
                        #UIstring = UIstring + "-{}: {} {}\n".format(entry[1], playerStatus, entry[3])
                        print(entry[1] + ": " + playerStatus + entry[3] +"\n")
                    elif PlayerisWerewolf and EntryisWerewolf:
                        UIstring = UIstring + entry[1] + ": " + playerStatus + entry[3] +"\n"
                        #UIstring = UIstring + "-{}: {} {}\n".format(entry[1], playerStatus, entry[3])
                        print(entry[1] + ": " + playerStatus + entry[3] +"\n")
                    else:
                        UIstring = UIstring + entry[1] + ": " + playerStatus+"\n"
                        #UIstring = UIstring + "-{}: {}\n".format(entry[1], playerStatus)
                        print(entry[1] + ": " + playerStatus +"\n")

                #players should now be done in UIstring so adding seperator
                UIstring = UIstring + "-------------------------------------------\nYour Actions:\n"
                #adding !Wlynch since everyone has that action
                #adding !Wskip since everyone has that action
                UIstring = UIstring + "!Wlynch\n!Wskip\n"

                if not PlayerisVillager:
                    specialAct = self.getSpecialAction(playerRole)
                    UIstring = UIstring + specialAct

                #adding in time of day
                if isDay:
                    UIstring = UIstring + "\n-------------------------------------------\nIt is Daytime```"
                else:
                    UIstring = UIstring + "\n-------------------------------------------\nIt is Nighttime```"

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally: 
            cursor.close()
            connection.close()
            print("****************************************************")
            return UIstring

    #returns a list of current werewolf names
    def listWerewolves(self):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)
            
            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to obtain list of werewolves")
                cursor.execute("SELECT * FROM round WHERE roleName = 'werewolf'")
                playerList = cursor.fetchall()
                nameList = []
                for player in playerList:
                    nameList.append(player[0])
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            cursor.close()
            connection.close()
            print("****************************************************")
            return nameList


    #returns special action for input role
    def getSpecialAction(self, roleName):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)
            
            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to obtain special action information")
                cursor.execute("SELECT * FROM roles WHERE roleName = %s", (roleName, ))
                specialAction = cursor.fetchone()
                print("Found special action for " + roleName + " is " + specialAction[2])

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")
                return specialAction[2]

    #returns list with playerID and associated role and status. Used for logic in special moves
    def getRoundInfo(self):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to obtain current playerlist\n")
                playerList = []
                cursor.execute("SELECT * FROM round WHERE status = '1'")
                players = cursor.fetchall()
                for entry in players:
                    playerList.append((entry[1], entry[2], entry[3]))
                for entry in playerList:
                    print(entry)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")
                return playerList

    #returns ID of playerName input
    def getPlayerid(self, playerName):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to get player id\n")
                cursor.execute("SELECT * FROM players WHERE name = %s", playerName)
                playerInfo = cursor.fetchone()
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")
                return playerInfo[0]

    #returns name of playerID input
    def getPlayerName(self, playerid):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to get player name\n")
                cursor.execute("SELECT * FROM players WHERE userID = %s", playerid)
                playerInfo = cursor.fetchone()
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")
                return playerInfo[1]

    #returns current number of players registered for game
    def getPlayerCount(self):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to obtain current player count\n")
                cursor.execute("SELECT COUNT(*) FROM players")
                playerCount = cursor.fetchone()
                print("there are {} players\n".format(playerCount[0]))
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")
                return playerCount

    #returns current list of playerid registered for game
    def getPlayerList(self):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to obtain current playerlist\n")
                playerList = []
                cursor.execute("SELECT * FROM players")
                players = cursor.fetchall()
                for entry in players:
                    playerList.append((entry[0], entry[1]))
                for entry in playerList:
                    print(entry)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")
                return playerList

    def WLkill(self, userID):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                database = self.dbName,
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                print("Accessing database to kill player\n")
                sql = ("UPDATE round SET status = '0' WHERE userID = %s")
                victim = (userID, )
                cursor.execute(sql, victim)
                connection.commit()

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("****************************************************")

    #for populating database with saved test users
    def WLfillUsers(self):
        try:
            userListFile = open(self.testUserList, "r")
            print("****************************************************\n")
            print("Filling database with saved users\n")
            user = []
            TOKEN = open(self.dbPassLoc, "r").read()
            for line in userListFile:
                user = re.split('[:\n]', line)
                try:
                    connection = mysql.connector.connect(
                        host = 'localhost', 
                        database = self.dbName, #change db name if necessary
                        user = 'root',
                        password = TOKEN)

                    if connection.is_connected():
                        cursor = connection.cursor()
                        sql = "INSERT INTO players (userID, name) VALUES (%s, %s)"
                        values = (user[0], user[1])
                        cursor.execute(sql, values)
                        connection.commit()

                except Error as e:
                    print("Error while connecting to MySQL", e)
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
                        print("Saved userID {} and user {} added to database\n".format(user[0], user[1]))
        except:
            print("File for test users does not exist\n")
        finally:
            userListFile.close()
            print("****************************************************\n")

    #for saving current test users in database
    #WARNING: will delete previously saved set of test users
    def WLsaveUsers(self):
        try:
            print("****************************************************\n")
            print("Loading users from database to save\n")
            userListFile = open(self.testUserList, "w")
            try:
                TOKEN = open(self.dbPassLoc, "r").read()
                connection = mysql.connector.connect(
                    host = 'localhost',
                    database = self.dbName,
                    user = 'root',
                    password = TOKEN)
                
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM players")
                    userList = cursor.fetchall()
                    for user in userList:
                        userListFile.write("{}:{}\n".format(user[0], user[1]))
                        print("adding {} {} to file\n".format(user[0], user[1]))
            
            except Error as e:
                print("Error while connecting to MySQL", e)
            finally:
                cursor.close()
                connection.close()
        
        except:
            print("Failed to open user file for saving\n")
        finally:
            print("Completed saving test users from database")
            print("****************************************************\n")
            userListFile.close()