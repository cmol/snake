#!/usr/bin/env python
import argparse
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

parser = argparse.ArgumentParser(prog='snake.py',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                description='Small snake game for many players')
parser.add_argument('-p', '--players', type=int, default=1, help='Number of players')
parser.add_argument('-g', '--grid', type=int, default=100, help='Grid size')
parser.add_argument('--fullscreen',action='store_true', help='Fullscreen')
parser.add_argument('-b', '--block', type=int, default=5, help='Block size')
args = parser.parse_args()

game = snake.game.Game(args.players, args.grid, args.block, args.fullscreen)
reactor.listenTCP(9999, SnakeFactory())
#reactor.callInThread(game.start_game())

#game.start_game()
game.start()
reactor.run()
