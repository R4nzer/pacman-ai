#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#
import util
from game import Directions

class AStarToNearestFood:
    def __init__(self, gameState):
        self.startingGameState = gameState
        self.walls = gameState.getWalls()
        self.foodGrid = gameState.getFood()
        self.start = gameState.getPacmanPosition()
        self.goal = self.find_closest_food()

    def find_closest_food(self):
        from util import manhattanDistance
        foods = self.foodGrid.asList()
        reachable = []
        for food in foods:
            if self._is_reachable(food):
                reachable.append(food)
        return min(reachable, key=lambda f: manhattanDistance(self.start, f)) if reachable else None

    def _is_reachable(self, goal):
        from util import Queue
        queue = Queue()
        queue.push(self.start)
        visited = set()
        while not queue.isEmpty():
            curr = queue.pop()
            if curr == goal:
                return True
            if curr in visited:
                continue
            visited.add(curr)
            x, y = curr
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                nx, ny = x + dx, y + dy
                if not self.walls[nx][ny] and (nx, ny) not in visited:
                    queue.push((nx, ny))
        return False

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state == self.goal

    def getSuccessors(self, state):
        successors = []
        x, y = state
        for dx, dy, action in [
            (0, 1, Directions.NORTH),
            (0, -1, Directions.SOUTH),
            (1, 0, Directions.EAST),
            (-1, 0, Directions.WEST)
        ]:
            next_x, next_y = x + dx, y + dy
            if not self.walls[next_x][next_y]:
                successors.append(((next_x, next_y), action, 1))
        return successors

def q1c_solver(problem):
    total_actions = []
    current_state = problem.getStartState()
    food_grid = current_state[1]
    game_state = problem.startingGameState

    while food_grid.count() > 0:
        sub_problem = AStarToNearestFood(game_state)
        actions = a_star_search(sub_problem)
        if not actions:
            break  # No more reachable food
        for action in actions:
            game_state = game_state.generateSuccessor(0, action)
        total_actions += actions
        current_state = (game_state.getPacmanPosition(), game_state.getFood())
        food_grid = current_state[1]

    return total_actions


def a_star_search(problem):
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, []), heuristic(start, problem))
    explored = set()
    cost_so_far = {start: 0}

    while not frontier.isEmpty():
        state, path = frontier.pop()
        if problem.isGoalState(state):
            return path

        if state in explored:
            continue
        explored.add(state)

        for successor, action, stepCost in problem.getSuccessors(state):
            new_cost = cost_so_far[state] + stepCost
            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, path + [action]), priority)

    return []


def heuristic(state, problem):
    from util import manhattanDistance
    return manhattanDistance(state, problem.goal) if problem.goal else 0
