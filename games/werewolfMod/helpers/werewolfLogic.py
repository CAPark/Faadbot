from werewolfSQL import werewolfSQL

class werewolfLogic:
    def __init__(self):
        self.werewolfSQL = werewolfSQL()

    #returns tuple containing (Boolean, string). Boolean indicates permission to 
    #run input action by playerID, string indicates associated message
    def checkNightActionPermission(self, isDay, actionName, playerID, targetName):
        status = None
        if isDay: #check if night
            status = "```Cannot use this action during the day```"
            return (False, status)
        else: 
            targetExists = False
            playerAlive = False
            playerPermission = False
            playerList = self.werewolfSQL.getRoundInfo()
            for player in playerList:
                if player[0] == targetName: #check target exists/alive
                    targetExists = True
                if int(player[1]) == playerID: #check player alive
                    playerAlive = True
                    roleAction = self.werewolfSQL.getSpecialAction(player[2])
                    if roleAction == actionName: #check player permissions for action
                        playerPermission = True
            
            #returning status messages in order of importance if failed
            if not targetExists:
                status = "```That target is dead or does not exist```"
                return (False, status)
            elif not playerAlive:
                status = "```You cannot use actions while dead```"
                return (False, status)
            elif not playerPermission:
                status = "```Your role does not have access to that action```"
                return (False, status)
            elif targetExists and playerAlive and playerPermission:
                return (True, status)

    def findAdjPlayers(self, playerName):
        playerLeft = None
        playerLeftLoc = 0
        playerCenter = playerName
        playerRight = None
        playerRightLoc = 0
        playerNameLoc = 0

        playerList = self.werewolfSQL.getRoundInfo()
        for index, player in enumerate(playerList):
            if player[0] == playerName:
                playerNameLoc = index
        
        if playerNameLoc == 0:
            playerLeftLoc = len(playerList) -1
            playerRightLoc = 1
        elif playerNameLoc == len(playerList) - 1:
            playerLeftLoc = playerNameLoc - 1
            playerRightLoc = 0
        else: 
            playerLeftLoc = playerNameLoc - 1
            playerRightLoc = playerNameLoc + 1

        playerTuple = playerList[playerLeftLoc]
        playerLeft = playerTuple[0]
        playerTuple = playerList[playerRightLoc]
        playerRight = playerTuple[0]

        names = []
        names.append(playerLeft)
        names.append(playerCenter)
        names.append(playerRight)

        return names

    def checkNightDone(self, roleSet, killDone, protectDone, checkDone,
        werewolfTarget, bodyguardTarget):
        infoList = []
        if roleSet == 'justVillagers': #TODO finish villagers
            if killDone:
                return True
            else:
                return False
        elif roleSet == 'basicSpecials':
            bodyguardStatus = self.werewolfSQL.checkBodyGuardStatus()
            seerStatus = self.werewolfSQL.checkSeerStatus()
            if bodyguardStatus: #bodyguard alive
                protectStatus = protectDone
            else:
                protectStatus = True #skip check if bodyguard is dead
            
            if seerStatus: #seer alive
                checkStatus = checkDone
            else:
                checkStatus = True #skip check if seer is dead
            if killDone and checkStatus and protectStatus:
                if not werewolfTarget == bodyguardTarget:
                    self.werewolfSQL.WLkill(werewolfTarget)
                return True
            else:
                return False