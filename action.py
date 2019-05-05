INSERT = 1
FINISH = 2

class Insert:
  def __init__(self, sample_id, time):
    self.sample_id = sample_id
    self.time = time
    self.action_type = INSERT

  def __repr__(self):
    return "Insert({}, {})".format(self.sample_id, self.time)

  def __eq__(self, o):
     return o.sample_id == self.sample_id and o.time == self.time if isinstance(o, Insert) else False 

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
