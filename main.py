import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
PET_UPDATE_INTERVAL = 5000  # Pet updates energy every 5 seconds

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Devagotchi Game")

# Load pet images (replace with your pet's art assets)
# Example: pet_image = pygame.image.load("pet.png")
sprite_sheet = pygame.image.load("Assets/character_idle.png")
frame_width, frame_height = 32, 32
# Create a list of Rectangles for the animation frames
frame_rectangles = []
for x in range(0, sprite_sheet.get_width(), frame_width):
    frame_rect = pygame.Rect(x, 0, frame_width, frame_height)
    frame_rectangles.append(frame_rect)

# Create a Pet class
class Pet:
    def __init__(self, x, y):
        self.energy = 100
        self.current_frame = 0  # Current frame index
        self.animation_delay = 200  # Delay between frame changes in milliseconds
        self.last_frame_update = pygame.time.get_ticks()
        self.x = x  # Initial x position
        self.y = y  # Initial y position

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

        # Update the animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(frame_rectangles)
            self.last_frame_update = current_time

# Create buttons
class Button:
    def __init__(self, x, y, image_path, action):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)


coffee_button = Button(100, 450, "Assets/item_coffee.png", Pet.feed)
contract_button = Button(300, 450, "Assets/item_scroll.png", Pet.start_work)

# Main game loop
pet = Pet(400,300)
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
    # Draw the pet

    # blit animation frames
    current_frame_rect = frame_rectangles[pet.current_frame]
    screen.blit(sprite_sheet, (pet.x, pet.y), current_frame_rect)

    # Draw buttons
    coffee_button.draw(screen)
    contract_button.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
