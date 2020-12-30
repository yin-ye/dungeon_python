# link.py
#
# The code that defines the behaviour of Link. You should be able to
# do all you need in here, using access methods from world.py, and
# using makeMove() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import world
import random
import utils
from utils import Directions
import config

class Link():

    def __init__(self, dungeon):

        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # initialize dictionary to store grid positions and their respective utilities
        self.dict = {}

        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

        # get number of rows and columns of game grid
        self.worldBreadth = config.worldBreadth
        self.worldLength = config.worldLength

        # get directional probability for moving in the supposed and unintentional directions
        self.directionProbability = config.directionProbability
        self.otherDirectionProbability = config.otherDirectionProbability

        self.direction = ''
        self.count_when = 0

        """
        reward for wumpus and pit will depend on if the game is dynamic or static. If the game is
        dynamic, a lower value for pits and wumpus will be given
        """
        self.wumpus_reward = 0
        self.pit_reward = 0

    """
    if the game is static, wait for 20+ iterations to begin to move Link
    """
    def move_static(self):
        self.wumpus_reward = -1 
        self.pit_reward = -1.3
        
        if self.count_when >= 20:
            self.moveLink()

    """
    game is dynamic. Call moveLink() without any delay
    """
    def move_dynamic(self):
        self.wumpus_reward = -3
        self.pit_reward = -2
        self.moveLink()


    def makeMove(self):
        self.positionAndUtility()
        self.getAndPositionUtility()

        # checks for dynamic value of the game
        if config.dynamic == False:
            self.move_static()
        elif config.dynamic == True:
            self.move_dynamic()
        else:
            return

        # moves Link depending on the greatest utility
        if self.direction == 'left':
            return Directions.WEST
        elif self.direction == 'right':
            return Directions.EAST
        elif self.direction == 'up':
            return Directions.SOUTH
        elif self.direction == 'down':
            return Directions.NORTH
        else: 
            return
        

    """
    gets initial positions of pits, wumpus and golds. The dictionary checks for the other
    grid positions and stores accordingly. Keeps updating the positions of pits, wumpus and gold.
    """
    def positionAndUtility(self):
        # Get the location of the gold.
        allGold = self.gameWorld.getGoldLocation()

        # Get the location of the wumpus.
        wumpusLocation = self.gameWorld.getWumpusLocation()
        
        # Get the location of the pits.
        pitLocation = self.gameWorld.getPitsLocation()

        # first append the grids that have a value
        for gold in allGold:
            self.dict[(gold.x, gold.y)] = 1
        for wumpus in wumpusLocation:
            self.dict[(wumpus.x, wumpus.y)] = self.wumpus_reward
        for pit in pitLocation:
            self.dict[(pit.x, pit.y)] = self.pit_reward

        for x in range(self.worldBreadth):
            for y in range(self.worldLength):
                if (x, y) not in self.dict:
                    self.dict[(x, y)] = 0


    """
    calculates utility and update with grid position in dictionary, and stores in self.dict
    """ 
    def getAndPositionUtility(self):
        self.count_when += 1
        # reward to moving
        reward = -0.04

        for keys in self.dict:
            #calculate up, down, left and right utilities for the positions ("key")
            up = self.calculateUtilityForUp(keys)
            down = self.calculateUtilityForDown(keys)
            left = self.calculateUtilityForLeft(keys)
            right = self.calculateUtilityForRight(keys)

            # store that utility for the specific "keys"
            self.dict[keys] = reward + max(up, down, left, right)


    def moveLink(self):
        # Get the location of Link.
        linkLocation = self.gameWorld.getLinkLocation()
        
        pos_dict = {}
        
        """
        check if it is possible to move in all the directions(up, left, down, right). 
        If it is, assign the current utility of that grid position. Give a value (-2) 
        greater than the current worst reward for grid positions that are not available
        """
        # left
        if linkLocation.x - 1 < 0:
            left = -12
        else:
            left = self.dict[(linkLocation.x - 1, linkLocation.y)]
        pos_dict['left'] = left
        
        # right
        if linkLocation.x + 1 >= self.worldBreadth:
            right = -12
        else:
            right = self.dict[(linkLocation.x + 1, linkLocation.y)]
        pos_dict['right'] = right

        # down
        if linkLocation.y + 1 < self.worldLength:
            down = self.dict[(linkLocation.x, linkLocation.y + 1)]
        else:
            down = -12
        pos_dict['down'] = down
        
        # up
        if linkLocation.y - 1 < 0:
            up = -12
        else:
            up = self.dict[(linkLocation.x, linkLocation.y - 1)]
        pos_dict['up'] = up
        

        # get the maximum utility and move Link to that position
        max_util = max(up, down, left, right)
        
        # get the key that belongs to that max utility and move Link
        max_util_key = list(pos_dict.keys())
        max_util_val = list(pos_dict.values())
 
        position = max_util_val.index(max_util)
        self.direction = max_util_key[position] 
           
    """
    calculate all the utility and probability(for up, down, left and right) for all grid positions
    """
    def calculateUtilityForUp(self, keys):
        #get for up direction
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if y - 1 < 0:
            utility += self.directionProbability * self.dict[(x, y)]
        else:
            utility += self.directionProbability * self.dict[(x, y - 1)]

        #going left to the intended direction
        if x - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x - 1, y)]

        #going rigth to the intended direction
        if x + 1 >= self.worldBreadth:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x + 1, y)]

        # going down
        if y + 1 < self.worldLength:
            utility += self.otherDirectionProbability * self.dict[(x, y + 1)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        
        return utility
        
    def calculateUtilityForDown(self, keys):
        x = keys[0]
        y = keys[1]
        utility = 0
        
        # going in the intended direction with P = 0.8
        if y + 1 < self.worldLength:
            utility += self.directionProbability * self.dict[(x, y + 1)]
        else:
            utility += self.directionProbability * self.dict[(x, y)]

        #going left to the intended direction
        if x - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x - 1, y)]

        #going rigth to the intended direction
        if x + 1 >= self.worldBreadth:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x + 1, y)]

        # going up
        if y - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y - 1)]

        return utility
        
    def calculateUtilityForLeft(self, keys):
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if x - 1 < 0:
            utility += self.directionProbability * self.dict[(x, y)]
        else:
            utility += self.directionProbability * self.dict[(x - 1, y)]

        #going left to the intended direction
        if y + 1 < self.worldLength:
            utility += self.otherDirectionProbability * self.dict[(x, y + 1)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y)]

        #going rigth to the intended direction
        if x + 1 >= self.worldBreadth:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x + 1, y)]

        # going up
        if y - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y - 1)]

        return utility
        
    def calculateUtilityForRight(self, keys):
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if x + 1 >= self.worldBreadth:
            utility += self.directionProbability * self.dict[(x, y)]
        else:
            utility += self.directionProbability * self.dict[(x + 1, y)]
        
        #going right to the intended direction
        if y + 1 < self.worldLength:
            utility += self.otherDirectionProbability * self.dict[(x, y + 1)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y)]

        #going left to the intended direction
        if x - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x - 1, y)]

        # going down
        if y - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y - 1)]

        return utility
        
