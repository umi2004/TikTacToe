import sys
import pygame

from c import *

# Pygame set up
pygame.init()  # Initialize
scn = pygame.display.set_mode((W, H))  # set the screen size
pygame.display.set_caption('Tic Tac Toe With AI')  # Title
scn.fill(BG_C)  # Background Colour


# Base Main Format
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


main()
