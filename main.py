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

    def tiles_with_values(self, just_numbers=False):
        for y in range(self.height):
            for x in range(self.width):
                value = self.board[y][x]
                if just_numbers and value in [self.UNKNOWN, self.MINE, self.CLEAR]:
                    continue
                yield (x,y), value

    def flag_mines(self):
        # We check surrounding tiles of a tile. If the sum of surrounding unknown tiles
        # and flagged mines equals the tile's number, we conclude that the unknown tiles are mines. 
        for (x,y), value in self.tiles_with_values(just_numbers=True):
            surr = self.get_surrounding_tiles(x,y)
            unknowns = [p for p in surr if self.board[p[1]][p[0]] == self.UNKNOWN] #count unknowns
            mines = [p for p in surr if self.board[p[1]][p[0]] == self.MINE] #count mines
            if len(unknowns) + len(mines) == value:
                for u in unknowns:
                    self.mouse.right_click(u[0], u[1])
                    self.board[u[1]][u[0]] = self.MINE

    def possible_moves(self):
        # We check surrounding tiles of a tile. If the number of surrounding mines equals tile's number,
        # we conclude that surrounding unknown tiles are clear.
        moves = []
        for (x,y), value in self.tiles_with_values(just_numbers=True):
            surr = self.get_surrounding_tiles(x,y)
            mines = [p for p in surr if self.board[p[1]][p[0]] == self.MINE] #count mines
            if len(mines) == value:
                for p in surr:
                    if self.board[p[1]][p[0]] == self.UNKNOWN: #every surrounding unknown is playable
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
        pass

    def moves_with_chance(self, chance: float):
        pass

    def game(self):
        self.mouse.click(0, 0) #focus click
        self.mouse.click(0, 0) #initial click

        while True:
            self.mouse.move_away_mouse()
            self.update_board()
            self.flag_mines()
            moves = self.possible_moves()

            for move in set(moves):
                self.mouse.click(move[0], move[1])      
                        
            if not moves:
                self.moves_with_chance(0.5)
                print('[+] I could not find a move.')
                i = input('[+] Play a move and press Enter to let me continue.')
                if i == "b":
                    self.print_board()

player = Strategy()
player.game()



