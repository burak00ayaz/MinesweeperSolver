import cv2
import pyautogui
import numpy as np
from random import *
from enum import Enum
from game_board import GameBoard


class Strategy(GameBoard):
    def __init__(self):
        GameBoard.__init__(self)
        self.game()

    def filter_value(self, tiles, value):
        res = []
        for p in tiles:
            x = p[0]
            y = p[1]
            if self.board[x][y] == value:
                res.append(p)
        return res

    def calculate_moves(self):
        moves = []
        for h in range(self.height):
            for w in range(self.width):
                if self.board[h][w] == 1:
                    surr = self.get_surrounding_tiles(w,h)
                    
                    ones = self.filter_value(surr, 1)
                    if len(ones) == 1:
                        moves.append(ones[0])
                        
                    

    def click_unknown_tile(self):
        for w in range(self.width):
            for h in range(self.height):
                if self.board[h][w] == 0:
                    self.mouse.click(w, h)
                    return

    def flag_mines(self):
        pass


    def game(self):
        self.mouse.click(0, 0) #focus click
        self.mouse.click(0, 0) #initial click
        
        while True:
            self.mouse.move_away_mouse()
            self.update_board()
            self.flag_mines()
            
            moves = self.calculate_moves()
            print(self.board)
            
            if not moves:
                self.click_unknown_tile()
            else:
                for move in moves:
                    self.click(move[0], move[1])


Strategy()



