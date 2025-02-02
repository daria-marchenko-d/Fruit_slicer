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
def menu_level(language):
    running = True
    font = pygame.font.Font(None, 36)
    options = language["level"]
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
                            main_menu(language)
                        running = False


# Rules
def rules(language):
    running = True
    while running:
        gameDisplay.blit(background, (0, 0))
        font = pygame.font.Font(None, 36)
        options = language["rules"]  # Взяти правила з мови
        y_positions = [90, 130, 170, 210, 250, 290, 330]

        for i, text in enumerate(options):
            text_rendered = font.render(text, True, BLACK)
            gameDisplay.blit(text_rendered, (200, y_positions[i]))

        back_text = "Go back"
        back_text_rendered = font.render(back_text, True, YELLOW) 
        back_text_width = back_text_rendered.get_width()
        back_text_height = back_text_rendered.get_height()
        back_text_x = (gameDisplay.get_width() - back_text_width) // 2  
        back_text_y = 370

        gameDisplay.blit(back_text_rendered, (back_text_x, back_text_y))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_x, mouse_y = event.pos
                if 200 < mouse_x < 500:  
                    if 370 < mouse_y < 450:
                        text_rendered = font.render(text, True, YELLOW)
                        main_menu(language) 

# Languages
def change_language(lang):
    with open("languages.json", "r", encoding="utf-8") as file:
        languages = json.load(file) 

    print(f"Language set to: {lang}") 
    return languages.get(lang, languages["en"])
# -------------------------------------------------------------------Showing Languages menu
# Menu languages
def menu_lang(language):
    running = True
    font = pygame.font.Font(None, 36)
    options = language["Language"]
    languages = ["en", "fr", "uk"]
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
                        # if index == 0:
                        #     return "en"
                        # elif index == 1:
                        #     return "fr"
                        # elif index == 2:
                        #     return "uk"
                        # elif index == 3:
                        #     return None      
                        if index == 3:  # "Go back"
                            return language  # Повертаємо поточну мову, щоб залишитися в меню
                        else:
                            return languages[index]
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
def menu_history(language):
    running = True
    font = pygame.font.Font(None, 36)
    options = language["history"]
    y_positions = [200, 250]

    while running:
        gameDisplay.blit(background, (0, 0)) 
         # Mouse coordinates
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
                            main_menu(language)
                        running = False



# ---------------------------------------------------------------------Showing the menu
def main_menu(language):
    running = True
    font = pygame.font.Font(None, 36)
    # options = language["menu"]
    # y_positions = [150, 200, 250, 300, 350]


    while running:
        options = language["menu"]
        y_positions = [150, 200, 250, 300, 350]

        gameDisplay.blit(background, (0, 0)) 
         # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Center text
        text_rects = []
        for i, text in enumerate(options):
            rendered_text = font.render(text, True, YELLOW)
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
                        print(f"Main menu option {options[index]} selected.")
                        if index == 0:
                            menu_level(language)
                        elif index == 1:
                            rules(language)
                        elif index == 2:
                            new_language = menu_lang(language)
                            if new_language != language:
                                language = change_language(new_language)  # Тепер передаємо нову мову
                        elif index == 3:
                            menu_history(language)
                        elif index == 4:
                            quit_game(language)
                        # running = False
                        pygame.display.flip()
        
def quit_game(language):
    pygame.quit()
    sys.exit()


# Run the menu
language = change_language("en")
main_menu(language)    
pygame.quit()