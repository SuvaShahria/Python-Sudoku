import pygame
pygame.font.init()
import math
from Sudoku import allowed, find_empty, backtrack


class Grid:
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    set_values = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.boxes = [[Box(self.board[i][j], i, j, width, height,self.set_values) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = None
        self.window = window
        self.new_board = None
        self.update()
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                if self.board[i][j] != 0:
                    self.set_values[i][j] = 1

    def update(self):
        self.new_board = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected

        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set(val)
            self.update()

            if allowed(self.new_board, val, (row, col)):
                return True
            else:
                self.boxes[row][col].set_tmp(0)
                self.boxes[row][col].set(0)
                self.update()
                return False

    def clear(self):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set_tmp(0)
        if self.set_values[row][col] != 1:
            self.boxes[row][col].set(0)
            self.boxes[row][col].set_tmp(0)
            self.update()

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selected = False

        self.boxes[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            size = self.width / 9
            x = math.floor(pos[0] / size)
            y = math.floor(pos[1] / size)
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].value == 0:
                    return False
        return True

    def gray_in(self, val):
        row, col = self.selected
        self.boxes[row][col].set_tmp(val)

    def make_board(self):
        size = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0, 0, 0), (0, i * size), (self.width, i * size), thick)
            pygame.draw.line(self.window, (0, 0, 0), (i * size, 0), (i * size, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].make_box(self.window)


class Box:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height, set_values):
        self.value = value
        self.tmp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.set_values = set_values

    def make_box(self, window):
        font = pygame.font.SysFont("comicsans", 40)

        size = self.width / 9
        x = self.col * size
        y = self.row * size

        if self.tmp != 0 and self.value == 0:
            text = font.render(str(self.tmp), 1, (120, 120, 120))
            window.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (size / 2 - text.get_width() / 2), y + (size / 2 - text.get_height() / 2)))

        if self.selected:
            if self.set_values[self.row][self.col] != 1:
                pygame.draw.rect(window, (250, 0, 0), (x, y, size, size), 3)
            else:
                pygame.draw.rect(window, (0, 250, 0), (x, y, size, size), 3)

    def set(self, val):
        self.value = val

    def set_tmp(self, val):
        self.tmp = val


def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, window)
    key = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.boxes[i][j].tmp != 0:
                        if not board.place(board.boxes[i][j].tmp):
                            print("Invalid")
                        key = None

                        if board.is_finished():
                            print("Solved")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.gray_in(key)

        window.fill((250, 250, 250))
        board.make_board()
        pygame.display.update()

main()
pygame.quit()
