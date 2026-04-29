import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1b_problem:
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState = gameState
        self.startState = gameState.getPacmanPosition()
        self.goal = gameState.getFood()
        self.walls = gameState.getWalls()
        self.costFn = 1
        self.goal_positions = set(self.goal.asList())

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.startState

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        return state in self.goal_positions

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        successors = []
        x, y = state

        directions = [
            (0, 1, Directions.NORTH),
            (0, -1, Directions.SOUTH),
            (1, 0, Directions.EAST),
            (-1, 0, Directions.WEST),
        ]

        for dx, dy, action in directions:
            next_x, next_y = x + dx, y + dy
            if not self.walls[next_x][next_y]:
                successors.append(((next_x, next_y), action, self.costFn))
        return successors