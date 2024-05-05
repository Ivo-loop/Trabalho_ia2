# import numpy as np
# import pandas as pd

from player import HumanPlayer, RandomPlayer, GreedyPlayer, MiniMaxPlayer
from game import Game

game = Game()
result = game.start_game(GreedyPlayer, MiniMaxPlayer, visual=True, pause=0.1)
print(result)
#game.start_games(GreedyPlayer, MiniMaxPlayer, n=3)

