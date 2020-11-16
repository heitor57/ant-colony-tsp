import numpy as np
class SelectionPolicy:
    def __init__(self, alpha, beta, costs, pheromones):
        self.alpha = alpha
        self.beta = beta
        self.costs = costs
        self.pheromones = pheromones

    # def compute_one(self, ant, mask, denominator):

    #     return numerator/denominator
    def compute_probabilities(self, ant):
        mask = np.ones(len(self.costs),dtype=bool)
        mask[ant.solution] = False
        # mask = ~ant.solution
        # mask = ant.solution
        probabilities = np.zeros(len(self.costs),dtype=float)
        numerators = (self.pheromones[ant.solution[-1]][mask])**self.alpha\
            *(1/self.costs[ant.solution[-1]][mask])**self.beta
        

        denominator = np.sum((self.pheromones[ant.solution[-1]][mask])**self.alpha\
            *(1/self.costs[ant.solution[-1]][mask])**self.beta)
        probabilities[mask] = numerators/denominator
        return probabilities

    def select(self,ant):
        probabilities = self.compute_probabilities(ant)
        # print(np.sum(probabilities))
        # print(probabilities)
        selected = np.random.choice(np.arange(len(probabilities)),p=probabilities)
        ant.visit(selected)

    def select_path(self, ant, num_vertexes, objective):
        for j in range(num_vertexes-1):
            self.select(ant)
        ant.solution = np.array(ant.solution)
        ant.solution_value = objective.compute(ant.solution)
        
