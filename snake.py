#!/usr/bin/env python
import argparse
import snake
from snake.game_server import GameServer, GameServerFactory
from twisted.internet import threads, protocol, reactor

parser = argparse.ArgumentParser(prog='snake.py',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                description='Small snake game for many players')
parser.add_argument('-p', '--players', type=int, default=1, help='Number of players')
parser.add_argument('-g', '--grid', type=int, default=100, help='Grid size')
parser.add_argument('--fullscreen',action='store_true', help='Fullscreen')
parser.add_argument('-b', '--block', type=int, default=5, help='Block size')
parser.add_argument('-s', '--server', action='store_true', help='Is this a server?')
parser.add_argument('-c', '--connect', type=str, default='127.0.0.1', help='If this is a cliient, what is the server address?')
args = parser.parse_args()

if args.server:
  server = GameServer()
#  server.start()
  reactor.listenTCP(9999, GameServerFactory())
  reactor.run()
else:
  pass
#  game = snake.game.Game(args.players, args.grid, args.block, args.fullscreen)
