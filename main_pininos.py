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
text_surface = text_font.render('My game', False, 'Black')

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

# game loop
while True:
    # loop through events
    for event in pg.event.get():
        # QUIT = x button of the window
        if event.type == pg.QUIT:
            pg.quit()
            exit()  # to close the while: True loop

    # draw background
    screen.blit(sky_surf, (0, 0))  # (x, y) position
    screen.blit(ground_surf, (0, height - 200))

    # draw hero
    screen.blit(hero_surf, hero_rect)
    if hero_rect.left > width: hero_rect.left = 0

    # draw enemy_01
    screen.blit(enemy_01_surf, enemy_01_rect)

    # draw enemy_02
    screen.blit(enemy_02_surf, enemy_02_rect)

    # # draw text
    # screen.blit(text_surface, (25, 25))

    # update everything
    pg.display.update()
    clock.tick(60)  # ceiling limit of 60 fps
