#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

class AStarData:
    def __init__(self):
        self.frontier = util.PriorityQueue()
        self.explored = set()
        self.cost_so_far = dict()

def astar_initialise(problem):
    astarData = AStarData()
    startState = problem.getStartState()
    astarData.frontier.push((startState, [], 0), 0)
    astarData.cost_so_far[startState] = 0
    return astarData

def astar_loop_body(problem, astarData):
    if astarData.frontier.isEmpty():
        return True, []

    state, actions, cost = astarData.frontier.pop()

    if problem.isGoalState(state):
        return True, actions

    if state in astarData.explored:
        return False, []

    astarData.explored.add(state)

    for successor, action, stepCost in problem.getSuccessors(state):
        newActions = actions + [action]
        newCost = cost + stepCost

        if successor in astarData.explored:
            continue

        if successor not in astarData.cost_so_far or newCost < astarData.cost_so_far[successor]:
            astarData.cost_so_far[successor] = newCost
            heuristicValue = astar_heuristic(successor, problem)
            totalCost = newCost + heuristicValue
            astarData.frontier.update((successor, newActions, newCost), totalCost)

    return False, []

def astar_heuristic(current, problem):
    food_list = problem.goal.asList()
    if not food_list:
        return 0
    return min (2 * util.manhattanDistance(current, dot) for dot in food_list)