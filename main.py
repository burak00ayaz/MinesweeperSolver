import cv2
import pyautogui
import numpy as np
from random import *
from enum import Enum
from game_board import GameBoard
import time
import os


class Strategy(GameBoard):
    def __init__(self):
        GameBoard.__init__(self)

    def at(self, x, y, board):
        return board[y][x]

    def mark(self, x, y, board, value):
        board[y][x] = value

    def tiles_with_values(self, board, numbers=False, unknowns=False, mines=False, clears=False):
        for y in range(self.height):
            for x in range(self.width):
                value = board[y][x]
                if not numbers and value not in [self.UNKNOWN, self.MINE, self.CLEAR]:
                    continue
                if not unknowns and value == self.UNKNOWN:
                    continue
                if not mines and value == self.MINE:
                    continue
                if not clears and value == self.CLEAR:
                    continue
                yield x, y, value

    def filtered(self, tiles, board, values):
        return [p for p in tiles if self.at(p[0],p[1],board) in values]

    def flag_mines(self, board, click=True):
        # We check surrounding tiles of a tile. If the sum of surrounding unknown tiles
        # and flagged mines equals the tile's number, we conclude that the unknown tiles are mines. 
        for x, y, value in self.tiles_with_values(board, numbers=True):
            surr = self.get_surrounding_tiles(x,y)
            unknowns = self.filtered(surr, board, [self.UNKNOWN])
            mines = self.filtered(surr, board, [self.MINE])
            if len(unknowns) + len(mines) == value:
                for u in unknowns:
                    if click:
                        self.mouse.right_click(u[0], u[1])
                    self.mark(u[0], u[1], board, value=self.MINE)

    def possible_moves(self, board):
        # We check surrounding tiles of a tile. If the number of surrounding mines equals tile's number,
        # we conclude that surrounding unknown tiles are clear.
        moves = []
        for x, y, value in self.tiles_with_values(board, numbers=True):
            surr = self.get_surrounding_tiles(x,y)
            mines = self.filtered(surr, board, [self.MINE])
            if len(mines) == value:
                for p in surr:
                    if self.at(p[0], p[1], board) == self.UNKNOWN: #every surrounding unknown is playable
                        moves.append(p)
        return moves

    #TODO
    def find_contradiction(self, board) -> bool:
        # when we can not find a move to play, we flag a random tile as mine, and then try to find contradictions.
        # we try to play moves that have the highest probability of being false. Highest it can get is 1/2.
        # if we can find a contradiction, then we know that given tile is clear. we will use this function recursively.

        #iki turlu contradiction bulabiliriz: 
        #1. tile'in etrafinda olmasi gerekenden cok mayin isaretledik
        #2. tile'in etrafinda yeterince mayin olamaz. bos yerlerin sayisi yetmiyor.
        while True:
            self.flag_mines(board, click=False)
            moves = self.possible_moves(board)
            if not moves:
                return False
            for move in set(moves):
                self.mark(move[0], move[1], board, value=self.CLEAR)
            for x, y, value in self.tiles_with_values(board, numbers=True):
                surr = self.get_surrounding_tiles(x,y)
                mines = self.filtered(surr, board, [self.MINE])
                if len(mines) > value:
                    return True
                unknowns = self.filtered(surr, board, [self.UNKNOWN])
                if len(mines) + len(unknowns) < value:
                    return True

    #what makes a random move playable? 
    def playable_random_moves(self, board):
        for x, y, value in self.tiles_with_values(board, unknowns=True):
            surr = self.get_surrounding_tiles(x,y)
            knowns = self.filtered(surr, board, [self.ONE, self.TWO, self.THREE, self.FOUR, self.FIVE, self.SIX, self.MINE])
            if len(knowns) >= 1:
                yield x, y



    def game(self):
        self.mouse.click(0, 0) #focus click
        self.mouse.click(0, 0) #initial click

        while True:
            self.mouse.move_away_mouse()
            self.update_board()
            self.flag_mines(self.board)
            moves = self.possible_moves(self.board)
            played_moves = []
            found_a_move = False

            if moves:
                found_a_move = True

            for move in set(moves):
                self.mouse.click(move[0], move[1])
                played_moves.append(move)  
                        
            for x, y in self.playable_random_moves(self.board):
                if (x,y) in played_moves:
                    continue
                print(f"{x},{y} is playable. marking it as mine and trying to find a contradiction.")
                new_board = np.copy(self.board)
                self.mark(x, y, new_board, self.MINE)
                if self.find_contradiction(new_board):
                    print("found a contradiction!!!")
                    found_a_move = True
                    self.mouse.click(x,y)

            if not found_a_move:
                i = input('[+] Play a move and press Enter to let me continue.')
                if i == "b":
                    self.print_board()

player = Strategy()
player.game()



