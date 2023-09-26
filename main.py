from stringprep import c22_specials
import pygame
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# class of colors
class Color:
    white = (255,255,255)
    grey_light = (180,180,180)
    grey = (125,125,125)
    black = (0,0,0)

class State(Enum):
    Idle = 1
    Happy = 2
    Item = 3
    Working = 4

class Computer:
    def __init__(self, x, y):
        self.animation_delay = 200  # Delay between frame changes in milliseconds
        self.last_frame_update = pygame.time.get_ticks()
        self.x = x  # Initial x position
        self.y = y  # Initial y position
        self.scale = 5
        self.image = get_image(computer_idle_sheet,0,32,32,self.scale)
        self.state = State.Idle
        self.current_frame = 0   #current frame of sprite sheet
        self.total_frames = 0      #how many cycles to lock state change

    def start_work(self):
        self.change_state(State.Working,12)
        print("working time")

    def change_state(self, new_state, total_frames):
        self.current_frame = 0
        self.total_frames = total_frames
        self.state = new_state

    def update(self):
        # Update the animation frame if enough time is passed
        current_time = pygame.time.get_ticks()
        print(f"state: {self.state.name}, frame:{self.current_frame}/{self.total_frames}")
        if current_time - self.last_frame_update > self.animation_delay:
            # change states
            if self.total_frames <= self.current_frame:
                self.change_state(State.Idle,2)

            if(self.state == State.Idle):
                self.image = get_image(computer_idle_sheet, self.current_frame%2 ,32,32,self.scale)
            elif(self.state == State.Working):
                    self.image = get_image(computer_work_sheet, self.current_frame%12 ,32,32,self.scale)

            self.current_frame += 1
        

# Create a Pet class
class Pet:
    def __init__(self, x, y):
        self.energy = 100
        self.animation_delay = 200  # Delay between frame changes in milliseconds
        self.last_frame_update = pygame.time.get_ticks()
        self.x = x  # Initial x position
        self.y = y  # Initial y position
        self.scale = 10
        self.image = get_image(character_idle_sheet,0,16,16,10)
        self.state = State.Idle
        self.current_frame = 0   #current frame of sprite sheet
        self.total_frames = 0      #how many cycles to lock state change

    def decrease_energy(self):
        self.energy -= 1
        if self.energy < 0:
            self.energy = 0

    def feed(self):
        print("feeding time")
        self.change_state(State.Item,2)
        self.energy = 100

    def start_work(self):
        self.change_state(State.Working,12)
        print("working time")

    def change_state(self, new_state, total_frames):
        self.current_frame = 0
        self.total_frames = total_frames
        self.state = new_state

    def update(self):
        self.decrease_energy()
        # Update the animation frame if enough time is passed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update > self.animation_delay:
            # change states
            if self.total_frames <= self.current_frame:
                random_state = random.randint(0,10)
                if random_state == 0:
                    self.change_state(State.Happy,2)
                else:
                    self.change_state(State.Idle,2)

            #change anim based on states
            random_frame = random.randint(0,3)
            if(self.state == State.Idle):
                # toggle idle animation frames
                if random_frame == 0:
                    self.image = get_image(character_idle_sheet, 1 ,16,16,self.scale)
                else:
                    self.image = get_image(character_idle_sheet, 0 ,16,16,self.scale)

            elif(self.state == State.Happy):
                # toggle happy animation frames
                if random_frame == 0:
                    self.image = get_image(character_happy_idle_sheet, 1 ,16,16,self.scale)
                else:
                    self.image = get_image(character_happy_idle_sheet, 0 ,16,16,self.scale)

            elif(self.state == State.Item):
                self.image = get_image(character_item_image,0,16,16,self.scale)

            elif(self.state == State.Working):
                
                self.image = get_image(character_work_sheet, self.current_frame%4, 16, 16, self.scale)

            self.current_frame += 1


# Create buttons
class Button:
    def __init__(self, x, y, image_path, action, bg_color):
        self.image = get_image(pygame.image.load(image_path), 0, 32, 32, 7)
        self.bg_color = bg_color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (self.rect.x, self.rect.y, 204, 204))
        screen.blit(self.image, self.rect)

def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width,height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0,0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image
# ---Constants---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = Color.grey
PET_UPDATE_INTERVAL = 750  # Pet updates energy every x*1000 seconds
# Set up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Devagotchi Game")

# Load  images to memory
character_idle_sheet = pygame.image.load('Assets/character_idle.png').convert_alpha()
character_happy_idle_sheet = pygame.image.load('Assets/happy_idle.png').convert_alpha()
character_item_image = pygame.image.load('Assets/character_item_received.png').convert_alpha()
character_work_sheet = pygame.image.load('Assets/character_working.png').convert_alpha()

computer_idle_sheet = pygame.image.load('Assets/computer_idle.png').convert_alpha()
computer_work_sheet = pygame.image.load('Assets/computer_work.png').convert_alpha()

keyboard_image = pygame.image.load('Assets/keyboard.png').convert_alpha()

# ---Create Assets---
# Buttons
coffee_button = Button(0, 0, "Assets/item_coffee.png", Pet.feed, Color.grey_light)
contract_button = Button(270, 0, "Assets/item_scroll.png", Pet.start_work, Color.grey_light)
# Player
pet = Pet(250,300)
computer = Computer(400,300)

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
                computer.start_work()

    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > PET_UPDATE_INTERVAL:
        pet.update()
        computer.update()
        last_update_time = current_time

    screen.fill(BACKGROUND_COLOR)

    # blit pets animation frames
    screen.blit(pet.image, (pet.x, pet.y))
    screen.blit(computer.image, (computer.x, computer.y))

    # blit static images
    coffee_button.draw(screen)
    contract_button.draw(screen)
    if(pet.state ==  State.Working):
        screen.blit(get_image(keyboard_image, 0, 32, 132, 10), (pet.x+1, pet.y+1))
        
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
