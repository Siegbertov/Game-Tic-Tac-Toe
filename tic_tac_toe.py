from copy import deepcopy
import numpy as np
import pygame

pygame.init()
pygame.display.set_caption('TIC-TAC-TOE')
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)


def quit_game():
    pygame.quit()
    quit()


class Metadata:
    D_WIDTH = 450
    D_HEIGHT = 450
    C_SIZE = D_WIDTH // 3

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    LIGHT_RED = (200, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (0, 200, 0)

    # =================================================> COMMENT IT IF YOU WANT TO PLAY IN CONSOLE (call console_game)
    X_IMG = pygame.transform.scale(pygame.image.load("CROSS.png"), (C_SIZE, C_SIZE))
    O_IMG = pygame.transform.scale(pygame.image.load("NOUGHT.png"), (C_SIZE, C_SIZE))
    WINDOW = pygame.display.set_mode((D_WIDTH, D_HEIGHT))