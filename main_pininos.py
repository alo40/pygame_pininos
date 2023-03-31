import pygame as pg
from sys import exit

# game init
pg.init()

# screen setup
width = 800
height = 400
screen = pg.display.set_mode((800, 400))  # (width, height)

# set game title
pg.display.set_caption('pininos')

# create font
text_font = pg.font.Font('font/Pixeltype.ttf', 50)
text_surface = text_font.render('My game', False, 'Black')

# create clock object to control the frame rates
clock = pg.time.Clock()

# create sky surface
# sky_surface = pg.image.load('graphics/sky.png')
sky_surface = pg.Surface((800, 350))
sky_surface.fill((0, 255, 255))  # cyan

# create ground surface
ground_surface = pg.image.load('graphics/ground.png').convert()

# create hero surface
hero_surface = pg.image.load('graphics/hero.png').convert_alpha()
hero_x_position = 200

# create enemy_01 surface
enemy_01_surface = pg.image.load('graphics/enemy_01.xcf').convert_alpha()
enemy_01_x_position = 100

# create enemy_02 surface
enemy_02_surface = pg.image.load('graphics/enemy_02.xcf').convert_alpha()
enemy_02_x_position = 500

# game loop
while True:
    # loop through events
    for event in pg.event.get():
        # QUIT = x button of the window
        if event.type == pg.QUIT:
            pg.quit()
            exit()  # to close the while: True loop

    # draw background
    screen.blit(sky_surface, (0, 0))  # (x, y) position
    screen.blit(ground_surface, (0, 350))

    # draw hero
    hero_x_position -= 4
    screen.blit(hero_surface, (hero_x_position, 40))
    if hero_x_position < -350: hero_x_position = 800

    # draw enemy_01
    screen.blit(enemy_01_surface, (enemy_01_x_position, 40))

    # draw enemy_02
    screen.blit(enemy_02_surface, (enemy_02_x_position, 40))

    # # draw text
    # screen.blit(text_surface, (25, 25))

    # update everything
    pg.display.update()
    clock.tick(60)  # ceiling limit of 60 fps
