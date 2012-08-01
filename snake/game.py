#!/usr/bin/env python
import sys, pygame
from snake import Snake
from cheese import Cheese

pygame.init()

# Background color
bg_color = 0, 0, 0
done = False

grid_size = 100
BLOCK_SIZE = 5

pos_x, pos_y = 0, 0
direction = 0

SNAKE_HEAD = [(18, 255, 0),(86,162,210),(209,86,210),(241,136,13)]

CHEESE_COL = 255, 255, 0

clock=pygame.time.Clock()

snakes = [Snake(x = 3,y = 1)]
cheese = Cheese(grid_size)

# Inititalize screen and set caption
size = width, height = grid_size*BLOCK_SIZE, grid_size*BLOCK_SIZE
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")

# Draw a square
def draw_square(screen, rect, color):
  screen.fill(color, rect)

while done==False:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

    if event.type == pygame.KEYDOWN:
    # Figure out if it was an arrow key, and set direction
      if event.key == pygame.K_LEFT:
        snakes[0].direc(Snake.DIRECTION_LEFT)
      if event.key == pygame.K_RIGHT:
        snakes[0].direc(Snake.DIRECTION_RIGHT)
      if event.key == pygame.K_UP:
        snakes[0].direc(Snake.DIRECTION_UP)
      if event.key == pygame.K_DOWN:
        snakes[0].direc(Snake.DIRECTION_DOWN)
      if event.key == pygame.K_ESCAPE:
        sys.exit()

      if len(snakes) == 1:
        if (event.key == pygame.K_a or event.key == pygame.K_d or event.key ==
            pygame.K_w or event.key == pygame.K_s) and len(snakes) == 1:
          snakes.append(Snake(x = 20, y = 1))
      else:
        if event.key == pygame.K_a:
          snakes[1].direc(Snake.DIRECTION_LEFT)
        if event.key == pygame.K_d:
          snakes[1].direc(Snake.DIRECTION_RIGHT)
        if event.key == pygame.K_w:
          snakes[1].direc(Snake.DIRECTION_UP)
        if event.key == pygame.K_s:
          snakes[1].direc(Snake.DIRECTION_DOWN)
  
  # Check for collision with walls
  for snake in snakes:
    if snake.oos(grid_size) == True or snake.oos(grid_size) == True:
      sys.exit()

  # Move the snake
  for snake in snakes:
    snake.move()
  
  for snake in snakes:
    if snake.position()[0][0] == cheese.position()[0] and snake.position()[0][1] == cheese.position()[1]:
      snake.add(10)
      del cheese
      cheese = Cheese(grid_size)

  clock.tick(60)
#  print(clock.get_fps())
  
  # Clear screen and draw background
  screen.fill(bg_color)
  
  draw_square(screen, [cheese.position()[0]*BLOCK_SIZE,cheese.position()[1]*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE], CHEESE_COL)
  
  # Draw the snake itself
  snake_draw = 0
  for snake in snakes:
    for point in snake.position():
      draw_square(screen, [point[0]*BLOCK_SIZE,point[1]*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE], SNAKE_HEAD[snake_draw])
    snake_draw += 1

  # Flip the buffer to the display to show the snake
  pygame.display.flip()
  
pygame.quit()
