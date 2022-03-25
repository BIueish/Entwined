import sys

MIN_VER = (3, 7)

if sys.version_info[:2] < MIN_VER:
    sys.exit("This game requires Python {}.{}".format(*MIN_VER))

from src.game import Game

game = Game()
game.run()
