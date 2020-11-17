import os
from concurrent.futures import ProcessPoolExecutor
import itertools
import yaml

import numpy as np
import pandas as pd
import sys

from lib.constants import *
from lib.utils import *

loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
        [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))
parser = argparse.ArgumentParser()
parser.add_argument('--config_file','-c',
                    default="config.yaml",
                    type=str,
                    help="Configuration file.")

args = parser.parse_args()
f = open(args.config_file)
config = yaml.load(f,Loader=loader)

to_search = {
    'pheromony_policies': {'AntSystem':{"rho": [0.3,0.5,0.7],
                                         "Q": [75, 100, 125]}},
    "selection":{"beta": [3,5,7]},
    'parameters':{"instance_name": ['lau15','sgb128'],
                  "eid": list(range(1,NUM_EXECUTIONS+1))},
}
# parameters_names=['rho','Q','betas','eid']

keys_to_value, combinations=utils.get_names_combinations(config,to_search)
result_df = pd.DataFrame(columns=
                         [keys[-1] for keys in keys_to_value])

parameters_names = [i[-1] for i in keys_to_value]
for combination in combinations:
    for keys, v in zip(keys_to_value,combination):
        tmp = config
        for k in keys[:-1]:
            tmp = tmp[k]
        tmp[keys[-1]] = v

        result_df.loc[i,keys[-1]] = v
        
    ac = AntColony(pheromony_kwargs=config['pheromony_policies'][config['parameters']['pheromony_policy']],
                   selection_policy_kwargs=config['selection'],
                   **config['parameters'])
    df = ac.load_results()
    result_df.loc[i,'Best fitness global'] = df.iloc[-1]['Best fitness global']
    result_df.loc[i,'Best fitness'] = df.iloc[-1]['Best fitness']
    result_df.loc[i,'Mean fitness'] = df.iloc[-1]['Mean fitness']
    result_df.loc[i,'Median fitness'] = df.iloc[-1]['Median fitness']
    result_df.loc[i,'Worst fitness'] = df.iloc[-1]['Worst fitness']

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
