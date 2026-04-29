import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"
        def alpha_beta(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), None

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth

            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state), None

            if agentIndex == 0:
                value = -float('inf')
                bestAction = None
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    successorValue, _ = alpha_beta(successor, nextDepth, nextAgent, alpha, beta)
                    if successorValue > value:
                        value = successorValue
                        bestAction = action
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
                return value, bestAction
            else:
                value = float('inf')
                bestAction = None
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    successorValue, _ = alpha_beta(successor, nextDepth, nextAgent, alpha, beta)
                    if successorValue < value:
                        value = successorValue
                        bestAction = action
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
                return value, bestAction

        _, action = alpha_beta(gameState, self.depth, 0, -float('inf'), float('inf'))
        return action
    
def betterEvaluationFunction(currentGameState):
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    score = currentGameState.getScore()

    minFoodDist = min([manhattanDistance(pacmanPos, food) for food in foodList]) if foodList else 0
    minCapsuleDist = min([manhattanDistance(pacmanPos, c) for c in capsules]) if capsules else 0

    activeGhosts = []
    scaredGhosts = []

    for ghost in ghostStates:
        if ghost.scaredTimer > 0:
            scaredGhosts.append(ghost)
        else:
            activeGhosts.append(ghost)

    activeGhostDistances = [manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in activeGhosts]
    scaredGhostDistances = [manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in scaredGhosts]

    evalScore = score

    if foodList:
        evalScore += 12.0 / (minFoodDist + 1)
    evalScore += 120.0 / (len(foodList) + 1)

    if capsules:
        evalScore += 15.0 / (minCapsuleDist + 1)

    for dist in scaredGhostDistances:
        evalScore += 300.0 / (dist + 1)

    for dist in activeGhostDistances:
        if dist <= 1:
            evalScore -= 1200
        else:
            evalScore -= 10.0 / (dist + 0.1)

    return evalScore
