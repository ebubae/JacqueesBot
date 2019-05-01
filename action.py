INSERT = 1
REMOVE = 2

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

class Remove:
  def __init__(self, insert_id):
    self.insert_id = insert_id
    self.action_type = REMOVE

  def __repr__(self):
    return "Remove({})".format(self.sample_id)

  def __eq__(self, o):
     return o.insert_id == self.inser_id if isinstance(o, Insert) else False 

  def __ne__(self, o):
    return not self == o

  def __hash__(self):
    return hash(self.__repr__())
