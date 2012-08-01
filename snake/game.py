#!/usr/bin/env python
import sys, pygame
from snake import Snake
from cheese import Cheese

pygame.init()

class Game (object):

  # Background color
  bg_color = 0, 0, 0
  done = False

  BLOCK_SIZE = 5
  grid_size = 100
  grid_x = pygame.display.Info().current_w / BLOCK_SIZE
  grid_y = pygame.display.Info().current_h / BLOCK_SIZE

  pos_x, pos_y = 0, 0
  direction = 0

  snakes = []
  
  SNAKE_HEAD = [(18, 255, 0),(86,162,210),(209,86,210),(241,136,13)]
  SNAKE_POS = [(3, 1), (3, 11), (3, 21), (3, 31)]

  CHEESE_COL = 255, 255, 0

  clock=pygame.time.Clock()

  screen = None
  size = None
  cheese = None
  
  fullscreen = pygame.FULLSCREEN
  
  # Constructor
  def __init__(self, players, grid, block, fullscreen):
    
    self.grid_size = grid
    if not fullscreen:
      self.fullscreen = 0
      self.grid_x , self.grid_y = self.grid_size, self.grid_size
    
    self.size = width, height = self.grid_x*self.BLOCK_SIZE, self.grid_y*self.BLOCK_SIZE
    self.screen = pygame.display.set_mode(self.size, self.fullscreen)
    pygame.display.set_caption("Snake")
    self.cheese = Cheese(self.grid_x, self.grid_y)
    # Create the snakes
    for i in range(0,players):
      self.snakes.append(Snake(*self.SNAKE_POS[i]))

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
        if snake.oos(self.grid_x, self.grid_y) == True:
          sys.exit()

      # Move the snake
      for snake in self.snakes:
        snake.move()
        
      if snake.position()[0][0] == self.cheese.position()[0] and snake.position()[0][1] == self.cheese.position()[1]:
        snake.add(10)
        #del self.cheese
        self.cheese = Cheese(self.grid_x, self.grid_y)
      
      for current_snake in self.snakes:
        for other_snake in self.snakes:
          if other_snake is not current_snake:
            if current_snake.collision(other_snake):
              print("collition")
              current_snake.add(-5)
              #sys.exit()

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
