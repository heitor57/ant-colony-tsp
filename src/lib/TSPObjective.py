import math
import numpy as np



from numba import jit

@jit(nopython=True)
def _tsp_objective(distances,solution):
    n = len(solution)
    v = 0
    # print(v)
    for i in range(n-1):
        v += distances[solution[i],solution[i+1]]
        # print(solution[i],solution[i+1],distances[solution[i],solution[i+1]], v)
    v += distances[solution[n-1],solution[0]]
    # print(v)
    return v

class TSPObjective:
    def __init__(self, tsp):
        self.tsp = tsp
    def compute(self, solution):
        return _tsp_objective(self.tsp.distances,solution)

# if __name__ == '__main__':
