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
YELLOW = (255, 200, 50)

background = pygame.image.load("image/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 32)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
# lives_icon = pygame.image.load('images/white_lives.png')


# Function for button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None, radius=15, padding=5):
    # Draws a button with hover and click effects
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        color = hover_color
        if click[0] == 1 and action is not None:
            action()
    else:
        color = default_color
    
    pygame.draw.rect(gameDisplay, color, (x, y, width, height), border_radius=radius)


    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  
    gameDisplay.blit(text_surface, text_rect)

# ---------------------------------------Showing the menu

def main_menu():
    running = True
    while running:
          # Clear the screen each frame
        gameDisplay.blit(background, (0, 0))  

        # Corrected button positions (using numbers for coordinates)
        draw_button(300, 150, 200, 50, "The level", YELLOW, GREEN)
        draw_button(300, 220, 200, 50, "Play", YELLOW, GREEN)
        draw_button(300, 290, 200, 50, "Language", YELLOW, GREEN)
        draw_button(300, 360, 200, 50, "Exit", YELLOW, GREEN, action=pygame.quit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(FPS)
def change_language():
    print("")

# Run the menu
main_menu()    
pygame.quit()