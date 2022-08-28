import cv2
import pyautogui
import numpy as np
from random import *


def get_screenshot() -> np.ndarray:
    image = pyautogui.screenshot()
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def template_match(small_image: np.ndarray, large_image: np.ndarray):
    w, h = small_image.shape[:-1]
    result = cv2.matchTemplate(small_image, large_image, cv2.TM_CCOEFF_NORMED)
    threshold = .95
    loc = np.where(result >= threshold)
    results = []
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        results.append((int(pt[0] + w/2), int(pt[1] + h/2)))
        #cv2.rectangle(large_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    #cv2.imshow('res', large_image)
    return results

class Game:
    def __init__(self):
        screenshot = get_screenshot()
        tiles = template_match(square, screenshot)
        if not tiles:
            print ('Minesweeper screen should be visible..')
            exit(1)
        x_diff = tiles[1][0] - tiles[0][0]
        self.width = int((tiles[-1][0] - tiles[0][0]) / x_diff) + 1
        y_diff = tiles[self.width][1] - tiles[0][1]
        self.height = int((tiles[-1][1] - tiles[0][1]) / y_diff) + 1
        self.tiles = np.reshape(tiles, (self.height, self.width, 2))
        # 0: unknown, 1,..6: mine numbers, 8:empty, -1: mine (flagged)
        self.board = np.zeros((self.height, self.width), dtype=np.byte)
        self.game()

    def click(self, point):
        pyautogui.click(point[0], point[1])

    def distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def update_tile(self, coord: (int, int), value: int):
        for w in range(self.width):
            for h in range(self.height):
                if self.distance(self.tiles[w][h], coord) < 5:
                    self.board[w][h] = value
                    return

    def find_figures(self, screenshot, image, value):
        results = template_match(image, screenshot)
        for p in results:
            self.update_tile(p, value)
        return results
        

    def update_board(self):
        screenshot = get_screenshot()
        if self.find_figures(screenshot, dead, 0):
            exit(0)
        self.find_figures(screenshot, one, 1)
        self.find_figures(screenshot, two, 2)
        self.find_figures(screenshot, three, 3)
        self.find_figures(screenshot, four, 4)
        self.find_figures(screenshot, five, 5)           
        for w in range(self.width):
            for h in range(self.height):
                if self.board[w][h] == 0:
                    self.board[w][h] = 8
        self.find_figures(screenshot, square, 0)


    def move_away_mouse(self):
        pyautogui.moveTo(self.tiles[0][0][0] - 50, self.tiles[0][0][1] - 50)

    def calculate_moves(self):
        pass

    def click_unknown_tile(self):
        for w in range(self.width):
            for h in range(self.height):
                if self.board[w][h] == 0:
                    self.click(self.tiles[w][h])
                    return

    def game(self):
        self.click(self.tiles[0][0]) #focus click
        self.click(self.tiles[0][0]) #initial click
        
        while True:
            self.move_away_mouse()
            self.update_board()
            print(self.board)
            moves = self.calculate_moves()
            
            if not moves:
                self.click_unknown_tile()
            else:
                for tile in moves:
                    self.click(tile)

square = cv2.imread('images/square.png')
one = cv2.imread('images/one.png')
two = cv2.imread('images/two.png')
three = cv2.imread('images/three.png')
four = cv2.imread('images/four.png')
five = cv2.imread('images/five.png')
empty = cv2.imread('images/empty.png')
dead = cv2.imread('images/dead.png')

Game()
print("end")



