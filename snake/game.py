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

SNAKE_HEAD = 18, 255, 0
CHEESE_COL = 255, 255, 0

clock=pygame.time.Clock()

snake1 = Snake()
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
        snake1.direc(2)
      if event.key == pygame.K_RIGHT:
        snake1.direc(0)
      if event.key == pygame.K_UP:
        snake1.direc(3)
      if event.key == pygame.K_DOWN:
        snake1.direc(1)
  
  # Check for collision with walls
  if snake1.oos(grid_size) == True:
    sys.exit()
  # Limit to 60 FPS

  # Move the snake
  snake1.move()
  
  if snake1.position()[0][0] == cheese.position()[0] and snake1.position()[0][1] == cheese.position()[1]:
    snake1.add()
    del cheese
    cheese = Cheese(grid_size)
    
  clock.tick(60)
  
  # Clear screen and draw background
  screen.fill(bg_color)
  
  draw_square(screen, [cheese.position()[0]*BLOCK_SIZE,cheese.position()[1]*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE], CHEESE_COL)
  
  # Draw the snake itself
  for point in snake1.position():
      draw_square(screen, [point[0]*BLOCK_SIZE,point[1]*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE], SNAKE_HEAD)
  
  # Flip the buffer to the display to show the snake
  pygame.display.flip()
  
pygame.quit()