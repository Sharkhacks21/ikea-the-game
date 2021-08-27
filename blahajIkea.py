### Stabby balloon game
import random
import pygame
import time

#################################################################
# Constants for the game

# display window size
display_width = 900
display_height = 700

blahaj_speed = 5

# set colour values arrrays
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 91, 74)
green = (89, 240, 86)
blue = (47, 235, 245)

# width of icon (tbd)
blahaj_width = 135
blahaj_height = 154

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
    pass


"""
Sample code for rendering objects on the screen

# render stabby at the start of the game
def stabby(x, y):
    # render stabby in the game using blit
    gameDisplay.blit(stabbyImg, (x, y))
    
# Need to create one generic function that works for all images loaded

"""

# def gen_render(x, y, character):
#     # render the character in the game using blit
#     gameDisplay.blit(character, x, y)


def text_objects(text, font):
    # render text objects
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def game_loop():

    # calculate starting position for blahaj ralative to the screen (to be modified)
    blahaj_posX = 0
    blahaj_posY = 0

    # calculate starting position for the grabby hand (to be modified)
    grabby_postY = 0


    # variables to be tracked in the game
    dist_travelled = 0
    score = 0
    dist_from_hand = 0

    gameOver = False

    # run the starting sequence


    # while loop to check if the game is still in play or if the player has lost

    while not gameOver:
        # codes to keep track of the status of the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    # pos_shift_left = True

                if event.key == pygame.K_RIGHT:
                    x_change = 5
                    # pos_shift_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        # based on the new positions of the characters in the game, check collisions


        # if there is a collision reducte the scores

        # if a power up is picked up increment the score and despawn the power up

        # if a meatball is picked up, despawn and increment the score

        # check variables to see if new object should be spawned

        # check if distance has been reached (to check for transition to next scene)

        # if lose condition end the gameloop

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
    # global programIcon
    # programIcon = pygame.image.load('otherSources/logo.png')
    # pygame.display.set_icon(programIcon)

    # run the game logic loop
    game_loop()

    # end the program if the game_loop is exited
    pygame.quit()

    # no need to quit
    quit()

    return
