import numpy as np
class Ant:
    def __init__(self,solution=None, solution_value=None):
        self.solution = solution
        self.solution_value = solution_value

    def set_start(self,target):
        # self.solution = np.zeros(num_vertexes,dtype=bool)
        # self.solution[index] = True
        self.solution = [target]
        self.solution_value = -99999999

    def visit(self,target):
        self.solution.append(target)
