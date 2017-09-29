from functools import reduce
import sys,inspect,os,time
REPO_DIR = os.path.dirname(os.path.abspath(os.path.join(inspect.getfile(inspect.currentframe()), "..")))
sys.path.append(REPO_DIR)
sys.path.append(REPO_DIR+"/algorithms/")
sys.path.append(REPO_DIR+"/games/")
sys.path.append(REPO_DIR+"/projectClasses/")
# print(sys.path)
from BoardFunctions import checkCondition
from constraintClasses import *
import opDictionary
from copy import copy
class FutoshikiProblem(object):
    """Futoshiki problem class"""
    def __init__(self, variables, constraintObjects, inputConstraints):
        self.variables = variables
        self.constraintObjects = constraintObjects
        self.inputConstraints = inputConstraints

    def generateConstraints(self):
        for constraint in self.inputConstraints:
            # Constraints are of the form
            #   [op, value, var1 ...]
            print("FutoshikiProblem.generateConstraints-constraint: {}".format(constraint))
            # DEBUG - Prints each element of constraint
            for i in range(0,len(constraint)):
                print("constraint[{}] = {}".format(i,constraint[i]))

            op = constraint[0]
            if type(op) == int:
                vars = [self.variables[tuple(constraint[1])]]
                self.constraintObjects.append(GenericConstraint(vars, checkCondition, "abs", constraint[0]))
            else:

                # Convert the list of coordinates ([x1,y1], [x2,y2]...) to a list of tuples ((x1,y1), (x2,y2)...)
                vars = map(tuple, constraint[1:])

                # Replace each var tuple with the corresponding ConstraintVar in self.variables
                vars = list(map(lambda key: self.variables[key], vars))
                print("MY VARS: {}", vars)

                self.constraintObjects.append(GenericConstraint(vars, checkCondition, copy(constraint[0]), True))
    """
    Checks if the assignment list is the same length as the amount of variables

    @param assignment           List of assignments for backtracking algorithms

    @rtval True                 Lens are the same
    @rtval False                Lens are not the same
    """
    def isComplete(self, assignment):
        if len(assignment) == len(self.variables):
            return True
        return False
