class Snake(object):
  """class for managin snake(s) - Snake"""

  DIRECTION_UP = 1 
  DIRECTION_DOWN = 2 
  DIRECTION_LEFT = 3 
  DIRECTION_RIGHT = 4

  # Variables for Snake objects

  def __init__(self, color, x, y):
    # Get snake color
    self._col = color
    self._length = 3
    self._snake_arr = []
    self._snake_arr.append([x,y])
    self._direction = self.DIRECTION_RIGHT

  # Method for moving the snake
  def move(self):
    if self._direction == self.DIRECTION_RIGHT:
      self._snake_arr.insert(0, [self._snake_arr[0][0]+1, self._snake_arr[0][1]])
    elif self._direction == self.DIRECTION_DOWN:
      self._snake_arr.insert(0, [self._snake_arr[0][0], self._snake_arr[0][1]+1])
    elif self._direction == self.DIRECTION_LEFT:
      self._snake_arr.insert(0, [self._snake_arr[0][0]-1, self._snake_arr[0][1]])
    elif self._direction == self.DIRECTION_UP:
      self._snake_arr.insert(0, [self._snake_arr[0][0], self._snake_arr[0][1]-1])
    
    self._snake_arr = self._snake_arr[:self._length]  
      
  def add(self, amount):
    self._length += amount
    if self._length <= 0:
      self._length = 1
  
  def position(self):
    return self._snake_arr
    
  def color(self):
    return self._col
  
  def direc(self, direction):
    self._direction = direction

  """ See if this snake (self) has crashed into the other snake (snake) """
  def collision(self, snake):
    for other_snake in snake._snake_arr:
      if other_snake == self._snake_arr[0]:
        return True
    return False

  # Out of stage
  def oos(self, grid_x, grid_y):
    if self._snake_arr[0][0] >= grid_x or self._snake_arr[0][1] >= grid_y or self._snake_arr[0][0] < 0 or self._snake_arr[0][1] < 0:
      return True
    else:
      return False
