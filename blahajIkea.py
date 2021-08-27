### blahaj at ikea game

import random
import pygame
import time

#################################################################
# Constants for the game

# display window size
display_width = 1100
display_height = 700

blahaj_speed = 5

# set colour values arrrays
black = (0, 0, 0)
gray = (50, 50, 50)
light_gray = (180, 180, 180)
white = (255, 255, 255)
red = (240, 91, 74)
green = (89, 240, 86)
blue = (47, 235, 245)
yellow = (240, 240, 89)

# width of icon (tbd)
blahaj_width = 163
blahaj_height = 93

meatball_size = 30

#################################################################


# function that is called from main to open the window for the game
def load_images():
    # for each of the images in the game, create a global object for it, then laod it eg:
    """
    global stabbyImg
    stabbyImg = pygame.image.load('otherSources/glow_nyoomba_stabby.png')
    global gladBotImg
    gladBotImg = pygame.image.load('otherSources/glow_nyoomba_gladbot.png')
    # print(stabbyImg.get_rect().size)
    stabbyImg = pygame.transform.scale(stabbyImg, (stabby_width, stabby_height)
    """

    global blahajImg
    blahajImg = pygame.image.load('images/blahajSwim.jpg')
    blahajImg = pygame.transform.scale(blahajImg, (blahaj_width, blahaj_height))

    global meatballImg
    meatballImg = pygame.image.load('images/meatball1.jpg')
    meatballImg = pygame.transform.scale(meatballImg, (meatball_size, meatball_size))



"""
Sample code for rendering objects on the screen

# render stabby at the start of the game
def stabby(x, y):
    # render stabby in the game using blit
    gameDisplay.blit(stabbyImg, (x, y))
    
# Need to create one generic function that works for all images loaded

"""


def text_objects(text, font):
    # render text objects
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def boost_render(boost_val):
    # render bar
    if boost_val > 70:
        color = green
    elif boost_val > 30:
        color = yellow
    else:
        color = red

    bar_posX = 90
    bar_posY = 10
    bar_height = 30

    boost_bar_outline = pygame.draw.rect(gameDisplay, black, pygame.Rect(bar_posX - 2,
                                                                        bar_posY - 2,
                                                                        100 + 4,
                                                                        bar_height + 4))
    boost_bar_bg = pygame.draw.rect(gameDisplay, gray, pygame.Rect(bar_posX, bar_posY, 100, bar_height))
    boost_bar = pygame.draw.rect(gameDisplay, color, pygame.Rect(bar_posX, bar_posY, boost_val, bar_height))


    # add label in front [boost]
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("Boost", True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (50, 25)

    gameDisplay.blit(text_obj, text_rect)


def scoreRender(score):
    # add label in front [boost]
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("Score", True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (960, 25)

    gameDisplay.blit(text_obj, text_rect)

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render(str(score), True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (1040, 25)

    gameDisplay.blit(text_obj, text_rect)


def header_render():
    header_bar = pygame.draw.rect(gameDisplay, light_gray, pygame.Rect(0, 0, display_width, 50))


def game_loop():
    powerup_min_time = 2000
    powerup_max_time = 5000

    point_min_time = 100
    point_max_time = 500

    point_item_speed = 7

    # calculate starting position for blahaj ralative to the screen (to be modified)
    blahaj_posX = int((display_width - 50) * 0.25 + 50)
    blahaj_posY = int(display_height * 0.425)
    print(blahaj_posX)

    step_back = -2
    x_change_blahaj = step_back
    y_change_blahaj = 0

    # calculate starting position for the grabby hand (to be modified)
    grabby_postY = 0
    grabby_posX = 0

    # position and spawning of powerup item
    powerup_item_posX = 0
    powerup_item_posY = 0

    next_powerup_wait = random.randint(powerup_min_time, powerup_max_time)
    next_powerup_count = 0
    powerup_item_onScreen = False

    # position and spawning of point items
    point_item_posX = 1100
    point_item_posY = random.randint(60, 600)

    next_point_wait = random.randint(point_min_time, point_max_time)
    next_point_count = 0
    point_item_onScreen = False

    # variables to be tracked in the game
    dist_travelled = 0
    score = 0
    score_count = 0
    dist_from_hand = 0

    boost_meter = 100
    boost_change = 2

    gameOver = False
    win = False

    # run the starting sequence


    # while loop to check if the game is still in play or if the player has lost

    while not gameOver:
        # codes to keep track of the status of the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change_blahaj = -5
                    # pos_shift_left = True

                if event.key == pygame.K_DOWN:
                    y_change_blahaj = 5
                    # pos_shift_right = True

                if event.key == pygame.K_RIGHT:
                    x_change_blahaj = 5
                    boost_change = -2
                    # pos_shift_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change_blahaj = 0

                if event.key == pygame.K_RIGHT:
                    boost_change = 2
                    x_change_blahaj = step_back

        # update blahaj position
        if boost_meter == 0:
            x_change_blahaj = step_back
        if x_change_blahaj < 0:
            if blahaj_posX > 100:
                blahaj_posX += x_change_blahaj
        else:
            if blahaj_posX < 930:
                blahaj_posX += x_change_blahaj

        if y_change_blahaj < 0:
            if blahaj_posY > 70:
                blahaj_posY += y_change_blahaj
        else:
            if blahaj_posY < 590:
                blahaj_posY += y_change_blahaj

        # update boost position
        boost_meter += boost_change
        if boost_meter > 100:
            boost_meter = 100
        elif boost_meter < 0:
            boost_meter = 0

        # value tracking and counting
        # score
        score_count += 1
        if score_count == 5:
            score += 5
            score_count = 0

        # powerup spawning


        # point spawning
        next_point_count += 1
        if next_point_count == next_point_wait:
            next_point_count = 0
            next_point_wait = random.randint(point_min_time, point_max_time)
            point_item_onScreen = True
            point_item_posX = 1100
            point_item_posY = random.randint(60, 600)
            # print("point spawned")

        if point_item_onScreen:
            point_item_posX -= point_item_speed
            if (point_item_posY > blahaj_posY and point_item_posY < blahaj_posY + blahaj_height):
                if (point_item_posX > blahaj_posX and point_item_posX < blahaj_posX + blahaj_width):

                    point_item_onScreen = False
                    score += 100
                    # print("point scored")

        # based on the new positions of the characters in the game, check collisions


        # if there is a collision reducte the scores

        # if a power up is picked up increment the score and despawn the power up

        # if a meatball is picked up, despawn and increment the score

        # check variables to see if new object should be spawned

        # check if distance has been reached (to check for transition to next scene)

        # if lose condition end the gameloop

        if not win:

            gameDisplay.blit(blahajImg, (blahaj_posX, blahaj_posY))

            if point_item_onScreen:
                gameDisplay.blit(meatballImg, (point_item_posX, point_item_posY))

            header_render()
            boost_render(boost_meter)
            scoreRender(score)



        pygame.display.update()
        clock.tick(60)




def runBlahajGame():
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

    # set the window icon (top corner)
    global programIcon
    programIcon = pygame.image.load("images/blahajIcon.jpg")
    pygame.display.set_icon(programIcon)

    # run the game logic loop
    game_loop()

    # end the program if the game_loop is exited
    pygame.quit()

    # no need to quit
    quit()

    return
