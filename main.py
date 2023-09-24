from stringprep import c22_specials
import pygame
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# class of colors
class Color:
    white = (255,255,255)
    black = (0,0,0)

class PetState(Enum):
    Happy = 1
    Idle = 2
    Item = 3

# Create a Pet class
class Pet:
    def __init__(self, x, y):
        self.energy = 100
        self.current_frame = 0  # Current frame index
        self.animation_delay = 200  # Delay between frame changes in milliseconds
        self.last_frame_update = pygame.time.get_ticks()
        self.x = x  # Initial x position
        self.y = y  # Initial y position
        self.scale = 10
        self.image = get_image(character_idle_sheet,0,16,16,10)
        self.state = PetState.Idle

    def decrease_energy(self):
        self.energy -= 1
        if self.energy < 0:
            self.energy = 0

    def feed(self):
        print("feeding time")
        self.energy = 100

    def start_work(self):
        # TODO
        print("working time")
        pass

    def update(self):
        self.decrease_energy()

        # Update the animation frame if enough time is passed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update > self.animation_delay:
            # change states
            random_state = random.randint(0,10)
            if random_state == 0:
                print('happy')
                self.state = PetState.Happy
            else:
                print('idle')
                self.state = PetState.Idle

            # change anim based on states
            random_frame = random.randint(0,3)
            if(self.state == PetState.Idle):
                # toggle idle animation frames
                if random_frame == 0:
                    self.image = get_image(character_idle_sheet, 1 ,16,16,self.scale)
                else:
                    self.image = get_image(character_idle_sheet, 0 ,16,16,self.scale)
            elif(self.state == PetState.Happy):
                # toggle happy animation frames
                if random_frame == 0:
                    self.image = get_image(character_happy_idle_sheet, 1 ,16,16,self.scale)
                else:
                    self.image = get_image(character_happy_idle_sheet, 0 ,16,16,self.scale)


# Create buttons
class Button:
    def __init__(self, x, y, image_path, action):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ---Constants---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = Color.white
PET_UPDATE_INTERVAL = 750  # Pet updates energy every x*1000 seconds
# Set up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Devagotchi Game")

# Load pet images to memory
character_idle_sheet = pygame.image.load('Assets/character_idle.png').convert_alpha()
character_happy_idle_sheet = pygame.image.load('Assets/happy_idle.png').convert_alpha()

def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width,height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0,0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image
 

# ---Create Assets---
# Buttons
coffee_button = Button(100, 450, "Assets/item_coffee.png", Pet.feed)
contract_button = Button(300, 450, "Assets/item_scroll.png", Pet.start_work)
# Player
pet = Pet(400,300)
frame_0 = get_image(character_idle_sheet, 0, 16, 16, 10)
frame_1 = get_image(character_idle_sheet, 1, 16, 16, 10)

# Main game loop
clock = pygame.time.Clock()

running = True
last_update_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if coffee_button.rect.collidepoint(event.pos):
                pet.feed()
            if contract_button.rect.collidepoint(event.pos):
                pet.start_work()

    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > PET_UPDATE_INTERVAL:
        pet.update()
        last_update_time = current_time

    screen.fill(BACKGROUND_COLOR)

    # blit pets animation frames
    
    screen.blit(pet.image, (0,0))


    # Draw buttons
    coffee_button.draw(screen)
    contract_button.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
