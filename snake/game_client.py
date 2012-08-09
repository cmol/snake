import cPickle
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import pygame
from snake import Snake
from cheese import Cheese
from client_input import ClientInput
import threading

pygame.init()
  
class GameClient(LineReceiver):
  # End string
  end = "DEAD"
  direction = None
  
  # Colors
  bg_color = 0, 0, 0
  CHEESE_COL = 255, 255, 0
  
  # Vars for screen building (TODO: Move this data to server)
  block_size = 5
  grid_size = 100
  grid_x = grid_size
  grid_y = grid_size
  
  def __init__(self):
    # Initialize screen 
    size = width, height = self.grid_x*self.block_size, self.grid_y*self.block_size
    self.screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
    self.client_input = ClientInput(self)
    self.client_input.start()
    
  # Draw a square
  def draw_square(self, screen, rect, color):
    screen.fill(color, rect)
  
  # Check for events (key press etc.)  
  def check_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT: self.end_game()
      # Check for key presses and if they are in our event_map
      if event.type == pygame.KEYDOWN:
        if event.key in self.event_map:
          self.sendLine(str(self.event_map[event.key]))
        elif event.key == pygame.K_ESCAPE:
         self.end_game()
  
  def draw_screen(self):
    # Paint everything black
    self.screen.fill(self.bg_color)
      
    # Draw the snake itself
    for snake in self.snakes:
      for point in snake.position():
        self.draw_square(
          self.screen,
          [
            point[0]*self.block_size,
            point[1]*self.block_size,
            self.block_size,
            self.block_size
          ],
          snake.color()
        )
        
    # Draw the cheeses
    for cheese in self.cheeses:
      self.draw_square(
        self.screen,
          [
            cheese.position()[0]*self.block_size,
            cheese.position()[1]*self.block_size,
            self.block_size*cheese.size,
            self.block_size*cheese.size
          ],
          self.CHEESE_COL
        )
    
    # Show everything
    pygame.display.flip()
    
  # Do whatever needs to be done pr update
  def play_round(self):
    self.draw_screen()
        
  # End the game nicely
  def end_game(self):
    self.stopProducing() # That's nice!
  
  # ==== From here networking occurs ====  
  def connectionMade(self):
    print("Connection made")


  def lineReceived(self, line):
    try:
      data = cPickle.loads(line)
      self.snakes = data["snakes"]
      self.cheeses = data["cheeses"]
    except Exception as e:
      print p_data
      print e
    self.play_round()

class GameClientFactory(ClientFactory):
  protocol = GameClient

  def clientConnectionFailed(self, connector, reason):
    print 'connection failed:', reason.getErrorMessage()
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print 'connection lost:', reason.getErrorMessage()
    reactor.stop()
