from .prob_rg import *
from .prob_comb import *
from .tools_aux import *
from .tools_illustris import *
from .tools_ndpredict import *
from .tools_writing import *

import os

cwd = os.getcwd()

dir_name = cwd+'\\Results'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    
dir_name = cwd+'\\Results\\kk'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    
dir_name = cwd+'\\Results\\loop'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    
dir_name = cwd+'\\Results\\liop'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    
dir_name = cwd+'\\Results\\coefs'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)