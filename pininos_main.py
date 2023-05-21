""" 
    Pininos' game is about compromises and jumps, enjoy it!
    Copyright (C) 2023  Alejandro Nieto Cuarenta

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Contact email: alejandronieto40@gmail.com
"""

#########################################################################################
# IMPORT MODULES
#########################################################################################

# used for game
import pygame as pg
import pandas as pd
from sys import exit, version
from random import randint, choice  # choice will be used to random spawn different types of enemies
from enum import Enum

# # used for performance (comment if not used)
# import matplotlib.pyplot as plt
# import time  # using better the pygame time
# import csv
# import numpy as np


#########################################################################################
# GLOBAL PARAMETERS
#########################################################################################

# GLOBAL screen parameters
GROUND_HEIGHT = 200
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1600
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # canvas for everything!

# GLOBAL game parameters
GAME_WIN_SCORE = 20  # default 20

# GLOBAL hero parameters
HERO_LIFE = 3  # default 3
HERO_X_START_POS = 200  # default 200

# GLOBAL enemy parameters
ENEMY_SPAWN_TIME_DAY_1 = 1000  # default 1000
ENEMY_MOVE_SPEED_DAY_1 = 8  # default 8

ENEMY_SPAWN_TIME_DAY_2 = 800  # default 800
ENEMY_MOVE_SPEED_DAY_2 = 10  # default 10

ENEMY_SPAWN_TIME_DAY_3 = 600  # default 600
ENEMY_MOVE_SPEED_DAY_3 = 12  # default 12

# GLOBAL performance parameters
cycle_time = []  # in seconds
test_time_limit = 50000  # in ms
test_spawn_time = 1000  # for performance test


#########################################################################################
# CLASSES
#########################################################################################

class Hero(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # move/jump parameters
        self.move_speed = 10
        self.jump_force = 0
        self.jump_force_max = 100
        self.jump_timer = 0
        self.jump_velocity = 0
        self.jump_pixel = 0
        self.gravity = 10
        self.action = Action.ON_GROUND

        # life parameters
        self.heart_counter = HERO_LIFE

        # hero model
        model = 'soldier'
        # model = 'stickman'

        # standing frames
        stand_01 = pg.image.load(f'graphics/{model}/{model}_standing1.png').convert_alpha()
        stand_02 = pg.image.load(f'graphics/{model}/{model}_standing2.png').convert_alpha()
        stand_03 = pg.image.load(f'graphics/{model}/{model}_standing1.png').convert_alpha()
        stand_04 = stand_02
        standing_frames = [stand_01, stand_02, stand_03, stand_04]

        # crouching frames
        crouch_01 = pg.image.load(f'graphics/{model}/{model}_jumping2.png').convert_alpha()
        crouch_02 = pg.image.load(f'graphics/{model}/{model}_jumping3.png').convert_alpha()
        crouch_03 = pg.image.load(f'graphics/{model}/{model}_jumping4.png').convert_alpha()
        crouch_04 = pg.image.load(f'graphics/{model}/{model}_jumping5.png').convert_alpha()
        crouch_05 = pg.image.load(f'graphics/{model}/{model}_jumping6.png').convert_alpha()
        crouch_06 = pg.image.load(f'graphics/{model}/{model}_jumping7.png').convert_alpha()
        crouch_07 = pg.image.load(f'graphics/{model}/{model}_jumping8.png').convert_alpha()
        crouch_08 = pg.image.load(f'graphics/{model}/{model}_jumping9.png').convert_alpha()
        crouching_frames = [crouch_01, crouch_02, crouch_03, crouch_04,
                            crouch_05, crouch_06, crouch_07, crouch_08]

        # jumping frames
        jump_01 = pg.image.load(f'graphics/{model}/{model}_jumping10.png').convert_alpha()  # jumping
        jumping_frames = [jump_01]

        # concatenate all animation frames
        self.frames = standing_frames + crouching_frames + jumping_frames
        self.frame_index = 0

        # create image, rect and mask
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(HERO_X_START_POS, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.mask = pg.mask.from_surface(self.image)

        # save original rect height and bottom (used in rect resize method)
        self.rect_original_height = self.rect.height
        self.rect_original_bottom = self.rect.bottom

        # add jump sound
        self.jump_sound = pg.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.02)

    def update(self):

        # self.standing()  # used in the event: timer_hero_standing_animation
        self.walking()
        self.jumping()

        # update mask
        self.mask = pg.mask.from_surface(self.image)

        # only for testing
        # self.draw_boundaries()
        # self.draw_mask_outline()

    def standing(self):

        # animation
        self.frame_index += 1
        if self.frame_index > 3:
            self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def walking(self):

        # get key
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_LEFT]:
            self.rect.x -= self.move_speed

        # press keyboard right
        elif keys[pg.K_RIGHT]:
            self.rect.x += self.move_speed

        # reset position if screen limit is reached
        if self.rect.left > SCREEN_WIDTH: self.rect.right = 0  # redraw hero on left end
        if self.rect.right < 0: self.rect.left = SCREEN_WIDTH  # # redraw hero on right end

    def jumping(self):

        # get key
        keys = pg.key.get_pressed()

        # jump force
        if keys[pg.K_DOWN] and self.action == Action.ON_GROUND:
            self.jump_force += 4  # force increase as long key held press
            if self.jump_force > self.jump_force_max:
                self.jump_force = self.jump_force_max

            # crouching animation (static)
            self.frame_index = int(self.jump_force/self.jump_force_max * 8) + 3
            self.image = self.frames[self.frame_index]

            # # crouching animation (dynamic)
            # self.image, self.rect = self.resize_rect()

        elif not self.action == Action.JUMPING:

            # play jump sound (only once)
            if pg.mixer.get_busy() == 0 and self.jump_force > 0:
                self.jump_sound.play()

            # initiate jump timer > 0
            self.jump_velocity = self.jump_force
            self.jump_timer = 0.1
            self.action = Action.JUMPING
            self.jump_force = 0  # reset after key release

        else:
            # jumping animation
            self.frame_index = 12
            self.image = self.frames[self.frame_index]

        # update jump timer
        if self.jump_timer > 0 and self.action == Action.JUMPING:
            self.jump_timer += 0.5

        # jump in pixels
        self.jump_pixel = - self.jump_velocity * self.jump_timer \
                          + 0.5 * self.gravity * self.jump_timer ** 2
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT + self.jump_pixel

        # on ground action
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.jump_timer = 0  # reset jump timer
            self.action = Action.ON_GROUND

    def draw_boundaries(self):

        # draw the red rectangle within the boundary (only for testing)
        rect_x = self.rect.x
        rect_y = self.rect.y
        rect_width = self.rect.width
        rect_height = self.rect.height
        pg.draw.rect(SCREEN, 'red', pg.Rect(rect_x, rect_y, rect_width, rect_height), 4)

    def resize_rect(self):  # deprecated due to masks

        # create a mask from the image surface
        mask = pg.mask.from_surface(self.image)

        # get the bounding rectangle of the mask
        mask_rect = mask.get_bounding_rects()[0]

        # calculate the position of the most upper pixel
        upper_pixel_y = mask_rect.top

        # crop image
        rect_crop = pg.Rect(0,  # left
                            0 + upper_pixel_y,  # top
                            100,  # width
                            200 - upper_pixel_y)  # height
        image_crop = self.image.subsurface(rect_crop)
        rect_crop = image_crop.get_rect()

        # move rect coordinates
        rect_crop.x = self.rect.x + 0
        rect_crop.y = self.rect.y + upper_pixel_y

        return image_crop, rect_crop


class Enemy(pg.sprite.Sprite):

    def __init__(self, type, game_mode):
        super().__init__()

        # enemy speed depending on the day
        self.move_speed = globals()[f'ENEMY_MOVE_SPEED_{game_mode.name}']

        # parameter used for the score
        self.hero_dodge = False

        if type == 'enemy_01':

            # enemy_01 new frames
            frame1 = pg.image.load('graphics/evil_eye_mini1.png').convert_alpha()
            frame2 = pg.image.load('graphics/evil_eye_mini2.png').convert_alpha()
            frame3 = pg.image.load('graphics/evil_eye_mini3.png').convert_alpha()
            frame4 = pg.image.load('graphics/evil_eye_mini4.png').convert_alpha()
            frame5 = pg.image.load('graphics/evil_eye_mini5.png').convert_alpha()
            frame6 = pg.image.load('graphics/evil_eye_mini6.png').convert_alpha()
            frame7 = frame5
            frame8 = frame4
            frame9 = frame3
            frame10 = frame2

            # concatenate frames
            self.frames = [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9, frame10]
            self.frame_index = 0

        else:  # other type of enemy can be used here
            pass

        # obstacle appear at random position
        rand_position_x = randint(1200, 1800)
        rand_position_y = SCREEN_HEIGHT - GROUND_HEIGHT - randint(0, 300)

        # create Enemy_x image and rect
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(bottomright=(rand_position_x, rand_position_y))
        self.mask = pg.mask.from_surface(self.image)

    def update(self):

        self.movement()
        self.garbage()

    def movement(self):

        self.rect.x -= self.move_speed

    def animation(self):

        # change enemy_01_frame_index: from 0 to 1 or form 1 to 0
        self.frame_index += 1
        if self.frame_index > len(self.frames) - 1:
            self.frame_index = 0

        # update enemy_01 surface
        self.image = self.frames[self.frame_index]

    def garbage(self):

        # destroy enemy sprite
        if self.rect.x < -100:
            self.kill()


class Heart(pg.sprite.Sprite):

    def __init__(self, heart_counter):
        super().__init__()

        # heart frames, image and rect
        frame1 = pg.image.load('graphics/soldier_heart1.png')
        frame2 = pg.image.load('graphics/soldier_heart7.png')
        self.frames = [frame1, frame2]
        self.frame_index = 0  # 0: void, 1: full
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(100 + 100 * heart_counter, 750))

    def update(self):
        pass

    def empty_heart(self):
        self.image = self.frames[-1]

    def full_heart(self):
        self.image = self.frames[0]


class Action(Enum):
    ON_GROUND = 1
    JUMPING = 2
    # FALLING = 3  # not used


class Game(Enum):
    START = 1
    OVER = 2
    WON = 3
    DAY_1 = 4
    DAY_2 = 5
    DAY_3 = 6
    NEXT = 7


def main():
    #########################################################################################
    # game mode: GAME INIT
    #########################################################################################
    pg.init()

    # set to True for game over / False for game active
    game_mode = Game.START  # default
    game_day = Game.DAY_1  # default

    # initialize game score
    game_score = 0

    # set game title
    pg.display.set_caption('pininos')

    # create fonts
    game_font_small = pg.font.Font('font/Pixeltype.ttf', 50)
    game_font_big = pg.font.Font('font/Pixeltype.ttf', 200)

    # create clock object to control the frame rates
    game_clock = pg.time.Clock()

    # initialize last collision time
    cooldown_time = 1000  # in milliseconds
    last_collision_time = pg.time.get_ticks() - cooldown_time

    # for background music
    play_music = True  # default True

    # declare hero group and hero
    hero = pg.sprite.GroupSingle()
    hero.add(Hero())

    # declare heart group (hero life)
    heart_group = pg.sprite.Group()
    for heart in range(HERO_LIFE):
        heart_group.add(Heart(heart))

    # declare enemy group
    enemy_group = pg.sprite.Group()

    # timers hero standing animation
    timer_hero_standing_animation = pg.USEREVENT + 1  # +1 is used to avoid conflicts with pygame user events
    pg.time.set_timer(timer_hero_standing_animation, 200)  # tigger event in x ms

    # timers enemy_01 spawn
    timer_enemy_01_spawn = pg.USEREVENT + 2  # +2 is used to avoid conflicts with pygame user events
    pg.time.set_timer(timer_enemy_01_spawn, test_spawn_time)  # tigger event in x ms (default)

    # timers enemy_01 animation
    timer_enemy_01_animation = pg.USEREVENT + 3  # +3 is used to avoid conflicts with pygame user events
    pg.time.set_timer(timer_enemy_01_animation, 200)  # tigger event in x ms

    # game loop
    while True:
        # start measuring time
        start_time = pg.time.get_ticks()

        #####################################################################################
        # game mode: EVENTS
        #####################################################################################
        # loop through events
        for event in pg.event.get():

            # EVENT: QUIT BUTTON
            if event.type == pg.QUIT:  # QUIT = x button of the window
                pg.quit()
                exit() # to close the while: True loop

            # TIMER EVENT: HERO STANDING ANIMATION
            if event.type == timer_hero_standing_animation \
                    and (game_mode == Game.DAY_1 or game_mode == Game.DAY_2 or game_mode == Game.DAY_3) \
                    and hero.sprite.action == Action.ON_GROUND \
                    and hero.sprite.jump_force == 0:  # to avoid conflict with crouch animation

                # update hero image
                hero.sprite.standing()

            # TIMER EVENT: ENEMY_01 SPAWN
            if event.type == timer_enemy_01_spawn \
                    and (game_mode == Game.DAY_1 or game_mode == Game.DAY_2 or game_mode == Game.DAY_3):

                # add new element to enemy group
                enemy_group.add(Enemy('enemy_01', game_mode))

            # TIMER EVENT: ENEMY_01 ANIMATION
            if event.type == timer_enemy_01_animation \
                    and (game_mode == Game.DAY_1 or game_mode == Game.DAY_2 or game_mode == Game.DAY_3):

                # enemy animation
                if len(enemy_group.sprites()) == 0:
                    pass
                else:
                    for enemy in enemy_group.sprites():
                        enemy.animation()

        #####################################################################################
        # game mode: GAME WON
        #####################################################################################
        if game_mode == Game.WON:
            # colors
            fill_color = 'lightyellow'
            text_color = 'orange'
            text_message = f"GAME {game_mode.name}"

            if play_music:
                pg.mixer.music.load("audio/cinematic-dramatic-11120.mp3")
                pg.mixer.music.play(-1)
                text_music = "Music by AleXZavesa from Pixabay"
                play_music = False

            # black screen
            SCREEN.fill(fill_color)

            # game over text (big font)
            game_mode_text = game_font_big.render(text_message, True, text_color)
            game_mode_rect = game_mode_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            SCREEN.blit(game_mode_text, game_mode_rect)

            # restart text (small font)
            game_restart_text = game_font_small.render(f"press ENTER to restart", True, text_color)
            game_restart_rect = game_restart_text.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 100))
            SCREEN.blit(game_restart_text, game_restart_rect)

            # print music credit
            text_screen = game_font_small.render(text_music, False, text_color)
            SCREEN.blit(text_screen, (1000, 750))

            # Get the state of the keyboard
            keys = pg.key.get_pressed()

            # press keyboard left
            if keys[pg.K_RETURN]:
                play_music = True  # restart music
                game_mode = Game.START  # restart game

        #####################################################################################
        # game mode: GAME START/OVER/NEXT
        #####################################################################################
        if game_mode == Game.START or game_mode == Game.OVER or game_mode == Game.NEXT:

            # colors
            if game_mode == Game.START:
                fill_color = 'lightblue'
                text_color = 'blue'
                text_message = "PININOS' a game of JUMPS!!"

                if play_music:
                    pg.mixer.music.load("audio/chill-abstract-intention-12099.mp3")
                    pg.mixer.music.play(-1)  # -1 to play it continuosly
                    text_music = "Music by Coma-Media from Pixabay"
                    play_music = False

            elif game_mode == Game.OVER:
                fill_color = 'black'
                text_color = 'red'
                text_message = f"GAME {game_mode.name}"

                if play_music:
                    pg.mixer.music.load("audio/76376__deleted_user_877451__game_over.wav")
                    pg.mixer.music.play()
                    text_music = "Sound by deleted_user_877451"
                    play_music = False

            else:  # game_mode = Game.NEXT
                fill_color = 'lightyellow'
                text_color = 'orange'
                text_message = "NEXT LEVEL"

            # black screen
            SCREEN.fill(fill_color)

            # game over text (big font)
            game_mode_text = game_font_big.render(text_message, True, text_color)
            game_mode_rect = game_mode_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            SCREEN.blit(game_mode_text, game_mode_rect)

            # restart text (small font)
            game_restart_text = game_font_small.render(f"press SPACE to continue", True, text_color)
            game_restart_rect = game_restart_text.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 100))
            SCREEN.blit(game_restart_text, game_restart_rect)

            # print music credit
            text_screen = game_font_small.render(text_music, False, text_color)
            SCREEN.blit(text_screen, (1000, 750))

            # restart hero life
            hero.sprite.heart_counter = HERO_LIFE
            for heart in range(HERO_LIFE):
                heart_group.sprites()[heart].full_heart()

            # restart enemy_01 rectangle list
            enemy_group.empty()

            # Get the state of the keyboard
            keys = pg.key.get_pressed()

            # press keyboard left
            if keys[pg.K_SPACE]:

                # restart hero and enemies position
                hero.sprite.rect.x = HERO_X_START_POS
                hero.sprite.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                # enemy_02_rect.x = 1000

                # restart jump parameters
                hero.sprite.jump_velocity = 0
                hero.sprite.jump_timer = 0
                hero.sprite.jump_pixel = 0

                # reset game score
                game_score = 0

                # restart background music
                play_music = True

                # restart game
                if game_mode == Game.NEXT:
                    if game_day == Game.DAY_1:
                        game_mode = Game.DAY_2
                    elif game_day == Game.DAY_2:
                        game_mode = Game.DAY_3
                else:
                    game_mode = game_day  # continue from current day

                # set enemy spawn timer depending on the day
                pg.time.set_timer(timer_enemy_01_spawn, globals()[f'ENEMY_SPAWN_TIME_{game_mode.name}'])

        #####################################################################################
        # game mode: GAME ACTIVE
        #####################################################################################
        elif game_mode == Game.DAY_1 or game_mode == Game.DAY_2 or game_mode == Game.DAY_3:

            # PLAY MUSIC  ###################################################################

            # play/stop background music
            if play_music:
                if game_mode == Game.DAY_1:
                    pg.mixer.music.load("audio/chill-ambient-11322.mp3")
                    pg.mixer.music.play(-1)
                    text_music = "Music by Coma-Media from Pixabay"
                    play_music = False

                elif game_mode == Game.DAY_2:
                    pg.mixer.music.load("audio/middle-east-127104.mp3")
                    pg.mixer.music.play(-1)
                    text_music = "Music by AlexiAction from Pixabay"
                    play_music = False

                elif game_mode == Game.DAY_3:
                    pg.mixer.music.load("audio/sinister-night-halloween-trap-hip-hop-music-121202.mp3")
                    pg.mixer.music.play(-1)
                    text_music = "Music by SoulProdMusic from Pixabay"
                    play_music = False

            # DRAW SURFACES #################################################################

            # create horizon surface
            horizon_surf = pg.image.load(f'graphics/horizont_{game_mode.name}.png').convert()

            # draw background
            SCREEN.blit(horizon_surf, (0, 0))

            # draw hero using sprites
            hero.draw(SCREEN)
            hero.update()

            # # hero mask image (only for testing)
            # mask = hero.sprite.mask
            # mask_surface = mask.to_surface()
            # screen.blit(mask_surface, (0, 600))

            # draw heart (hero life)
            heart_group.draw(SCREEN)

            # draw enemy group
            enemy_group.draw(SCREEN)
            enemy_group.update()

            # COLLISIONS  ###################################################################

            current_time = pg.time.get_ticks()
            # check cooldown time
            if current_time - last_collision_time > cooldown_time:
                # check hero collision with enemy group rect
                if pg.sprite.spritecollide(hero.sprite, enemy_group, False):
                    # check hero collision with enemy group mask
                    if pg.sprite.spritecollide(hero.sprite, enemy_group, False, pg.sprite.collide_mask):

                        # reduce hero life
                        hero.sprite.heart_counter -= 1
                        heart_group.sprites()[hero.sprite.heart_counter].empty_heart()
                        if hero.sprite.heart_counter == 0:
                            game_day = game_mode  # save game day
                            game_mode = Game.OVER  # GAME OVER!
                            play_music = True  # to change background music

                        # save collision time (for cooldown time)
                        last_collision_time = current_time

                        # print collision text (only for testing)
                        text_collision = game_font_small.render('ENEMY COLLISION!', False, 'Red')
                        SCREEN.blit(text_collision, (600, 90))

            # GAME SCORE  ###################################################################

            # count game score
            # if len(enemy_group) > 0:
            for enemy in enemy_group.sprites():
                if hero.sprite.rect.bottom < enemy.rect.top \
                    and enemy.rect.x < hero.sprite.rect.x < enemy.rect.x + 50 \
                        and not enemy.hero_dodge:

                    game_score += 1
                    enemy.hero_dodge = True  # to avoid more than one score increment

            # win score selection
            if game_score >= GAME_WIN_SCORE:
                if game_mode == Game.DAY_3:
                    play_music = True  # to change background music
                    game_day = Game.DAY_1
                    game_mode = Game.WON  # GAME END!
                else:
                    game_day = game_mode  # save day for next level
                    game_mode = Game.NEXT

            # GRID LINES  ###################################################################

            # Draw the horizontal lines of the grid
            for y in range(0, SCREEN_HEIGHT, 50):
                pg.draw.line(SCREEN, 'Black', (0, y), (SCREEN_WIDTH, y))

            # Draw the vertical lines of the grid
            for x in range(0, SCREEN_WIDTH, 50):
                pg.draw.line(SCREEN, 'Black', (x, 0), (x, SCREEN_HEIGHT))

            # TEXT MESSAGES #################################################################

            # print hero action on screen
            text_screen = game_font_small.render(f'Action mode: {hero.sprite.action.name}', False, 'Black')
            SCREEN.blit(text_screen, (10, 10))

            # print jump force list on screen
            text_screen = game_font_small.render(f'JUMP force: {hero.sprite.jump_force}', False, 'Black')
            SCREEN.blit(text_screen, (10, 50))

            # print game score list on screen
            text_screen = game_font_small.render(f'JUMP timer: {hero.sprite.jump_timer}', False, 'Black')
            SCREEN.blit(text_screen, (10, 90))

            # print heart_counter text
            text_collision = game_font_small.render(f'HERO life: {hero.sprite.heart_counter}', False, 'Black')
            SCREEN.blit(text_collision, (600, 10))

            # print enemy list on screen
            text_screen = game_font_small.render(f'ENEMY group members: {len(enemy_group.sprites())}', False, 'Black')
            SCREEN.blit(text_screen, (600, 50))

            # print game score on screen
            text_screen = game_font_small.render(f'Score: {game_score}', False, 'Black')
            SCREEN.blit(text_screen, (1200, 10))

            # print music credit
            text_screen = game_font_small.render(text_music, False, 'Black')
            SCREEN.blit(text_screen, (1000, 750))

            # # print execution time
            frame_time = pg.time.get_ticks() - start_time  # measure the time elapsed since the last frame
            text_screen = game_font_small.render(f'Total time: {pg.time.get_ticks()} ms', False, 'Black')
            SCREEN.blit(text_screen, (1200, 50))

            # PERFORMANCE ###################################################################

            # # only for performance test
            # cycle_time.append(frame_time)
            # if pg.time.get_ticks() > test_time_limit:
            #     # save performance values to csv
            #     my_array = np.array(cycle_time)
            #     col_names = ['cycle_time']
            #     pd.DataFrame(my_array, columns=col_names).to_csv(f'performance/'
            #                                                      f'python_{sys.version}'
            #                                                      f'_spawn_time_{test_spawn_time}_ms'
            #                                                      f'_test_time_{test_time_limit}_ms.csv')
            #     pg.quit()
            #     exit()

        # LOOP END ##########################################################################

        # # Show frame rate in title bar
        # fps = game_clock.get_fps()
        # pg.display.set_caption(f"My Game - FPS: {fps:.2f}")

        # update everything
        pg.display.update()
        game_clock.tick(60)  # ceiling limit of 60 fps


def performance():
    pg.quit()  # use to avoid error by pygame screen open

    # read csv files
    df_310 = pd.read_csv('performance/'
                         'python_3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0]_spawn_time_1_ms_test_time_50000.csv')
    df_311 = pd.read_csv('performance/'
                         'python_3.11.3 (main, Apr  5 2023, 14:14:37) [GCC 11.3.0]_spawn_time_1_ms_test_time_50000.csv')

    # plot the two dataframes on the same figure
    fig, ax = plt.subplots()
    df_310.plot(y='cycle_time', ax=ax, label='python_3.10')
    df_311.plot(y='cycle_time', ax=ax, label='python_3.11')

    # set the plot title and labels
    ax.set_title(f'timer_enemy_01_spawn = {test_spawn_time} ms | pg.time.get_ticks() > {test_time_limit} | '
                 f'game_clock.tick(60)')
    ax.set_xlabel('cycle number')
    ax.set_ylabel('cycle time (ms)')

    # # set the axis limits
    # ax.set_xlim([0, 1000])
    # ax.set_ylim([0, 25])

    plt.show()


if __name__ == '__main__':
    main()
    # performance()
