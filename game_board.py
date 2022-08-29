import cv2
import pyautogui
import numpy as np
from random import *
from enum import Enum
import os

class GameBoard:
    def __init__(self):
        os.system('color')
        screenshot = self.get_screenshot()
        tiles = self.template_match(square, screenshot)
        if not tiles:
            print ('Minesweeper screen should be visible..')
            exit(1)
        x_diff = tiles[1][0] - tiles[0][0]
        self.width = int((tiles[-1][0] - tiles[0][0]) / x_diff) + 1
        y_diff = tiles[self.width][1] - tiles[0][1]
        self.height = int((tiles[-1][1] - tiles[0][1]) / y_diff) + 1
        self.tiles = np.reshape(tiles, (self.height, self.width, 2))
        self.board = np.zeros((self.height, self.width), dtype=np.byte)
        self.mouse = GameBoard.MouseController(self)
        print('width: ' + str(self.width))
        print('height: ' + str(self.height))

    def template_match(self, small_image: np.ndarray, large_image: np.ndarray):
        w, h = small_image.shape[:-1]
        result = cv2.matchTemplate(small_image, large_image, cv2.TM_CCOEFF_NORMED)
        threshold = .95
        loc = np.where(result >= threshold)
        results = []
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            results.append((int(pt[0] + w/2), int(pt[1] + h/2)))
            #cv2.rectangle(large_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        #cv2.imshow('res', large_image)
        #cv2.waitKey(0)
        return results

    def get_screenshot(self) -> np.ndarray:
        image = pyautogui.screenshot()
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    class TileType(Enum):
        UNKNOWN = 0
        MINE = -1
        CLEAR = 8
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    class MouseController:
        def __init__(self, outer_instance):
            self.game = outer_instance
            self.tiles = outer_instance.tiles

        def click(self, x: int, y: int):
            point = self.tiles[y][x]
            pyautogui.click(point[0], point[1])

        def right_click(self, x: int, y: int):
            point = self.tiles[y][x]
            pyautogui.click(point[0], point[1], button='right')

        def move_away_mouse(self):
            pyautogui.moveTo(self.tiles[0][0][0] - 50, self.tiles[0][0][1] - 50)

    def print_board(self):
        color_dict = {1: '\033[94m', 2: '\033[92m', 3: '\033[95m', 
                        4: '\033[96m', 5: '\033[93m', 6: '\033[93m', '': '\033[93m',
                        0: '\033[93m', -1: '\033[91m', -2: '\033[0m'}

        for h in range(self.height):
            print('[', end='')
            for w in range(self.width):
                value = self.board[h][w]
                value = '' if value == 8 else value
                print(f'{color_dict[value]}{value:3}{color_dict[-2]}', end='')
            print(']')
        print()

    #starting from top, in clock direction
    def get_surrounding_tiles(self, x, y):
        surr = [(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),
                (x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1)]
        return [p for p in surr if p[0] >= 0 and p[0] < self.width
                and p[1] >= 0 and p[1] < self.height]


    def distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def update_tile(self, coord: (int, int), value: int):
        for h in range(self.height):
            for w in range(self.width):
                if self.distance(self.tiles[h][w], coord) < 5:
                    self.board[h][w] = value
                    return

    def find_figures(self, screenshot, image, value):
        results = self.template_match(image, screenshot)
        for p in results:
            self.update_tile(p, value)
        return results
        

    def update_board(self):
        screenshot = self.get_screenshot()
        if self.template_match(dead, screenshot):
            print("Sorry...")
            exit(0)
        if self.template_match(won, screenshot):
            print("Completed :)")
            exit(0)
        self.find_figures(screenshot, one, 1)
        self.find_figures(screenshot, two, 2)
        self.find_figures(screenshot, three, 3)
        self.find_figures(screenshot, four, 4)
        self.find_figures(screenshot, five, 5)
        self.board[self.board == 0] = 8
        self.find_figures(screenshot, square, 0)

os.chdir('images')
square = cv2.imread('square.png')
one = cv2.imread('one.png')
two = cv2.imread('two.png')
three = cv2.imread('three.png')
four = cv2.imread('four.png')
five = cv2.imread('five.png')
dead = cv2.imread('dead.png')
won = cv2.imread('won.png')
