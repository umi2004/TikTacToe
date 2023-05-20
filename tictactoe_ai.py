import copy
import random
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
        self.empty_sqrs = self.squares  # list of squares
        self.marked_sqrs = 0  # list of numbers

    def final_state(self):
        """
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        """

        # vertical wins
        for col in range(CS):
            if self.squares[0][col] == self.squares[1][col] == \
                    self.squares[2][col] != 0:
                return self.squares[0][col]  # call for player number

        # horizontal wins
        for row in range(RS):
            if self.squares[row][0] == self.squares[row][1] == \
                    self.squares[row][2] != 0:
                return self.squares[row][0]  # call for player number

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == \
                self.squares[2][2] != 0:
            return self.squares[1][1]  # call for player number

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == \
                self.squares[0][2] != 0:
            return self.squares[1][1]  # call for player number

        return 0  # still there's no win yet

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # Get the current empty squares left in the game
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(RS):
            for col in range(CS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs

    # Check if the marked squares become full
    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


# AI class
class AI:
    def __init__(self, level=1, player=2):  # level 0 is random AI default
        self.level = level
        self.player = player

    def randoms(self, board):
        empty_sqra = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqra))

        return empty_sqra[idx]  # return some (row and col)

    def minimax(self, board, maximizing):
        # Base case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # eval, move

        # player 2 wins (ai)
        if case == 2:
            return -1, None  # eval, move

        # draw
        elif board.isfull():
            return 0, None  # eval, move

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqra = board.get_empty_sqrs()

            for (row, col) in empty_sqra:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqra = board.get_empty_sqrs()

            for (row, col) in empty_sqra:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.randoms(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}"')

        return move  # row and col


# Game Class
class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.show_lines()
        self.player = 1  # player 1 as cross and 2 as circles
        self.gamemode = 'ai'  # game mode as pvp
        self.running = True

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
    ai = game.ai

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

        if game.gamemode == 'ai' and game.player == ai.player:
            pygame.display.update()

            row, col = ai.eval(board)

            board.mark_sqr(row, col, ai.player)
            game.draw_fig(row, col)
            game.next_turn()

        pygame.display.update()  # Update


main()
