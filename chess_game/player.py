import logging as log

from random import choice
from math import inf
from itertools import zip_longest
from typing import Any

from chess import Board, Move

from abc import ABC, abstractmethod

try:
    from board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from config import BOARD_SCORES, END_SCORES, PIECES
except ModuleNotFoundError:
    from .board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from .config import BOARD_SCORES, END_SCORES, PIECES

log.basicConfig(level=log.INFO,
                format='%(levelname)s - %(asctime)s - %(message)s',
                datefmt='%H:%M:%S')


class Player(ABC):
    def __init__(self, player: bool, solver: str = None):
        self.player = player
        self.solver = solver

    @abstractmethod
    def move(self, board: Board):
        pass


def _print_moves(moves):
    iters = [iter(moves)] * 4
    iters = zip_longest(*iters)

    for group in iters:
        print(" | ".join(move for move in group if move is not None))


class HumanPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "human")

    def _get_move(self, board: Board) -> str:
        uci = input(f"({turn_side(board)}) Your turn! Choose move (in uci): ")

        # check legal uci move
        try:
            Move.from_uci(uci)
        except ValueError:
            uci = None
        return uci

    def move(self, board: Board) -> str:
        assert board.turn == self.player, "Not your turn to move!"

        legal_moves = [move.uci() for move in board.legal_moves]

        move = self._get_move(board)

        while move is None:
            print("Invalid uci move! Try again.", )
            move = self._get_move(board)

        while move not in legal_moves:
            print("Not a legal move! Avaliable moves:\n")
            _print_moves(legal_moves)
            move = self._get_move(board)

        return move


# WARNING: PLAYER aleatorio original do codigo
class RandomPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "random")

    def move(self, board: Board) -> str:
        assert board.turn == self.player, "Not bot turn to move!"

        moves = list(board.legal_moves)
        move = choice(moves).uci()

        return move


# WARNING: PLAYER Ganancioso sempre escolhe o melhor primeiro movimento.
class GreedyPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "greedy")

    def move(self, board: Board) -> str:
        moves = list(board.legal_moves)

        for move in moves:
            test_board = board.copy()

            test_board.push(move)
            move.score = eval_board_state(test_board, self.player, BOARD_SCORES)

        moves = sorted(moves, key=lambda move: move.score, reverse=True)

        return moves[0].uci()


# WARNING: PLAYER minimo e maximo sempre escolhe o melhor primeiro movimento e melhor movimento do outro player.
class MiniMaxPlayer(Player):
    def __init__(self, player, depth=3):
        super().__init__(player, "minimax")
        self.depth = depth
        self.verbose = False  # se quiser enteder as escolhas dele
        self.random_first_move = False

    def _minimax(self, board: Board, player: bool, depth: int, alpha: float = -inf, beta: float = inf) -> \
            list[float | None] | list[float | str | None | Any]:
        # confere se é jogavel
        if depth == 0 or game_over(board):
            return [game_score(board, self.player, END_SCORES, BOARD_SCORES), None]

        # se for branca primeiro movimento
        if len(board.move_stack) == 0:
            moves = list(board.legal_moves)
            white_opening = choice(moves)
            return [0.0, white_opening]

        moves = sorted_moves(board)

        #com base no player escolhe a melhor ou pior jogada
        if board.turn == player:
            return self._max(alpha, beta, board, depth, moves, player)
        else:
            return self._min(alpha, beta, board, depth, moves, player)

    def _max(self, alpha, beta, board, depth, moves, player):
        max_score, best_move = -inf, None
        for move, piece in moves:
            test_board = board.copy()
            test_board.push(move)

            score = self._minimax(test_board, not player, depth - 1, alpha, beta)

            if self.verbose:
                log.info(
                    f"{turn_side(test_board)}, M{len(moves)}, D{depth}, {PIECES[piece]}:{move} - SCORE: {score}")

            #com ajuda do chatgpt
            alpha = max(alpha, score[0])
            if beta <= alpha:
                break

            if score[0] >= max_score:
                max_score = score[0]
                best_move = move
        return [max_score, best_move]

    def _min(self, alpha, beta, board, depth, moves, player):
        min_score, best_move = inf, None
        for move, piece in moves:
            test_board = board.copy()
            test_board.push(move)

            score = self._minimax(test_board, player, depth - 1, alpha, beta)

            if self.verbose:
                log.info(
                    f"{turn_side(test_board)}, M{len(moves)}, D{depth}, {PIECES[piece]}:{move} - SCORE: {score}")

            beta = min(beta, score[0])
            if beta <= alpha:
                break

            if score[0] <= min_score:
                min_score = score[0]
                best_move = move
        return [min_score, best_move]

    def move(self, board: Board) -> str:
        best_move = self._minimax(board, self.player, self.depth)
        return best_move[1].uci()
