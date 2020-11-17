import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import argparse
import yaml
import re
import itertools

from tqdm import tqdm
import numpy as np

import lib.utils as utils
from lib.AntColony import AntColony
from .constants import *

def dict_to_list_gen(d):
    for k, v in zip(d.keys(), d.values()):
        if v == None:
            continue
        if type(v) == dict: 
            v = '{'+get_parameters_name(v,num_dirs=0)+'}'
        yield [k,v]

def dict_to_list(d):
    return list(dict_to_list_gen(d))

def get_parameters_name(parameters,num_dirs=0):
    # parameters = {k:v for k,v in parameters if v}
    list_parameters=['_'.join(map(str,i)) for i in dict_to_list(parameters)]
    string = '/'.join(list_parameters[:num_dirs]) +\
        ('/' if num_dirs else '')
    string += '_'.join(list_parameters[num_dirs:])
    return string

if __name__ == '__main__':
    print(get_parameters_name({'a':2, 'b':3}))
    print(get_parameters_name({'a':2, 'b':3,'d':{'alpha':1, 'xd':{'s':5}}}))
    pass

def run_parallel(func, args,chunksize = None,use_tqdm=True):
    executor = ProcessPoolExecutor()
    num_args = len(args)
    if not chunksize:
        chunksize = int(num_args/multiprocessing.cpu_count())
    if use_tqdm:
        ff = tqdm
    else:
        ff = lambda x,*y,**z: x 
    results = [i for i in ff(executor.map(func,*list(zip(*args)),chunksize=chunksize),total=num_args)]
    return results

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parameters_init():
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

    ac = AntColony(pheromony_kwargs=config['pheromony_policies'][config['parameters']['pheromony_policy']],
                   selection_policy_kwargs=config['selection'],
                   **config['parameters'])
    return config, ac

def get_names_combinations(config, to_search):
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
    return keys_to_value,combinations
