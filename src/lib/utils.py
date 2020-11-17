import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import argparse
import yaml
import re

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
    config = yaml.load(open('config.yaml'),Loader=loader)
    parameters = config['parameters']
    pheromony_policies = list(config['pheromony_policies'].keys())
    for k, v in parameters.items():
        parser.add_argument('--' + k, default=v,
                            type=type(v))

    names = []
    for k1, v1 in config['pheromony_policies'].items():
        for k2, v2 in v1.items():
            names.append('--' + k1+'_'+k2)
            parser.add_argument(names[-1], default=v2,
                                type=type(v2))

    for k, v in config['selection'].items():
        parser.add_argument('--selection_' + k, default=v,
                            type=type(v))
    args = parser.parse_args()

    for k, v in vars(args).items():
        if parameters['pheromony_policy'] != k and 'selection_' not in k:
            parameters[k] = v

    for k, v in vars(args).items():
        if parameters['pheromony_policy'] == k:
            config['pheromony_policies'][parameters['pheromony_policy']][k.split("_")[-1]] = v


    for k, v in vars(args).items():
        if 'selection_' in k:
            config['selection'][k.split("_")[-1]] = v

    for i in pheromony_policies:
        for j in list(parameters.keys()):
            if i in j:
                del parameters[j]

    ac = AntColony(pheromony_kwargs=config['pheromony_policies'][parameters['pheromony_policy']],
                selection_policy_kwargs=config['selection'],
                **parameters)
    return config, ac
