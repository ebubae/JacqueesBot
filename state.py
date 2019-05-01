import json

from copy import deepcopy

from action import Insert, Remove, INSERT, REMOVE
from sample import Sample

class State:
  
  def __init__(self, config, min_delta=0.1):
    '''
    config - the filename for a JSON file that lists all the samples and their attributes
    min_delta - the minimum difference in insert times (default 0.1)
    '''
    self.samples = []
    self.inserted = []
    self.times = []
    self.stacked = set()
    self.min_delta = min_delta
    data = json.load(config)
    for d in data[('samples')]:
      s = Sample(**d)
      self.samples.append(s)

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
      self.stacked -= self.get_removable_stacked(insert_id)
      RPR_DeleteTrack(track)

  def insert(self, sample_id, t):
    '''
    Inserts a sample into the state at a specific time
    '''
    # TODO: check if valid sample ID and time
    sample = samples[sample_id]
    start_time = t
    end_time = t + len(sample)

    self.stacked |= self.get_new_stacked(sample_id, t)

    self.times.append((start_time, end_time))
    self.inserted.append((sample_id, t))
    # reaper deletion
		track = RPR_InsertMedia(params.MEDIA_FILE_LOCATION + sample.path, 1)
		track_idx = RPR_CountTracks(0)
		media_track = RPR_GetTrack(0,track_idx)
		sample.track = media_track

  # TODO: Dev this is all you
  def export(self):
    pass

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

  def __eq__(self, o):
     return o.insert_id == self.inser_id if isinstance(o, Insert) else False 

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())
