# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def heuristic1(state, problem=None):
    from search_agents import FoodSearchProblem
    
    # 
    # heuristic for the find-the-goal problem
    # 
    
    # ADDED CODE 
    # print(state)
    # print(problem)
    # help(state)
    # ADDED CODE 

    if isinstance(problem, SearchProblem):
        # data
        pacman_x, pacman_y = state
        goal_x, goal_y     = problem.goal
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
        optimisitic_number_of_steps_to_goal = abs(pacman_x - goal_x) + abs(pacman_y - goal_y)
        return optimisitic_number_of_steps_to_goal
    # 
    # traveling-salesman problem (collect multiple food pellets)
    # 
    elif isinstance(problem, FoodSearchProblem):
        # the state includes a grid of where the food is (problem isn't ter)
        position, food_grid = state
        pacman_x, pacman_y = position
        
        # ADDED CODE 
        #help(food_grid)
        #food_grid.data
        # ADDED CODE 

        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)

        optimisitic_number_of_steps_to_goal = 0
        remaining_food = food_grid.as_list()
        for x, y in remaining_food:
            optimisitic_number_of_steps_to_goal += (abs(pacman_x - x) + abs(pacman_y - y))
        return optimisitic_number_of_steps_to_goal

def a_star_search(problem, heuristic=heuristic1):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # What does this function need to return?
    #     list of actions that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    # start_state = problem.get_start_state()
    # transitions = problem.get_successors(start_state)
    # heuristic(start_state, problem)
    # example_path = [  transitions[0].action  ]
    # path_cost = problem.get_cost_of_actions(example_path)
    # return example_path

    from queue import PriorityQueue
    import heapq
    
    class Node:
        def __init__(self, state, h, action=None, parent=None, g=None):
            self.state = state
            self.action = action
            self.parent = parent
            if parent:
                self.g = g + parent.g
            else:
                self.g = 0
            self.h = h
            self.f = self.g + self.h

        def __lt__(self, other):
            return True

        def output_actions(self):
            actions = []
            node = self
            while node:
                if node.action:
                    actions.append(node.action)
                node = node.parent
            actions.reverse()
            return list(actions)

    #frontier = PriorityQueue()
    frontier = []
    start_state = problem.get_start_state()
    h_calc = heuristic(start_state, problem)
    #print(h_calc)
    root = Node(start_state, h_calc)
    #frontier.put(root.f, root)
    heapq.heappush(frontier, (root.f, root))
    reached = {}
    reached[start_state] = 0

    #while not frontier.empty():
    while frontier:
        #node = frontier.get()
        node = heapq.heappop(frontier)[1]
        #print(node)
        if problem.is_goal_state(node.state):
            return node.output_actions()
        successors = problem.get_successors(node.state)
        for succState, succAction, succCost in successors:
            child_h_calc = heuristic(succState, problem)
            child = Node(succState, child_h_calc, succAction, node, succCost)
            if succState not in reached or child.g < reached[succState]:
                reached[succState] = child.g
                #frontier.put(child.f, child)
                #print("Child.f: ")
                #print(child.f)
                heapq.heappush(frontier, (child.f, child))
    
    return ["Action not found"]

    util.raise_not_defined()


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search