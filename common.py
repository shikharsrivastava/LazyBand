import pygame


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

pygame.init()
DISPLAY = pygame.display.set_mode((1360,650))
pygame.display.set_caption('LazyBand')

DISPLAY.fill(BLACK)


# The volumes for grid in fractions (0 - 1)
MIN_VOLUME = 0.2
MAX_VOLUME = 1.0


# The loop durations in seconds
MIN_DURATION = 0.3
MAX_DURATION = 2


# The music board dimensions
GRID_ROW = 8
GRID_COLUMN = 8

# The maximum sounds per cell
LINE_COUNT = 4


INITIAL_X=120
INITIAL_Y=80
ENDING_X = 800
ENDING_Y = 600


SOUND_BOARD_LENGTH = 350
GAP = 50

SOUND_INX = ENDING_X + GAP
SOUND_EX = SOUND_INX + SOUND_BOARD_LENGTH
PLAY_CHANNEL = 101

