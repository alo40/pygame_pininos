import pygame as pg
from sys import exit

# game init
pg.init()

# screen setup
width = 1600
height = 800
screen = pg.display.set_mode((width, height))  # (width, height)

# set game title
pg.display.set_caption('pininos')

# create font
text_font = pg.font.Font('font/Pixeltype.ttf', 50)

# create clock object to control the frame rates
clock = pg.time.Clock()

# create ground surface
ground_surf = pg.image.load('graphics/ground_1600x200.xcf').convert()
ground_rect = ground_surf.get_rect(bottomleft=(0, height))

# create sky surface
# sky_surface = pg.image.load('graphics/sky.png')
sky_surf = pg.Surface((width, height - ground_rect.height))
sky_surf.fill((0, 255, 255))  # cyan

# create hero surface/rectangle
hero_surf = pg.image.load('graphics/hero_200x300.xcf').convert_alpha()
hero_rect = hero_surf.get_rect(midbottom=(200, height - ground_rect.height))

# create enemy_01 surface/rectangle
enemy_01_surf = pg.image.load('graphics/enemy_01.xcf').convert_alpha()
enemy_01_rect = enemy_01_surf.get_rect(midbottom=(600, height - ground_rect.height))

# create enemy_02 surface/rectangle
enemy_02_surf = pg.image.load('graphics/enemy_02.xcf').convert_alpha()
enemy_02_rect = enemy_02_surf.get_rect(midbottom=(1000, height - ground_rect.height))

# game parameters
mov_speed = 2  # hero and enemies movement speed

# game loop
while True:
    # loop through events
    for event in pg.event.get():
        # QUIT = x button of the window
        if event.type == pg.QUIT:
            pg.quit()
            exit()  # to close the while: True loop

    ## DRAWING #######################################################################

    # draw background
    screen.blit(sky_surf, (0, 0))  # (x, y) position
    screen.blit(ground_surf, (0, height - ground_rect.height))

    # draw hero
    screen.blit(hero_surf, hero_rect)
    hero_rect.left += mov_speed
    if hero_rect.left > width: hero_rect.right = 0

    # # draw enemy_01 (to be used later)
    # screen.blit(enemy_01_surf, enemy_01_rect)

    # draw enemy_02
    screen.blit(enemy_02_surf, enemy_02_rect)
    enemy_02_rect.left -= mov_speed
    if enemy_02_rect.right < 0: enemy_02_rect.left = width

    ## MOUSE STATUS ####################################################################

    # Get the position of the mouse
    mouse_pos = pg.mouse.get_pos()

    # Create a text surface with the mouse position
    text_mouse_pos = text_font.render(f"Mouse position: {mouse_pos}", True, (0, 0, 0))
    screen.blit(text_mouse_pos, (10, 10))

    # Get the values of the mouse clicks
    mouse_val = pg.mouse.get_pressed()

    # Create a text surface with the mouse position
    text_mouse_pos = text_font.render(f"Mouse pressed: {mouse_val}", True, (0, 0, 0))
    screen.blit(text_mouse_pos, (10, 50))

    ## COLLISION #######################################################################

    # Create a text surface for collision text
    text_collision = text_font.render('COLLISION!', False, 'Red')

    # hero collision with enemy_02!
    if hero_rect.colliderect(enemy_02_rect):
        screen.blit(text_collision, (10, 90))

    # hero collision with mouse!
    if hero_rect.collidepoint(mouse_pos):
        screen.blit(text_collision, (10, 90))

    # update everything
    pg.display.update()
    clock.tick(60)  # ceiling limit of 60 fps
