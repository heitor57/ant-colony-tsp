import argparse
import yaml
import re
import logging

import lib.utils as utils
from lib.AntColony import AntColony
from lib.constants import *


config, ac = utils.parameters_init()

logging.basicConfig()
logger = logging.getLogger('default')
logger.setLevel(eval(f"logging.{config['general']['logging_level']}"))
ac.run(config['general']['distances_suffix'],config['general']['solution_suffix'])
