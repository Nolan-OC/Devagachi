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

# Load pet images
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
        # Implement the feeding logic (e.g., increase energy)
        self.energy = 100

    def start_event(self):
        # Implement the special event logic
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
    def __init__(self, x, y, width, height, color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

coffee_button = Button(100, 450, 150, 50, (255, 0, 0), "Coffee", Pet.feed)
contract_button = Button(300, 450, 150, 50, (0, 0, 255), "Contract", Pet.start_event)

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
                pet.start_event()

    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > PET_UPDATE_INTERVAL:
        pet.update()
        last_update_time = current_time

    screen.fill(BACKGROUND_COLOR)
    # Draw the pet
    # blit your pet's image or animation frames
    current_frame_rect = frame_rectangles[pet.current_frame]
    screen.blit(sprite_sheet, (pet.x, pet.y), current_frame_rect)

    # Draw buttons
    coffee_button.draw(screen)
    contract_button.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
