import pygame as pg
from sys import exit

# game init
pg.init()

# screen setup
width = 1600
height = 800
screen = pg.display.set_mode((width, height))  # canvas for everything!

# set game title
pg.display.set_caption('pininos')

# create fonts
game_active_font = pg.font.Font('font/Pixeltype.ttf', 50)
game_over_font = pg.font.Font('font/Pixeltype.ttf', 200)

# create clock object to control the frame rates
game_clock = pg.time.Clock()

# create ground surface
ground_surf = pg.image.load('graphics/ground_1600x200.xcf').convert()
ground_rect = ground_surf.get_rect(bottomleft=(0, height))

# create sky surface
# sky_surface = pg.image.load('graphics/sky.png')
sky_surf = pg.Surface((width, height - ground_rect.height))
sky_surf.fill((0, 255, 255))  # cyan

# create hero surface/rectangle
# hero_surf = pg.image.load('graphics/hero_200x300.xcf').convert_alpha()
hero_surf = pg.image.load('graphics/soldier_256x256.png').convert_alpha()
hero_rect = hero_surf.get_rect(midbottom=(200, height - ground_rect.height))

# create enemy_01 surface/rectangle
enemy_01_surf = pg.image.load('graphics/enemy_01.xcf').convert_alpha()
enemy_01_rect = enemy_01_surf.get_rect(midbottom=(600, height - ground_rect.height))

# create enemy_02 surface/rectangle
# enemy_02_surf = pg.image.load('graphics/enemy_02.xcf').convert_alpha()
enemy_02_surf = pg.image.load('graphics/ogre_ia_scaled.png').convert_alpha()
enemy_02_rect = enemy_02_surf.get_rect(midbottom=(1000, height - ground_rect.height))

# create a surface to draw the attack on
attack_surf = pg.Surface((width, height), pg.SRCALPHA)

# set the time to display the attack
attack_display_time = 1000  # in milliseconds
attack_start_time = 0

# game parameters
move_speed = 10  # overall movement speed
jump_gravity = 10  # overall gravity (not realistic)
game_over = False  # set to True for game over

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

    # Game mode: game over
    if game_over:

        # black screen
        screen.fill('Black')

        # game over text (big font)
        text_game_over = game_over_font.render(f"GAME OVER", True, 'Red')
        game_over_rect = text_game_over.get_rect(center=(width/2, height/2))
        screen.blit(text_game_over, game_over_rect)

        # restart text (small font)
        text_game_restart = game_active_font.render(f"press SPACE to restart", True, 'Red')
        game_restart_rect = text_game_restart.get_rect(center=(width/2, (height/2)+100))
        screen.blit(text_game_restart, game_restart_rect)

        # Get the state of the keyboard
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_SPACE]:

            # restart hero and enemies position
            hero_rect.x = 200
            hero_rect.y = height - ground_rect.height
            enemy_02_rect.x = 1000

            # restart game
            game_over = False

    # Game mode: game active
    else:

        ## DRAW BACKGROUND #################################################################

        # draw background
        screen.blit(sky_surf, (0, 0))  # (x, y) position
        screen.blit(ground_surf, (0, height - ground_rect.height))

        ## MOUSE STATUS ####################################################################

        # Get the position of the mouse
        mouse_pos = pg.mouse.get_pos()

        # Create a text surface with the mouse position
        text_mouse_pos = game_active_font.render(f"Mouse position: {mouse_pos}", True, 'Black')
        screen.blit(text_mouse_pos, (10, 10))

        # Get the values of the mouse clicks
        mouse_val = pg.mouse.get_pressed()

        # Create a text surface with the mouse position
        text_mouse_val = game_active_font.render(f"Mouse pressed: {mouse_val}", True, 'Black')
        screen.blit(text_mouse_val, (10, 50))

        ## HERO MOVEMENT #################################################################

        # Get the state of the keyboard
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_LEFT]:
            hero_rect.x -= move_speed

        # press keyboard right
        elif keys[pg.K_RIGHT]:
            hero_rect.x += move_speed

        # reset position if screen limit is reached
        if hero_rect.left > width: hero_rect.right = 0  # redraw hero on left end
        if hero_rect.right < 0: hero_rect.left = width  # # redraw hero on right end

        # press keyboard up
        if keys[pg.K_UP]:
            # jump action
            text_action = game_active_font.render('Action mode: JUMP', False, 'Black')
            hero_rect.y -= jump_gravity  # positive y-axis is facing down
        else:
            # on ground action
            text_action = game_active_font.render('Action mode: ON GROUND', False, 'Black')
            if hero_rect.bottom >= height - ground_rect.height:
                hero_rect.bottom = height - ground_rect.height
            else:
                # falling action
                text_action = game_active_font.render('Action mode: FALLING', False, 'Black')
                hero_rect.y += 1.5 * jump_gravity

        # draw jump action in screen
        screen.blit(text_action, (10, 90))

        # draw hero
        screen.blit(hero_surf, hero_rect)

        ## HERO ATTACK #####################################################################

        # draw the circle surface on top of the screen surface (after draw background)
        screen.blit(attack_surf, (0, 0))

        # check if the circle has been displayed for long enough
        attack_delta_time = pg.time.get_ticks() - attack_start_time
        if attack_start_time is not None and attack_delta_time >= attack_display_time:

            # reset the start time and clear the circle surface
            attack_start_time = 0
            attack_surf.fill((0, 0, 0, 0))

        # Create a text surface with the mouse position (for testing only)
        text_attack_time = game_active_font.render(f"attack_start_time: {attack_start_time}", True, 'Black')
        screen.blit(text_attack_time, (1150, 10))
        ###
        text_attack_time = game_active_font.render(f"pg.time.get_ticks(): {pg.time.get_ticks()}", True, 'Black')
        screen.blit(text_attack_time, (1150, 50))
        ###
        text_attack_time = game_active_font.render(f"attack_delta_time: {attack_delta_time}", True, 'Black')
        screen.blit(text_attack_time, (1150, 90))

        ## ENEMIES MOVEMENT ################################################################

        # # draw enemy_01 (to be used later)
        # screen.blit(enemy_01_surf, enemy_01_rect)

        # draw enemy_02
        screen.blit(enemy_02_surf, enemy_02_rect)
        enemy_02_rect.left -= move_speed / 4  # slower than hero movement speed
        if enemy_02_rect.right < 0: enemy_02_rect.left = width

        ## COLLISION #######################################################################

        # hero collision with enemy_02!
        if hero_rect.colliderect(enemy_02_rect):
            text_collision = game_active_font.render('Enemy collision: GAME OVER!', False, 'Red')
            screen.blit(text_collision, (650, 10))
            game_over = True  # GAME OVER!

        # hero collision with mouse!
        if hero_rect.collidepoint(mouse_pos):
            text_collision = game_active_font.render('Mouse collision!', False, 'Red')
            screen.blit(text_collision, (650, 10))

    ## LOOP END ########################################################################

    # update everything
    pg.display.update()
    game_clock.tick(60)  # ceiling limit of 60 fps
