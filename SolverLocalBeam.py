import sys,inspect,os,time
REPO_DIR = os.path.dirname(os.path.abspath(os.path.join(inspect.getfile(inspect.currentframe()), "..")))
sys.path.append(REPO_DIR+"/algorithms/")
sys.path.append(REPO_DIR+"/games/")
sys.path.append(REPO_DIR+"/projectClasses/")
from solverClass import Solver
from collections import deque
from copy import deepcopy
from Hanoi import *
from SlidingPuzzle import SlidingPuzzleNode
from SlidingPuzzle import SlidingPuzzleProblem

class SolverLocalBeam(Solver):

    def __init__(self, problem, beamWidth=9, goal=None):
        """
        @param problem         Expect a problem object
        @param beamWidth        number of childen to explore at each depth
        @param initialState    Expect a Node object
        @param goal             Goal State
        """
        self.problem = problem
        self.search_depth = 1
        self.solution = None
        self.beam_width = beamWidth
        self.nodeCount = 0
        self.nodeClass = {HanoiProblem: HanoiNode, SlidingPuzzleProblem: SlidingPuzzleNode}

        self.frontier = deque()

        #Generate initial root node
        #begin populating queue

        self.initialNode = self.nodeClass[type(self.problem)](self.problem.initialState)
        self.frontier.append(self.initialNode)

    def setBeamWidth(self, width):
        self.beam_width = width

    def beam(self):
        #does one depth of local beam search
        candidates = dict()

        #search until frontier empty
        while len(self.frontier) > 0:
            node = self.frontier.popleft()
            # print("Node: {}".format(node))
            self.nodeCount += 1
            #check if node is goal state
            if self.problem.isGoal(node.getState()):
                print("found Solution")
                return node
            for child in node.expand(self.problem):
                # print("CHILD: {}\tVALUE: {}".format(child.getState(), child.value))
                if self.problem.isGoal(node.getState()):
                    return child
                #add next depth nodes to list of candidates
                candidates[child] = child.value

        sorted_candidates = sorted(candidates, key=lambda node: node.value)
        # print(list(map(lambda node: node.value, sorted_candidates)))
        for i in range(0, self.beam_width):
            if i < len(sorted_candidates):
                self.frontier.append(sorted_candidates[i])
        return None

    def solve(self):
        if len(self.initialNode.getState()) == 2:
            print("Unsolvable")
        iterations = 0
        while self.solution == None:
            if iterations > 2 ** (len(self.initialNode.getState())):
                print("Unsolvable with this beam width and basic heuristic")
                return None
            self.solution = self.beam()
            iterations += 1
        print(self.solution.getSolution())
        print("Node's Visited: " + str(self.nodeCount))

        return None

    def printSolution(self):
        #prints out moves to goal one per line
        print(convertMoves(self.solution.moves))

#tests
solver = SolverLocalBeam(HanoiProblem(3))
solver.solve()
solver2 = SolverLocalBeam(SlidingPuzzleProblem([[1,2,3],[4,0,6],[7,5,8]]))
solver2.solve()





