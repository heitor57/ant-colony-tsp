import yaml
import argparse
import re
import itertools
from lib.constants import *
# from pathlib import Path


# Path().mkdir(parents=True, exist_ok=True)

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

def get_dict_element(d,keys):
    for k in keys:
        d = d[k]
    return d

def get_keys_to_value(d,current_key=(), keys=[]):
    if isinstance(d,dict):
        for key in d:
            new_current_key = current_key+(key,)
            get_keys_to_value(d[key],new_current_key,keys)
    else:
        keys.append(current_key)
        return False
    return True
keys_to_value = []
# print(to_search["selection":{"beta"])
get_keys_to_value(to_search,keys=keys_to_value)
values = [get_dict_element(to_search,keys) for keys in keys_to_value]

combinations = itertools.product(*values)
i = 0
for combination in combinations:
    for keys, v in zip(keys_to_value,combination):
        tmp = config
        for k in keys[:-1]:
            tmp = tmp[k]
        tmp[keys[-1]] = v
    yaml.dump(config,open(f"{DIRS['CONFIGS']}{i}.yaml",'w+'))
    i+=1
