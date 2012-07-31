class Snake(object):
  """class for managin snake(s) - Snake"""
  
  # Variables for Snake objects
  snake_arr = [[3,3], [2,3], [1,3]]
  add = False
  direction = 0

  # Method for moving the snake
  def move(self):
    if self.direction == 0:
      self.snake_arr.insert(0, [self.snake_arr[0][0]+1, self.snake_arr[0][1]])
    elif self.direction == 1:
      self.snake_arr.insert(0, [self.snake_arr[0][0], self.snake_arr[0][1]+1])
    elif self.direction == 2:
      self.snake_arr.insert(0, [self.snake_arr[0][0]-1, self.snake_arr[0][1]])
    elif self.direction == 3:
      self.snake_arr.insert(0, [self.snake_arr[0][0], self.snake_arr[0][1]-1])
      
    if self.add:
      self.add = False
    else:
      self.snake_arr.pop()
      print(self.snake_arr)
      
  def add(self):
    self.add = True
  
  def position(self):
    return self.snake_arr
  
  def direc(self, direction):
    self.direction = direction