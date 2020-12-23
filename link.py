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

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

        # initialize dictionary to store grid positions and their respective utilities
        self.dict = {}

        # get number of rows and columns of game grid
        self.worldBreadth = config.worldBreadth
        self.worldLength = config.worldLength

        # get directional probability for moving in the supposed and unintentional directions
        self.directionProbability = config.directionProbability
        self.otherDirectionProbability = config.otherDirectionProbability
        
    def makeMove(self):
        self.positionAndUtility()
        self.getAndPositionUtility()
        """
        if len(allGold) > 0:
            nextGold = allGold[0]
        myPosition = self.gameWorld.getLinkLocation()
        # If not at the same x coordinate, reduce the difference
        if nextGold.x > myPosition.x:
            return Directions.EAST
        if nextGold.x < myPosition.x:
            return Directions.WEST
        # If not at the same y coordinate, reduce the difference
        if nextGold.y > myPosition.y:
            return Directions.NORTH
        if nextGold.y < myPosition.y:
            return Directions.SOUTH
        """

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
        
        # Get the location of Link.
        linkLocation = self.gameWorld.getLinkLocation()

        # first append the grids that have a value
        for gold in allGold:
            self.dict[(gold.x, gold.y)] = 1
        for wumpus in wumpusLocation:
            self.dict[(wumpus.x, wumpus.y)] = -1
        for pit in pitLocation:
            self.dict[(pit.x, pit.y)] = -1

        for x in range(self.worldBreadth):
            for y in range(self.worldLength):
                if (x, y) not in self.dict:
                    self.dict[(x, y)] = 0

    # calculate utility and update with grid position in dictionary, self.dict
    def getAndPositionUtility(self):
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
        

    def calculateUtilityForUp(self, keys):
        #get for up direction
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if x + 1 < self.worldBreadth:
            utility += self.directionProbability * self.dict[(x + 1, y)]
        else:
            utility += self.directionProbability * self.dict[(x, y)]

        #going left to the intended direction
        if y - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y - 1)]

        #going rigth to the intended direction
        if y + 1 >= self.worldLength:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y + 1)]

        # going down
        if x - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x - 1, y)]
        
        return utility
        
    def calculateUtilityForDown(self, keys):
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if x - 1 < 0:
            utility += self.directionProbability * self.dict[(x, y)]
        else:
            utility += self.directionProbability * self.dict[(x - 1, y)]

        #going left to the intended direction
        if y - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y - 1)]

        #going rigth to the intended direction
        if y + 1 >= self.worldLength:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y + 1)]

        # going up
        if x + 1 < self.worldBreadth:
            utility += self.otherDirectionProbability * self.dict[(x + 1, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y)]

        return utility
        
    def calculateUtilityForLeft(self, keys):
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if y - 1 < 0:
            utility += self.directionProbability * self.dict[(x, y)]
        else:
            utility += self.directionProbability * self.dict[(x, y - 1)]

        #going left to the intended direction
        if x + 1 < self.worldBreadth:
            utility += self.otherDirectionProbability * self.dict[(x + 1, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y)]

        #going rigth to the intended direction
        if y + 1 >= self.worldLength:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y + 1)]

        # going down
        if x - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x - 1, y)]

        return utility
        
    def calculateUtilityForRight(self, keys):
        x = keys[0]
        y = keys[1]
        utility = 0

        # going in the intended direction with P = 0.8
        if y + 1 >= self.worldLength:
            utility += self.directionProbability * self.dict[(x, y)]
        else:
            utility += self.directionProbability * self.dict[(x, y + 1)]
        
        #going right to the intended direction
        if x + 1 < self.worldBreadth:
            utility += self.otherDirectionProbability * self.dict[(x + 1, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y)]

        #going left to the intended direction
        if y - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x, y - 1)]

        # going down
        if x - 1 < 0:
            utility += self.otherDirectionProbability * self.dict[(x, y)]
        else:
            utility += self.otherDirectionProbability * self.dict[(x - 1, y)]

        return utility
        
