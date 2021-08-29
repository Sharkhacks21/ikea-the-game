### the home screen ui
import math

import pygame

# display window size
display_width = 1075
display_height = 600

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

bg_width = 1075
bg_height = 600

cursor_width = 87
cursor_height = 94

button_width = 120
button_height = 50


###########################

pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)

# sound effect channel
channel3 = pygame.mixer.Channel(3)

def load_images():

    # homeScreen
    # global home_bg_Img
    # home_bg_Img = pygame.image.load('images/homeScreen/kiddieRug.jpg')
    # home_bg_Img = pygame.transform.scale(home_bg_Img, (bg_width, bg_height))

    global home_bg_Img1
    home_bg_Img1 = pygame.image.load('images/homeScreen/kiddieRug1.png')
    home_bg_Img1 = pygame.transform.scale(home_bg_Img1, (bg_width, bg_height))

    global home_bg_Img2
    home_bg_Img2 = pygame.image.load('images/homeScreen/kiddieRug2.png')
    home_bg_Img2 = pygame.transform.scale(home_bg_Img2, (bg_width, bg_height))


    global cursor_Img
    cursor_Img = pygame.image.load('images/homeScreen/CarCursor.png')
    cursor_Img = pygame.transform.scale(cursor_Img, (cursor_width, cursor_height))

def homescreen_loop():
    # set up
    option_selected = False
    game_selected = False

    pygame.mouse.set_visible(False)

    bg_swap_count = 0
    bg_num = 1

    # while loop to detect movement and click
    while not option_selected:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("click pos", mouse_x, mouse_y)
                dist_new_game = math.sqrt((mouse_x - 175)**2 + (mouse_y - 175)**2)
                dist_high_score = math.sqrt((mouse_x - 820)**2 + (mouse_y - 290)**2)

                if dist_new_game <= 50:
                    option_selected = True
                    game_selected = True

                if dist_high_score <= 59:
                    option_selected = True
                    game_selected = False

        bg_swap_count += 1
        if bg_swap_count > 20:
            bg_num = 1 if bg_num == 2 else 2
            bg_swap_count = 0

        # render images
        if bg_num == 1:
            gameDisplay.blit(home_bg_Img1, (0, 0))
        else:
            gameDisplay.blit(home_bg_Img2, (0, 0))

        # pygame.draw.circle(gameDisplay, red, (175, 175), 100) # game pos
        # pygame.draw.circle(gameDisplay, blue, (820, 290), 118) # high score pos

        gameDisplay.blit(cursor_Img, (mouse_x - cursor_width / 2, mouse_y - cursor_height / 2))

        pygame.display.update()
        clock.tick(60)

    # return value is true if game screen, false if high score
    return game_selected


def load_audio():
    # bgm
    global bgm_music
    bgm_music = pygame.mixer.Sound("audio/Cat_life.mp3")


def run_homescreen():
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


    # load images
    load_images()

    load_audio()

    # set the window icon (top corner)
    global programIcon
    programIcon = pygame.image.load("images/characters/blahajIcon.jpg")
    pygame.display.set_icon(programIcon)

    channel3.set_volume(0.5)
    channel3.play(bgm_music)

    game_selected = homescreen_loop()

    channel3.stop()

    # end the program if the game_loop is exited
    pygame.quit()

    return game_selected