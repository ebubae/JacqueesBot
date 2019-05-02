import params

class Sample:
  def __init__(self, path, instrument, pitch):
    '''
    path - the file path of the sample (e.g. "/instruments/uke.wav")
    instrument - name of the instrument (e.g. "ukulele, kazoo")
    length - the length of the sample in seconds (e.g. 4.2)
    pitch - the pitch of the instrument if it is pitched (e.g. "Bb", "A", None)
    '''
    self.path = str(path)
    self.pitch = str(pitch)
    self.instrument = str(instrument)
    self.length = float(length)
    self.track = None

  def __len__(self):
    return self.length
  
  def __str__(self):
    return "{} sample @ {}".format(self.instrument, self.path)
    
  # TODO: I've kept this here for reference but we should delete this code
  def add(self, media_item):
    track = RPR_InsertMedia(params.MEDIA_FILE_LOCATION + name, 1)
    track_idx = RPR_CountTracks(0)
    media_track = RPR_GetTrack(0,track_idx)
    return media_track, track_idx

  def remove(self):
     RPR_DeleteTrack(self.track)


