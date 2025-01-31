import pygame, sys
import os
import random
import json

# Initialize Pygame
pygame.init()

player_lives = 3
score = 0
fruits = ['apple', 'orange', 'lemon', 'kiwi', 'watermelon', 'bomb', 'ice']

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

# ----------------------------------------------------------------Check or initialize the JSON file
if not os.path.exists("history.json"):
    with open("history.json", "w") as file: 
        json.dump({"scores": []}, file)  # Initialize with an empty structure


#------------------------------------------------------------------ Background
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 32)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
# lives_icon = pygame.image.load('images/white_lives.png')

# Add sounds and music
music = pygame.mixer.music.load("sounds/music-game.mp3")
fail_sound = pygame.mixer.Sound("sounds/failfare.mp3")
click_sound = pygame.mixer.Sound("sounds/click.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
cut_sound = pygame.mixer.Sound("sounds/slice.mp3")
time_sound = pygame.mixer.Sound("sounds/time-sound.mp3")
win_sound = pygame.mixer.Sound("sounds/fanfare.mp3")

pygame.mixer.music.play(-1)


# --------------------------------------------------------------------Function for button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None, radius=15, padding=5):
    # Draws a button with hover and click effects
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(gameDisplay, hover_color, (x, y, width, height))
        # color = hover_color
        if click[0] == 1 and action is not None:
            click_sound.play()
            pygame.time.delay(150)
            action()
    else:
        # color = default_color
        pygame.draw.rect(gameDisplay, default_color, (x, y, width, height), border_radius=radius)


    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  
    gameDisplay.blit(text_surface, text_rect)

# Languages
def change_language():
    print("")

# Menu languages
def menu_lang():
    running = True
    try:
        while running: 
            # Clear the screen each frame
                gameDisplay.blit(background, (0, 0))  

                # Corrected button positions (using numbers for coordinates)
                draw_button(300, 150, 200, 50, "English", YELLOW, GREEN)
                draw_button(300, 220, 200, 50, "French", YELLOW, GREEN)
                draw_button(300, 290, 200, 50, "Ukrainian", YELLOW, GREEN, change_language)
                draw_button(300, 360, 200, 50, "Main menu", YELLOW, GREEN, main_menu)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                clock.tick(FPS)
    except KeyboardInterrupt:
        print("Finish")





# Initialize history
history = []


def write_json(name, bomb, lives, result):
    with open("history.json", "r+") as file:
        data = json.load(file)  # Charge les données existantes
        if name is None and lives is None and bomb is None:
            # Cas d'une expression brute
            data["scores"].append({
                "expression": result,  # Enregistre l'expression brute avec son résultat
                "result": result
            })
        else:
            # Cas classique
            data["scores"].append({
                "fails": bomb,
                "name": name,
                "lives": lives,
                "result": result
            })
        file.seek(0)  # Retourne au début du fichier
        json.dump(data, file, indent=4)  # Écrit les nouvelles données


def read_history():
    with open("history.json", "r") as file:
        data = json.load(file)  # Charge les données de l'historique
        if data["scores"]:
            print("\nScore History:")
            for calc in data["scores"]:
                if "expression" in calc:
                    # Affiche une expression brute
                    print(f"Expression: {calc['expression']} = {calc['result']}")
                else:
                    # Affiche un calcul classique
                    print(f"{calc['name: ']} {calc['fails']} {calc['lives']} = {calc['result']}")
        else:
            print("No scores found in history.")

# ---------------------------------------------------------------------Showing the menu

def main_menu():
    running = True
    try:
        while running:
            # Clear the screen each frame
            gameDisplay.blit(background, (0, 0))  

            # Corrected button positions (using numbers for coordinates)
            draw_button(300, 150, 200, 50, "The level", YELLOW, GREEN)
            draw_button(300, 220, 200, 50, "Play", YELLOW, GREEN)
            draw_button(300, 290, 200, 50, "Language", YELLOW, GREEN, menu_lang)
            draw_button(300, 360, 200, 50, "Exit", YELLOW, GREEN, quit_game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
            clock.tick(FPS)
    except KeyboardInterrupt:
        print("Finish")
        
def quit_game():
    pygame.quit()
    sys.exit()


# Run the menu
main_menu()    
pygame.quit()