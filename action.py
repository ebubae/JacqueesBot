INSERT = 1
HOLD = 2
FINISH = 3

class Insert:
  def __init__(self, sample_id, time, track):
    self.sample_id = sample_id
    self.time = time
    self.track = track
    self.action_type = INSERT

  def __repr__(self):
    return "Insert({}, {}, {})".format(self.sample_id, self.time, self.track)

  def __eq__(self, o):
     return o.sample_id == self.sample_id and o.time == self.time and o.track == o.track if isinstance(o, Insert) else False 

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())

class Hold:
  def __init__(self, track):
    self.action_type = HOLD
    self.track = track

  def __repr__(self):
    return "Hold()"

  def __eq__(self, o):
     return isinstance(o, Hold)

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())

class Finish:
  def __init__(self):
    self.action_type = FINISH

  def __repr__(self):
    return "Finish()"

  def __eq__(self, o):
     return isinstance(o, Finish)

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())
