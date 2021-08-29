import math
import pandas as pd
import pygame

# display window size
display_width = 700
display_height = 500

score_width = 120

# set colour values arrays
black = (0, 0, 0)
dark_gray = (50, 50, 50)
gray = (130, 130, 130)
light_gray = (180, 180, 180)
white = (255, 255, 255)
red = (240, 91, 74)
green = (89, 240, 86)
blue = (47, 235, 245)
yellow = (240, 240, 89)

bg_width = 700
bg_height = 600

meatball_size = 50

button_width = 120
button_height = 50


###########################

pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)

# sound effect channel
channel5 = pygame.mixer.Channel(5)

def load_images():

    global titlescreen_bg_Img
    titlescreen_bg_Img = pygame.image.load('images/swedish-meatballs - Copy.png')
    titlescreen_bg_Img = pygame.transform.scale(titlescreen_bg_Img, (bg_width, bg_height))


def render_title(x, y, fontsize, text):
    text_font = pygame.font.Font('freesansbold.ttf', fontsize)
    text_obj = text_font.render(text, True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)

    gameDisplay.blit(text_obj, text_rect)

def titlescreen_loop():
    # set up
    option_selected = False

    pygame.mouse.set_visible(False)

    # while loop to detect movement and click
    while not option_selected:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                option_selected = True


        # gameDisplay.blit(highscore_bg_Img, (0, 0))
        gameDisplay.fill(white)

        render_title(350, 150, 70, "Bla-hajimemashite")
        render_title(350, 230, 30, "Nice to Meat you!")
        render_title(350, 450, 20, "Press any key to continue")

        pygame.display.update()
        clock.tick(60)

    # return value is true if game screen, false if high score
    return


def load_audio():
    # bgm
    global bgm_music
    bgm_music = pygame.mixer.Sound("audio/highscoreBGM.mp3")

def run_title():
    ## Pygame segment
    # start pygame
    pygame.init()

    # create display window
    global gameDisplay
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Ikea the game')

    # create clock timer
    global clock
    clock = pygame.time.Clock()

    # load images and audio
    load_images()
    load_audio()

    # set the window icon (top corner)
    global programIcon
    programIcon = pygame.image.load("images/characters/blahajIcon.jpg")
    pygame.display.set_icon(programIcon)

    channel5.set_volume(0.5)
    channel5.play(bgm_music)

    titlescreen_loop()

    channel5.stop()

    # end the program if the game_loop is exited
    pygame.quit()

    return
