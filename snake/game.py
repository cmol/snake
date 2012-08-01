#!/usr/bin/env python
import sys, pygame
from snake import Snake
from cheese import Cheese

pygame.init()

class Game (object):

  # Background color
  bg_color = 0, 0, 0
  done = False

  grid_size = 100
  BLOCK_SIZE = 5

  pos_x, pos_y = 0, 0
  direction = 0

  snakes = []
  
  SNAKE_HEAD = [(18, 255, 0),(86,162,210),(209,86,210),(241,136,13)]
  SNAKE_POS = [(4, 1), (50, 50), (23, 1), (33, 1)]

  CHEESE_COL = 255, 255, 0

  clock=pygame.time.Clock()

  cheese = Cheese(grid_size)

  screen = None
  size = None
  
  # Constructor
  def __init__(self, players, grid, block):
    self.grid_size = grid
    
    self.size = width, height = self.grid_size*self.BLOCK_SIZE, self.grid_size*self.BLOCK_SIZE
    self.screen = pygame.display.set_mode(self.size)
    pygame.display.set_caption("Snake")
    
    # Create the snakes
    for i in range(0,players):
      self.snakes.append(Snake(x = self.SNAKE_POS[i][0], y = self.SNAKE_POS[i][1]))
      print i

  # Inititalize screen and set caption

  # Draw a square
  def draw_square(self, screen, rect, color):
    screen.fill(color, rect)

  def start_game(self):
    while self.done==False:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
        # Figure out if it was an arrow key, and set direction
          if event.key == pygame.K_LEFT:
            self.snakes[0].direc(Snake.DIRECTION_LEFT)
          if event.key == pygame.K_RIGHT:
            self.snakes[0].direc(Snake.DIRECTION_RIGHT)
          if event.key == pygame.K_UP:
            self.snakes[0].direc(Snake.DIRECTION_UP)
          if event.key == pygame.K_DOWN:
            self.snakes[0].direc(Snake.DIRECTION_DOWN)
          if event.key == pygame.K_ESCAPE:
            sys.exit()

          if len(self.snakes) == 1:
            if (event.key == pygame.K_a or event.key == pygame.K_d or event.key ==
                pygame.K_w or event.key == pygame.K_s) and len(self.snakes) == 1:
              self.snakes.append(Snake(x = 20, y = 1))
          else:
            if event.key == pygame.K_a:
              self.snakes[1].direc(Snake.DIRECTION_LEFT)
            if event.key == pygame.K_d:
              self.snakes[1].direc(Snake.DIRECTION_RIGHT)
            if event.key == pygame.K_w:
              self.snakes[1].direc(Snake.DIRECTION_UP)
            if event.key == pygame.K_s:
              self.snakes[1].direc(Snake.DIRECTION_DOWN)
      
      # Check for collision with walls
      for snake in self.snakes:
        if snake.oos(self.grid_size) == True or snake.oos(self.grid_size) == True:
          sys.exit()

      # Move the snake
      for snake in self.snakes:
        snake.move()
        
      if snake.position()[0][0] == self.cheese.position()[0] and snake.position()[0][1] == self.cheese.position()[1]:
        snake.add(10)
        #del self.cheese
        self.cheese = Cheese(self.grid_size)
      
      for current_snake in self.snakes:
        for other_snake in self.snakes:
          if other_snake is not current_snake:
            if current_snake.collision(other_snake):
              print("collition")
              sys.exit()

      self.clock.tick(60)
    #  print(clock.get_fps())
      
      # Clear screen and draw background
      self.screen.fill(self.bg_color)
      
      self.draw_square(
          self.screen,
          [self.cheese.position()[0]*self.BLOCK_SIZE,
            self.cheese.position()[1]*self.BLOCK_SIZE,
            self.BLOCK_SIZE,self.BLOCK_SIZE],
          self.CHEESE_COL)
      
      # Draw the snake itself
      snake_draw = 0
      for snake in self.snakes:
        for point in snake.position():
          self.draw_square(
            self.screen,
            [point[0]*self.BLOCK_SIZE,
              point[1]*self.BLOCK_SIZE,
              self.BLOCK_SIZE,self.BLOCK_SIZE],
            self.SNAKE_HEAD[snake_draw])
        
        snake_draw += 1

      # Flip the buffer to the display to show the snake
      pygame.display.flip()
      
    pygame.quit()