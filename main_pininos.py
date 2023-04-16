import pygame as pg
from sys import exit
from random import randint, choice  # choice will be used to random spawn different types of enemies
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
        self.action = Action.ON_GROUND

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

        # concatenate all animation frames
        self.frames = standing_frames + crouching_frames + jumping_frames
        self.frame_index = 0

        # create image and rect
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(200, screen_height - ground_rect.height))

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

        # only for testing
        self.draw_boundaries()

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
        if self.rect.left > screen_width: self.rect.right = 0  # redraw hero on left end
        if self.rect.right < 0: self.rect.left = screen_width  # # redraw hero on right end

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

            # crouching animation (dynamic)
            self.image, self.rect = self.resize_rect()

        elif not self.action == Action.JUMPING:

            # # play jump sound (only once)
            # if pg.mixer.get_busy() == 0 and self.jump_force > 0:
            #     self.jump_sound.play()

            # initiate jump timer > 0
            self.jump_velocity = self.jump_force
            self.jump_timer = 0.1
            self.action = Action.JUMPING
            self.jump_force = 0  # reset after key release

        else:
            # jumping animation
            self.frame_index = 12
            self.image = self.frames[self.frame_index]
            self.rect.height = 200  # reset rect height

        # update jump timer
        if self.jump_timer > 0 and self.action == Action.JUMPING:
            self.jump_timer += 0.5

        # jump in pixels
        self.jump_pixel = - self.jump_velocity * self.jump_timer + 0.5 * self.gravity * self.jump_timer ** 2
        self.rect.bottom = screen_height - ground_rect.height + self.jump_pixel

        # on ground action
        if self.rect.bottom >= screen_height - ground_rect.height:
            self.rect.bottom = screen_height - ground_rect.height
            self.jump_timer = 0  # reset jump timer
            self.action = Action.ON_GROUND

    def draw_boundaries(self):

        # draw the red rectangle within the boundary (only for testing)
        rect_x = self.rect.x
        rect_y = self.rect.y
        rect_width = self.rect.width
        rect_height = self.rect.height
        pg.draw.rect(screen, 'Red', pg.Rect(rect_x, rect_y, rect_width, rect_height), 4)

    def resize_rect(self):

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

    def __init__(self, type):
        super().__init__()

        # parameters
        self.move_speed = 5

        if type == 'enemy_01':

            # enemy_01 frames
            frame1 = pg.image.load('graphics/eye_sprite1.png').convert_alpha()
            frame2 = pg.image.load('graphics/eye_sprite2.png').convert_alpha()
            frame3 = pg.image.load('graphics/eye_sprite3.png').convert_alpha()
            frame4 = pg.image.load('graphics/eye_sprite2.png').convert_alpha()

            # concatenate frames
            self.frames = [frame1, frame2, frame3, frame4]
            self.frame_index = 0

        else:  # other type of enemy can be used here
            pass

        # obstacle appear at random position
        rand_position_x = randint(1200, 1800)
        rand_position_y = screen_height - ground_rect.height - randint(0, 300)

        # create Enemy_x image and rect
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(bottomright=(rand_position_x, rand_position_y))

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


class Action(Enum):

    ON_GROUND = 1
    JUMPING = 2
    # FALLING = 3  # not used


# game init
pg.init()

# set to True for game over / False for game active
game_over = False

# screen setup (global variables)
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

# declare hero group and hero
hero = pg.sprite.GroupSingle()
hero.add(Hero())

# hero action init
hero_action = Action.ON_GROUND

# declare enemy group
enemy_group = pg.sprite.Group()

# timers hero standing animation
timer_hero_standing_animation = pg.USEREVENT + 1  # + 2 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_hero_standing_animation, 200)  # tigger event in x ms

# timers enemy_01 spawn
timer_enemy_01_spawn = pg.USEREVENT + 2  # + 1 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_enemy_01_spawn, 1000)  # tigger event in x ms

# timers enemy_01 animation
timer_enemy_01_animation = pg.USEREVENT + 3  # + 2 is used to avoid conflicts with pygame user events
pg.time.set_timer(timer_enemy_01_animation, 200)  # tigger event in x ms

# game loop
while True:

    # loop through events
    for event in pg.event.get():

        ## EVENT: QUIT BUTTON ##########################################################
        if event.type == pg.QUIT:  # QUIT = x button of the window
            pg.quit()
            exit()  # to close the while: True loop

        ## TIMER EVENT: HERO STANDING ANIMATION ########################################
        if event.type == timer_hero_standing_animation \
                and not game_over \
                and hero.sprite.action == Action.ON_GROUND \
                and hero.sprite.jump_force == 0:  # to avoid conflict with crouch animation

            # update hero image
            hero.sprite.standing()

        ## TIMER EVENT: ENEMY_01 SPAWN #################################################
        if event.type == timer_enemy_01_spawn and not game_over:

            # add new element to enemy group
            enemy_group.add(Enemy('enemy_01'))

        ## TIMER EVENT: ENEMY_01 ANIMATION #############################################
        if event.type == timer_enemy_01_animation and not game_over:

            # enemy animation
            if len(enemy_group.sprites()) == 0:
                pass
            else:
                for enemy in enemy_group.sprites():
                    enemy.animation()

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
        enemy_group.empty()

        # Get the state of the keyboard
        keys = pg.key.get_pressed()

        # press keyboard left
        if keys[pg.K_SPACE]:

            # restart hero and enemies position
            hero.sprite.rect.x = 200
            hero.sprite.rect.bottom = screen_height - ground_rect.height
            # enemy_02_rect.x = 1000

            # restart jump parameters
            hero.sprite.jump_velocity = 0
            hero.sprite.jump_timer = 0
            hero.sprite.jump_pixel = 0

            # reset game score
            game_score = 0

            # restart game
            game_over = False

    ####################################################################################
    # game mode: GAME ACTIVE
    ####################################################################################
    else:

        # draw background
        screen.blit(sky_surf, (0, 0))  # (x, y) position
        screen.blit(ground_surf, (0, screen_height - ground_rect.height))

        # draw second hero using sprites
        hero.draw(screen)
        hero.update()

        # draws class Enemy
        enemy_group.draw(screen)
        enemy_group.update()

        # hero collision with enemy_group!
        if pg.sprite.spritecollide(hero.sprite, enemy_group, False):
            text_collision = game_active_font.render('Enemy collision: GAME OVER!', False, 'Red')
            screen.blit(text_collision, (600, 50))
            # game_over = True  # GAME OVER!

    ## SCORE AND GRID LINES ############################################################

    # # count game score
    # if hero_rect.bottom < enemy_01_rect.top and hero_rect.x > enemy_01_rect.x:
    #     game_score += 1

    # Draw the horizontal lines of the grid
    for y in range(0, screen_height, 50):
        pg.draw.line(screen, 'Black', (0, y), (screen_width, y))

    # Draw the vertical lines of the grid
    for x in range(0, screen_width, 50):
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

    # # print enemy list on screen
    # text_screen = game_active_font.render(f'ENEMY group elements: {len(enemy_group.sprites())}', False, 'Black')
    # screen.blit(text_screen, (600, 10))

    # # print game score on screen
    # text_screen = game_active_font.render(f'Score: {game_score}', False, 'Black')
    # screen.blit(text_screen, (10, 90))

    # update everything
    pg.display.update()
    game_clock.tick(60)  # ceiling limit of 60 fps
