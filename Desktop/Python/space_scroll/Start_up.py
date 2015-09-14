import pygame
import random
import math
pygame.init()
clock = pygame.time.Clock()


def deg_to_rad(degrees):
    return degrees / 180.0 * math.pi

# variables to control game states
home_state = 1
info_state = 2
game_state = 3
pause_state = 4
shop_state = 5
quit_state = 6

# colours used
main_theme = (0, 100, 100)
red = (100, 0, 0)

# game settings
show_notes = True
star_chance = 10  # chance of a star is 1 in 10 every update
initial_stars = 100  # create 100 stars to fill the screen
package_change = 10  # chance of a package drop is 1 in 10 every enemy kill
enemy_chance = 200  # chance of an enemy is 1 in 200 every update
enemy_health_max = 3  # limit this to 4 as i have only added 4 colours to the enemy class (add more in enemy class)
particle_count = 20  # amount of particles created when an enemy is killed
# if your game runs slow, set particle count and star chance higher

width = 800
height = 500
main_s = pygame.display.set_mode((width, height))
main_s.fill((255, 255, 255))
pygame.display.set_caption("SPACE SHIPS")
pygame.display.set_icon(pygame.image.load("Images/Icon.png"))
font = pygame.font.Font("./Font/tall bolder.ttf", 15)
menu_font = pygame.font.Font("./Font/tall bolder.ttf", 25)
title_font = pygame.font.Font("./Font/tall bolder.ttf", 45)

screen_rect = pygame.sprite.Sprite()
# screen_rect is slightly bigger than the screen so that objects do not get removed
# when created off screen. many objects are checked as still on screen to remove it
# from a list that it is in
screen_rect.rect = pygame.Surface((width + 30, height + 30)).get_rect()
screen_rect.rect.x = 0
screen_rect.rect.y = 0
