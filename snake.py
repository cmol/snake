#!/usr/bin/env python
import argparse
import snake

parser = argparse.ArgumentParser(prog='snake.py',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                description='Small snake game for many players')
parser.add_argument('-p', '--players', type=int, default=1, help='Number of players')
parser.add_argument('-g', '--grid', type=int, default=100, help='Grid size')
parser.add_argument('--fullscreen',action='store_true', help='Fullscreen')
parser.add_argument('-b', '--block', type=int, default=5, help='Block size')
args = parser.parse_args()

game = snake.game.Game(args.players, args.grid, args.block, args.fullscreen)
game.start_game()