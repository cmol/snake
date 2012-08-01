from random import randint

class Cheese(object):
  
  pos = [0, 0]
  
  def __init__(self, grid):
    self.pos = randint(0,grid-1), randint(0,grid-1)
  
  def position(self):
    return self.pos