import argparse
import yaml
import re
import logging

import lib.utils as utils
from lib.AntColony import AntColony
from lib.constants import *

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

logging.basicConfig()
logger = logging.getLogger('default')
logger.setLevel(eval(f"logging.{config['general']['logging_level']}"))

ac = AntColony(pheromony_kwargs=config['pheromony_policies'][parameters['pheromony_policy']],
               selection_policy_kwargs=config['selection'],
               **parameters)
ac.run()
