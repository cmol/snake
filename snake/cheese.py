from random import randint

class Cheese(object):
  
  def __init__(self, grid_x,grid_y):
    self.size = 2 if (randint(0, 9) > 7) else 1
    self.pos = randint(0,grid_x-self.size), randint(0,grid_y-self.size)
  
  def position(self):
    return self.pos
    
  def size(self):
    return self.size
    
  def collide_with(self, x, y):
    ret = False
    if x >= self.pos[0] and x < self.pos[0] + self.size and y >= self.pos[1] and y < self.pos[1] + self.size:
      ret = True
    return ret