import sys
import pygame
import numpy as np

from c import *

# Pygame set up
pygame.init()  # Initialize
scn = pygame.display.set_mode((W, H))  # set the screen size
pygame.display.set_caption('Tic Tac Toe With AI')  # Title
scn.fill(BG_C)  # Background Colour


class Board:
    def __init__(self):
        self.squares = np.zeros((RS, CS))

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0


# Game Class
class Game:
    def __init__(self):
        self.board = Board()
        self.show_lines()
        self.player = 1  # player 1 as cross and 2 as circles

    # Tik Tac Toe 3 by 3 lines
    def show_lines(self):
        # vertical
        pygame.draw.line(scn, LINE_C, (SQ, 0), (SQ, H), LINE_W)
        pygame.draw.line(scn, LINE_C, (W - SQ, 0), (W - SQ, H), LINE_W)

        # horizontal
        pygame.draw.line(scn, LINE_C, (0, SQ), (W, SQ), LINE_W)
        pygame.draw.line(scn, LINE_C, (0, H - SQ), (W, H - SQ), LINE_W)

    def next_turn(self):
        self.player = self.player % 2 + 1  # Use module to switch player 1 & 2

    def draw_fig(self, row, col):
        if self.player == 1:
            # desc line
            st_desc = (col * SQ + OFF_SET, row * SQ + OFF_SET)
            end_desc = (col * SQ + SQ - OFF_SET, row * SQ + SQ - OFF_SET)
            pygame.draw.line(scn, CROSS_C, st_desc, end_desc, CROSS_W)

            # asc line
            st_asc = (col * SQ + OFF_SET, row * SQ + SQ - OFF_SET)
            end_asc = (col * SQ + SQ - OFF_SET, row * SQ + OFF_SET)
            pygame.draw.line(scn, CROSS_C, st_asc, end_asc, CROSS_W)

        elif self.player == 2:
            # Draw circle
            center = (col * SQ + SQ // 2, row * SQ + SQ // 2)
            pygame.draw.circle(scn, CIRC_C, center, RAD, CIRC_W)


# Base Main Format
def main():
    # object
    game = Game()
    board = game.board  # Simplicity

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos  # input as pixel
                row = pos[1] // SQ  # set it as 3 rows
                col = pos[0] // SQ  # set it as 3 columns

                # Marked on board if it already clicked on specific box
                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
                    # print(board.squares)  # Display

        pygame.display.update()  # Update


main()
