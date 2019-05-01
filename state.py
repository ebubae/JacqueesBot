state.py
Samples
Stacked
Insert_Times

class State:
	def __init__(self, sample_files, min.delta=0.1):
		self.name = name
		self.samples = make_samples(sample_files)
		self.stacked = set() #stacked #set()
		self.insert_times = []
		# self.track = track

	def add(self, sample):
		track = RPR_InsertMedia(params.MEDIA_FILE_LOCATION + sample.name, 1)
		track_idx = RPR_CountTracks(0)
		media_track = RPR_GetTrack(0,track_idx)
		self.track = media_track
		return media_track, track_idx

	def remove(self, sample):
		 RPR_DeleteTrack(self.track)
		 return self

#	def get_history