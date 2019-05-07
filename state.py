import json

from copy import deepcopy
from os.path import join

import beyond.Reaper
import sys

from action import Insert, Finish, Hold, INSERT, FINISH, HOLD
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
    #self.times = []
    self.stacked = set()
    self.terminal = False

    data = json.load(open(config, 'r'))

    self.num_tracks = data['num_tracks']
    self.inserted = [set() for _ in range(self.num_tracks)]
    self.cursor = [0 for _ in range(self.num_tracks)]
    self.inspiration = data['inspiration']
    self.inspiration_sample = Sample(self.inspiration, "INSP", -1)
    self.delta = float(data['delta'])
    self.max_time = self.inspiration_sample.length + self.delta
    self.eps = float(data['eps'])
    self.project_name = data['project_name']
    self.export_path = data['export_path']

    for d in data['samples']:
      s = Sample(**d)
      self.samples.append(s)

  def getPossibleActions(self):
    c = self.cursor
    return [Hold(track) for track in range(self.num_tracks) if c[track] < self.max_time] + \
           [Insert(s, time, track) for s in range(len(self.samples)) 
                                   for time in c 
                                   for track in range(self.num_tracks) if all((s, time) not in tr for tr in self.inserted)
                                                                          and time < self.max_time] + \
           [Finish()]
    

  def takeAction(self, act):
    new_state = deepcopy(self)

    if act.action_type == FINISH:
      new_state.terminal = True
      return new_state
    elif act.action_type == INSERT:
      new_state.insert(act.sample_id, act.time, act.track)
    elif act.action_type == HOLD:
      new_state.cursor[act.track] += self.eps
    return new_state


  def isTerminal(self): return self.terminal


  def getReward(self):
    out_file = self.export()
    return -sys.maxsize if all(len(i) == 0 for i in self.inserted) else get_reward(self.inspiration, out_file, self.eps, self.delta)

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
      # RPR_DeleteTrack(track)

  def insert(self, sample_id, t, track):
    '''
    Inserts a sample into the state at a specific time
    '''
    print("Inserting sample {} at time {} on track{}".format(sample_id, t, track))
    # TODO: check if valid sample ID and time
    sample = self.samples[sample_id]
    start_time = t
    end_time = t + sample.length

    #self.stacked |= self.get_new_stacked(sample_id, t)

    # reaper deletion
  #   RPR_InsertMedia(params.MEDIA_FILE_LOCATION + sample.path, 1)
  #   track_idx = RPR_CountTracks(0)
		# media_track = RPR_GetTrack(0,track_idx)
		#sample.track = media_track

    #self.times.append((start_time, end_time))
    self.inserted[track].add((sample_id, t))
    self.cursor[track] = end_time

  def show(self):
    with Reaper as r:
      for track_idx in range(self.num_tracks):
        r.DeleteTrack(r.GetTrack(0, track_idx))

      for _ in range(self.num_tracks):
        r.InsertTrackAtIndex(0, 0)

      for curr_track, inserted_samples in enumerate(self.inserted):
        media_track = r.GetTrack(0, curr_track)
        r.SetTrackSelected(media_track, True)
        for (s, time) in inserted_samples:
          r.InsertMedia(self.samples[s].path, 0)
          media_item = r.GetMediaItem(0, r.CountMediaItems(0)-1)
          r.SetMediaItemPosition(media_item, time, True)

  # TODO: Dev this is all you
  def export(self, export_file='out.wav'):
    self.show()
    Reaper.Main_SaveProject(0, False)
    to_export = join(self.export_path, export_file)
    status = Reaper.RenderFileSection('/Users/echuba/JacqueesBot/jacquees.RPP', to_export,0,1,1)
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
    return "\nCurrent state\n\nSamples:\n" + "\n".join(['{}. {}'.format(idx, str(s)) for idx, s in enumerate(self.samples)]) + "\nInserted:\n" + "\n".join(['{}. sample {} inserted @ {}'.format(idx, s_id, t) for idx, (s_id, t) in enumerate(self.inserted)]) + "\nStacked:\n" + "\n".join(['{} and {}'.format(s1, s2) for s1, s2 in self.stacked])

  def __str__(self):
    return sellf.__repr__()

  def __eq__(self, o):
     return o.insert_id == self.inser_id if isinstance(o, Insert) else False 

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())
