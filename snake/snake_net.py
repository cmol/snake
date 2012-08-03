import snake
from twisted.internet import threads, protocol, reactor

class SnakeRemote(protocol.Protocol):
  def connectionMade(self):
    print("Con made")
    #raise Exception("!")
    self.snakie = snake.game.Game.spawnSnake()
        
  def dataReceived(self, data):
    data = int(data.rstrip())
    snake.game.Game.event_map[data][0].direc(snake.game.Game.event_map[data][1])

class SnakeFactory(protocol.Factory):
  def buildProtocol(self, addr):
    return SnakeRemote()

