import threading
import pygame

pygame.init()

class ClientInput(threading.Thread):
  # Directions
  DIRECTION_UP = 1 
  DIRECTION_DOWN = 2 
  DIRECTION_LEFT = 3 
  DIRECTION_RIGHT = 4
  
  # Event keys
  event_map = {pygame.K_LEFT: DIRECTION_LEFT,
      pygame.K_UP: DIRECTION_UP,
      pygame.K_RIGHT: DIRECTION_RIGHT,
      pygame.K_DOWN: DIRECTION_DOWN}
      
  # Event loop boolean
  done = False
  
  # Clock to limit fps (runs per second in this case)
  clock = pygame.time.Clock()
  
  def __init__(self, protocol):
    threading.Thread.__init__(self)
    self.protocol = protocol
    
  def run(self):
    while self.done == False:
      self.clock.tick(30)
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.protocol.end_game()
          self.done = True
        # Check for key presses and if they are in our event_map
        if event.type == pygame.KEYDOWN:
          if event.key in self.event_map:
            self.protocol.sendLine(str(self.event_map[event.key]))
          elif event.key == pygame.K_ESCAPE:
            self.protocol.end_game()
            self.done = True