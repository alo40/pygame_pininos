import pygame as pg
from sys import exit
from random import randint
from enum import Enum

# game init
pg.init()

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
# sky_surface = pg.image.load('graphics/sky.png')
sky_surf = pg.Surface((screen_width, screen_height - ground_rect.height))
sky_surf.fill('#EFBBEB')  # light purple

# create hero surface/rectangle
hero_surf = pg.image.load('graphics/soldier_simple.png').convert_alpha()
hero_surf = pg.transform.scale(hero_surf, (100, 200))
hero_rect = hero_surf.get_rect(midbottom=(200, screen_height - ground_rect.height))

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

# create a surface to draw the attack on
attack_surf = pg.Surface((screen_width, screen_height), pg.SRCALPHA)

# set the time to display the attack
attack_display_time = 2000  # in milliseconds
attack_start_time = 0

# timers enemy_01 spawn
timer_enemy_01_spawn = pg.USEREVENT + 1  # + 1 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_enemy_01_spawn, 1000)  # tigger event in x ms

# timers enemy_01 animation
timer_enemy_01_animation = pg.USEREVENT + 2  # + 2 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_enemy_01_animation, 200)  # tigger event in x ms

# game parameters
move_speed = 10  # overall movement speed
gravity = 10  # overall gravity (not realistic)
jump_velocity = 0
jump_timer = 0
jump_force = 0
jump_y = 0
game_over = False  # set to True for game over
game_score = 0

# hero actions (using Enum)
class action(Enum):
    ON_GROUND = 1
    JUMPING = 2
    FALLING = 3

# hero action init
hero_action = action.ON_GROUND

# game loop
while True:

    # loop through events
    for event in pg.event.get():

        ## EVENT: QUIT BUTTON ##########################################################
        if event.type == pg.QUIT:  # QUIT = x button of the window
            pg.quit()
            exit()  # to close the while: True loop

        ## EVENT: HERO ATTACK ##########################################################
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button

                # get the position of the mouse click
                mouse_pos = pg.mouse.get_pos()

                # draw the attack on the attack surface at the mouse position
                pg.draw.circle(attack_surf, 'Red', mouse_pos, 10)

                # set the start time for the attack display
                attack_start_time = pg.time.get_ticks()

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
            hero_rect.x = 200
            hero_rect.bottom = screen_height - ground_rect.height
            # enemy_02_rect.x = 1000

            # restart jump parameters
            jump_velocity = 0
            jump_timer = 0
            jump_y = 0

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

        # draw hero
        screen.blit(hero_surf, hero_rect)

        # Get the state of the keyboard
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_LEFT]:# and hero_action == action.ON_GROUND:
            hero_rect.x -= move_speed

        # press keyboard right
        elif keys[pg.K_RIGHT]:# and hero_action == action.ON_GROUND:
            hero_rect.x += move_speed

        # reset position if screen limit is reached
        if hero_rect.left > screen_width: hero_rect.right = 0  # redraw hero on left end
        if hero_rect.right < 0: hero_rect.left = screen_width  # # redraw hero on right end

        ## HERO MOVEMENT: JUMP #########################################################

        # # press keyboard up
        # if keys[pg.K_UP] and hero_action == action.ON_GROUND:
        #     jump_velocity = 80
        #     jump_time = 0.1  # initiate jump timer > 0
        #     hero_action = action.JUMPING

        # jump force
        if keys[pg.K_UP] and hero_action == action.ON_GROUND:
            jump_force += 2  # force increase as long key held press
            if jump_force > 100:
                jump_force = 100  # max jump force

        elif not hero_action == action.JUMPING:
            jump_velocity = jump_force
            jump_timer = 0.1  # initiate jump timer > 0
            hero_action = action.JUMPING
            jump_force = 0  # reset after key release

        # jump gravity
        jump_y = - jump_velocity * jump_timer + 0.5 * gravity * jump_timer ** 2
        hero_rect.bottom = screen_height - ground_rect.height + jump_y

        # update jump timer
        if jump_timer > 0 and not hero_action == action.ON_GROUND:
            jump_timer += 0.5

        # on ground action
        if hero_rect.bottom >= screen_height - ground_rect.height:
            hero_rect.bottom = screen_height - ground_rect.height
            jump_timer = 0  # reset jump timer
            hero_action = action.ON_GROUND

        ## HERO ANIMATION: JUMP ########################################################

        # if keys[pg.K_SPACE] and hero_action == action.ON_GROUND:
        #     print('animation!')
        #     hero_surf = pg.transform.scale(hero_surf, (100, 100))
        #     # hero_rect = hero_surf.get_rect(midbottom=(600, screen_height - ground_rect.height))

        ## HERO ATTACK #################################################################

        # draw the circle surface on top of the screen surface (after draw background)
        screen.blit(attack_surf, (0, 0))

        # check if the circle has been displayed for long enough
        attack_delta_time = pg.time.get_ticks() - attack_start_time
        if attack_start_time is not None and attack_delta_time >= attack_display_time:

            # reset the start time and clear the circle surface
            attack_start_time = 0
            attack_surf.fill((0, 0, 0, 0))

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
            if hero_rect.colliderect(enemy_01_rect_index):
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

    ## SCORE #######################################################################

    # count game score
    if hero_rect.bottom < enemy_01_rect.top and hero_rect.x > enemy_01_rect.x:
        game_score += 1

    # Draw the horizontal lines of the grid
    for y in range(0, screen_height, 100):
        pg.draw.line(screen, 'Black', (0, y), (screen_width, y))

    # Draw the vertical lines of the grid
    for x in range(0, screen_width, 100):
        pg.draw.line(screen, 'Black', (x, 0), (x, screen_height))

    ## LOOP END ########################################################################

    # print hero action on screen
    text_screen = game_active_font.render(f'Action mode: {hero_action.name}', False, 'Black')
    screen.blit(text_screen, (10, 10))

    # print jump force list on screen
    text_screen = game_active_font.render(f'JUMP force: {jump_force}', False, 'Black')
    screen.blit(text_screen, (10, 50))

    # print game score list on screen
    text_screen = game_active_font.render(f'JUMP timer: {jump_timer}', False, 'Black')
    screen.blit(text_screen, (10, 90))

    # # print game score list on screen
    # text_screen = game_active_font.render(f'Score: {game_score}', False, 'Black')
    # screen.blit(text_screen, (10, 90))

    # update everything
    pg.display.update()
    game_clock.tick(60)  # ceiling limit of 60 fps
