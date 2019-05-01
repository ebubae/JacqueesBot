INSERT = 1
REMOVE = 2

class Insert:
  def __init__(self, sample_id, time):
    self.sample_id = sample_id
    self.time = time
    self.action_type = INSERT

class Remove:
  def __init__(self, insert_id):
    self.insert_id = insert_id
    self.action_type = REMOVE
