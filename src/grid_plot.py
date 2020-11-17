import os
from concurrent.futures import ProcessPoolExecutor
import itertools
import yaml

import numpy as np
import pandas as pd
import sys

from lib.constants import *
from lib.utils import *
TOP_N = 15
config = yaml.safe_load(open('config.yaml'))
parameters = {k: [v] for k, v in config['parameters'].items()}
to_update = {
    "AntSystem_rho": [0.3,0.5,0.7],
    "AntSystem_Q": [75, 100, 125],
    "selection_beta": [3,5,7],
    "instance_name": ['lau15'],
    "eid": list(range(1,NUM_EXECUTIONS+1)),
}
parameters.update(to_update)
parameters_names = list(parameters.keys())
combinations = itertools.product(*list(parameters.values()))
# args = [('python genetic_algorithm.py '+' '.join([f'--{k}={v}' for k,v in zip(parameters_names,combination)]),)
 # for combination in combinations]
result_df = pd.DataFrame(columns=parameters_names)
for i,combination in enumerate(combinations):
    p = {k:v for k,v in zip(parameters_names,combination)}
    name = get_parameters_name(p)
    # print(DIRS['DATA']+name+'.json')
    df = pd.read_json(DIRS['RESULTS']+name+'.json')
    result_df.loc[i,parameters_names] = combination
    result_df.loc[i,'Best fitness global'] = df.iloc[-1]['Best fitness global']
    result_df.loc[i,'Best fitness'] = df.iloc[-1]['Best fitness']
    result_df.loc[i,'Mean fitness'] = df.iloc[-1]['Mean fitness']
    result_df.loc[i,'Median fitness'] = df.iloc[-1]['Median fitness']
    result_df.loc[i,'Worst fitness'] = df.iloc[-1]['Worst fitness']
    # if i == 49:
    #     break
result_df['eid']=pd.to_numeric(result_df['eid'])
# print('Top best fitness')
import pandas
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    pandas.set_option('display.expand_frame_repr', False)
    tmp = list(to_update.keys())
    tmp.remove('eid')
    a=result_df.groupby(list(set(result_df.columns)-{'Best fitness','Mean fitness','Median fitness', 'eid'})).\
        agg({i: ['mean','std'] for i in {'Best fitness','Mean fitness','Median fitness', 'eid'}}).\
        sort_values(by=[('Best fitness','mean')],ascending=False).reset_index()[tmp+['Best fitness','Mean fitness','Median fitness']].head(TOP_N)
    open(f"{sys.argv[1]}_output.txt",'w').write(a.to_string())


# print('Top mean fitness')
# print(result_df.groupby(list(set(result_df.columns)-{'Best fitness','Mean fitness', 'eid'})).\
    #       agg({i: ['mean','median','std'] for i in {'Best fitness','Mean fitness', 'eid'}}).\
    #       sort_values(by=[('Mean fitness','mean')],ascending=True).reset_index()[list(set(to_update.keys())-{'eid'})+['Best fitness','Mean fitness']].head(TOP_N))
