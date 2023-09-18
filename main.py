from itertools import filterfalse
from turtle import width
import os
import pygame
###
#   Make tomadachi game where I am the little developer in a room you can interact with
#   You can give him compliments or thumbs up, which are "tracked" by the site and displayed
#   You can offer him a job or send him a message both of which open up a message window to say something
#   Just simele things to grab attention
###

WIDTH, HEIGHT = 600,300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("devagotchi game")

FPS = 15

character_image = pygame.image.load(os.path.join('Assets', 'character.png'))
character_image = pygame.transform.scale(character_image, (75,75))

class Pet:
    """A developer in a box"""
    pos = (0,0)
    mood = 10
    max_mood = 10
    food = 10
    max_food = 10

class Item:
    """A consumable item"""
    pos = (0,0)
    response_dialogue = ("")

class Color:
    white = (255,255,255)
    black = (0,0,0)
    green = (0,255,0)

def draw_window():
    WIN.fill(Color.white)
    WIN.blit(character_image, (300,150))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()


    pygame.quit()

if __name__ == "__main__":
    main()