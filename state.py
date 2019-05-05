import json

from copy import deepcopy

from action import Insert, Finish, INSERT, FINISH
from reward import get_reward
from sample import Sample

class State:
  
  def __init__(self, config):
    '''
    config - the filename for a JSON file that lists all the samples and their attributes
    eps - the minimum difference in insert times (default 0.1)
    delta - how long
    '''
    self.samples = []
    self.inserted = []
    self.times = []
    self.stacked = set()
    self.terminal = False
    self.cursor = 0

    data = json.load(config)

    self.num_tracks = data['num_tracks']
    self.inspiration = data['inspiration']
    self.delta = float(data['delta'])
    self.eps = float(data['eps'])

    for d in data['samples']:
      s = Sample(**d)
      self.samples.append(s)

  def getPossibleActions(self): pass

  def takeAction(self, act):
    new_state = deepcopy(self)

    if act.action_type == FINISH:
      new_state.terminal = True
      new_state.cursor = max((t[1] for t in new_state.times))
      return new_state
    
    assert(act.action_type == INSERT)
    
    new_state.insert(act.sample_id, self.time)
    return new_state


  def isTerminal(self): return self.terminal

  def getReward(self):
    assert(self.terminal)
    # TODO: Dev this is you
    # First, clear REAPER state and repalce with self state
    out_file = self.export()
    return get_reward(self.inspiration, out_file, self.eps, self.delta)

  def remove(self, insert_id):
    '''
    Removes a specific instance of a sample from the state 
    also removes its references (if any) in stacked
    '''
    # TODO: check valid insert ID
    to_remove = self.inserted[insert_id]
    if to_remove:
      track = samples[to_remove[0]].track
      self.inserted[act.insert_id] = None
      #self.stacked -= self.get_removable_stacked(insert_id)
      RPR_DeleteTrack(track)

  def insert(self, sample_id, t):
    '''
    Inserts a sample into the state at a specific time
    '''
    # TODO: check if valid sample ID and time
    sample = samples[sample_id]
    start_time = t
    end_time = t + len(sample)

    #self.stacked |= self.get_new_stacked(sample_id, t)

    self.times.append((start_time, end_time))
    self.inserted.append((sample_id, t))
    # reaper deletion
		track = RPR_InsertMedia(params.MEDIA_FILE_LOCATION + sample.path, 1)
		track_idx = RPR_CountTracks(0)
		media_track = RPR_GetTrack(0,track_idx)
		sample.track = media_track

  # TODO: Dev this is all you
  def export(self):
    export_file = self.export_path + "\out.wav"
    RPR_RenderFileSection(self.project, export_file,0,1,1)
    return export_file

  def get_removable_stacked(self, insert_idx):
    '''
    Return the set of elements that should be unstacked after deletion of sample at insert_idx
    '''
    return {(s1, s2) for (s1, s2) in self.stacked if s1 != insert_idx and s2 != insert_idx}

  def get_new_stacked(self, sample_id, t):
    '''
    Return the new elements to add to stacked after the hypothetical addition
    of sample at sample_id at time t
    '''
    new_idx = len(self.inserted)
    new_stacked = set()

    for insert_idx, (s, e) in enumerate(self.times):
      not_stacked = e < start_time or s > end_time
      if not not_stacked:
        new_stacked.add((insert_idx, new_idx)) # older ID first

    return new_stacked
 
  def __repr__(self):
    return "\nCurrent state\n\nSamples:\n" + "\n".join(['{}. {}'.format(idx, str(s)) for idx, s in enumerate(self.samples)]) +
           "\nInserted:\n" + "\n".join(['{}. sample {} inserted @ {}'.format(idx, s_id, t) for idx, (s_id, t) in enumerate(self.inserted)]) + 
           "\nStacked:\n" + "\n".join(['{} and {}'.format(s1, s2) for s1, s2 in self.stacked])

  def __str__(self):
    return sellf.__repr__()

  def __eq__(self, o):
     return o.insert_id == self.inser_id if isinstance(o, Insert) else False 

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())
