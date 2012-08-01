from random import randint

class Cheese(object):
  
  pos = [0, 0]
  
  def __init__(self, grid_x,grid_y):
    self.pos = randint(0,grid_x-1), randint(0,grid_y-1)
  
  def position(self):
    return self.pos