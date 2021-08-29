### the high score UI

### the home screen ui
import math
import pandas as pd
import pygame

# display window size
display_width = 700
display_height = 600

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

bg_width = 1075
bg_height = 600

cursor_width = 87
cursor_height = 94

button_width = 120
button_height = 50


###########################

pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)

# sound effect channel
channel4 = pygame.mixer.Channel(4)

def load_images():

    global highscore_bg_Img
    highscore_bg_Img = pygame.image.load('images/homeScreen/kiddieRug1.png')
    highscore_bg_Img = pygame.transform.scale(highscore_bg_Img, (bg_width, bg_height))

    # global home_bg_Img2
    # home_bg_Img2 = pygame.image.load('images/homeScreen/kiddieRug2.png')
    # home_bg_Img2 = pygame.transform.scale(home_bg_Img2, (bg_width, bg_height))

    global cursor_Img
    cursor_Img = pygame.image.load('images/homeScreen/CarCursor.png')
    cursor_Img = pygame.transform.scale(cursor_Img, (cursor_width, cursor_height))

def render_text(x, y, width, text, color):
    pygame.draw.rect(gameDisplay, color, pygame.Rect(x, y, width, button_height))

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render(text, True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (x + width/2, y + button_height/2)

    gameDisplay.blit(text_obj, text_rect)

def render_title(x, y, fontsize, text):
    text_font = pygame.font.Font('freesansbold.ttf', fontsize)
    text_obj = text_font.render(text, True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)

    gameDisplay.blit(text_obj, text_rect)

def highscore_loop(player1, player2, player3, score1, score2, score3):
    # set up
    option_selected = False
    game_selected = False

    pygame.mouse.set_visible(False)

    back_btn_posX = 100
    back_btn_posY = 500

    # while loop to detect movement and click
    while not option_selected:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("click pos", mouse_x, mouse_y)
                if back_btn_posX < mouse_x < back_btn_posX + 120 \
                        and back_btn_posY < mouse_y < back_btn_posY + button_height:
                    option_selected = True


        # gameDisplay.blit(highscore_bg_Img, (0, 0))
        gameDisplay.fill(white)

        render_title(350, 70, 50, "High Scores")
        render_title(250, 150, 30, "Player")
        render_title(450, 150, 30, "Score")

        render_text(200, 200, score_width, player1, green)
        render_text(200, 300, score_width, player2, green)
        render_text(200, 400, score_width, player3, green)

        render_text(400, 200, score_width, str(score1), green)
        render_text(400, 300, score_width, str(score2), green)
        render_text(400, 400, score_width, str(score3), green)

        render_text(back_btn_posX, back_btn_posY, 120, "Back", blue)

        # pygame.draw.circle(gameDisplay, red, (175, 175), 100) # game pos
        # pygame.draw.circle(gameDisplay, blue, (820, 290), 118) # high score pos

        gameDisplay.blit(cursor_Img, (mouse_x - cursor_width / 2, mouse_y - cursor_height / 2))

        pygame.display.update()
        clock.tick(60)

    # return value is true if game screen, false if high score
    return


def load_audio():
    # bgm
    global bgm_music
    bgm_music = pygame.mixer.Sound("audio/highscoreBGM.mp3")

def get_highscores():
    # read the excel
    df = pd.read_excel("savedData/blahajData.xlsx", sheet_name="win")

    player1 = df.loc[0]["player"]
    player2 = df.loc[1]["player"]
    player3 = df.loc[2]["player"]
    score1 = df.loc[0]["score"]
    score2 = df.loc[1]["score"]
    score3 = df.loc[2]["score"]

    return player1, player2, player3, score1, score2, score3

def run_highscore():
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

    player1, player2, player3, score1, score2, score3 = get_highscores()

    # set the window icon (top corner)
    global programIcon
    programIcon = pygame.image.load("images/characters/blahajIcon.jpg")
    pygame.display.set_icon(programIcon)

    channel4.set_volume(0.5)
    channel4.play(bgm_music)

    highscore_loop(player1, player2, player3, score1, score2, score3)

    channel4.stop()

    # end the program if the game_loop is exited
    pygame.quit()

    return
