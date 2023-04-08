import pygame as pg
from sys import exit
from random import randint
from enum import Enum

class Hero(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # parameters
        self.move_speed = 10
        self.jump_force = 0
        self.jump_force_max = 100
        self.jump_timer = 0
        self.jump_velocity = 0
        self.jump_pixel = 0
        self.gravity = 10
        self.action = action.ON_GROUND

        # standing frames
        stand_01 = pg.image.load('graphics/soldier_simple_standing1.png').convert_alpha()
        stand_02 = pg.image.load('graphics/soldier_simple_standing2.png').convert_alpha()
        stand_03 = pg.image.load('graphics/soldier_simple_standing1.png').convert_alpha()
        stand_04 = stand_02
        standing_frames = [stand_01, stand_02, stand_03, stand_04]

        # crouching frames
        crouch_01 = pg.image.load('graphics/soldier_simple_jumping2.png').convert_alpha()
        crouch_02 = pg.image.load('graphics/soldier_simple_jumping3.png').convert_alpha()
        crouch_03 = pg.image.load('graphics/soldier_simple_jumping4.png').convert_alpha()
        crouch_04 = pg.image.load('graphics/soldier_simple_jumping5.png').convert_alpha()
        crouch_05 = pg.image.load('graphics/soldier_simple_jumping6.png').convert_alpha()
        crouch_06 = pg.image.load('graphics/soldier_simple_jumping7.png').convert_alpha()
        crouch_07 = pg.image.load('graphics/soldier_simple_jumping8.png').convert_alpha()
        crouch_08 = pg.image.load('graphics/soldier_simple_jumping9.png').convert_alpha()
        crouching_frames = [crouch_01, crouch_02, crouch_03, crouch_04,
                            crouch_05, crouch_06, crouch_07, crouch_08]

        # jumping frames
        jump_01 = pg.image.load('graphics/soldier_simple_jumping10.png').convert_alpha()  # jumping
        jumping_frames = [jump_01]

        self.frames = standing_frames + crouching_frames + jumping_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.image = pg.image.load('graphics/soldier_simple_standing1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(200, screen_height - ground_rect.height))

    # def animation(self):
    #     self.frame_index = 0
    #     self.image = self.frames[self.frame_index]

    def update(self):
        # self.standing()
        self.walking()
        self.jumping()

    def standing(self):

        # animation
        self.frame_index += 1
        if self.frame_index > 3:
            self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def walking(self):

        # global screen_width, screen_height

        # get key
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_LEFT]:
            self.rect.x -= self.move_speed

        # press keyboard right
        elif keys[pg.K_RIGHT]:
            self.rect.x += self.move_speed

        # reset position if screen limit is reached
        if self.rect.left > screen_width: self.rect.right = 0  # redraw hero on left end
        if self.rect.right < 0: self.rect.left = screen_width  # # redraw hero on right end

    def jumping(self):

        # get key
        keys = pg.key.get_pressed()

        # jump force
        if keys[pg.K_DOWN] and self.action == action.ON_GROUND:
            self.jump_force += 4  # force increase as long key held press
            if self.jump_force > self.jump_force_max:
                self.jump_force = self.jump_force_max

            # crouching animation
            self.frame_index = int(self.jump_force/self.jump_force_max * 8) + 3
            self.image = self.frames[self.frame_index]
            print(f'{self.frame_index}')

        elif not self.action == action.JUMPING:
            self.jump_velocity = self.jump_force
            self.jump_timer = 0.1  # initiate jump timer > 0
            self.action = action.JUMPING
            self.jump_force = 0  # reset after key release

        else:
            # jumping animation
            self.frame_index = 12
            self.image = self.frames[self.frame_index]

        # update jump timer
        if self.jump_timer > 0 and self.action == action.JUMPING:
            self.jump_timer += 0.5

        # jump in pixels
        self.jump_pixel = - self.jump_velocity * self.jump_timer + 0.5 * self.gravity * self.jump_timer ** 2
        self.rect.bottom = screen_height - ground_rect.height + self.jump_pixel

        # on ground action
        if self.rect.bottom >= screen_height - ground_rect.height:
            self.rect.bottom = screen_height - ground_rect.height
            self.jump_timer = 0  # reset jump timer
            self.action = action.ON_GROUND


# hero actions (using Enum)
class action(Enum):
    ON_GROUND = 1
    JUMPING = 2
    # FALLING = 3


# game init
pg.init()

# set to True for game over / False for game active
game_over = False

# screen setup
screen_width = 1600
screen_height = 800
screen = pg.display.set_mode((screen_width, screen_height))  # canvas for everything!

# set game title
pg.display.set_caption('pininos')

# create fonts
game_active_font = pg.font.Font('font/Pixeltype.ttf', 50)
game_over_font = pg.font.Font('font/Pixeltype.ttf', 200)

# create clock object to control the frame rates
game_clock = pg.time.Clock()

# create ground surface
ground_surf = pg.image.load('graphics/ground_1600x200.png').convert()
ground_rect = ground_surf.get_rect(bottomleft=(0, screen_height))

# create sky surface
sky_surf = pg.Surface((screen_width, screen_height - ground_rect.height))
sky_surf.fill('#EFBBEB')  # light purple

# declare hero
hero = pg.sprite.GroupSingle()
hero.add(Hero())

# hero action init
hero_action = action.ON_GROUND


# # create hero surface/rectangle
# hero_frame0 = pg.image.load('graphics/soldier_simple_standing1.png').convert_alpha()  # standing
# hero_frame1 = pg.image.load('graphics/soldier_simple_standing2.png').convert_alpha()  # standing
# hero_frame2 = pg.image.load('graphics/soldier_simple_standing3.png').convert_alpha()  # standing
# hero_frame3 = pg.image.load('graphics/soldier_simple_standing2.png').convert_alpha()  # standing
# hero_frame4 = pg.image.load('graphics/soldier_simple_jumping2.png').convert_alpha()  # crounching
# hero_frame5 = pg.image.load('graphics/soldier_simple_jumping3.png').convert_alpha()  # crounching
# hero_frame6 = pg.image.load('graphics/soldier_simple_jumping4.png').convert_alpha()  # crounching
# hero_frame7 = pg.image.load('graphics/soldier_simple_jumping5.png').convert_alpha()  # crounching
# hero_frame8 = pg.image.load('graphics/soldier_simple_jumping6.png').convert_alpha()  # crounching
# hero_frame9 = pg.image.load('graphics/soldier_simple_jumping7.png').convert_alpha()  # crounching
# hero_frame10 = pg.image.load('graphics/soldier_simple_jumping8.png').convert_alpha()  # crounching
# hero_frame11 = pg.image.load('graphics/soldier_simple_jumping9.png').convert_alpha()  # crounching
# hero_frame12 = pg.image.load('graphics/soldier_simple_jumping10.png').convert_alpha()  # jumping
# hero_frames = [hero_frame0, hero_frame1, hero_frame2, hero_frame3,  # standing
#                hero_frame4, hero_frame5, hero_frame6, hero_frame7,  # crounching
#                hero_frame8, hero_frame9, hero_frame10, hero_frame11,  # crounching
#                hero_frame12]  # jumping
# hero_frame_index = 0
# hero_surf = hero_frames[hero_frame_index]
# hero_rect = hero_surf.get_rect(midbottom=(200, screen_height - ground_rect.height))

# create enemy_01 surface/rectangle
enemy_01_frame1 = pg.image.load('graphics/eye_sprite1.png').convert_alpha()
enemy_01_frame2 = pg.image.load('graphics/eye_sprite2.png').convert_alpha()
enemy_01_frame3 = pg.image.load('graphics/eye_sprite3.png').convert_alpha()
enemy_01_frame4 = pg.image.load('graphics/eye_sprite2.png').convert_alpha()
enemy_01_frames = [enemy_01_frame1, enemy_01_frame2, enemy_01_frame3, enemy_01_frame4]
enemy_01_frame_index = 0
enemy_01_surf = enemy_01_frames[enemy_01_frame_index]
enemy_01_rect = enemy_01_surf.get_rect(midbottom=(600, screen_height - ground_rect.height))

# create enemy_01 rectangle list
enemy_01_rect_list = []

# # create enemy_02 surface/rectangle
# enemy_02_surf = pg.image.load('graphics/ogre_ia_simple.png').convert_alpha()
# enemy_02_rect = enemy_02_surf.get_rect(midbottom=(1000, height - ground_rect.height))

# # create a surface to draw the attack on
# attack_surf = pg.Surface((screen_width, screen_height), pg.SRCALPHA)

# # set the time to display the attack
# attack_display_time = 2000  # in milliseconds
# attack_start_time = 0

# timers hero standing animation
timer_hero_standing_animation = pg.USEREVENT + 1  # + 2 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_hero_standing_animation, 200)  # tigger event in x ms

# timers enemy_01 spawn
timer_enemy_01_spawn = pg.USEREVENT + 2  # + 1 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_enemy_01_spawn, 1000)  # tigger event in x ms

# timers enemy_01 animation
timer_enemy_01_animation = pg.USEREVENT + 3  # + 2 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_enemy_01_animation, 200)  # tigger event in x ms

# # game parameters
move_speed = 10  # overall movement speed
# gravity = 10  # overall gravity (not realistic)
# jump_velocity = 0
# jump_timer = 0
# jump_force = 0
# jump_y = 0
# game_score = 0


# game loop
while True:

    # loop through events
    for event in pg.event.get():

        ## EVENT: QUIT BUTTON ##########################################################
        if event.type == pg.QUIT:  # QUIT = x button of the window
            pg.quit()
            exit()  # to close the while: True loop

        # ## EVENT: HERO ATTACK ##########################################################
        # elif event.type == pg.MOUSEBUTTONDOWN:
        #     if event.button == 1:  # left mouse button
        #
        #         # get the position of the mouse click
        #         mouse_pos = pg.mouse.get_pos()
        #
        #         # draw the attack on the attack surface at the mouse position
        #         pg.draw.circle(attack_surf, 'Red', mouse_pos, 10)
        #
        #         # set the start time for the attack display
        #         attack_start_time = pg.time.get_ticks()

        ## TIMER EVENT: HERO STANDING ANIMATION ########################################
        if event.type == timer_hero_standing_animation \
                and not game_over \
                and hero.sprite.action == action.ON_GROUND \
                and hero.sprite.jump_force == 0:  # to avoid conflict with crounch animtation

            # # change hero_frame_index: from 0 to 1 or form 1 to 0
            # hero_frame_index += 1
            # if hero_frame_index > 3:
            #     hero_frame_index = 0
            #
            # # update hero surface
            # hero_surf = hero_frames[hero_frame_index]

            # update hero image
            hero.sprite.standing()

        ## TIMER EVENT: ENEMY_01 SPAWN #################################################
        if event.type == timer_enemy_01_spawn and not game_over:

            # obstacle appear at random position
            rand_position_x = randint(1200, 1800)
            rand_position_y = screen_height - ground_rect.height - randint(0, 300)
            enemy_01_rect_index = enemy_01_surf.get_rect(bottomright=(rand_position_x, rand_position_y))

            # append obstacle only if
            if not enemy_01_rect_list:  # empty list
                enemy_01_rect_list.append(enemy_01_rect_index)
            else:
                enemy_01_rect_list.append(enemy_01_rect_index)

                # remove enemy_01 if out of the screen (left side)
                for enemy_01 in enemy_01_rect_list:
                    if enemy_01.x < 0: enemy_01_rect_list.remove(enemy_01)

        ## TIMER EVENT: ENEMY_01 ANIMATION #############################################
        if event.type == timer_enemy_01_animation and not game_over:

            # change enemy_01_frame_index: from 0 to 1 or form 1 to 0
            enemy_01_frame_index += 1
            if enemy_01_frame_index > len(enemy_01_frames) - 1:
                enemy_01_frame_index = 0

            # update enemy_01 surface
            enemy_01_surf = enemy_01_frames[enemy_01_frame_index]


    ####################################################################################
    # game mode: GAME OVER
    ####################################################################################
    if game_over:

        # black screen
        screen.fill('Black')

        # game over text (big font)
        text_game_over = game_over_font.render(f"GAME OVER", True, 'Red')
        game_over_rect = text_game_over.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text_game_over, game_over_rect)

        # restart text (small font)
        text_game_restart = game_active_font.render(f"press SPACE to restart", True, 'Red')
        game_restart_rect = text_game_restart.get_rect(center=(screen_width / 2, (screen_height / 2) + 100))
        screen.blit(text_game_restart, game_restart_rect)

        # restart enemy_01 rectangle list
        enemy_01_rect_list = []

        # Get the state of the keyboard
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_SPACE]:

            # restart hero and enemies position
            hero.rect.x = 200
            hero.rect.bottom = screen_height - ground_rect.height
            # enemy_02_rect.x = 1000

            # restart jump parameters
            hero.jump_velocity = 0
            hero.jump_timer = 0
            hero.jump_pixel = 0

            # reset game score
            game_score = 0

            # restart game
            game_over = False

    ####################################################################################
    # game mode: GAME ACTIVE
    ####################################################################################
    else:

        ## BACKGROUND ##################################################################

        # draw background
        screen.blit(sky_surf, (0, 0))  # (x, y) position
        screen.blit(ground_surf, (0, screen_height - ground_rect.height))

        ## MOUSE STATUS ################################################################

        # # Get the position of the mouse
        # mouse_pos = pg.mouse.get_pos()
        #
        # # Create a text surface with the mouse position
        # text_mouse_pos = game_active_font.render(f"Mouse position: {mouse_pos}", True, 'Black')
        # screen.blit(text_mouse_pos, (10, 10))
        #
        # # Get the values of the mouse clicks
        # mouse_val = pg.mouse.get_pressed()
        #
        # # Create a text surface with the mouse position
        # text_mouse_val = game_active_font.render(f"Mouse pressed: {mouse_val}", True, 'Black')
        # screen.blit(text_mouse_val, (10, 50))

        ## HERO MOVEMENT: LEFT/RIGHT ###################################################

        # # draw hero
        # screen.blit(hero_surf, hero_rect)

        # draw second hero using sprites
        hero.draw(screen)
        hero.update()

        # # Get the state of the keyboard
        # keys = pg.key.get_pressed()
        #
        # # press keyboard left
        # if keys[pg.K_LEFT]:# and hero_action == action.ON_GROUND:
        #     hero_rect.x -= move_speed
        #
        # # press keyboard right
        # elif keys[pg.K_RIGHT]:# and hero_action == action.ON_GROUND:
        #     hero_rect.x += move_speed
        #
        # # reset position if screen limit is reached
        # if hero_rect.left > screen_width: hero_rect.right = 0  # redraw hero on left end
        # if hero_rect.right < 0: hero_rect.left = screen_width  # # redraw hero on right end

        ## HERO MOVEMENT: JUMP #########################################################

        # # jump force
        # if keys[pg.K_DOWN] and hero_action == action.ON_GROUND:
        #     jump_force += 3  # force increase as long key held press
        #     if jump_force > 100:
        #         jump_force = 100  # max jump force
        #
        #     # crounching animation
        #     if jump_force < 10:
        #         hero_frame_index = 4
        #     elif jump_force < 20:
        #         hero_frame_index = 5
        #     elif jump_force < 30:
        #         hero_frame_index = 6
        #     elif jump_force < 40:
        #         hero_frame_index = 7
        #     elif jump_force < 50:
        #         hero_frame_index = 8
        #     elif jump_force < 60:
        #         hero_frame_index = 9
        #     elif jump_force < 70:
        #         hero_frame_index = 10
        #     elif jump_force < 80:
        #         hero_frame_index = 11
        #     hero_surf = hero_frames[hero_frame_index]
        #
        # elif not hero_action == action.JUMPING:
        #     jump_velocity = jump_force
        #     jump_timer = 0.1  # initiate jump timer > 0
        #     hero_action = action.JUMPING
        #     jump_force = 0  # reset after key release
        #
        # # jump gravity
        # jump_y = - jump_velocity * jump_timer + 0.5 * gravity * jump_timer ** 2
        # hero_rect.bottom = screen_height - ground_rect.height + jump_y
        #
        # # on ground action
        # if hero_rect.bottom >= screen_height - ground_rect.height:
        #     hero_rect.bottom = screen_height - ground_rect.height
        #     jump_timer = 0  # reset jump timer
        #     hero_action = action.ON_GROUND
        #
        # # update jump timer
        # if jump_timer > 0 and hero_action == action.JUMPING:
        #     jump_timer += 0.5
        #
        #     # jumping animation
        #     hero_frame_index = 12
        #     hero_surf = hero_frames[hero_frame_index]

        ## HERO ATTACK #################################################################

        # # draw the circle surface on top of the screen surface (after draw background)
        # screen.blit(attack_surf, (0, 0))
        #
        # # check if the circle has been displayed for long enough
        # attack_delta_time = pg.time.get_ticks() - attack_start_time
        # if attack_start_time is not None and attack_delta_time >= attack_display_time:
        #
        #     # reset the start time and clear the circle surface
        #     attack_start_time = 0
        #     attack_surf.fill((0, 0, 0, 0))

        # # Create a text surface with the mouse position (for testing only)
        # text_attack_time = game_active_font.render(f"attack_start_time: {attack_start_time}", True, 'Black')
        # screen.blit(text_attack_time, (1150, 10))
        # ###
        # text_attack_time = game_active_font.render(f"pg.time.get_ticks(): {pg.time.get_ticks()}", True, 'Black')
        # screen.blit(text_attack_time, (1150, 50))
        # ###
        # text_attack_time = game_active_font.render(f"attack_delta_time: {attack_delta_time}", True, 'Black')
        # screen.blit(text_attack_time, (1150, 90))

        ## ENEMIES MOVEMENT ############################################################

        # draw enemy_01 and movement
        if enemy_01_rect_list:  # check if list is not empty
            for enemy_01_rect_index in enemy_01_rect_list:
                screen.blit(enemy_01_surf, enemy_01_rect_index)
                enemy_01_rect_index.x -= move_speed

        # # draw enemy_02 and movement
        # screen.blit(enemy_02_surf, enemy_02_rect)
        # enemy_02_rect.left -= move_speed / 4  # slower than hero movement speed
        # if enemy_02_rect.right < 0: enemy_02_rect.left = width

        ## COLLISION ###################################################################

        # hero collision with enemy_01!
        for enemy_01_rect_index in enemy_01_rect_list:
            if hero.sprite.rect.colliderect(enemy_01_rect_index):
                text_collision = game_active_font.render('Enemy collision: GAME OVER!', False, 'Red')
                screen.blit(text_collision, (650, 10))
                # game_over = True  # GAME OVER!

        # # hero collision with enemy_02!
        # if hero_rect.colliderect(enemy_02_rect):
        #     text_collision = game_active_font.render('Enemy collision: GAME OVER!', False, 'Red')
        #     screen.blit(text_collision, (650, 10))
        #     # game_over = True  # GAME OVER!

        # # hero collision with mouse!
        # if hero_rect.collidepoint(mouse_pos):
        #     text_collision = game_active_font.render('Mouse collision!', False, 'Red')
        #     screen.blit(text_collision, (650, 50))

    ## SCORE AND GRID LINES ############################################################

    # # count game score
    # if hero_rect.bottom < enemy_01_rect.top and hero_rect.x > enemy_01_rect.x:
    #     game_score += 1

    # Draw the horizontal lines of the grid
    for y in range(0, screen_height, 100):
        pg.draw.line(screen, 'Black', (0, y), (screen_width, y))

    # Draw the vertical lines of the grid
    for x in range(0, screen_width, 100):
        pg.draw.line(screen, 'Black', (x, 0), (x, screen_height))

    ## LOOP END ########################################################################

    # print hero action on screen
    text_screen = game_active_font.render(f'Action mode: {hero.sprite.action.name}', False, 'Black')
    screen.blit(text_screen, (10, 10))

    # print jump force list on screen
    text_screen = game_active_font.render(f'JUMP force: {hero.sprite.jump_force}', False, 'Black')
    screen.blit(text_screen, (10, 50))

    # print game score list on screen
    text_screen = game_active_font.render(f'JUMP timer: {hero.sprite.jump_timer}', False, 'Black')
    screen.blit(text_screen, (10, 90))

    # # print game score list on screen
    # text_screen = game_active_font.render(f'Score: {game_score}', False, 'Black')
    # screen.blit(text_screen, (10, 90))

    # update everything
    pg.display.update()
    game_clock.tick(60)  # ceiling limit of 60 fps
