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
    # Get mouse position and check if clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Define the button area as a rectangle
    button_rect = pygame.Rect(x, y, width, height)


    # Check if the mouse is within the button area
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(gameDisplay, hover_color, button_rect)  # Show hover color
        
        # Check if the button was clicked (on left mouse button press)
        if click[0] == 1 and action is not None:
            pygame.time.delay(150)  # Delay to avoid multiple clicks in quick succession
            action()  # Execute action bound to the button
    else:
        pygame.draw.rect(gameDisplay, default_color, button_rect, border_radius=radius)  # Default button color

    # Render the button text and place it centered in the button
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    gameDisplay.blit(text_surface, text_rect)

# Languages
def change_language():
    print("")

# Menu levels
def menu_level():
    print("")

# Rules
def rules():
    running = True
    while running:
        gameDisplay.blit(background, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("To cut an apple - press 'a'", True, BLACK)
        text2 = font.render("To cut a bomb - press 'b'", True, BLACK)
        text3 = font.render("To cut an ice - press 'i'", True, BLACK)
        text4 = font.render("To cut a kiwi - press 'k'", True, BLACK)
        text5 = font.render("To cut a lemon - press 'l'", True, BLACK)
        text6 = font.render("To cut an orange - press 'o'", True, BLACK)
        text7 = font.render("To cut a watermelon - press 'w'", True, BLACK)
        # option1 = font.render("Go back", True, YELLOW)
        

        # To show the text 
        gameDisplay.blit(text, (200, 90))
        gameDisplay.blit(text2, (200, 130))
        gameDisplay.blit(text3, (200, 170))
        gameDisplay.blit(text4, (200, 210))
        gameDisplay.blit(text5, (200, 250))
        gameDisplay.blit(text6, (200, 290))
        gameDisplay.blit(text7, (200, 330))
        draw_button(200, 370, 200, 50, "Main menu", YELLOW, GREEN, main_menu)
        # gameDisplay.blit(option1, (200, 390))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_x, mouse_y = event.pos
                if 200 < mouse_x < 500:  
                    if 370 < mouse_y < 450:

                        main_menu() 


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
            draw_button(300, 80, 200, 50, "The level", YELLOW, GREEN, menu_level)
            draw_button(300, 150, 200, 50, "Play", YELLOW, GREEN)
            draw_button(300, 220, 200, 50, "Rules", YELLOW, GREEN, rules)
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