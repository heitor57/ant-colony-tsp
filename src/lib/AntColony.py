import numpy as np
import pandas as pd
import yaml
from tqdm import tqdm
import logging

import math
import random
import argparse
import collections
import sys
from pathlib import Path
import os
import copy
import re

from lib.constants import *

from lib.TSP import TSP
from lib.TSPObjective import TSPObjective
from lib.pheromony_policies import AntSystem, ElitismAntSystem
from lib.Ant import Ant
from lib.SelectionPolicy import SelectionPolicy
import lib.utils as utils

class AntColony:
    def __init__(self, initial_pheromone, ants_rate, num_iterations, instance_name, eid,
                 pheromony_policy, pheromony_kwargs,
                 selection_policy_kwargs):
        self.initial_pheromone = initial_pheromone
        self.ants_rate = ants_rate
        self.num_iterations = num_iterations
        self.instance_name = instance_name
        self.eid = eid
        self.pheromony_policy = pheromony_policy
        self.pheromony_kwargs = pheromony_kwargs
        self.selection_policy_kwargs = selection_policy_kwargs
    def run(self, distances_suffix, solution_suffix):
        tsp = TSP()
        tsp.load(DIRS['INPUT']+self.instance_name, distances_suffix, solution_suffix)
        best_ant = None
        objective = TSPObjective(tsp)
        pheromones = np.ones(tsp.distances.shape,dtype=float)*self.initial_pheromone
        num_vertexes = len(tsp.distances)
        num_ants = int(self.ants_rate * num_vertexes)
        population = [None]*num_ants
        selection_policy = SelectionPolicy(costs=tsp.distances,
            pheromones=pheromones,
            **self.selection_policy_kwargs)
        pheromony_policy = eval(self.pheromony_policy)(**self.pheromony_kwargs)

        columns = ['#Generation','Best fitness global','Best fitness','Mean fitness', 'Median fitness', 'Worst fitness']
        df = pd.DataFrame([],columns = columns)
        df = df.set_index(columns[0])

        for i in range(num_ants):
            population[i] = Ant()
        # count = 0
        logger = logging.getLogger('default')
        if logger.level <= logging.INFO:
            progress_bar = tqdm
        else:
            progress_bar = lambda x: x
            
        for i in progress_bar(range(1,self.num_iterations+1)):
            for ant in population:
                ant.set_start(int(random.uniform(0,num_vertexes-1)))
                # ant.set_start(count%num_vertexes)
                # count+=1
            
            for ant in population:
                selection_policy.select_path(ant, num_vertexes, objective)

            pheromony_policy.update(population, pheromones)
            solution_values = [ant.solution_value for ant in population]
            best_local_ant = population[np.argmin(solution_values)]
            # for ant in population:
            #     print(ant.solution)
            if best_ant == None or best_local_ant.solution_value < best_ant.solution_value:
                best_ant = copy.copy(best_local_ant)
            # print(best_ant.solution,best_ant.solution_value)
            # print(pheromones)
            df.loc[i] = [f'{best_ant.solution_value:.4f}',f'{np.min(solution_values):.4f}',f'{np.mean(solution_values):.4f}',f'{np.median(solution_values):.4f}',f'{np.max(solution_values):.4f}']
        logger.info(f"\n{df}")
        self.save_results(df)

    def __str__(self):
        string=""
        for k, v in self.__dict__.items():
            string+=f"{k} = {v}\n"
        return string

    # @staticmethod
    # def get_parameters_name(parameters):
    #     return f"{DIRS['RESULTS']}"+utils.get_parameters_name(parameters_dirs=3)+".json"

    def get_name(self):
        
        name = f"{DIRS['RESULTS']}"+utils.get_parameters_name(self.__dict__,num_dirs=3)+".json"
        l = name.split('/')
        for i in range(2,len(l)):
            directory = '/'.join(l[:i])
            logger = logging.getLogger('default')
            logger.debug(directory)
            Path(directory).mkdir(parents=True, exist_ok=True)
            
        return name

    def save_results(self, df):
        f = open(self.get_name(),'w')
        f.write(df.to_json(orient='records',lines=False))
        f.close()

    def load_results(self):
        string = self.get_name()
        # string = re.sub(r'{',r'\{',string)
        # string = re.sub(r'}',r'\}',string)
        # print(string)
        return pd.read_json(string)
