import cPickle
from twisted.internet import protocol
import pygame
import logging

from snake import Snake
from cheese import Cheese

logging.basicConfig(level=logging.DEBUG)

class GameServer(protocol.Protocol):

  __SNAKE_HEAD = [(18,255,0),(134,197,237),(209,86,210),(241,136,13),(255,0,0),(29,255,204),(255,255,0),(255,255,255)]
  __SNAKE_POS = [(3, 1), (3, 11), (3, 21), (3, 31), (3, 41), (3, 51), (3, 61), (3, 71)]
  __CHEESE_COL = 255, 255, 0

  #(blocksize, grid_x, grid_y)
  __playfield = (15, 100, 100)

  __snakes = []
  __servers = []
  __cheeses = []

  def __init__(self):
    if len(GameServer.__cheeses) == 0:
      GameServer.__cheeses.append(Cheese(GameServer.__playfield[1], GameServer.__playfield[2]))

  def connectionMade(self):
    logging.info("Connection established")
    self.__snake = GameServer.spawnSnake()
    GameServer.__servers.append(self)
    #Not ready in the client yet
    #self.transport.write(cPickle.dumps(GameServer.__playfield))

  def connectionLost(self, reason):
    logging.info("Connection lost, %s" % reason.getErrorMessage())
    GameServer.snakeRemove(self.__snake)
    for idx in range(len(self.__servers)):
      if self.__servers[idx] is self:
        del self.__servers[idx]
        del self
        logging.info("Instance killed")
        break

  def dataReceived(self, data):
    #self.transport.write('noget')
    try:
      self.__snake.direc(int(data.rstrip()[-1]))
    except Exception as e:
      logging.warning("Weird data received, %s, %s" % (data,e))

  @staticmethod
  def snakesMove():
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
    logging.info('Snake spawned')
    return snake

  @staticmethod
  def sendPlayfieldContent():
    if len(GameServer.__servers) > 0:
      data = {'snakes':GameServer.__snakes, 'cheeses':GameServer.__cheeses}
      #data = {'snakes':GameServer.__snakes}
      data_pickled = cPickle.dumps(data, -1)
      for server in GameServer.__servers:
        server.transport.write(data_pickled + "\r\n")
 
  #Wallcrash
  @staticmethod
  def snakesCrash():
    for snake in GameServer.__snakes:
      if snake.oos(GameServer.__playfield[1], GameServer.__playfield[2]) == True:
        logging.info("Snake crashed with playfield, removing")
        GameServer.snakeRemove(snake)

  @staticmethod
  def snakesCollide():
    for current_snake in GameServer.__snakes:
      for other_snake in GameServer.__snakes:
        if other_snake is not current_snake:
          if current_snake.collision(other_snake):
            logging.debug("collision")
            current_snake.add(-5)

  @staticmethod
  def snakeRemove(snake):
    """TODO: Reduce all this searching!"""
    for idx in range(len(GameServer.__snakes)):
      if GameServer.__snakes[idx] is snake:
        del GameServer.__snakes[idx]
        logging.info("Snake removed")
        return True
    logging.warning("Snake not in the game")
    return False

  #First come (in __snakes), first served
  @staticmethod
  def snakesNom():
    for sidx in range(len(GameServer.__snakes)):
      for cidx in range(len(GameServer.__cheeses)):
        if (GameServer.__cheeses[cidx].collide_with(GameServer.__snakes[sidx].position()[0][0], GameServer.__snakes[sidx].position()[0][1])):
          GameServer.__snakes[sidx].add(10)
          del GameServer.__cheeses[cidx]
          GameServer.__cheeses.append(Cheese(GameServer.__playfield[1], GameServer.__playfield[2]))
          logging.info("NOM!")

  def update(self):
    self.snakesMove()
    self.snakesCollide()
    self.snakesCrash()
    self.snakesNom()
    self.sendPlayfieldContent()

class GameServerFactory(protocol.Factory):
  def buildProtocol(self, addr):
    return GameServer()
