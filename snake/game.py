#!/usr/bin/env python
import sys, pygame

pygame.init()

# Background color
bg_color = 0, 0, 0
done = False

grid_size = 100
block_size = 5

pos_x, pos_y = 0, 0
direction = 0

snake_head_color = 18, 255, 00

clock=pygame.time.Clock()

# Inititalize screen and set caption
size = width, height = grid_size*block_size, grid_size*block_size
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
      direction = 2
    if event.key == pygame.K_RIGHT:
      direction = 0
    if event.key == pygame.K_UP:
      direction = 3
    if event.key == pygame.K_DOWN:
      direction = 1
  
  # Move the snake
  if direction == 0:
    pos_x +=1
  if direction == 1:
    pos_y +=1
  if direction == 2:
    pos_x -=1
  if direction == 3:
    pos_y -=1
  
  if pos_x >= grid_size or pos_y >= grid_size or pos_x < 0 or pos_y < 0:
    sys.exit()
  
  # Limit to 60 FPS
  clock.tick(60)
  print (clock.get_fps())
  
  # Draw stuff
  screen.fill(bg_color)
  draw_square(screen, [pos_x*block_size,pos_y*block_size,block_size,block_size], snake_head_color)
  pygame.display.flip()
  
pygame.quit()