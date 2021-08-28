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

# width of icon (tbd)
blahaj_width = 163
blahaj_height = 93

power_blahaj_width = 112
power_blahaj_height = 110

power_up_width = 50
power_up_height = 38

meatball_size = 30

total_levels = 1

level_distance = 500

"""
# Areas in order
0 - Childrens area
1 - Bedroom
2 - Bathroom
"""

### obstacle sizes
top_width = [
    155
]
top_height = [
    169
]

bottom_width = [
    160,
    144
]
bottom_height = [
    160,
    177
]
bg_width = [
    1960,
    2100
]
bg_height = [
    980,
    1190
]

# arrays for the level images (init empty)
obstacle_top_imgs = []
obstacle_bottom_imgs = []
bg_imgs = []

# image file paths
bg_img_paths = [
    'images/Children\'s Area/Children\'s Area BG.jpg',
    'images/Bedroom/BedroomBG.jpg'
]
top_img_paths = [
    'images/Children\'s Area/Children\'s Area top obs.png',
    'images/Bedroom/BedroomTopObs.png'
]
bottom_img_paths = [
    'images/Children\'s Area/Children\'s Area bottom obs.png',
    'images/Bedroom/BedroomBottomObs.png'
]
#################################################################


# function that is called from main to open the window for the game
def load_images():

    # blahaj
    global blahaj_Img
    blahaj_Img = pygame.image.load('images/characters/blahajSwim.png')
    blahaj_Img = pygame.transform.scale(blahaj_Img, (blahaj_width, blahaj_height))

    # blahaj with power up
    global power_blahaj_Img
    power_blahaj_Img = pygame.image.load('images/characters/Powerup.png')
    power_blahaj_Img = pygame.transform.scale(power_blahaj_Img, (power_blahaj_width, power_blahaj_height))

    # points and powerups
    global meatball_Img
    meatball_Img = pygame.image.load('images/characters/meatball1.png')
    meatball_Img = pygame.transform.scale(meatball_Img, (meatball_size, meatball_size))

    global powerup_item_Img
    powerup_item_Img = pygame.image.load('images/characters/PowerupIcon.png')
    powerup_item_Img = pygame.transform.scale(powerup_item_Img, (power_up_width, power_up_height))

    # add images
    for level in range(0, total_levels):
        bg_imgs.append(pygame.image.load(bg_img_paths[level]))
        bg_imgs[level] = pygame.transform.scale(bg_imgs[level],
                                                          (bg_width[level], bg_height[level])
                                                          )
        obstacle_top_imgs.append(pygame.image.load(top_img_paths[level]))
        obstacle_top_imgs[level] = pygame.transform.scale(obstacle_top_imgs[level],
                                                          (top_width[level], top_height[level])
                                                          )

        obstacle_bottom_imgs.append(pygame.image.load(bottom_img_paths[level]))
        obstacle_bottom_imgs[level] = pygame.transform.scale(obstacle_bottom_imgs[level],
                                                             (bottom_width[level], bottom_height[level])
                                                             )

    global miniBlahaj_Img
    miniBlahaj_Img = pygame.image.load('images/characters/mini_blahaj.png')
    miniBlahaj_Img = pygame.transform.scale(miniBlahaj_Img, (30, 30))


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

    bar_posX = 70
    bar_posY = 10
    bar_height = 30

    boost_bar_outline = pygame.draw.rect(gameDisplay, black, pygame.Rect(bar_posX - 2,
                                                                        bar_posY - 2,
                                                                        100 + 4,
                                                                        bar_height + 4))
    boost_bar_bg = pygame.draw.rect(gameDisplay, dark_gray, pygame.Rect(bar_posX, bar_posY, 100, bar_height))
    boost_bar = pygame.draw.rect(gameDisplay, color, pygame.Rect(bar_posX, bar_posY, boost_val, bar_height))


    # add label in front [boost]
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("Boost", True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (35, 25)

    gameDisplay.blit(text_obj, text_rect)


def scoreRender(score):
    # add label in front [boost]
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("Score:", True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (970, 25)

    gameDisplay.blit(text_obj, text_rect)

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render(str(score), True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (1050, 25)

    gameDisplay.blit(text_obj, text_rect)


def header_render():
    header_bar = pygame.draw.rect(gameDisplay, light_gray, pygame.Rect(0, 0, display_width, 50))


def damagable_indicator_render(collision_proof, invincibility, damagable):
    text = ""
    if collision_proof > 0:
        text += "[c]"
    if invincibility > 0:
        text += "[i]"
    if damagable:
        text += "[d]"

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render(text, True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (890, 25)

    gameDisplay.blit(text_obj, text_rect)


def dist_travel_bar(dist_travelled):
    # replace with icon travel
    bar_posX = 300
    bar_posY = 10

    pygame.draw.rect(gameDisplay, gray, pygame.Rect(bar_posX, bar_posY + 15, 350, 3))
    pygame.draw.rect(gameDisplay, gray, pygame.Rect(bar_posX, bar_posY, 3, 30))
    pygame.draw.rect(gameDisplay, gray, pygame.Rect(bar_posX + 347, bar_posY, 3, 30))

    gameDisplay.blit(miniBlahaj_Img, (bar_posX + dist_travelled/level_distance * 320, bar_posY))

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render(str(level_distance - dist_travelled), True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (bar_posX + 370, 25)

    gameDisplay.blit(text_obj, text_rect)

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("m remaning", True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (bar_posX + 450, 25)

    gameDisplay.blit(text_obj, text_rect)

def level_num_render(level):
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("level: " + str(level + 1), True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (220, 25)

    gameDisplay.blit(text_obj, text_rect)


def game_loop():
    ## Constants
    powerup_min_time = 500
    powerup_max_time = 1000

    point_min_time = 100
    point_max_time = 400

    obstacle_min_time = 50
    obstacle_max_time = 200

    obstacle_speed = 4

    collision_cooldown = 50
    invincibility_duration = 300

    ############################################################################

    ## calculate starting position for blahaj ralative to the screen (to be modified)
    blahaj_posX = int((display_width - 50) * 0.25 + 50)
    blahaj_posY = int(display_height * 0.425)

    step_back = -2
    x_change_blahaj = step_back
    y_change_blahaj = 0

    ## calculate starting position for the grabby hand (to be modified)
    grabby_postY = 0
    grabby_posX = 0

    ############################################################################

    ## position and spawning of powerup item
    powerup_item_posX = 0
    powerup_item_posY = 0
    next_powerup_wait = random.randint(powerup_min_time, powerup_max_time)
    next_powerup_count = 0
    powerup_item_onScreen = False
    powerup_item_speed = 7

    ## position and spawning of point items
    point_item_posX = 1100
    point_item_posY = random.randint(60, 600)
    next_point_wait = random.randint(point_min_time, point_max_time)
    next_point_count = 0
    point_item_onScreen = False
    point_item_speed = 7

    ############################################################################

    ## moving trolley obstacle
    trolley_posX = 0
    trolley_posY = -100
    trolley_speed = 0
    top_obstacle_onScreen = False
    top_obstacle_next = random.randint(point_min_time, point_max_time)
    top_obstacle_wait = 0

    ############################################################################
    # track the top and bottom obstacle spawning
    top_obstacle_posX = 0
    top_obstacle_posY = 0
    top_obstacle_onScreen = False
    top_obstacle_wait = random.randint(obstacle_min_time, obstacle_max_time)
    top_obstacle_next = 0

    bottom_obstacle_posX = 0
    bottom_obstacle_posY = 0
    bottom_obstacle_onScreen = False
    bottom_obstacle_wait = random.randint(obstacle_min_time, obstacle_max_time)
    bottom_obstacle_next = 0

    # print(bottom_obstacle_wait, top_obstacle_wait)

    ############################################################################

    # variables to be tracked in the game
    dist_travelled = 0
    dist_count = 0

    time_bonus = 0

    score = 0
    score_count = 0

    boost_meter = 100
    boost_change = 2

    gameOver = False
    win = False

    level = 0

    bg_posX = 0

    invincibility = 0
    collision_proof = 0


    ############################################################################

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

        ###################################################

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


        ###################################################

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

        # distance
        dist_count += 2
        if boost_change < 0 and boost_meter != 0:
            dist_count += 2

        if dist_count // 10:
            dist_count = dist_count % 10
            dist_travelled += 1
            time_bonus += 5

        bg_posX = ((level_distance - dist_travelled) / level_distance - 1) * (bg_width[level] - display_width)

        if invincibility != 0:
            invincibility -= 1
        if collision_proof != 0:
            collision_proof -= 1

        damagable = not (invincibility > 0 or collision_proof > 0)


        ###################################################

        # powerup spawning
        next_powerup_count += 1
        if next_powerup_count == next_powerup_wait and not powerup_item_onScreen:
            next_powerup_count = 0
            next_powerup_wait = random.randint(powerup_min_time, powerup_max_time)
            powerup_item_onScreen = True
            powerup_item_posX = 1100
            powerup_item_posY = random.randint(60, 600)
            powerup_item_speed = random.randint(4, 9)
            # print("powerup object spawned", powerup_item_posX, powerup_item_posY)

        if powerup_item_onScreen:
            powerup_item_posX -= powerup_item_speed
            if powerup_item_posX < -50:
                powerup_item_onScreen = False
                next_powerup_count = 0
                # print("powerup despawn")
            elif invincibility == 0  \
                    and not powerup_item_posY > blahaj_posY + blahaj_height \
                    and not powerup_item_posY + meatball_size < blahaj_posY + 10 \
                    and not powerup_item_posX + meatball_size < blahaj_posX \
                    and not powerup_item_posX > blahaj_posX + blahaj_width:
                next_powerup_count = 0
                powerup_item_onScreen = False
                score += 100
                invincibility = invincibility_duration
                # print("powerup collected")
            elif invincibility > 0 \
                    and not powerup_item_posY > blahaj_posY + power_blahaj_height \
                    and not powerup_item_posY + meatball_size < blahaj_posY + 10 \
                    and not powerup_item_posX + meatball_size < blahaj_posX \
                    and not powerup_item_posX > blahaj_posX + power_blahaj_width:
                next_powerup_count = 0
                powerup_item_onScreen = False
                score += 100
                invincibility = invincibility_duration
                # print("powerup collected")


        # point spawning
        next_point_count += 1
        if next_point_count == next_point_wait and not point_item_onScreen:
            next_point_count = 0
            next_point_wait = random.randint(point_min_time, point_max_time)
            point_item_onScreen = True
            point_item_posX = 1100
            point_item_posY = random.randint(60, 600)
            point_item_speed = random.randint(4, 9)
            # print("Point object spawned", point_item_posX, point_item_posY)

        if point_item_onScreen:
            point_item_posX -= point_item_speed
            if point_item_posX < -50:
                point_item_onScreen = False
                next_point_count = 0
                # print("point despawn")
            elif not point_item_posY > blahaj_posY + blahaj_height \
                    and not point_item_posY + meatball_size < blahaj_posY + 10 \
                    and not point_item_posX + meatball_size < blahaj_posX \
                    and not point_item_posX > blahaj_posX + blahaj_width:
                next_point_count = 0
                point_item_onScreen = False
                score += 100
                # print("point collected")

        ###################################################

        # static obstacle spawning
        top_obstacle_next += 1
        if top_obstacle_next == top_obstacle_wait and not top_obstacle_onScreen:
            top_obstacle_next = 0
            top_obstacle_wait = random.randint(obstacle_min_time, obstacle_max_time)
            top_obstacle_onScreen = True
            top_obstacle_posX = 1100
            top_obstacle_posY = random.randint(60, 370 - top_height[level])
            # print("obstacle", top_obstacle_posX, top_obstacle_posY)


        bottom_obstacle_next += 1
        if bottom_obstacle_next == bottom_obstacle_wait and not bottom_obstacle_onScreen:
            bottom_obstacle_next = 0
            bottom_obstacle_wait = random.randint(obstacle_min_time, obstacle_max_time)
            bottom_obstacle_onScreen = True
            bottom_obstacle_posX = 1100
            bottom_obstacle_posY = random.randint(370, 700 - bottom_height[level])

        # collision checking
        if top_obstacle_onScreen:
            top_obstacle_posX -= obstacle_speed
            if top_obstacle_posX < - top_width[level]:
                top_obstacle_onScreen = False
                top_obstacle_next = 0
            elif damagable \
                    and not top_obstacle_posY + top_height[level] < blahaj_posY + 10 \
                    and not top_obstacle_posY > blahaj_posY + blahaj_height - 20 \
                    and not top_obstacle_posX + top_width[level] < blahaj_posX + 10\
                    and not top_obstacle_posX > blahaj_posX + blahaj_width - 10:
                collision_proof = collision_cooldown
                score -= 100

        if bottom_obstacle_onScreen:
            bottom_obstacle_posX -= obstacle_speed
            if bottom_obstacle_posX < - top_width[level]:
                bottom_obstacle_onScreen = False
                bottom_obstacle_next = 0
            elif damagable \
                    and not bottom_obstacle_posY + bottom_height[level] < blahaj_posY + 10 \
                    and not bottom_obstacle_posY > blahaj_posY + blahaj_height - 20 \
                    and not bottom_obstacle_posX + bottom_width[level] < blahaj_posX + 10 \
                    and not bottom_obstacle_posX > blahaj_posX + blahaj_width - 10 :
                collision_proof = collision_cooldown
                score -= 100

        ###################################################

        # trolley spawning


        # collision checking

        ############################################################################

        score = score if score > 0 else 0

        # check if distance has been reached (to check for transition to next scene)
        if dist_travelled > level_distance:
            dist_travelled = 0
            # level += 1
            score += time_bonus
            time_bonus = 0

        # if lose condition end the gameloop


        if not win:

            # note item rendered first get rendered in behind

            # render bg
            gameDisplay.blit(bg_imgs[level], (bg_posX, 0))

            # render blahaj
            if invincibility > 0:
                gameDisplay.blit(power_blahaj_Img, (blahaj_posX, blahaj_posY))
            else:
                if collision_proof == 0 or \
                        (collision_proof > 0 and
                         (collision_proof % 5 == 0 or collision_proof % 5 == 1)):
                    gameDisplay.blit(blahaj_Img, (blahaj_posX, blahaj_posY))

            # render point and powerup objects
            if point_item_onScreen:
                gameDisplay.blit(meatball_Img, (point_item_posX, point_item_posY))

            if powerup_item_onScreen:
                gameDisplay.blit(powerup_item_Img, (powerup_item_posX, powerup_item_posY))


            # render obstacles
            if top_obstacle_onScreen:
                gameDisplay.blit(obstacle_top_imgs[level], (top_obstacle_posX, top_obstacle_posY))


            if bottom_obstacle_onScreen:
                gameDisplay.blit(obstacle_bottom_imgs[level], (bottom_obstacle_posX, bottom_obstacle_posY))


            # render grabby hand


            # render header labels
            header_render()
            boost_render(boost_meter)
            level_num_render(level)
            scoreRender(score)
            damagable_indicator_render(collision_proof, invincibility, damagable)
            dist_travel_bar(dist_travelled)

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
    programIcon = pygame.image.load("images/characters/blahajIcon.jpg")
    pygame.display.set_icon(programIcon)

    # run the game logic loop
    game_loop()

    # end the program if the game_loop is exited
    pygame.quit()

    # no need to quit
    quit()

    return
