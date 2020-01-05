#module meant to unit test werewolfMod game

import unittest #allows for unit testing
import math
import sys
#sys.path.insert('')
import werewolfSQL
import werewolfLogic

class TestWerewolfMod(unittest.TestCase):
    print("Beginning TestWerewolfMod!")
    print(sys.path)

        #self.werewolfLogic = werewolfLogic()
        
    def test_checkNightActionPermission(self): 
        #outline cases
        Pass = (True, None)
        notDay = (False, "```Cannot use this action during the day```")
        notExisting = (False, "```That target is dead or does not exist```")
        notAlive = (False, "```You cannot use actions while dead```")
        notPermitted = (False, "```Your role does not have access to that action```")

        #instantiate
        SQL = werewolfSQL.werewolfSQL()
        Logic = werewolfLogic.werewolfLogic()

        SQL.WLstartup() #reset database
        SQL.WLfillUsers() #fill database with users from test file
        
        playerCount = SQL.getPlayerCount()
        numWerewolves = int(math.floor(int(playerCount[0])/5))
        SQL.WLroleSetting(playerCount[0],numWerewolves, 2)

        

if __name__ == '__main__':
    unittest.main()