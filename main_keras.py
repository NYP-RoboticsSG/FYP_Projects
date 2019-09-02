import pygame
import time
import cv2
import numpy as np
import time
import keras
import os
import random
import tensorflow as tf
import time
import pygameMenu
from Music import music
from Sound import sound
from Utils import color as c
from Utils import utils as ut
from Pictures import pictures as pic
from adafruit_crickit import crickit


global cap

global camera_status
matches = 0
init_sound = 0
################################################################
import random
X = '\033[0m'
Bold = '\033[1;36m'
HighB = '\033[1;44m'

winEas = loseEas = tieEas = winInt = loseInt = tieInt = winHard = loseHard = tieHard = winExp = loseExp = tieExp = winspec = losespec = tiespec = 0.0

hiddenfound = False

buildTMatrix = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixL = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixT = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}

n = 3
m = 3
tMatrix = [[0] * m for i in range(n)]
tMatrixL = [[0] * m for i in range(n)]
tMatrixT = [[0] * m for i in range(n)]

probabilitiesRPS = [1/3,1/3,1/3]

buildTMatrixrpsclsp = {'rr': 1, 'rp': 1, 'rsc': 1, 'rl': 1, 'rsp': 1, 'pr': 1, 'pp': 1, 'psc': 1, 'pl': 1, 'psp': 1, 'scr': 1, 'scp': 1, 'scsc': 1, 'scl': 1, 'scsp': 1, 'lr': 1, 'lp': 1, 'lsc': 1, 'll': 1, 'lsp': 1, 'spr': 1, 'spp': 1, 'spsc': 1, 'spl': 1, 'spsp': 1}
buildTMatrixLrpsclsp = {'rr': 1, 'rp': 1, 'rsc': 1, 'rl': 1, 'rsp': 1, 'pr': 1, 'pp': 1, 'psc': 1, 'pl': 1, 'psp': 1, 'scr': 1, 'scp': 1, 'scsc': 1, 'scl': 1, 'scsp': 1, 'lr': 1, 'lp': 1, 'lsc': 1, 'll': 1, 'lsp': 1, 'spr': 1, 'spp': 1, 'spsc': 1, 'spl': 1, 'spsp': 1}
buildTMatrixTrpsclsp = {'rr': 1, 'rp': 1, 'rsc': 1, 'rl': 1, 'rsp': 1, 'pr': 1, 'pp': 1, 'psc': 1, 'pl': 1, 'psp': 1, 'scr': 1, 'scp': 1, 'scsc': 1, 'scl': 1, 'scsp': 1, 'lr': 1, 'lp': 1, 'lsc': 1, 'll': 1, 'lsp': 1, 'spr': 1, 'spp': 1, 'spsc': 1, 'spl': 1, 'spsp': 1}

sheldon = 5
cooper = 5
tMatrixrpsclsp = [[0] * sheldon for i in range(cooper)]
tMatrixLrpsclsp = [[0] * sheldon for i in range(cooper)]
tMatrixTrpsclsp = [[0] * sheldon for i in range(cooper)]

probabilitiesrpsclsp = [1/5,1/5,1/5,1/5,1/5]
################################################################
# Load CNN model for predicting gestures
model = keras.models.load_model('CNN/binary_weight.h5')
#interpreter = tf.lite.Interpreter("CNN/converted_model.tflite")
#interpreter.allocate_tensors()
#input_details = interpreter.get_input_details()
#output_details = interpreter.get_output_details()
#model = converted_model.tflite
################################################################

directory ="/home/nyp/Desktop/images"

################################################################
# Initializing for sound, music and pygame itself
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
################################################################


################################################################
# Setting window size, caption, icon and clock for FPS
display_width = 1200
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Scissor-Paper-Stone')


clock = pygame.time.Clock()


# Checking if camera is plugged in
def check_camera():
    count = 0
    while True:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            gameDisplay.fill(c.black)
            text('Please plug in a camera to play the game', 50, c.white, display_width, display_height, True)
            ut.update_screen(clock)
            count = 1
            ut.quit_x()
        else:
            if count == 1:
                camera_detected()
                break
            else:
                break
    cap.release()
    intro()

def camera_detected():
    start = time.time()
    while time.time() - start < 4:
        gameDisplay.fill(c.black)
        text('Camera detected! You will be directed to the main menu.', 50, c.white, display_width, display_height, True)
        ut.update_screen(clock)
        ut.quit_x()

################################################################
# Text
def text_object(msg, font, color, back_color=None):

    '''create text surface object, where text is drawn on it
    return text surface and rectangle'''

    
    textSurface = font.render(msg, True, color, back_color)
    return textSurface, textSurface.get_rect() #return text surface object and (get)rectangular surface

def text(msg, text_size, color, x, y, center_of_box = False, back_color=None, center_point=False, font_type='freesansbold.ttf'):
    # create font object
    font = pygame.font.Font(font_type, text_size)

    textSurf, textRect = text_object(msg, font, color, back_color) # get text surface object and rectangular area of the surface

    if center_of_box:
        textRect.center = (x // 2, y // 2)
    elif center_point:
        textRect.center = (x, y)
    else:
        textRect = (x, y)

    gameDisplay.blit(textSurf, textRect)  # draw image in this case text

################################################################
# Button
def button_text(msg, text_size, color, font_type, x, y, w, h):
    # create font object
    font = pygame.font.Font(font_type, text_size)

    textSurf, textRect = text_object(msg, font, color) # get text surface object and rectangular area of the surface

    textRect.center = (x + w // 2, y + h // 2) # get the center of the rectangle to be at the designated place

    gameDisplay.blit(textSurf, textRect) # draw image, in this case text

def button(placement, x, y, w, h, default_color, light_up_color, msg, text_size, text_color, previous, action=None, font_type='freesansbold.ttf'):
    global pressed
    global matches

    mouse = pygame.mouse.get_pos()
    #print(mouse)
    click = pygame.mouse.get_pressed()
    #print(click)

    # coordinate of button adjusting
    if placement == 'center':
        x = x - w//2
        y = y - h//2

    elif placement == 'top right':
        x = x - w

    elif placement == 'bottom left':
        y = y - h

    elif placement == 'bottom right':
        x = x - w
        y = y - h


    if x < mouse[0] < x+w and y < mouse[1] < y+h: # if mouse inside button
        pygame.draw.rect(gameDisplay, light_up_color, (x, y, w, h))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if previous == 'game':
                    cap.release()
                if action: # if there is action, do the action
                    if action == 'paused':
                        global resume
                        pygame.mixer.music.set_volume(0.3)
                        sound.pause()
                        pause_menu()
                    else:
                        pygame.mixer.music.set_volume(1.0)
                        if action == 'game_1':
                            if scanned == 1:
                                sound.play()
                                game_screen_1()
                            else:
                                pause_scan_first()
                        elif action == 'game_2':
                            if scanned == 1:
                                sound.play()
                                game_screen_2()
                            else:
                                pause_scan_first()
                        elif action == 'game_3':
                            if scanned == 1:
                                sound.play()
                                game_screen_3()
                            else:
                                pause_scan_first()
                        elif action == 'game_4':
                            if scanned == 1:
                                sound.play()
                                game_screen_4()
                            else:
                                pause_scan_first()
                        elif action == 'intro':
                            sound.select()
                            intro()
                        elif action == 'play':
                            sound.select()
                            chooseMode()
                        elif action == 'quit':
                            ut.quit_game()
                        elif action == 'easy':
                            sound.select()
                            hand_scan_screen_1()   
                        elif action == 'intermediate':
                            sound.select()
                            hand_scan_screen_2()
                        elif action == 'hard':
                            sound.select()
                            hand_scan_screen_3() 
                        elif action == 'expert':
                            sound.select()
                            hand_scan_screen_4() 
                        elif action == 'back':
                            sound.select()
                            intro()                                                   
                        elif action == 'hand_scan':
                            sound.play()
                            pressed = 1
                            return pressed
                        elif action == 'tutt_1':
                            if previous  == 'intro' or previous == 'paused':
                                music.stop()
                                music.instruc()
                                sound.select()
                                tutorial_one()
                            else:
                                sound.select()
                                tutorial_one()
                        elif action == 'tutt_2':
                            sound.select()
                            tutorial_two()
                        elif action == 'tutt_3':
                            sound.select()
                            tutorial_three()
                        elif action == 'tutt_4':
                            sound.select()
                            tutorial_four()
                        elif action == 'tutt_5':
                            sound.select()
                            tutorial_five()
                        elif action == 'tutt_6':
                            sound.select()
                            tutorial_six()
                        elif action == 'tutt_7':
                            sound.select()
                            tutorial_seven()
                        elif action == 'tutt_8':
                            sound.select()
                            tutorial_eight()
                        elif action == 'tutt_9':
                            sound.select()
                            tutorial_nine()
                        elif action == 'tutt_10':
                            sound.select()
                            tutorial_ten()
                        elif action == 'tutt_11':
                            sound.select()
                            tutorial_eleven()
                        elif action == 'tutt_12':
                            sound.select()
                            tutorial_twelve()
                        elif action == 'tutt_13':
                            sound.select()
                            tutorial_thirteen()
                        elif action == 'tutt_14':
                            sound.select()
                            tutorial_fourteen()
                        elif action == 'tutt_15':
                            sound.select()
                            tutorial_fifteen()
                        elif action == 'tutt_16':
                            sound.select()
                            tutorial_sixteen()
                        elif action == 'tutt_17':
                            sound.select()
                            tutorial_seventeen()
                        elif action == 'tutt_18':
                            sound.select()
                            tutorial_eighteen()
                        elif action == 'tutt_19':
                            sound.select()
                            tutorial_nineteen()
                        elif action == 'tutt_20':
                            sound.select()
                            tutorial_twenty()
                        elif action == 'tutt_21':
                            sound.select()
                            tutorial_twentyone()
                        elif action == 'credits_one':
                            if previous  == 'intro':
                                music.stop()
                                music.credits()
                                sound.select()
                                credits_one()
                            else:
                                sound.select()
                                credits_one()
                        elif action == 'credits_two':
                            sound.select()
                            credits_two()
                        elif action == 'credits_three':
                            sound.select()
                            credits_three()


    else:
        pygame.draw.rect(gameDisplay, default_color, (x, y, w, h))

    if msg == '':
        pass
    else:
        button_text(msg, text_size, text_color, font_type, x, y, w, h)

################################################################
def tutorial_one():
    while True:
        gameDisplay.blit(pic.tutorial_1, (1200, 800))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Main Menu', 50, c.black, 'tutt_1', 'intro')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_1', 'tutt_2')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_two():
    while True:
        gameDisplay.blit(pic.tutorial_2, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_2', 'tutt_1')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_2', 'tutt_3')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_three():
    while True:
        gameDisplay.blit(pic.tutorial_3, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_3', 'tutt_2')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_3', 'tutt_4')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_four():
    while True:
        gameDisplay.blit(pic.tutorial_4, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_4', 'tutt_3')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_4', 'tutt_5')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_five():
    while True:
        gameDisplay.blit(pic.tutorial_5, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_5', 'tutt_4')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_5', 'tutt_6')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_six():
    while True:
        gameDisplay.blit(pic.tutorial_6, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_6', 'tutt_5')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_6', 'tutt_7')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_seven():
    while True:
        gameDisplay.blit(pic.tutorial_7, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_7', 'tutt_6')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_7', 'tutt_8')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_eight():
    while True:
        gameDisplay.blit(pic.tutorial_8, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_8', 'tutt_7')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_8', 'tutt_9')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_nine():
    while True:
        gameDisplay.blit(pic.tutorial_9, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_9', 'tutt_8')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_9', 'tutt_10')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_ten():
    while True:
        gameDisplay.blit(pic.tutorial_10, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_10', 'tutt_9')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_10', 'tutt_11')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_eleven():
    while True:
        gameDisplay.blit(pic.tutorial_11, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_11', 'tutt_10')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_11', 'tutt_12')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_twelve():
    while True:
        print(ut.mouse_pos())
        gameDisplay.blit(pic.tutorial_12, (0, 0))
        button('top left', 30, 610, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_12', 'tutt_11')
        button('top right', display_width - 30, 610, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_12', 'tutt_13')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_thirteen():
    while True:
        gameDisplay.blit(pic.tutorial_13, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_13', 'tutt_12')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_13', 'tutt_14')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_fourteen():
    while True:
        gameDisplay.blit(pic.tutorial_14, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_14', 'tutt_13')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_14', 'tutt_15')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_fifteen():
    while True:
        gameDisplay.blit(pic.tutorial_15, (0, 0))
        button('top left', 30, 610, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_15', 'tutt_14')
        button('top right', display_width - 30, 610, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_15', 'tutt_16')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_sixteen():
    while True:
        gameDisplay.blit(pic.tutorial_16, (0, 0))
        button('top left', 30, 610, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_16', 'tutt_15')
        button('top right', display_width - 30, 610, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_16', 'tutt_17')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_seventeen():
    while True:
        gameDisplay.blit(pic.tutorial_17, (0, 0))
        button('top left', 30, 610, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_17', 'tutt_16')
        button('top right', display_width - 30, 610, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_17', 'tutt_18')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_eighteen():
    while True:
        gameDisplay.blit(pic.tutorial_18, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_18', 'tutt_17')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_18', 'tutt_19')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_nineteen():
    while True:
        gameDisplay.blit(pic.tutorial_19, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_19', 'tutt_18')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_19', 'tutt_20')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_twenty():
    while True:
        gameDisplay.blit(pic.tutorial_20, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_20', 'tutt_19')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Next', 50, c.black, 'tutt_20', 'tutt_21')
        ut.update_screen(clock)
        ut.quit_x()
def tutorial_twentyone():
    while True:
        gameDisplay.blit(pic.tutorial_21, (0, 0))
        button('bottom left', 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'tutt_21', 'tutt_20')
        button('bottom right', display_width - 30, display_height - 20, 300, 100, c.red_dim, c.red_lit, 'Main Menu', 50, c.black, 'tutt_21', 'intro')
        ut.update_screen(clock)
        ut.quit_x()
################################################################

def intro():
    music.stop()
    music.intro()
    while True:
        gameDisplay.blit(pic.background, (0, 0))

        text_size = 50
        button_w, button_h = 300, 100

        text('Scissor-Paper-Stone!', 100, c.white, display_width, display_height, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play', text_size, c.black, 'intro', 'play')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'intro', 'tutt_1')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'intro', 'quit')
        button('center', display_width // 4 * 2, display_height // 6 * 5, button_w, button_h, c.light_blue_dim, c.light_blue_lit, 'Credits', text_size, c.black, 'intro', 'credits_one')

        ut.update_screen(clock)
        ut.quit_x()

def chooseMode():
    music.stop()
    music.intro()
    while True:
        gameDisplay.blit(pic.background, (0, 0))

        text_size = 50
        button_w, button_h = 300, 100

        text('Choose your difficulty', 100, c.white, display_width, display_height, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Easy', text_size, c.black, 'chooseMode', 'easy')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Intermediate', text_size, c.black, 'chooseMode', 'intermediate')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.red_dim, c.red_lit, 'Hard', text_size, c.black, 'chooseMode', 'hard')
        button('center', display_width//4 * 2, display_height//6*5, button_w, button_h, c.blue_dim, c.blue_lit, 'Expert', text_size, c.black, 'chooseMode', 'expert')
        button('top right', display_width - 15, 15, 150, 50, c.green_dim, c.green_lit, 'Back', 50, c.black, 'chooseMode', 'back')

        ut.update_screen(clock)
        ut.quit_x()

def credits_one():
    while True:
        gameDisplay.blit(pic.credits_1, (0, 0))
        button('top left', 30, 30, 300, 100, c.red_dim, c.red_lit, 'Main Menu', 50, c.black, 'credits_one', 'intro')
        button('top right', display_width - 30, 30, 300, 100, c.green_dim, c.green_lit, 'Next', 50, c.black, 'credits_one', 'credits_two')
        ut.update_screen(clock)
        ut.quit_x()

def credits_two():
    while True:
        gameDisplay.blit(pic.credits_2, (0, 0))
        button('top left', 30, 30, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'credits_two', 'credits_one')
        button('top right', display_width - 30, 30, 300, 100, c.green_dim, c.green_lit, 'Next', 50, c.black, 'credits_two', 'credits_three')
        ut.update_screen(clock)
        ut.quit_x()

def credits_three():
    while True:
        gameDisplay.blit(pic.credits_3, (0, 0))
        button('top left', 30, 30, 300, 100, c.red_dim, c.red_lit, 'Back', 50, c.black, 'credits_three', 'credits_two')
        button('top right', display_width - 30, 30, 300, 100, c.red_dim, c.red_lit, 'Main Menu', 50, c.black, 'credits_three', 'intro')
        ut.update_screen(clock)
        ut.quit_x()

def SPS_timing(time):
    b_circle1_w, b_circle1_h = display_width // 3, int(display_height * (3 / 16))
    b_circle2_w, b_circle2_h = display_width // 2, int(display_height * (3 / 16))
    b_circle3_w, b_circle3_h = int(display_width * (2 / 3)), int(display_height * (3 / 16))
    s_circle1_w, s_circle1_h = int(display_width * (5 / 12)), int(display_height * (3 / 16))
    s_circle2_w, s_circle2_h = int(display_width * (7 / 12)), int(display_height * (3 / 16))
    #s_circle3_w, s_circle3_h = int(display_width * (9 / 12)), int(display_height * (3 / 16))
    lit = c.orange
    dim = c.pink_red
    ready_time = 2
    detect_now = False
    global init_sound


    if time < ready_time:
        init_sound = 0
        text('Ready?', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, dim, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, dim, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, dim, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, dim, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)

    elif ready_time < time < ready_time + 0.5:
        init_sound +=1
        text('Scissor...', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, dim, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, dim, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, dim, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        gameDisplay.blit(pic.scissors, (650, 160))
        if init_sound == 1:
            sound.timing()

    elif ready_time + 0.5 < time < ready_time + 0.5*2:
        init_sound = 0
        text('Scissor...', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, dim, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, dim, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        gameDisplay.blit(pic.scissors, (650, 160))




    elif ready_time + 0.5*2 < time < ready_time + 0.5*3:
        init_sound +=1
        text('Paper...', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, dim, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, dim, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        gameDisplay.blit(pic.paper, (650, 160))
        if init_sound == 1:
            sound.timing()


    elif ready_time + 0.5*3 < time < ready_time + 0.5*4:
        init_sound = 0
        text('Paper...', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, dim, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, dim, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        gameDisplay.blit(pic.paper, (650, 160))


    elif ready_time + 0.5*4 < time < ready_time + 0.5*5:
        init_sound +=1
        text('Stone!', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, dim, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        gameDisplay.blit(pic.stone, (650, 160))
        if init_sound == 1:
            sound.timing()

    elif ready_time + 0.5*5 < time < ready_time + 0.5*5 + 0.1:
        init_sound =0
        text('Stone!', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, lit, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        gameDisplay.blit(pic.stone, (650, 160))


    elif time > ready_time + 0.5*5 + 0.1:
        text('Stone!', 100, c.black, display_width, display_height // 8, True)
        pygame.draw.circle(gameDisplay, lit, (b_circle1_w, b_circle1_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle1_w, s_circle1_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle2_w, b_circle2_h), 50)
        pygame.draw.circle(gameDisplay, lit, (s_circle2_w, s_circle2_h), 30)
        pygame.draw.circle(gameDisplay, lit, (b_circle3_w, b_circle3_h), 50)
        #pygame.draw.circle(gameDisplay, lit, (s_circle3_w, s_circle3_h), 1)
        text('3', 100, c.black, b_circle1_w, b_circle1_h+5, False, None, True)
        text('2', 100, c.black, b_circle2_w, b_circle2_h + 5, False, None, True)
        text('1', 100, c.black, b_circle3_w, b_circle3_h + 5, False, None, True)
        detect_now = True

    return detect_now


def pause_menu():
    while True:
        text_size = 50
        button_w, button_h = 300, 100
        gameDisplay.blit(pic.background, (0, 0))
        text('Paused', 200, c.black, display_width, display_height//2, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.orange_dim, c.orange_lit, 'Main Menu', text_size, c.black, 'pause', 'intro')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.purple_dim, c.purple_lit, 'Scan', text_size, c.black, 'pause', 'scan_screen')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play', text_size, c.black, 'pause', 'game')
        button('center', display_width //3, display_height //6*5, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'pause', 'tutt_1')
        button('center', display_width//3*2, display_height//6*5, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'pause', 'quit')
        ut.update_screen(clock)
        ut.quit_x()

def pause_scan_first():
    sound.scan_first()
    pygame.mixer.music.set_volume(0.3)
    start = time.time()
    while True:
        text_size = 50
        button_w, button_h = 300, 100
        gameDisplay.blit(pic.background, (0, 0))
        text('Paused', 200, c.black, display_width, display_height//2, True)
        text('Please scan your hand first.', 100, c.white, display_width//2, display_height // 2, False, None, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.orange_dim, c.orange_lit, 'Main Menu', text_size, c.black, 'pause', 'intro')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.purple_dim, c.purple_lit, 'Scan', text_size, c.black, 'pause', 'scan_screen')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play', text_size, c.black, 'pause', 'game')
        button('center', display_width //3, display_height //6*5, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'pause', 'tutt_1')
        button('center', display_width//3*2, display_height//6*5, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'pause', 'quit')
        ut.update_screen(clock)
        ut.quit_x()
        if time.time()-start > 3:
            pause_menu()

def frame_adjust(frame, isit_scan=False):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if isit_scan:
        frame = translucent_obj(frame, draw_rect_right, 1.0)
    else:
        cv2.rectangle(frame, (10, 355), (213, 125), (0, 255, 0), 5)

    frame = np.rot90(frame)

    x_pos = (display_width // 2 - display_width // 24 - frame.shape[0])//2

    y_pos = display_height//4 + (display_height - display_height//4 - display_height//9*2 - frame.shape[1])//2


    frame = pygame.surfarray.make_surface(frame)

    gameDisplay.blit(frame, (x_pos, y_pos))

def hand_scan_screen_1():

    global hand_hist
    global cap
    hand_hist = None
    global scanned
    scanned = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        init_game_screen()
        frame_adjust(frame, True)

    

        text('Place your hand on the boxes and press "Scan".', 50, c.black, display_width, display_height//4, True)

        hand_x = display_width // 2 + display_width // 24 + (display_width - (display_width // 2 + display_width // 24 + 288))//2

        gameDisplay.blit(pic.hand, (hand_x, display_height//4))

        pressed = button('center', display_width//2, display_height-100, 300, 100, c.red_dim, c.red_lit, 'Scan', 50, c.black, 'scan_screen', 'hand_scan')

        if pressed == 1:
            hand_hist = hand_scan(frame)
            cap.release()
            scanned = 1
            game_screen_1()

        ut.update_screen(clock)

        ut.quit_x()
    cap.release()

def hand_scan_screen_2():

    global hand_hist
    global cap
    hand_hist = None
    global scanned
    scanned = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        init_game_screen()
        frame_adjust(frame, True)

    

        text('Place your hand on the boxes and press "Scan".', 50, c.black, display_width, display_height//4, True)

        hand_x = display_width // 2 + display_width // 24 + (display_width - (display_width // 2 + display_width // 24 + 288))//2

        gameDisplay.blit(pic.hand, (hand_x, display_height//4))

        pressed = button('center', display_width//2, display_height-100, 300, 100, c.red_dim, c.red_lit, 'Scan', 50, c.black, 'scan_screen', 'hand_scan')

        if pressed == 1:
            hand_hist = hand_scan(frame)
            cap.release()
            scanned = 1
            game_screen_2()

        ut.update_screen(clock)

        ut.quit_x()
    cap.release()

def hand_scan_screen_3():

    global hand_hist
    global cap
    hand_hist = None
    global scanned
    scanned = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        init_game_screen()
        frame_adjust(frame, True)

    

        text('Place your hand on the boxes and press "Scan".', 50, c.black, display_width, display_height//4, True)

        hand_x = display_width // 2 + display_width // 24 + (display_width - (display_width // 2 + display_width // 24 + 288))//2

        gameDisplay.blit(pic.hand, (hand_x, display_height//4))

        pressed = button('center', display_width//2, display_height-100, 300, 100, c.red_dim, c.red_lit, 'Scan', 50, c.black, 'scan_screen', 'hand_scan')

        if pressed == 1:
            hand_hist = hand_scan(frame)
            cap.release()
            scanned = 1
            game_screen_3()

        ut.update_screen(clock)

        ut.quit_x()
    cap.release()

def hand_scan_screen_4():

    global hand_hist
    global cap
    hand_hist = None
    global scanned
    scanned = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        init_game_screen()
        frame_adjust(frame, True)

    

        text('Place your hand on the boxes and press "Scan".', 50, c.black, display_width, display_height//4, True)

        hand_x = display_width // 2 + display_width // 24 + (display_width - (display_width // 2 + display_width // 24 + 288))//2

        gameDisplay.blit(pic.hand, (hand_x, display_height//4))

        pressed = button('center', display_width//2, display_height-100, 300, 100, c.red_dim, c.red_lit, 'Scan', 50, c.black, 'scan_screen', 'hand_scan')

        if pressed == 1:
            hand_hist = hand_scan(frame)
            cap.release()
            scanned = 1
            game_screen_4()

        ut.update_screen(clock)

        ut.quit_x()
    cap.release()


def draw_rect_right(frame, return_list_only=False, color=(200, 0, 255), thickness=2):
    '''Draw rectangles'''
    y, x, channel = frame.shape
    num_box = 12
    start_rect = []
    start = [x * 0.10, y * 0.35]
    end = [x * 0.23, y * 0.65]

    spacing = [((end[0] - start[0]) - (3 * 10)) // 2, ((end[1] - start[1]) - (4 * 10)) // 3]

    count_x = 0
    count_y = 0

    for i in range(1, num_box + 1):
        start_rect.append([int(start[0] + count_x * (10 + spacing[0])), int(start[1] + count_y * (10 + spacing[1]))])
        count_x = count_x + 1
        if i % 3 == 0:
            count_x = 0
            count_y = count_y + 1

    start_rect = np.array(start_rect)
    end_rect = start_rect + 10
    cv2.imwrite("image.jpg", frame)
    if not return_list_only:
        for i in range(0, num_box):
            frame = cv2.rectangle(frame, (start_rect[i][0], start_rect[i][1]), (end_rect[i][0], end_rect[i][1]), color,
                                  thickness)
   
        return frame, start_rect, end_rect
    else:
        return start_rect, end_rect

def translucent_obj(frame, action=None, alpha=0.5):
    '''Put a translucent object in the frame'''
    img = frame.copy()
    action(img)
    frame = cv2.addWeighted(img, alpha, frame, 1 - alpha, 0)
    return frame


def set_hand_hist(frame, start_rect, end_rect):
    '''Get hand histogram from the rectangles(more like squares though)'''
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([120, 10, 3], dtype=hsv.dtype)

    size = int(start_rect.size / 2)

    for i in range(size):
        roi[i * 10:i * 10 + 10, 0:10] = hsv[start_rect[i][1]:end_rect[i][1], start_rect[i][0]:end_rect[i][0]]
        # (H,S,V)
        # max(180, 255, 255)

    #         Just for checking
    #         if i == 0:
    #             print(roi)
    #             print('end')
    #             print(hsv[start_rect[i][1]:end_rect[i][1], start_rect[i][0]:end_rect[i][0]])

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)
    return hand_hist

def hand_scan(frame):
    start_rect, end_rect = draw_rect_right(frame, True)
    hand_hist = set_hand_hist(frame, start_rect, end_rect)
    return hand_hist

def crop_binary(frame):
    crop = frame[125:355, 10:213]  # y, x
    thresh = hist_mask(crop, hand_hist)
    clear = clearer(thresh, 5, 1)
    return clear


def hist_mask(frame, hand_hist):
    '''Return binary image of the skin'''
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hand_hist, [0, 181, 0, 256], 1)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    cv2.filter2D(dst, -1, disc, dst)
    ret, thresh1 = cv2.threshold(dst, 0, 255, 0)

    return thresh1

def clearer(frame, kernel_size=5, iteration=1):
    '''cover the holes in the image'''
    kernel = np.ones((kernel_size,kernel_size),np.uint8)
    frame = cv2.erode(frame,kernel,iterations = iteration)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    return frame

def nonzero_ratio(clear):
    h_clear = cv2.resize(clear, (100, 100))
    nonzero = cv2.countNonZero(h_clear)
    nonzero_ratio = (nonzero / (100 * 100)) * 100
    return nonzero_ratio, h_clear

def predict(h_clear):
    np_clear = h_clear.reshape(-1, 100, 100, 1)
    np_clear = np.array(np_clear)
    np_clear = np_clear / 255
    prediction = model.predict([np_clear])
    predictions = np.where(prediction == np.amax(prediction))
    # gesture = ''
    if predictions[1] == 0 and (prediction[0][0] >= 0.9):
        gesture = 'Stone'

    elif predictions[1] == 1 and (prediction[0][1] >= 0.9):
        gesture = 'Paper'

    elif predictions[1] == 2 and (prediction[0][2] >= 0.9):
        gesture = 'Scissor'
    else:
        gesture = '???'
    return gesture

def detect(frame, detect_now):
    if not detect_now:
        pass
    else:
        clear = crop_binary(frame)

        white_ratio, h_clear = nonzero_ratio(clear)

        if white_ratio > 14:
            gesture = predict(h_clear)
        else:
            gesture = 'Nothing'
        return gesture

def display_gesture(gesture, rand_gesture, frame):
    start = time.time()
    result_me_int = int(0)
    result_com_int = int(0)
    result_me, result_com = win_lose(gesture, rand_gesture)
    if result_me == 'You Win!':
        sound.win()
    elif result_me == 'Draw':
        sound.draw()
    elif result_me == 'You Lose':
        sound.lose()
    while True:
        init_game_screen()
        frame_adjust(frame)
        text(gesture, 100, c.black, 50, 650)
        text(rand_gesture, 100, c.black, 650, 650)
        #print (rand_gesture)   
        if rand_gesture == 'Scissor':
            gameDisplay.blit(pic.scissors, (650, 160))
        elif rand_gesture == 'Paper':
            gameDisplay.blit(pic.paper, (650, 160))
        elif rand_gesture == 'Stone':
            gameDisplay.blit(pic.stone, (650, 160))
        # result_me, result_com = win_lose(gesture, rand_gesture)
	# Place where results are printed
	#text('Tsk. You Win.', 165, c.black, display_width//2, display_height//4, False, c.grey_green, True)
        text(result_me, 171  , c.white, 600, 390, False, c.black, True)
        #text(result_com, 171, c.black, 1100, 30)
        text('You', 50, c.red_dim, 458, 661, False, c.white)
        text('Com', 50, c.blue_dim, display_width - 179, 661, False, c.white)

        if result_me == 'You Win!':
            result_me_int = int(1)

        elif result_me == 'Draw':
            result_me_int = int(1)

        elif result_me == 'You Lose':
            result_me_int = int(0)


        if result_com == 'Win':
            result_com_int = int(1)
        elif result_com == 'Draw':
            result_com_int = int(1)
        elif result_com == 'Lose':
            result_com_int = int(0)


        # print(mouse_pos())
        button('top right', display_width, 0, 50, 50, c.red_dim, c.red_lit, '', '', '', 'game', 'paused')
        pygame.draw.rect(gameDisplay, c.black, (display_width - 40, 10, 10, 30))
        pygame.draw.rect(gameDisplay, c.black, (display_width - 20, 10, 10, 30))
        ut.update_screen(clock)
        ut.quit_x()

        crickit.drive_1.frequency = 5000
        crickit.drive_2.frequency = 5000
        crickit.drive_3.frequency = 5000

        if rand_gesture == 'Scissor':
            crickit.drive_1.fraction = 0.0  # all the way off
            crickit.drive_2.fraction = 1.0  # all the way on  
            crickit.drive_3.fraction = 0.0  # all the way off
        elif rand_gesture == 'Paper':
            crickit.drive_1.fraction = 1.0  # all the way on
            crickit.drive_2.fraction = 1.0  # all the way on  
            crickit.drive_3.fraction = 1.0  # all the way on
        elif rand_gesture == 'Stone':
            crickit.drive_1.fraction = 0.0  # all the way off
            crickit.drive_2.fraction = 0.0  # all the way off   
            crickit.drive_3.fraction = 0.0  # all the way off

        if time.time() - start > 3:
            crickit.drive_1.fraction = 0.0  # all the way off
            crickit.drive_2.fraction = 0.0  # all the way off  
            crickit.drive_3.fraction = 0.0  # all the way off               
            break
    return result_me_int, result_com_int

def win_lose(gesture, rand_gesture):
    result_me = ''
    result_com = ''
    if gesture == rand_gesture:
        result_me = result_com = 'Draw'
    elif gesture == 'Scissor' and rand_gesture == 'Paper':
        result_me = 'You Win!'
        result_com = 'Lose'

    elif gesture == 'Stone' and rand_gesture == 'Paper':
        result_me = 'You Lose'
        result_com = 'Win'

    elif gesture == 'Paper' and rand_gesture == 'Scissor':
        result_me = 'You Lose'
        result_com = 'Win'

    elif gesture == 'Stone' and rand_gesture == 'Scissor':
        result_me = 'You Win!'
        result_com = 'Lose'

    elif gesture == 'Paper' and rand_gesture == 'Stone':
        result_me = 'You Win!'
        result_com = 'Lose'

    elif gesture == 'Scissor' and rand_gesture == 'Stone':
        result_me = 'You Lose'
        result_com = 'Win'
    elif gesture == 'Nothing':
        result_me = 'You Lose'
        result_com = 'Win'
    elif gesture == '???':
        result_me = 'You Lose'
        result_com = 'Win'

    return result_me, result_com

def init_game_screen():
    gameDisplay.fill(c.yellow_green)

    # vertical border
    #pygame.draw.rect(gameDisplay, c.grey_green, (display_width // 2 - display_width // 24, 0, display_width // 12, display_height))

    # creating space to write scissors, paper, stone
    pygame.draw.rect(gameDisplay, c.light_green_blue, (0, 0, display_width, display_height // 4))

    button('top right', display_width, 0, 50, 50, c.red_dim, c.red_lit, '', '', '', 'game', 'paused')
    pygame.draw.rect(gameDisplay, c.black, (display_width - 40, 10, 10, 30))
    pygame.draw.rect(gameDisplay, c.black, (display_width - 20, 10, 10, 30))

    # score
    pygame.draw.rect(gameDisplay, c.grey_yellow, (0, display_height // 9 * 7, display_width, display_height // 4))

def random_gesture():
    gesture_int = random.randint(0, 2)
    if gesture_int == 0:
        gesture = 'Scissor'
    if gesture_int == 1:
        gesture = 'Paper'
    if gesture_int == 2:
        gesture = 'Stone'
    return gesture  
          

def intermediate_gesture(gest_ture):
    gesture = ["Stone", "Paper", "Scissors"]
    continuePlaying = True
    prevGesture = ""
    reroll = ""
    #result = ""
    #alt = 0
    #numoff = 0
    choice = 3
    #cap = cv2.VideoCapture(0)
    start = time.time()
    #score_me = int(0)
    #score_com = int(0)

    #while True:   
    if gest_ture == 'Stone':
        gesture_integer = 0
    elif gest_ture == 'Paper':
        gesture_integer = 1
    elif gest_ture == 'Scissor':
        gesture_integer = 2
    elif gest_ture == 'Nothing':
        gesture_integer = 2
    elif gest_ture == '???' :
       gesture_integer = 2


    machine_int = random.randint(0, 2)
    if machine_int == 0:
        machine_gesture = 'Stone'
    elif machine_int == 1:
        machine_gesture = 'Paper'
    elif machine_int == 2:
        machine_gesture = 'Scissor'

    #print(gest_ture, machine_gesture)
    if gest_ture == machine_gesture:
        result = 'Draw'
    elif gest_ture == 'Scissor' and machine_gesture == 'Paper':
        result = 'You Win!'
    elif gest_ture == 'Stone' and machine_gesture == 'Paper':
        result= 'You Lose'
    elif gest_ture == 'Paper' and machine_gesture == 'Scissor':
        result = 'You Lose'
    elif gest_ture == 'Stone' and machine_gesture == 'Scissor':
        result ='You Win!'
    elif gest_ture == 'Paper' and machine_gesture == 'Stone':
        result = 'You Win!'
    elif gest_ture == 'Scissor' and machine_gesture == 'Stone':
        result = 'You Lose'
    elif gest_ture == 'Nothing':
        result = 'You Lose'
    elif gest_ture == '???':
        result = 'You Lose'

    #print(result)
    if result == "You Win!":
        reroll = random.randint(0, 1)
        if reroll == 0:
            machine_int = random.randint(0, 2)
        elif reroll == 1:
            machine_int == machine_int
    elif (result == "Draw"):
        if reroll == 0:
            machine_int = random.randint(0, 2)
        elif reroll == 1:
            machine_int == machine_int
    elif (result == "You Lose"):
        machine_int == machine_int

    #print(reroll)
    #print(machine_gesture)
    if machine_int == 0:
        machine_gesture = 'Stone'
    elif machine_int == 1:
        machine_gesture = 'Paper'
    elif machine_int == 2:
        machine_gesture = 'Scissor'


    '''#print(machine_integer)
    prevGesture = gesture_integer
    print(prevGesture)
    return streak
    machine_int = prevGesture - 2
    if (machine_int < 0):
        machine_int += 3
        if (result == "You Win!"):
            streak += 1
        elif (result == "You Lose"):
            streak == streak
        elif (result == "Draw"):
            streak == streak'''

    return machine_gesture
    

def hard_gesture(gest_ture):
    global probabilitiesRPS
    choices = ["Rock","Paper","Scissors"]
    choi = ['r','p','s']
    continuePlaying = True
    prevGesture = ""
    result = ""
    choice = 3
    probRock = 0
    probPaper = 0
    probScissors = 0



    machineChoice = random.randint(0, 2)
    #result = checkWin(choice,machineChoice,3)
    if gest_ture == machineChoice:
        result = 'Draw'
    elif gest_ture == 'Scissor' and machineChoice == 'Paper':
        result = 'You Win!'
    elif gest_ture == 'Stone' and machineChoice == 'Paper':
        result= 'You Lose'
    elif gest_ture == 'Paper' and machineChoice == 'Scissor':
        result = 'You Lose'
    elif gest_ture == 'Stone' and machineChoice == 'Scissor':
        result ='You Win!'
    elif gest_ture == 'Paper' and machineChoice == 'Stone':
        result = 'You Win!'
    elif gest_ture == 'Scissor' and machineChoice == 'Stone':
        result = 'You Lose'
    elif gest_ture == 'Nothing':
        result = 'You Lose'
    elif gest_ture == '???':
        result = 'You Lose'
  
    if gest_ture == 'Stone':
        gesture_integer = 0
    elif gest_ture == 'Paper':
        gesture_integer = 1
    elif gest_ture == 'Scissor':
        gesture_integer = 2
    elif gest_ture == 'Nothing':
        gesture_integer = 2
    elif gest_ture == '???' :
        gesture_integer = 2

    prevGesture = gesture_integer

    transMatrix = buildTransitionProbabilities(prevGesture,gesture_integer,result)
    machineChoice = random.randint(1, 100)
    probabilitiesRPS[0] = transMatrix[prevGesture][0]
    probabilitiesRPS[1] = transMatrix[prevGesture][1]
    probabilitiesRPS[2] = transMatrix[prevGesture][2]
    rangeR = probabilitiesRPS[0] * 100
    rangeP = probabilitiesRPS[1] * 100 + rangeR
    if (machineChoice <= rangeR):
        machineChoice = 1
    elif (machineChoice <= rangeP):
        machineChoice = 2
    else:
        machineChoice = 0

    if machineChoice == 0:
        machinechoice = 'Stone'
    elif machineChoice == 1:
        machinechoice = 'Paper'
    elif machineChoice == 2:
        machinechoice = 'Scissor'

    print("Your winning transition matrix is:\nr: %s\np: %s\ns: %s\n" % (tMatrix[0],tMatrix[1],tMatrix[2]))
    print("Your losing transition matrix is:\nr: %s\np: %s\ns: %s\n" % (tMatrixL[0],tMatrixL[1],tMatrixL[2]))
    print("Your tying transition matrix is:\nr: %s\np: %s\ns: %s\n" % (tMatrixT[0],tMatrixT[1],tMatrixT[2]))

    return machinechoice



def buildTransitionProbabilities(pC,c,winloss):
    global buildTMatrix
    global buildTMatrixL
    global buildTMatrixT
    choi = ['r','p','s']

    if winloss == "Win!":
        for i, x in buildTMatrix.items():
            if ('%s%s' % (choi[pC],choi[c]) == i):
                buildTMatrix['%s%s' % (choi[pC], choi[c])] += 1
    elif winloss == "Draw":
        for i, x in buildTMatrixT.items():
            if ('%s%s' % (choi[pC],choi[c]) == i):
                buildTMatrixT['%s%s' % (choi[pC], choi[c])] += 1
    else:
        for i, x in buildTMatrixL.items():
            if ('%s%s' % (choi[pC],choi[c]) == i):
                buildTMatrixL['%s%s' % (choi[pC], choi[c])] += 1

    return buildTransitionMatrix(winloss)

def buildTransitionMatrix(winlosstwo):
    global tMatrix
    global tMatrixL
    global tMatrixT

    if winlosstwo == "Win!":
        rock = buildTMatrix['rr'] + buildTMatrix['rs'] +buildTMatrix['rp']              #number of gesture that appeared
        paper = buildTMatrix['pr'] + buildTMatrix['ps'] +buildTMatrix['pp']
        scissors = buildTMatrix['sr'] + buildTMatrix['ss'] +buildTMatrix['sp']
        choi = ['r','p','s']
        for row_index, row in enumerate(tMatrix):
            for col_index, item in enumerate(row):
                a = int(buildTMatrix['%s%s' % (choi[row_index],choi[col_index])])
                if (row_index == 0):
                    c = a/rock
                elif (row_index == 1):
                    c = a/paper
                else:
                    c = a/scissors
                row[col_index] = float(c)
        return (tMatrix)
    elif winlosstwo == "Draw":
        rock = buildTMatrixT['rr'] + buildTMatrixT['rs'] +buildTMatrixT['rp']
        paper = buildTMatrixT['pr'] + buildTMatrixT['ps'] +buildTMatrixT['pp']
        scissors = buildTMatrixT['sr'] + buildTMatrixT['ss'] +buildTMatrixT['sp']
        choi = ['r','p','s']
        for row_index, row in enumerate(tMatrixT):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixT['%s%s' % (choi[row_index],choi[col_index])])
                if (row_index == 0):
                    c = a/rock
                elif (row_index == 1):
                    c = a/paper
                else:
                    c = a/scissors
                row[col_index] = float(c)
        return (tMatrixT)
  
    else:
        rock = buildTMatrixL['rr'] + buildTMatrixL['rs'] +buildTMatrixL['rp']
        paper = buildTMatrixL['pr'] + buildTMatrixL['ps'] +buildTMatrixL['pp']
        scissors = buildTMatrixL['sr'] + buildTMatrixL['ss'] +buildTMatrixL['sp']
        choi = ['r','p','s']
        for row_index, row in enumerate(tMatrixL):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixL['%s%s' % (choi[row_index],choi[col_index])])
                if (row_index == 0):
                    c = a/rock
                elif (row_index == 1):
                    c = a/paper
                else:
                    c = a/scissors
                row[col_index] = float(c)
        return (tMatrixL)


def expert_gesture(gest_ture):

    if gest_ture == 'Stone':
        machinechoice = 'Paper'
    elif gest_ture == 'Paper':
        machinechoice = 'Scissor'
    elif gest_ture == 'Scissor':
        machinechoice = 'Stone'
    elif gest_ture == 'Nothing':
        machinechoice = random.randint(0, 2)
        if machinechoice == 0:
            machinechoice = 'Scissor'
        if machinechoice == 1:
            machinechoice = 'Paper'
        if machinechoice == 2:
            machinechoice = 'Stone'
    elif gest_ture == '???' :
        machinechoice = random.randint(0, 2)
        if machinechoice == 0:
            machinechoice = 'Scissor'
        if machinechoice == 1:
            machinechoice = 'Paper'
        if machinechoice == 2:
            machinechoice = 'Stone'

    return machinechoice

def game_screen_1():
    music.stop()
    music.game()
    global cap
    global detect_now
    global matches
    global action
    global rand_gesture
    cap = cv2.VideoCapture(0)
    start = time.time()
    score_me = int(0)
    score_com = int(0)

    while cap.isOpened():
        # frame to display
        ret, frame = cap.read()

        mouse = pygame.mouse.get_pos()
        #print(mouse)

        init_game_screen()
        frame_adjust(frame)

        #text('You', 80, c.red_dim, 558, 661, False, c.white)
        #text('Com', 80, c.blue_dim, display_width-179, 661, False, c.white)

        passed = time.time()

        detect_now = SPS_timing(passed-start)

        gesture = detect(frame, detect_now)
        if detect_now:
            rand_gesture = random_gesture()
            win_lose_me, win_lose_com = display_gesture(gesture, rand_gesture, frame)
            score_me = int(score_me) + int(win_lose_me)
            score_com = int(score_com) + int(win_lose_com)
            matches += 1
            start = time.time()
            detect_now = False

        if matches == 5:
            cap.release()
            matches = 0
            result_screen_1(score_me, score_com)
        #print(ut.mouse_pos())
        ut.update_screen(clock)

        clear = crop_binary(frame)

        timestr = time.strftime("%H%M%S")
        #cv2.imwrite('/home/nyp/Desktop/pictures/pictures_{0}_{1}.jpg'.format(gesture, timestr), clear)
        #save binary image to folder
        #print(gesture)
        #time.sleep(3)
                                                                            
        ut.quit_x()                               

    cap.release()


def game_screen_2():
    music.stop()
    music.game()
    global cap
    global detect_now
    global matches
    global action
    global rand_gesture
    cap = cv2.VideoCapture(0)
    start = time.time()
    score_me = int(0)
    score_com = int(0)

    while cap.isOpened():
        # frame to display
        ret, frame = cap.read()

        mouse = pygame.mouse.get_pos()
        #print(mouse)

        init_game_screen()
        frame_adjust(frame)

        #text('You', 80, c.red_dim, 558, 661, False, c.white)
        #text('Com', 80, c.blue_dim, display_width-179, 661, False, c.white)

        passed = time.time()

        detect_now = SPS_timing(passed-start)

        gesture = detect(frame, detect_now)
        if detect_now:
            '''if score_me == 0  or score_com == 0:
                rand_gesture = intermediate_gesture(gesture)
            else:
                if (score_me < 0):
                    rand_gesture = random_gesture()
                elif (score_me > 0):'''
            rand_gesture= intermediate_gesture(gesture)
            win_lose_me, win_lose_com = display_gesture(gesture, rand_gesture, frame)
            score_me = int(score_me) + int(win_lose_me)
            score_com = int(score_com) + int(win_lose_com)
            matches += 1
            start = time.time()
            detect_now = False

        if matches == 5:
            cap.release()
            matches = 0
            result_screen_2(score_me, score_com)
        #print(ut.mouse_pos())
        ut.update_screen(clock)

        clear = crop_binary(frame)

        timestr = time.strftime("%H%M%S")
        #cv2.imwrite('/home/nyp/Desktop/pictures/pictures_{0}_{1}.jpg'.format(gesture, timestr), clear)
        #print(gesture)
        #time.sleep(3)
                                                                            
        ut.quit_x()                               

    cap.release()

def game_screen_3():
    music.stop()
    music.game()
    global cap
    global detect_now
    global matches
    global action
    global rand_gesture
    cap = cv2.VideoCapture(0)
    start = time.time()
    score_me = int(0)
    score_com = int(0)

    while cap.isOpened():
        # frame to display
        ret, frame = cap.read()

        mouse = pygame.mouse.get_pos()
        #print(mouse)

        init_game_screen()
        frame_adjust(frame)

        #text('You', 80, c.red_dim, 558, 661, False, c.white)
        #text('Com', 80, c.blue_dim, display_width-179, 661, False, c.white)

        passed = time.time()

        detect_now = SPS_timing(passed-start)

        gesture = detect(frame, detect_now)
        if detect_now:
            rand_gesture = hard_gesture(gesture)
            win_lose_me, win_lose_com = display_gesture(gesture, rand_gesture, frame)
            score_me = int(score_me) + int(win_lose_me)
            score_com = int(score_com) + int(win_lose_com)
            matches += 1
            start = time.time()
            detect_now = False

        if matches == 5:
            cap.release()
            matches = 0
            result_screen_3(score_me, score_com)
        #print(ut.mouse_pos())
        ut.update_screen(clock)

        clear = crop_binary(frame)

        timestr = time.strftime("%H%M%S")
        #cv2.imwrite('/home/nyp/Desktop/pictures/pictures_{0}_{1}.jpg'.format(gesture, timestr), clear)
        #print(gesture)
        #time.sleep(3)
                                                                            
        ut.quit_x()                               

    cap.release()


def game_screen_4():
    music.stop()
    music.game()
    global cap
    global detect_now
    global matches
    global action
    global rand_gesture
    cap = cv2.VideoCapture(0)
    start = time.time()
    score_me = int(0)
    score_com = int(0)

    while cap.isOpened():
        # frame to display
        ret, frame = cap.read()

        mouse = pygame.mouse.get_pos()
        #print(mouse)

        init_game_screen()
        frame_adjust(frame)

        #text('You', 80, c.red_dim, 558, 661, False, c.white)
        #text('Com', 80, c.blue_dim, display_width-179, 661, False, c.white)

        passed = time.time()

        detect_now = SPS_timing(passed-start)

        gesture = detect(frame, detect_now)
        if detect_now:
            rand_gesture = expert_gesture(gesture)
            win_lose_me, win_lose_com = display_gesture(gesture, rand_gesture, frame)
            score_me = int(score_me) + int(win_lose_me)
            score_com = int(score_com) + int(win_lose_com)
            matches += 1
            start = time.time()
            detect_now = False

        if matches == 5:
            cap.release()
            matches = 0
            result_screen_4(score_me, score_com)
        #print(ut.mouse_pos())
        ut.update_screen(clock)

        clear = crop_binary(frame)

        timestr = time.strftime("%H%M%S")
        #cv2.imwrite('/home/nyp/Desktop/pictures/pictures_{0}_{1}.jpg'.format(gesture, timestr), clear)
        #print(gesture)
        #time.sleep(3)
                                                                            
        ut.quit_x()                               

    cap.release()


def result_screen_1(score_me, score_com):
    text_size = 50
    button_w, button_h = 300, 100
    if score_me == score_com:
        music.stop()
        music.draw()
    elif score_me > score_com:
        music.stop()
        music.win()
    elif score_com > score_me:
        music.stop()
        music.lose()
    while True:
        #print(mouse_pos())
        gameDisplay.blit(pic.background, (0,0))
        if score_me == score_com:

            text('Draw? No fun here.', 120, c.black, display_width//2, display_height//10, False, c.grey_yellow, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_me > score_com:

            text('Tsk. You Win.', 120, c.black, display_width//2, display_height//10, False, c.grey_green, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_com > score_me:
            text('Ha-Hah! You Lose!', 120, c.black, display_width//2, display_height//10, False, c.pink_red, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.orange_dim, c.orange_lit, 'Main Menu', text_size, c.black, 'result', 'intro')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.purple_dim, c.purple_lit, 'Choose Mode', text_size, c.black, 'result', 'play')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play again', text_size, c.black, 'result', 'game_1')
        #button('center', display_width //3, display_height //6*5, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'result', 'tutt_1')
        button('center', display_width//4 * 2, display_height//6*5, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'result', 'quit')
        text('If lighting have changed or the next player is a different person,', 30, c.black, display_width//2, display_height-75, False, c.white, True)
        text("please select 'Scan again' if you want to play again.", 30, c.black, display_width//2, display_height-45, False, c.white, True)
        ut.update_screen(clock)
        ut.quit_x()

def result_screen_2(score_me, score_com):
    text_size = 50
    button_w, button_h = 300, 100
    if score_me == score_com:
        music.stop()
        music.draw()
    elif score_me > score_com:
        music.stop()
        music.win()
    elif score_com > score_me:
        music.stop()
        music.lose()
    while True:
        #print(mouse_pos())
        gameDisplay.blit(pic.background, (0,0))
        if score_me == score_com:

            text('Draw? No fun here.', 120, c.black, display_width//2, display_height//10, False, c.grey_yellow, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_me > score_com:

            text('Tsk. You Win.', 120, c.black, display_width//2, display_height//10, False, c.grey_green, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_com > score_me:
            text('Ha-Hah! You Lose!', 120, c.black, display_width//2, display_height//10, False, c.pink_red, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.orange_dim, c.orange_lit, 'Main Menu', text_size, c.black, 'result', 'intro')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.purple_dim, c.purple_lit, 'Choose Mode', text_size, c.black, 'result', 'play')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play again', text_size, c.black, 'result', 'game_2')
        #button('center', display_width //3, display_height //6*5, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'result', 'tutt_1')
        button('center', display_width//4 * 2, display_height//6*5, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'result', 'quit')
        text('If lighting have changed or the next player is a different person,', 30, c.black, display_width//2, display_height-75, False, c.white, True)
        text("please select 'Scan again' if you want to play again.", 30, c.black, display_width//2, display_height-45, False, c.white, True)
        ut.update_screen(clock)
        ut.quit_x()

def result_screen_3(score_me, score_com):
    text_size = 50
    button_w, button_h = 300, 100
    if score_me == score_com:
        music.stop()
        music.draw()
    elif score_me > score_com:
        music.stop()
        music.win()
    elif score_com > score_me:
        music.stop()
        music.lose()
    while True:
        #print(mouse_pos())
        gameDisplay.blit(pic.background, (0,0))
        if score_me == score_com:

            text('Draw? No fun here.', 120, c.black, display_width//2, display_height//10, False, c.grey_yellow, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_me > score_com:

            text('Tsk. You Win.', 120, c.black, display_width//2, display_height//10, False, c.grey_green, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_com > score_me:
            text('Ha-Hah! You Lose!', 120, c.black, display_width//2, display_height//10, False, c.pink_red, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.orange_dim, c.orange_lit, 'Main Menu', text_size, c.black, 'result', 'intro')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.purple_dim, c.purple_lit, 'Choose Mode', text_size, c.black, 'result', 'play')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play again', text_size, c.black, 'result', 'game_3')
        #button('center', display_width //3, display_height //6*5, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'result', 'tutt_1')
        button('center', display_width//4 * 2, display_height//6*5, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'result', 'quit')
        text('If lighting have changed or the next player is a different person,', 30, c.black, display_width//2, display_height-75, False, c.white, True)
        text("please select 'Scan again' if you want to play again.", 30, c.black, display_width//2, display_height-45, False, c.white, True)
        ut.update_screen(clock)
        ut.quit_x()

def result_screen_4(score_me, score_com):
    text_size = 50
    button_w, button_h = 300, 100
    if score_me == score_com:
        music.stop()
        music.draw()
    elif score_me > score_com:
        music.stop()
        music.win()
    elif score_com > score_me:
        music.stop()
        music.lose()
    while True:
        #print(mouse_pos())
        gameDisplay.blit(pic.background, (0,0))
        if score_me == score_com:

            text('Draw? No fun here.', 120, c.black, display_width//2, display_height//10, False, c.grey_yellow, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_me > score_com:

            text('Tsk. You Win.', 120, c.black, display_width//2, display_height//10, False, c.grey_green, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        elif score_com > score_me:
            text('Ha-Hah! You Lose!', 120, c.black, display_width//2, display_height//10, False, c.pink_red, True)
            text('Your Score:', 50, c.black, display_width//3, 300, False, c.yellow_green, True)
            text(str(score_me), 80, c.white, display_width//3, 400, False, None, True)
            text('Computer Score:', 50, c.black, display_width // 3*2, 300, False, c.light_green_blue, True)
            text(str(score_com), 80, c.white, display_width // 3*2, 400, False, None, True)
        button('center', display_width//4, display_height//3*2, button_w, button_h, c.orange_dim, c.orange_lit, 'Main Menu', text_size, c.black, 'result', 'intro')
        button('center', display_width//4 * 2, display_height//3*2, button_w, button_h, c.purple_dim, c.purple_lit, 'Choose Mode', text_size, c.black, 'result', 'play')
        button('center', display_width//4 * 3, display_height//3*2, button_w, button_h, c.green_dim, c.green_lit, 'Play again', text_size, c.black, 'result', 'game_4')
        #button('center', display_width //3, display_height //6*5, button_w, button_h, c.yellow_dim, c.yellow_lit, 'Instruction', text_size, c.black, 'result', 'tutt_1')
        button('center', display_width//4 * 2, display_height//6*5, button_w, button_h, c.red_dim, c.red_lit, 'Quit', text_size, c.black, 'result', 'quit')
        text('If lighting have changed or the next player is a different person,', 30, c.black, display_width//2, display_height-75, False, c.white, True)
        text("please select 'Scan again' if you want to play again.", 30, c.black, display_width//2, display_height-45, False, c.white, True)
        ut.update_screen(clock)
        ut.quit_x()



check_camera()


