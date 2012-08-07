import cPickle
from threading import Thread
from twisted.internet import protocol
from snake import Snake

#Mostly static?
class GameServer(protocol.Protocol, Thread):

  __SNAKE_HEAD = [(18,255,0),(134,197,237),(209,86,210),(241,136,13),(255,0,0),(29,255,204),(255,255,0),(255,255,255)]
  __SNAKE_POS = [(3, 1), (3, 11), (3, 21), (3, 31), (3, 41), (3, 51), (3, 61), (3, 71)]
  __CHEESE_COL = 255, 255, 0


  __snakes = []
  __servers = []
  #__server should not be in __servers
  __server = None
  
  def __init__(self):
    pass

  def threadServer(self):
    Thread.__init__(self) 
    GameServer.__server = self

  def connectionMade(self):
    print("Connection made")
    self.__snake = GameServer.spawnSnake()
    GameServer.__servers.append(self)

  def dataReceived(self, data):
    self.__snake.direc(int(data.rstrip()))

  @staticmethod
  def moveSnakes():
    for snake in GameServer.__snakes:
      snake.move()
    return True

  @staticmethod
  def spawnSnake():
    snake = Snake(
      GameServer.__SNAKE_HEAD
        [
          len(GameServer.__snakes)
        ], 
      *GameServer.__SNAKE_POS
        [len(GameServer.__snakes)
      ]
    )
    GameServer.__snakes.append(snake)
    print('Snake spawned')
    return snake

  @staticmethod
  def sendSnakes():
    data = {'snakes':GameServer.__snakes, 'cheeses':GameServer.__cheeses}
    data_pickled = pickle.dumps(data)
    for server in GameServer.__servers:
      server.transport.write(data_pickled)

class GameServerFactory(protocol.Factory):
  def buildProtocol(self, addr):
    return GameServer()


