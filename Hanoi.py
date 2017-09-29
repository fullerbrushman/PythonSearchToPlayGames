import sys,inspect,os,time
REPO_DIR = os.path.dirname(os.path.abspath(os.path.join(inspect.getfile(inspect.currentframe()), "..")))
sys.path.append(REPO_DIR+"/algorithms/")
sys.path.append(REPO_DIR+"/games/")
sys.path.append(REPO_DIR+"/projectClasses/")
from node import Node
from AIproblem import AIproblem
from copy import deepcopy,copy

#Helper function for SolverLocalBeam that removes duplicates from a list
def makeUnique(lst):
    return list(set(lst))

#Two quick functions to convert moves to format specified from a list of states passed




#extension of Node class to handle tracking moves made
class HanoiNode(Node):
    def __init__(self, state, parent=None, action=None):
        super().__init__(state, parent, action)
        self.moves=[]
        #self.value = sum(state)

    def makeChild( self, problem, action ):
        childState = problem.applyAction( self.state, action )
        child = HanoiNode( childState, self )
        child.moves = copy(self.moves)
        #child.moves.append(findMove(child.getState(), child.parent.getState()))
        child.moves.append(action)
        child.value = problem.evaluation(childState)
        return child

    def findMove(self, state, parent_state):
        for i in range(len(state)):
            if state[i] != parent_state[i]:
                return [parent_state[i], state[i]]
    #need to be able to test equality of nodes for Bidirectional search
    def __eq__(self, other):
        if other == None:
            return False
        return self.__hash__() == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return int(''.join(map(str,self.state)))

    def __repr__(self):
        """Represent the board as a one row per line"""

        if len(self.moves) == 0:
            return "\t" + str(self.getState())

        representation = "\t"
        for row in self.moves:
            representation += str(row) + "\n\t"
        return representation[:-1]

    def getSolution(self):
        new_list = []
        for i in range(len(self.moves)):
            if i == 0:
                new_list.append(self.findMove([3,3,3], self.moves[i]))
            else:
                new_list.append(self.findMove(self.moves[i], self.moves[i-1]))
        return str(new_list)

#extension of AIproblem for Towers of Hanoi Problem
class HanoiProblem(AIproblem):
    #state is defined as follows:
    #list of disks, with numbers 1,2,3 representing the 3 pegs
    #smallest disks first, largest last
    #example state: [3, 3, 1]
    def __init__(self, size, evalFn=None):
        self.size = size

        self.initialState = []
        for i in range(0, size):
            self.initialState.append(1)

        self.goal = []
        for i in range(0, size):
            self.goal.append(3)
        self.heuristics = {"disksOnWrongItem": self.disksOnWrongItem, "misplacedDisks": self.misplacedDisks}
    # Potential additional method of getNeighbors, but essentially this is the same as expanding a node
    # so really not necessary.
    # return [ applyAction( state, a) for a in getActions( state ) ]

    def getRandomAction( self, state ):
    # randomly produce a single action applicable for this state
        return None

    def getActions( self, state ):
        # produce a list of valid states that can be reached from current state
        actions = []
        #consider moving each disk to each of the 3 pegs
        for i in range(0, len(state)):
            # if i == 0:
                # new_state = deepcopy(state)
                # for target_peg in range(1,4):
                    # if target_peg != state[i]:
                        # new_state[i] = target_peg
                        # actions.append(new_state)
            # else:
            for target_peg in range(1,4):
                #don't consider moving disk to current peg
                if target_peg != state[i]:
                    #check that no disk that is smaller is on target peg
                    #and that no smaller disks are on disk considering moving
                    if any((disk == target_peg) | (disk == state[i]) for disk in state[:i]) == False:
                        new_state = copy(state)
                        new_state[i] = target_peg
                        actions.append(new_state)

        return actions

    def applyAction ( self, state, action ):
        #if action exists, returns action
        #this function wouldn't be necessary for my implementation
        #is included to fit specifications
        if not action:
            return None
        else:
            return action

    def misplacedDisks( self, state ):
        #is heuristic for tower of hanoi
        #if state[-1] == 3:
        #    return 0
        #return len([elem for elem in state if elem == state[-1]]) - 1

        #bad heuristic: number of disks not on peg 3.
        return len([elem for elem in state if elem != 3]) - 1

    def disksOnWrongItem( self, state ):
        #good heuristic: number of disks on wrong item.
        return len([x for x in range(0, len(state) - 1) if (state[x] != state[x+1])]) + (1 & (state[-1] != 3))

    def evaluation (self, state, chosenHeuristic="disksOnWrongItem"):
        return self.heuristics[chosenHeuristic](state)

    def isGoal ( self, state ):
        # fringe = [[3,3,3]]
        # return any(all(state[i] == other[i] for i in range(0, self.size)) for other in fringe)
        # print("Checking isGoal for {} -> {}".format(state,all(disk == 3 for disk in state)))
        return all(disk == 3 for disk in state)
