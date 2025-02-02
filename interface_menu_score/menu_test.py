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
    with open("history.json", "w", ensure_ascii=False, encoding='utf-8') as file: 
        json.dump({"scores": []}, file, indent=4)  # Initialize with an empty structure


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

# -------------------------------------------------------------------Showing level menu
# Menu levels
def menu_level():
    running = True
    font = pygame.font.Font(None, 36)
    options = ["Light level", "Hard level", "Go back"]
    y_positions = [200, 250, 300]
    while running:
        gameDisplay.blit(background, (0, 0))
        
        # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Center text
        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        if index == 0:
                            print("Light level selected")
                        elif index == 1:
                            print("Hard level selected")
                        elif index == 2:
                            # to go to the main menu
                            main_menu()
                        running = False


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
        option1 = font.render("Go back", True, YELLOW)
        

        # To show the text 
        gameDisplay.blit(text, (200, 90))
        gameDisplay.blit(text2, (200, 130))
        gameDisplay.blit(text3, (200, 170))
        gameDisplay.blit(text4, (200, 210))
        gameDisplay.blit(text5, (200, 250))
        gameDisplay.blit(text6, (200, 290))
        gameDisplay.blit(text7, (200, 330))
        
        gameDisplay.blit(option1, (350, 390))

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

# Languages
def change_language():
    print("")
# -------------------------------------------------------------------Showing Languages menu
# Menu languages
def menu_lang():
    running = True
    font = pygame.font.Font(None, 36)
    options = ["English", "French", "Ukrainian", "Go back"]
    y_positions = [150, 200, 250, 300]
    while running:
        gameDisplay.blit(background, (0, 0))
        # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Center text
        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        if index == 0:
                            print("English")
                        elif index == 1:
                            print("French")
                        elif index == 2:
                            print("Ukrainian")
                        elif index == 3:
                            # to go to the main menu
                            main_menu()
                        running = False              


# Scores history
# Initialize history
history = []

def write_json(name, bomb, lives, result):
    with open("history.json", "r+", encoding='utf-8') as file:
        data = json.load(file)  # Charge les données existantes
        if name is None and lives is None and bomb is None:
            # Cas d'une expression brute
            data["scores"].append({
                "name": name,  
                "result": result
            })
        else:
            # Cas classique
            data["scores"].append({
                "name": name,
                "lives": lives,
                "fails": bomb,
                "result": result
            })
        file.seek(0)  # Retourne au début du fichier
        json.dump(data, file, ensure_ascii=False, indent=4)  # Écrit les nouvelles données

def delete_history():
    del history

# -------------------------------------------------------------------Showing scores history menu
def menu_history():
    running = True
    font = pygame.font.Font(None, 36)
    options = ["Delete history:", "Go back"]
    y_positions = [200, 250]

    while running:
        gameDisplay.blit(background, (0, 0)) 
        # Отримуємо координати мишки
        mouse_x, mouse_y = pygame.mouse.get_pos()

        def read_history():
            with open("history.json", "r", encoding='utf-8') as file:
                data = json.load(file)  # Charge les données de l'historique
                if data["scores"]:
                    print("\nScore History:")

                    # for calc in data["scores"]:
                    #     if "expression" in calc:
                    #         # Affiche une expression brute
                    #         print(f"Expression: {calc['expression']} = {calc['result']}")
                    #     else:
                    #         # Affiche un calcul classique
                    #         print(f"{calc['name: ']} {calc['fails']} {calc['lives']} = {calc['result']}")
                else:
                    print("No scores found in history.")
        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))



        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        if index == 0:
                            delete_history()
                            print("The history is deleted")
                        elif index == 1:
                            main_menu()
                        running = False



# ---------------------------------------------------------------------Showing the menu
def main_menu():
    running = True
    font = pygame.font.Font(None, 36)
    options = ["Level", "Rules", "Language", "Scores", "Exit"]
    y_positions = [150, 200, 250, 300, 350]

    while running:
        gameDisplay.blit(background, (0, 0)) 
        # Отримуємо координати мишки
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Відображення кожного пункту в центрі екрана
        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        if index == 0:
                            menu_level()
                        elif index == 1:
                            rules()
                        elif index == 2:
                            menu_lang()
                        elif index == 3:
                            menu_history()
                        elif index == 4:
                            quit_game()
                        running = False
        
def quit_game():
    pygame.quit()
    sys.exit()


# Run the menu
main_menu()    
pygame.quit()