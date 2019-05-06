
from copy import deepcopy
from os import chdir

from action import INSERT, REMOVE
from setup_experiment import setup
from state import State

from mcts import mcts

# time limit for MCTS in seconds
MAX_RUNTIME = 120

# promt user for set up data, save json, cd into project dir
exp_dir = setup()
chdir(exp_dir)

init_state = State('config.json')
mcts = mcts(timeLimit=MAX_RUNTIME)
mcts.search(initalState=init_state)
final_state = mcts.getBestChild(mcts.root, 0)
final_state.export()
print("Final reward: {}".format(final_state.getReward()))

