#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

def q1a_solver(problem: q1a_problem):
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
        self.cost_so_far = {}

def astar_initialise(problem):
    data = AStarData()
    start = problem.getStartState()
    data.frontier.push((start, [], 0), 0)
    data.cost_so_far[start] = 0
    return data

def astar_loop_body(problem, data):
    if data.frontier.isEmpty():
        return True, []

    state, actions, cost = data.frontier.pop()

    if state in data.explored:
        return False, []

    data.explored.add(state)

    if problem.isGoalState(state):
        return True, actions

    for successor, action, stepCost in problem.getSuccessors(state):
        if successor in data.explored:
            continue
        newCost = cost + stepCost
        if successor not in data.cost_so_far or newCost < data.cost_so_far[successor]:
            data.cost_so_far[successor] = newCost
            heuristic = astar_heuristic(successor, problem)
            totalCost = newCost + heuristic
            data.frontier.update((successor, actions + [action], newCost), totalCost)

    return False, []

def astar_heuristic(state, problem):
    return util.manhattanDistance(state, problem.goal_pos)