import pygame,sys
from pygame.locals import *
import random
import time
from math import log
import subprocess

pygame.init()
DISPLAY = pygame.display.set_mode((1200,650))
pygame.display.set_caption('LazyBand')
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED= (255,0,0)
GREEN = (0, 255,0)
BLUE = (0,0, 255)
AQUA=(0, 255, 255)
FUCHSIA=(255,0, 255)
GRAY=(128, 128, 128)
OLIVE=(128, 128,0)
PURPLE=(128,0, 128)
YELLOW=(255, 255,0)
TEAL=( 0, 128, 128)



INITIAL_X=120
INITIAL_Y=80
ENDING_X = 800
ENDING_Y = 600

SOUND_BOARD_LENGTH = 200
GAP = 50

SOUND_INX = ENDING_X + GAP
SOUND_EX = SOUND_INX + SOUND_BOARD_LENGTH

DISPLAY.fill(BLACK)
GRID_ROW = 5
GRID_COLUMN = 5
SOUND_ROW = 3
SOUND_COLUMN = 2


def draw_grid(row, col, inx, iny, endx, endy):
    x_side = (endx - inx)/(col)
    y_side = (endy - iny)/(row)
    print(x_side, y_side)
    for i in range(col):
        curx = inx + i * x_side
        for j in range(row):
            cury = iny + j * y_side
            print(curx, cury)
            pygame.draw.rect(DISPLAY, WHITE, (curx, cury, x_side, y_side), 2)


def draw_board():
    draw_grid(GRID_ROW, GRID_COLUMN, INITIAL_X, INITIAL_Y, ENDING_X, ENDING_Y)
    draw_grid(SOUND_ROW, SOUND_COLUMN, SOUND_INX, INITIAL_Y, SOUND_EX, ENDING_Y)  


def get_board_position(inx, iny, endx, endy, row, col, mx, my):

    x_side = (endx - inx)/(col)
    y_side = (endy - iny)/(row)
    y = (mx - inx) // x_side
    x = (my - iny) // y_side
    return int(x), int(y)


def get_position(mx, my):
    if INITIAL_X <= mx <= ENDING_X and INITIAL_Y <= my <= ENDING_Y:
        return 1, get_board_position(INITIAL_X, INITIAL_Y, ENDING_X, ENDING_Y,  GRID_ROW, GRID_COLUMN, mx, my)
    elif SOUND_INX <= mx <= SOUND_EX and INITIAL_Y <= my <= ENDING_Y:
        return 2, get_board_position(SOUND_INX, INITIAL_Y, SOUND_EX, ENDING_Y, SOUND_ROW, SOUND_COLUMN, mx, my)
    else:
        return 3, "chud lo"


if __name__ == '__main__':
 
    draw_board()
    #draw_sounds(2)
                
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type==MOUSEBUTTONDOWN:
                mousePos=list(pygame.mouse.get_pos())
                print(mousePos)
                print(get_position(mousePos[0], mousePos[1]))

