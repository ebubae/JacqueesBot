from copy import deepcopy

from action import INSERT, REMOVE
from setup_experiment import setup
from state import State

exp_dir = setup()

def do_action(state, act):
  '''
  Add or removethe sample to the state. This should add to our model as well as 
  onto a new Reaper track

  Return new state without modifying state passed in
  '''
  new_state = deepcopy(state)
  if act.action_type == REMOVE:
    new_state.remove(act.insert_id)
  elif act.action_type == INSERT
    # TODO: error check that time and sample ID are appropriate
    new_state.insert(act.sample_id, t)

  return new_state
