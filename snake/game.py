#!/usr/bin/env python
import pygame
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
  
  DIRECTION_UP = 1 
  DIRECTION_DOWN = 2 
  DIRECTION_LEFT = 3 
  DIRECTION_RIGHT = 4
  
  event_map = {}
  event_keys = [
    [[pygame.K_LEFT, DIRECTION_LEFT],
      [pygame.K_UP, DIRECTION_UP],
      [pygame.K_RIGHT, DIRECTION_RIGHT],
      [pygame.K_DOWN, DIRECTION_DOWN]],
    [[pygame.K_a, DIRECTION_LEFT],
      [pygame.K_w, DIRECTION_UP],
      [pygame.K_d, DIRECTION_RIGHT],
      [pygame.K_s, DIRECTION_DOWN]],
    [[pygame.K_j, DIRECTION_LEFT],
      [pygame.K_i, DIRECTION_UP],
      [pygame.K_l, DIRECTION_RIGHT],
      [pygame.K_k, DIRECTION_DOWN]],
    [[pygame.K_f, DIRECTION_LEFT],
      [pygame.K_t, DIRECTION_UP],
      [pygame.K_h, DIRECTION_RIGHT],
      [pygame.K_g, DIRECTION_DOWN]]
    ]
  
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
    
    # Create the snakes and attach keys to them
    for i in range(0,players):
      snake = Snake(*self.SNAKE_POS[i])
      self.snakes.append(snake)
      self.attach_keys(snake, self.event_keys[i])

  # Draw a square
  def draw_square(self, screen, rect, color):
    screen.fill(color, rect)
  
  # Place keys from our event_keys in our event_map
  def attach_keys(self, snake, key_maps):
    for key_map in key_maps:
      self.event_map[key_map[0]] = [snake, key_map[1]]
  
  # End game nicely
  def end_game(self):
    exit()
    pygame.quit()

  # Run god dammit! RUN!
  def start_game(self):
    # Main loop
    while self.done==False:
      
      # Check for events (key press etc.)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        # Check for key presses and if they are in our event_map
        if event.type == pygame.KEYDOWN:
          if event.key in self.event_map:
            self.event_map[event.key][0].direc(self.event_map[event.key][1])
      
      # Check for collision with walls
      snake_num = 0
      for snake in self.snakes:
        if snake.oos(self.grid_x, self.grid_y) == True:
          self.snakes.pop(snake_num)
          
          # If less than 2 players are left, end game
          if len(self.snakes) < 2:
            self.end_game()
        snake_num += 1

      # Move the snake
      for snake in self.snakes:
        snake.move()
        
        # If snake head is colliding with cheese, make new cheese and add to snake
        if (self.cheese.collide_with(snake.position()[0][0], snake.position()[0][1])):
#        if snake.position()[0][0] == self.cheese.position()[0] and snake.position()[0][1] == self.cheese.position()[1]:
          snake.add(10)
          self.cheese = Cheese(self.grid_x, self.grid_y)
      
      # Check for collision between snakes
      for current_snake in self.snakes:
        for other_snake in self.snakes:
          if other_snake is not current_snake:
            if current_snake.collision(other_snake):
              print("collition")
              current_snake.add(-5)

      self.clock.tick(60)
      #print(clock.get_fps())
      
      # Clear screen and draw background
      self.screen.fill(self.bg_color)
      
      # Draw the cheese
      self.draw_square(
          self.screen,
          [self.cheese.position()[0]*self.BLOCK_SIZE,
            self.cheese.position()[1]*self.BLOCK_SIZE,
            self.BLOCK_SIZE*self.cheese.size,self.BLOCK_SIZE*self.cheese.size],
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
