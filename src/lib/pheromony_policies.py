import numpy as np

class BaseSystem:
    def __init__(self, rho, Q):
        if rho > 0 and rho <= 1:
            self.rho= rho
        else:
            raise ValueError
        self.Q = Q

class AntSystem(BaseSystem):
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    def update(self,population,pheromones):
        pheromones *= (1-self.rho)
        for ant in population:
            tmp = self.Q/ant.solution_value
            for i in range(len(ant.solution)-1):
                pheromones[ant.solution[i],ant.solution[i+1]] += tmp
            pheromones[ant.solution[len(ant.solution)-1],ant.solution[0]] += tmp

class ElitismAntSystem(BaseSystem):
    def __init__(self,epsilon,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.epsilon = epsilon
    def update(self,population,pheromones):
        pheromones *= (1-self.rho)
        best_ant = population[np.argmin([ant.solution_value for ant in population])]
        for ant in population:
            tmp = self.Q/ant.solution_value
            for i in range(len(ant.solution)-1):
                pheromones[ant.solution[i],ant.solution[i+1]] += tmp

            pheromones[ant.solution[len(ant.solution)-1],ant.solution[0]] += tmp

        for i in range(len(best_ant.solution)-1):
            pheromones[best_ant.solution[i],best_ant.solution[i+1]] += self.epsilon*tmp

        pheromones[best_ant.solution[len(ant.solution)-1],best_ant.solution[0]] += self.epsilon*tmp
