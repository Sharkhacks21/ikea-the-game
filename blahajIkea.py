### blahaj at ikea game
import math
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

grabby_width = 43
grabby_height = 100

trolley_width = 114
trolley_height = 120

meatball_size = 30

total_levels = 3

level_distance = 700

"""
# Areas in order
0 - Childrens area
1 - Bedroom
2 - Bathroom
"""

### obstacle sizes
top_width = [
    155,
    130,
    165
]
top_height = [
    169,
    143,
    113
]

bottom_width = [
    160,
    131,
    105
]
bottom_height = [
    160,
    165,
    160
]
bg_width = [
    1960,
    2100,
    2000
]
bg_height = [
    980,
    1190,
    1000
]

# arrays for the level images (init empty)
obstacle_top_imgs = []
obstacle_bottom_imgs = []
bg_imgs = []

# image file paths
bg_img_paths = [
    'images/Children\'s Area/Children\'s Area BG.jpg',
    'images/Bedroom/BedroomBG.jpg',
    'images/Bathroom/BathroomBG.jpg'
]
top_img_paths = [
    'images/Children\'s Area/Children\'s Area top obs.png',
    'images/Bedroom/BedroomTopObs.png',
    'images/Bathroom/BathroomTopObs.png'
]
bottom_img_paths = [
    'images/Children\'s Area/Children\'s Area bottom obs.png',
    'images/Bedroom/BedroomBottomObs.png',
    'images/Bathroom/BathroomBottomObs.png'
]

#################################################################
## variables

replay = False

# initialize pygame.mixer
pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
# init() channels refers to mono vs stereo, not playback Channel object

# create separate Channel objects for simultaneous playback
channel1 = pygame.mixer.Channel(0) # argument must be int
channel2 = pygame.mixer.Channel(1)

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

    # grabby
    global grabby_Img
    grabby_Img = pygame.image.load('images/characters/GrabbyHand.png')
    grabby_Img = pygame.transform.scale(grabby_Img, (grabby_width, grabby_height))

    # points and powerups
    global meatball_Img
    meatball_Img = pygame.image.load('images/characters/meatball1.png')
    meatball_Img = pygame.transform.scale(meatball_Img, (meatball_size, meatball_size))

    global powerup_item_Img
    powerup_item_Img = pygame.image.load('images/characters/PowerupIcon.png')
    powerup_item_Img = pygame.transform.scale(powerup_item_Img, (power_up_width, power_up_height))

    # trolley image
    global trolley_Img
    trolley_Img = pygame.image.load('images/characters/Trolley.png')
    trolley_Img = pygame.transform.scale(trolley_Img, (trolley_width, trolley_height))

    global trolley_left_Img
    trolley_left_Img = pygame.image.load('images/characters/Trolley_left.png')
    trolley_left_Img = pygame.transform.scale(trolley_left_Img, (trolley_width, trolley_height))


    # add level images
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


def load_sounds():
    global col_sound
    col_sound = pygame.mixer.Sound("audio/collisionSound.mp3")

    global powerup_sound
    powerup_sound = pygame.mixer.Sound("audio/powerupSound.mp3")

    global eat_sound
    eat_sound = pygame.mixer.Sound("audio/eatingSound.mp3")

    global lose_sound
    lose_sound = pygame.mixer.Sound("audio/loseSound.mp3")

    global win_sound
    win_sound = pygame.mixer.Sound("audio/winSound.mp3")

def scoreRender(score):
    # add label in front [boost]
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("Score:", True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (970, 25)

    gameDisplay.blit(text_obj, text_rect)

    pygame.draw.rect(gameDisplay, gray, pygame.Rect(1005, 10, 90, 33))

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

def countdown_text(i):
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("use up down and left arrow keys to move", True, white)
    text_rect = text_obj.get_rect()
    text_rect.center = (display_width / 2, 200)

    gameDisplay.blit(text_obj, text_rect)

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("collect meatballs and powerup files", True, white)
    text_rect = text_obj.get_rect()
    text_rect.center = (display_width / 2, 230)

    gameDisplay.blit(text_obj, text_rect)

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render("avoid obstacles", True, white)
    text_rect = text_obj.get_rect()
    text_rect.center = (display_width / 2, 260)

    gameDisplay.blit(text_obj, text_rect)

    text_font = pygame.font.Font('freesansbold.ttf', 100)
    text_obj = text_font.render(str(i), True, white)
    text_rect = text_obj.get_rect()
    text_rect.center = (display_width / 2, display_height / 2 + 100)

    gameDisplay.blit(text_obj, text_rect)

def countdown_loop():
    countdown = list(range(0, 4))[::-1]

    for i in countdown:
        gameDisplay.fill(black)

        countdown_text(i)
        print(i)

        pygame.display.update()
        pygame.time.wait(1000)


def game_loop():
    ## Constants
    powerup_min_time = 500
    powerup_max_time = 1000

    grabby_lunge_min_time = 300
    grabby_lunge_max_time = 430

    grabby_forward_mim_time = 50
    grabby_forward_max_time = 90

    point_min_time = 100
    point_max_time = 400

    obstacle_min_time = 50
    obstacle_max_time = 200

    obstacle_speed = 4

    trolley_min_time = 200
    trolley_max_time = 500

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
    grabby_posX = 0
    grabby_posY = int(display_height * 0.425) - (grabby_height - blahaj_height)/2

    # for grabby to lunge
    grabby_lunge_wait = random.randint(grabby_lunge_min_time, grabby_lunge_max_time)
    grabby_lunge_next = 0
    grabby_lunge_now = False
    grabby_lunge_timer = 10

    grabby_speed = 3

    # to allow grabby to move foward else drift backwards
    grabby_forward_timer = 10
    grabby_forward_next = 0
    grabby_forward_wait = random.randint(grabby_forward_mim_time, grabby_forward_max_time)
    grabby_forward_now = False

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
    trolley_destX = 0
    trolley_destY = 0
    trolley_speed = random.randint(3, 7)
    trolley_onScreen = False
    trolley_next = 0
    trolley_wait = random.randint(trolley_min_time, trolley_max_time)

    trolley_X_positive = True
    trolley_Y_positive = True

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
    boost_drop_count = 0
    boost_refill = False

    gameOver = False
    win = False

    level = 0

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
            if blahaj_posX > 0:
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
        if collision_proof > 0:
            boost_drop_count += 1

        if boost_drop_count > 5:
            boost_drop_count = 0
            boost_change -= 1

        if boost_refill:
            boost_change += 10
            boost_refill = False

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
                channel1.play(powerup_sound)

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
                boost_refill = True
                channel1.play(eat_sound)

        ###################################################

        ## update grabby position
        # lunge timer countdown
        if grabby_lunge_now:
            grabby_lunge_timer -= 1

        if grabby_lunge_timer == 0:
            grabby_lunge_now = False

        # check if lunge
        grabby_lunge_next += 1
        if grabby_lunge_next == grabby_lunge_wait:
            grabby_lunge_next = 0
            grabby_lunge_wait = random.randint(grabby_lunge_min_time, grabby_lunge_max_time)
            grabby_lunge_now = True
            grabby_lunge_timer = random.randint(22, 33)

        # fowward timer countdown
        if grabby_forward_now:
            grabby_forward_timer -= 1

        if grabby_forward_timer == 0:
            grabby_forward_now = False

        # check if forward
        grabby_forward_next += 1
        if grabby_forward_next == grabby_forward_wait:
            grabby_forward_next = 0
            grabby_forward_wait = random.randint(grabby_forward_mim_time, grabby_forward_max_time)
            grabby_forward_now = True
            grabby_forward_timer = random.randint(18, 25)

        # calculate distance between blahaj and grabby
        grabby_center_coords = [grabby_posX + grabby_width * 0.5, grabby_posY + grabby_height * 0.5]
        blahaj_center_coords = [blahaj_posX + blahaj_width * 0.5, blahaj_posY + blahaj_height * 0.5]
        dist_from_grabby = math.sqrt((grabby_center_coords[0]-blahaj_center_coords[0])**2 +
                                     (grabby_center_coords[1]-blahaj_center_coords[1])**2)

        grabby_speed = 7 if grabby_lunge_now else 3

        if dist_from_grabby == 0:
            scaled_dist_ratio = 1
        else:
            scaled_dist_ratio = grabby_speed / dist_from_grabby

        if grabby_forward_now or grabby_lunge_now:
            grabby_posX += scaled_dist_ratio * (blahaj_center_coords[0] - grabby_center_coords[0])
        else:
            grabby_posX -= 2 # drift backwards

        grabby_posY += scaled_dist_ratio * (blahaj_center_coords[1] - grabby_center_coords[1])

        if grabby_posX < 0:
            grabby_posX = 0

        # check grabby collisions
        if damagable \
                and not grabby_posY + grabby_height < blahaj_posY + 10 \
                and not grabby_posY > blahaj_posY + blahaj_height - 20 \
                and not grabby_posX + grabby_width < blahaj_posX + 10 \
                and not grabby_posX > blahaj_posX + blahaj_width - 20:
            gameOver = True
            win = False
            score -= 100


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
                channel1.play(col_sound)


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
                channel1.play(col_sound)

        ###################################################

        # trolley spawning
        trolley_next += 1
        if trolley_next == trolley_wait and not trolley_onScreen:
            trolley_next = 0
            trolley_wait = random.randint(obstacle_min_time, obstacle_max_time)
            trolley_onScreen = True
            trolley_speed = random.randint(3, 6)
            trolley_posX = random.randint(0, display_width - trolley_width)
            trolley_posY = random.choice([-101, 701])
            trolley_destX = random.randint(0, display_width - trolley_width)
            trolley_destY = -101 if trolley_posY == 701 else 701
            # print("trolley spawned!")

            trolley_X_positive = (trolley_destX - trolley_posX) > 0 # going right
            trolley_Y_positive = (trolley_destY - trolley_posY) > 0 # going down

        # collision checking
        if trolley_onScreen:
            if trolley_X_positive:
                trolley_posX += trolley_speed
            else:
                trolley_posX -= trolley_speed

            if trolley_Y_positive:
                trolley_posY += trolley_speed
            else:
                trolley_posY -= trolley_speed

            if (not trolley_Y_positive and trolley_posY < -trolley_height)\
                    or (trolley_Y_positive and trolley_posY > 700 + trolley_height):
                trolley_onScreen = False
                trolley_next = 0
            elif damagable \
                    and not trolley_posY + bottom_height[level] < blahaj_posY + 10 \
                    and not trolley_posY > blahaj_posY + blahaj_height - 20 \
                    and not trolley_posX + bottom_width[level] < blahaj_posX + 10 \
                    and not trolley_posX > blahaj_posX + blahaj_width - 10:
                collision_proof = collision_cooldown
                score -= 100
                channel1.play(col_sound)



        ############################################################################

        score = score if score > 0 else 0

        # check if distance has been reached (to check for transition to next scene)
        if dist_travelled > level_distance:
            dist_travelled = 0
            level += 1
            if level > total_levels:
                win = True
                gamevOver = True
            score += time_bonus
            time_bonus = 0

        # if lose condition end the gameloop

        if not gameOver:

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

            # render grabby hand
            gameDisplay.blit(grabby_Img, (grabby_posX, grabby_posY))

            # render point and powerup objects
            if point_item_onScreen:
                gameDisplay.blit(meatball_Img, (point_item_posX, point_item_posY))

            if powerup_item_onScreen:
                gameDisplay.blit(powerup_item_Img, (powerup_item_posX, powerup_item_posY))

            # render obstacles
            if top_obstacle_onScreen:
                gameDisplay.blit(obstacle_top_imgs[level], (top_obstacle_posX, top_obstacle_posY))

            if trolley_onScreen:
                if trolley_X_positive:
                    gameDisplay.blit(trolley_left_Img, (trolley_posX, trolley_posY))
                else:
                    gameDisplay.blit(trolley_Img, (trolley_posX, trolley_posY))

            if bottom_obstacle_onScreen:
                gameDisplay.blit(obstacle_bottom_imgs[level], (bottom_obstacle_posX, bottom_obstacle_posY))

            # render header labels
            header_render()
            boost_render(boost_meter)
            level_num_render(level)
            scoreRender(score)
            damagable_indicator_render(collision_proof, invincibility, damagable)
            dist_travel_bar(dist_travelled)

        else:
            if win:
                channel1.play(win_sound)
                # save as win
                return win
            else:
                channel1.play(lose_sound)
                # save as lose
                return win

        pygame.display.update()
        clock.tick(60)

def win_screen_loop():
    # show win screen
    # while True:
        # render win bg
        # render win text
        # render replay button
        # check for input
    # return replay
    pass

def lose_screen_loop():
    # show lose

    # while True:
    #     # render lose bg
    #     # render lose text
    #     # render replay button
    #     # check for input
    #
    # return replay
    pass

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

    load_sounds()

    # set the window icon (top corner)
    global programIcon
    programIcon = pygame.image.load("images/characters/blahajIcon.jpg")
    pygame.display.set_icon(programIcon)

    play = True

    # run the game logic loop'
    # while play:
        # run game loop
        # if win run win screen
        # if lose run lose creen
    countdown_loop()
    win = game_loop()

    # end the program if the game_loop is exited
    pygame.quit()

    # no need to quit this ends the program
    # quit()

    return
