import cv2
import pyautogui
import numpy as np
from random import *
from enum import Enum
from game_board import GameBoard
import time


class Strategy(GameBoard):
    def __init__(self):
        GameBoard.__init__(self)

    def click_unknown_tile(self):
        for h in range(self.height):
            for w in range(self.width):
                if self.board[h][w] == 0:
                    self.mouse.click(w, h)
                    return

    def flag_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                value = self.board[y][x]
                surr = self.get_surrounding_tiles(x,y)
                unknowns = [p for p in surr if self.board[p[1]][p[0]] == 0] #count unknowns
                mines = [p for p in surr if self.board[p[1]][p[0]] == -1] #count mines
                if len(unknowns) + len(mines) == value:
                    for u in unknowns:
                        self.mouse.right_click(u[0], u[1])
                        self.board[u[1]][u[0]] = -1 #flag mine

    def possible_moves(self):
        moves = []
        for y in range(self.height):
            for x in range(self.width):
                value = self.board[y][x]
                if value == 0 or value == -1 or value == 8:
                    continue
                surr = self.get_surrounding_tiles(x,y)
                mines = [p for p in surr if self.board[p[1]][p[0]] == -1] #count mines
                if len(mines) == value:
                    for p in surr:
                        if self.board[p[1]][p[0]] == 0: #every surrounding unknown is playable
                            moves.append(p)
        return moves


    def game(self):
        self.mouse.click(0, 0) #focus click
        self.mouse.click(0, 0) #initial click
        
        while True:
            self.mouse.move_away_mouse()
            self.update_board()
            self.flag_mines()
            moves = self.possible_moves()

            if not moves:
                #self.click_unknown_tile()
                input('I could not find a move.')
            else:
                for move in set(moves):
                    self.mouse.click(move[0], move[1])


player = Strategy()
player.game()



