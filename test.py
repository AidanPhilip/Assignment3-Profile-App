import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fading Circles')

# Define colors
brown = (139, 69, 19)
green = (0, 128, 0)

# Create surfaces for the circles
brown_circle = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(brown_circle, brown, (50, 50), 50)

green_circle = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(green_circle, (green[0], green[1], green[2], 255), (50, 50), 50)  # Set initial alpha to 255

# Main game loop
clock = pygame.time.Clock()
alpha_value = 255

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Blit the brown circle onto the screen
    screen.blit(brown_circle, (100, 200))

    # Decrease the alpha value for the green circle
    alpha_value -= 1
    if alpha_value < 0:
        alpha_value = 0

    # Blit the green circle with the updated alpha onto the screen
    screen.blit(green_circle, (250, 200), special_flags=BLEND_RGBA_MULT)
    pygame.draw.circle(green_circle, (green[0], green[1], green[2], alpha_value), (50, 50), 50)

    pygame.display.flip()

    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()
sys.exit()
