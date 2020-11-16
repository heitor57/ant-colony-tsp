import re
import numpy as np
from .TSPObjective import TSPObjective
class TSP:
    def __init__(self, distances=None, optimal_solution=None):
        self.distances = distances
        self.optimal_solution = optimal_solution
    def load(self, instance_name):
        self.distances = []
        for line in open(instance_name+"_dist.txt"):
            if line[0] == "#":
                continue
            line=re.sub("\s+"," ",line).strip()
            dists = list(map(int,line.split(' ')))
            self.distances.append(dists)

        self.distances = np.array(self.distances)
        num_vertexes = len(self.distances)
        np.fill_diagonal(self.distances,np.iinfo(self.distances.dtype).max)
        try:
            self.optimal_solution = []

            for line in open(instance_name+"_tsp.txt"):
                if line[0] == "#":
                    continue
                self.optimal_solution.append(int(line))
            if self.optimal_solution[-1] == self.optimal_solution[0]:
                self.optimal_solution = self.optimal_solution[:-1]
            self.optimal_solution=np.array(self.optimal_solution)
            self.optimal_solution=self.optimal_solution-1
            print("Optimal solution:",self.optimal_solution,"-",TSPObjective(self).compute(self.optimal_solution))
        except:
            pass
        # raise SystemExit
    def __str__(self):
        return f"""{self.distances}
{self.optimal_solution}
"""
