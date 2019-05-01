import params

class Sample:
	def __init__(self, name, instrument, length, is_pitched, pitch, embedding, track):
		self.name = name
		self.is_pitched = is_pitched
		self.pitch = pitch
		self.instrument = instrument
		self.length = length
		self.embedding = embedding
		# self.track = track

	def add(self, media_item):
		track = RPR_InsertMedia(params.MEDIA_FILE_LOCATION + name, 1)
		track_idx = RPR_CountTracks(0)
		media_track = RPR_GetTrack(0,track_idx)
		self.track = media_track
		return media_track, track_idx

	def remove(self):
		 RPR_DeleteTrack(self.track)
		 return self


