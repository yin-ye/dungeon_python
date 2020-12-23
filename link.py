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

class Link():

    def __init__(self, dungeon):

        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        
    def makeMove(self):
        # This is the function you need to define

        # Get the location of the gold.
        allGold = self.gameWorld.getGoldLocation()

        # Get the location of the wumpus.
        wumpusLocation = self.gameWorld.getWumpusLocation()
        #print(wumpusLocation[0].x)
        #print(wumpusLocation[0].y)

        # Get the location of the pits.
        pitLocation = self.gameWorld.getPitsLocation()
        # there are many pits, wumpus and golds
        #print(pitLocation[0].x)
        #print(pitLocation[0].y)

        # Get the location of the Link.
        linkLocation = self.gameWorld.getLinkLocation()
        print(linkLocation.x)

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

    def staticMovement(self):
        pass
