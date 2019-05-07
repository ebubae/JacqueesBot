from os import chdir

from setup_experiment import setup
from state import State

from mcts import mcts

# time limit for MCTS in seconds
MAX_RUNTIME = 600

# promt user for set up data, save json, cd into project dir
exp_dir = setup()
chdir(exp_dir)

init_state = State('config.json')
#RPR_ShowConsoleMsg("GOth here")
mcts = mcts(timeLimit=MAX_RUNTIME * 1000)
mcts.search(initialState=init_state)
final_state = mcts.getBestChild(mcts.root, 0).state
final_state.export()
# TODO: pickle mcts tree`
print("Final reward: {}".format(final_state.getReward()))

