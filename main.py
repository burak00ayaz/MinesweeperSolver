import cv2
import pyautogui
import numpy as np


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

    def update_board(self):
        screenshot = get_screenshot()
        ones = template_match(one, screenshot)
        for p in ones:
            self.update_tile(p, 1)
        twos = template_match(two, screenshot)
        for p in twos:
            self.update_tile(p, 2)
        threes = template_match(three, screenshot)
        for p in threes:
            self.update_tile(p, 3)
        fours = template_match(four, screenshot)
        for p in fours:
            self.update_tile(p, 4)
        fives = template_match(five, screenshot)
        for p in fives:
            self.update_tile(p, 5)
            
        for w in range(self.width):
            for h in range(self.height):
                if self.board[w][h] == 0:
                    self.board[w][h] = 8

        remaining = template_match(square, screenshot)
        for p in remaining:
            self.update_tile(p, 0)

    def move_away_mouse(self):
        pyautogui.moveTo(self.tiles[0][0][0] - 50, self.tiles[0][0][1] - 50)

    def game(self):
        self.click(self.tiles[2][2]) #focus click
        self.click(self.tiles[2][2])
        self.move_away_mouse()
        self.update_board()
        print(self.board)

square = cv2.imread('square.png')
one = cv2.imread('one.png')
two = cv2.imread('two.png')
three = cv2.imread('three.png')
four = cv2.imread('four.png')
five = cv2.imread('five.png')
empty = cv2.imread('empty.png')

Game()
print("end")



