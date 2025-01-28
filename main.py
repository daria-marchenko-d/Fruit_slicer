import pygame, sys
import os
import random

# Initialize Pygame
pygame.init()

player_lives = 3
score = 0
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']

# Configure the window
WIDTH = 800
HEIGHT = 500
FPS = 12
pygame.display.set_caption("FRUIT NINJA")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
gameDisplay.fill((BLACK))
# background = pygame.image.load("background.jpg")

font = pygame.font.Font(None, 32)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
# lives_icon = pygame.image.load('images/white_lives.png')


# Function for button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None, padding=5):
    # Draws a button with hover and click effects
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(gameDisplay, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, default_color, (x, y, width, height))

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  
    gameDisplay.blit(text_surface, text_rect)

# ---------------------------------------Showing the menu

def main_menu():
    running = True
    while running:
        gameDisplay.fill(BLACK)  # Clear the screen each frame

        # Corrected button positions (using numbers for coordinates)
        draw_button(300, 150, 200, 50, "The level", BLUE, GREEN)
        draw_button(300, 220, 200, 50, "Play", BLUE, GREEN)
        draw_button(300, 290, 200, 50, "Language", BLUE, GREEN)
        draw_button(300, 360, 200, 50, "Exit", BLUE, GREEN, action=pygame.quit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(FPS)

# Run the menu
main_menu()    
pygame.quit()