import pygame,sys
from pygame.locals import *
import random
import time
import os
from common import *
import utils
from board import *


sound_row = 5
sound_column = 2

    


def draw_grid(row, col, inx, iny, endx, endy, textName=""):
    x_side = (endx - inx)/(col)
    y_side = (endy - iny)/(row)
    #print(x_side, y_side)
    font = pygame.font.SysFont("comicsansms", 15)
    text_cord_x = inx + (endx - inx) // 2
    text_cord_y = iny - 30
    text = font.render(textName, True, WHITE)
    DISPLAY.blit(text, (text_cord_x - text.get_width() // 2, text_cord_y - text.get_height() // 2))

    for i in range(col):
        curx = inx + i * x_side
        for j in range(row):
            cury = iny + j * y_side
            #print(curx, cury)
            pygame.draw.rect(DISPLAY, WHITE, (curx, cury, x_side, y_side), 2)


def draw_board():
    board_text = "Music Box"
    sound_text = "Sounds"
    draw_grid(GRID_ROW, GRID_COLUMN, INITIAL_X, INITIAL_Y, ENDING_X, ENDING_Y, board_text)
    draw_grid(sound_row, sound_column, SOUND_INX, INITIAL_Y, SOUND_EX, ENDING_Y, sound_text)  


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
        return 2, get_board_position(SOUND_INX, INITIAL_Y, SOUND_EX, ENDING_Y, sound_row, sound_column, mx, my)
    else:
        return 3, ("chud lo", 'gaand marao')

def writeTextSound(dirName):
     cat_list = sorted([name for name in os.listdir(dirName)])[:40]
     side_x = (SOUND_EX - SOUND_INX) / sound_column
     side_y = (ENDING_Y - INITIAL_Y) / sound_row
     font = pygame.font.SysFont("comicsansms", int(side_x) // 10)
     for y in range(sound_row):
        for x in range(sound_column):
            centre_cord_y = INITIAL_Y + (y * side_y + side_y / 2)
            centre_cord_x = SOUND_INX + (x * side_x + side_x / 2)
            print(centre_cord_x, centre_cord_y)
            index = y * sound_column + x
            text = font.render(cat_list[index], True, WHITE)
            DISPLAY.blit(text, (centre_cord_x - text.get_width() // 2, centre_cord_y - text.get_height() // 2))







def draw_back():
    global sound_row, sound_column
    cat_list = sorted([name for name in os.listdir('sounds')])
    sound_row = len(cat_list) // 2
    sound_column = 2
    pygame.draw.rect(DISPLAY, BLACK, (SOUND_INX, INITIAL_Y, SOUND_EX - SOUND_INX, ENDING_Y - INITIAL_Y))
    draw_grid(sound_row, sound_column, SOUND_INX, INITIAL_Y, SOUND_EX, ENDING_Y)
    writeTextSound('sounds')


def preview_track(track):
    sound = pygame.mixer.Sound('sounds/'+track)
    pygame.mixer.Channel(PLAY_CHANNEL).play(sound) 



if __name__ == '__main__':
 
    lazyband_board = MusicBoard(GRID_ROW, GRID_COLUMN, MIN_DURATION, MAX_DURATION, MIN_VOLUME, MAX_VOLUME)
    cur_track = None
    cur_cat = None
    cat_list = sorted([name for name in os.listdir('sounds')])
    sound_row = len(cat_list) // 2
    sound_column = 2
    draw_board()
    writeTextSound('sounds')

    # board drawn now

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type==MOUSEBUTTONDOWN:
                mousePos=list(pygame.mouse.get_pos())
                grid_type, (x, y) = get_position(mousePos[0], mousePos[1])
                print("grid type = ", str(grid_type))
                # TODO states
                

                if grid_type == 1:
                    if not cur_track:
                        if len(lazyband_board.board[x][y]) > 0:
                            id = lazyband_board.board[x][y][-1].id
                            lazyband_board.delete(x,y, id)
                        continue

                    print('adding %s to %d, %d'% (cur_track, x, y))
                    lazyband_board.add(os.path.join('sounds', cur_track), x, y)

                    print("CAlling makeline")
                    cur_track = None

                elif grid_type == 2:
                    if not cur_cat: 
                        cat_id = x * sound_column + y
                        cur_cat = cat_list[cat_id]
                        sounds_list = sorted([name for name in os.listdir('sounds/%s' % cur_cat)])[:40]
                        sound_row = len(sounds_list) // 3
                        sound_column = 3
                        pygame.draw.rect(DISPLAY, BLACK, (SOUND_INX, INITIAL_Y, SOUND_EX - SOUND_INX, ENDING_Y - INITIAL_Y))
                        draw_grid(sound_row, sound_column, SOUND_INX, INITIAL_Y, SOUND_EX, ENDING_Y)
                        writeTextSound('sounds/%s' % cur_cat) 
                    else:
                        trackid = x * sound_column + y
                        cur_track = cur_cat + '/' + sounds_list[trackid]
                        preview_track(cur_track)
                        print('selected %s!' % cur_track)

                else:
                    print('whoopsie')
                    cur_track = None
                    cur_cat = None
                    draw_back()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_s]:
                    lazyband_board.saveConfig()
                elif keys[pygame.K_l]:
                    filename = sorted(os.listdir('exports'))[-1]
                    lazyband_board.loadConfig('exports/%s' % filename)
