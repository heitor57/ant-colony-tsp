import argparse
from pathlib import Path
import yaml
from lib.utils import *
import pandas as pd
import matplotlib.pyplot as plt
from lib.constants import *
from collections import OrderedDict
import functools
config, ac = utils.parameters_init()
config = OrderedDict(config)
fig, ax = plt.subplots()
name = ac.get_name()
dfs = []
for i in range(1,NUM_EXECUTIONS+1):
    ac.eid = i
    # name=get_parameters_name({k: v['value'] for k,v in parameters.items()})
    # df = pd.read_json(DIRS['RESULTS']+name+'.json')
    df = ac.load_results()
    dfs.append(df)
df = pd.DataFrame(functools.reduce(lambda x,y: x+y,dfs))/len(dfs)
# df = ac.load_results()
ax.plot(df['Best fitness global'],label='Melhor aptidão global')
ax.plot(df['Best fitness'],label='Melhor aptidão')
ax.plot(df['Mean fitness'],label='Aptidão média')
ax.plot(df['Median fitness'],label='Aptidão mediana')
ax.plot(df['Worst fitness'],label='Pior Aptidão')
ax.set_ylabel("Aptidão")
ax.set_xlabel("Iteração")
ax.legend()
fig.savefig(f"{DIRS['IMG']}{ac.instance_name}_{ac.pheromony_kwargs['rho']}_{ac.pheromony_kwargs['Q']}_{ac.selection_policy_kwargs['beta']}_mean_and_median_and_best.eps",bbox_inches="tight")
fig.savefig(f"{DIRS['IMG']}{ac.instance_name}_{ac.pheromony_kwargs['rho']}_{ac.pheromony_kwargs['Q']}_{ac.selection_policy_kwargs['beta']}_mean_and_median_and_best.png",bbox_inches="tight")

fig, ax = plt.subplots()
for i in range(1,NUM_EXECUTIONS+1):
    ac.eid = i
    # name=get_parameters_name({k: v['value'] for k,v in parameters.items()})
    # df = pd.read_json(DIRS['RESULTS']+name+'.json')
    df = ac.load_results()
    ax.plot(df['Best fitness global'],label=f'Execução {i}')

ax.set_ylabel("Aptidão")
ax.set_xlabel("Geração")
ax.legend()

fig.savefig(f"{DIRS['IMG']}{ac.instance_name}_{ac.pheromony_kwargs['rho']}_{ac.pheromony_kwargs['Q']}_{ac.selection_policy_kwargs['beta']}_multiple_executions.eps",bbox_inches="tight")
fig.savefig(f"{DIRS['IMG']}{ac.instance_name}_{ac.pheromony_kwargs['rho']}_{ac.pheromony_kwargs['Q']}_{ac.selection_policy_kwargs['beta']}_multiple_executions.png",bbox_inches="tight")

# dfs.append(df)
    # Path(os.path.dirname(DIRS['DATA']+name)).mkdir(parents=True, exist_ok=True)
