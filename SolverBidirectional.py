import sys
sys.path.append('../projectClasses')
sys.path.append('../games')
from solverClass import Solver
from collections import deque
from copy import deepcopy
from Hanoi import *


class SolverBidirectional(Solver):

    def __init__(self, testCase, goal=None):
        #testCase should just be number of disks.
        self.problem = HanoiProblem(testCase)
        self.initial_state = []
        self.goal_state = []
        for i in range(testCase):
            self.initial_state.append(1)
            self.goal_state.append(3)
        self.search_depth = 1
        self.forward_depth = 1
        self.backward_depth = 0
        self.solution = None
    
    def Bidirectional(self):
        #Generate root nodes
        forward_root = HanoiNode(self.initial_state)
        backward_root = HanoiNode(self.goal_state)
        
        #begin populating queues
        forward_frontier = deque()
        forward_frontier.append(forward_root)
        backward_frontier = deque()
        backward_frontier.append(backward_root)
    
        while self.search_depth > 0:
            if (self.search_depth % 2) == 1:
                #go forwards
                node = forward_frontier.popleft()
                #print(node.depth, self.search_depth, self.forward_depth, self.backward_depth)
                if node.depth > self.forward_depth:
                    forward_frontier.appendleft(node)
                    self.search_depth += 1
                    self.backward_depth += 1
                else:
                    #check if matches with any other direction nodes
                    for frontier_node in backward_frontier:
                        if frontier_node == node:
                            solution_node = HanoiNode(self.goal_state)
                            for move in node.moves:
                                solution_node.moves.append(move)
                            for move in frontier_node.moves[::-1]:
                                solution_node.moves.append(move)
                            print("found solution")
                            return solution_node
                    #if not then expand upon this node
                    for child in node.expand(self.problem):
                        forward_frontier.append(child)
                    
            else:
                #go backwards
                node = backward_frontier.popleft()
                if node.depth > self.backward_depth:
                    backward_frontier.appendleft(node)
                    self.search_depth += 1
                    self.forward_depth += 1
                else:
                    #check if matches with any other direction nodes
                    for frontier_node in forward_frontier:
                        if frontier_node == node:
                            solution_node = HanoiNode(self.goal_state)
                            for move in node.moves:
                                solution_node.moves.append(move)
                            for move in frontier_node.moves[::-1]:
                                solution_node.moves.append(move)
                            solution_node.moves.reverse()
                            solution_node.moves.append(self.goal_state)
                            print("found solution")
                            return solution_node
                    #if not then expand upon this node
                    for child in node.expand(self.problem):
                        backward_frontier.append(child)
        return None
		
    def solve(self):
        if len(self.initial_state) == 2:
            print("Unsolvable")
        self.solution = self.Bidirectional()
        self.printSolution()
        return None

    def printSolution(self):
        #prints out moves to goal one per line
        if self.solution:
            print(self.solution.getState())
            print(list(filter(lambda elem: elem != None, convertMoves(self.solution.moves))))

#tests
solver = SolverBidirectional(5)
solver.solve()




